import hashlib
from pathlib import Path
import fitz
from PIL import Image, ImageDraw
from pypdf import PdfReader
from .config import WIDTH, HEIGHT, MIN_TARGET
from .config import MONTHS
from .planner.dates import month_weeks

def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def validate_pdf(path,pages,nav,preview_folder):
    nav.check()
    assert path.is_file() and path.stat().st_size>1000
    raw=path.read_bytes()
    assert raw.startswith(b'%PDF-1.4') and raw.rstrip().endswith(b'%%EOF')
    reader=PdfReader(path,strict=True)
    doc=fitz.open(path)
    assert not doc.is_repaired and not doc.is_encrypted
    assert len(doc)==len(reader.pages)==len(pages)
    assert '/AcroForm' not in reader.trailer['/Root']
    counts=[]
    preview_folder.mkdir(parents=True,exist_ok=True)
    thumbs=[]
    minw,minh=WIDTH,HEIGHT
    for i,page in enumerate(doc):
        assert page.rect==fitz.Rect(0,0,WIDTH,HEIGHT)
        assert len(page.get_text().strip())>25, ('Empty page',i)
        expected=[e for e in nav.links if e['source']==i]
        annots=reader.pages[i].get('/Annots',[])
        assert len(annots)==len(expected)>0,(i,len(annots),len(expected))
        actual_rects=[]
        for ref,entry in zip(annots,expected):
            a=ref.get_object()
            assert a['/Subtype']=='/Link'
            target=nav.destinations[entry['target']]
            dest=a['/Dest']
            assert dest[0].idnum==reader.pages[target['page']].indirect_reference.idnum,(i,entry)
            assert dest[1]=='/'+target['fit']
            if target['fit']=='FitR':
                x,y,w,h=target['bounds']
                assert all(abs(float(a)-b)<.01 for a,b in zip(dest[2:],[x,HEIGHT-y-h,x+w,HEIGHT-y]))
            x,y,w,h=entry['bounds']
            assert min(w,h)>=MIN_TARGET
            assert all(abs(float(a)-b)<.01 for a,b in zip(a['/Rect'],[x,HEIGHT-y-h,x+w,HEIGHT-y]))
            actual=fitz.Rect(x,y,x+w,y+h)
            assert page.rect.contains(actual)
            for previous in actual_rects:
                assert not actual.intersects(previous),('Overlapping links',i,entry)
            actual_rects.append(actual)
            minw,minh=min(minw,w),min(minh,h)
        for block in page.get_text('dict')['blocks']:
            for line in block.get('lines',[]):
                for span in line['spans']:
                    assert page.rect.contains(fitz.Rect(span['bbox'])),('Text out of bounds',i,span['text'],span['bbox'])
                    # A text span may sit in one button, never partly cross its boundary.
                    box=fitz.Rect(span['bbox'])
                    for link_box in actual_rects:
                        if box.intersects(link_box):
                            assert link_box.contains(box),('Text crossing button',i,span['text'])
        for drawing in page.get_drawings():
            assert page.rect.contains(drawing['rect']),('Drawing out of bounds',i,drawing['rect'])
        assert not list(page.widgets())
        for font in page.get_fonts():
            # ReportLab adds an unused Helvetica resource; all text actually drawn uses embedded TTFs.
            if font[1] != 'n/a':
                assert len(doc.extract_font(font[0])[3])>0
        pix=page.get_pixmap(matrix=fitz.Matrix(.5,.5),alpha=False)
        thumb=Image.frombytes('RGB',(pix.width,pix.height),pix.samples)
        thumbs.append(thumb)
        counts.append(len(annots))
    for xref in range(1,doc.xref_length()):
        obj=doc.xref_object(xref)
        assert not any(token in obj for token in ['/JavaScript','/JS ', '/Launch','/EmbeddedFiles','/URI','/GoToR'])
    # Read the actual printed month cells, not only the generator's input dates.
    for key,target in nav.destinations.items():
        if key.startswith('month-') and target['fit']=='FitR':
            _,year,month=key.split('-')
            x,y,w,h=target['bounds']
            printed=doc[target['page']].get_text(clip=fitz.Rect(x,y,x+w,y+h)).split()
            numbers=[int(word) for word in printed if word.isdigit()]
            expected_numbers=[n for week in month_weeks(int(year),int(month)) for n in week if n]
            assert numbers==expected_numbers,('Printed calendar mismatch',key,numbers)
    for i,p in enumerate(pages):
        if 'year' in p:
            month_links=[entry for entry in nav.links if entry['source']==i and entry['label'] in MONTHS]
            assert len(month_links)==12
            for entry in month_links:
                number=MONTHS.index(entry['label'])+1
                correct='month' if p['year']==2026 and number==1 else f'month-{p["year"]}-{number:02d}'
                assert entry['target']==correct,('Wrong active year/month',p['id'],entry)
    for start in range(0,len(thumbs),12):
        sheet=Image.new('RGB',(4*282,3*505),'#E8E5E1')
        draw=ImageDraw.Draw(sheet)
        for j,im in enumerate(thumbs[start:start+12]):
            x=(j%4)*282+6; y=(j//4)*505+6
            sheet.paste(im,(x,y))
            draw.text((x+5,y+481),f'{start+j+1:02d} / {pages[start+j]["id"]}',fill='#363541')
        sheet.save(preview_folder/f'contact-{start//12+1:02d}.png')
    selected=['home','index','year-2028','month','calendar','week','day','life','cover-04','stickers','section-01','section-01-1']
    for key in selected:
        if key in nav.pages:
            doc[nav.pages[key]].get_pixmap(matrix=fitz.Matrix(1,1),alpha=False).save(preview_folder/f'{key}.png')
    report={'file':path.name,'pages':len(doc),'dimensions_pt':[WIDTH,HEIGHT],
            'links':sum(counts),'links_per_page':counts,'destinations':len(nav.destinations),
            'minimum_target_pt':[minw,minh],'minimum_target_at_360px':[minw*360/WIDTH,minh*360/WIDTH],
            'all_pages_reachable':True,
            'printed_calendars_and_active_year_links_checked':any(p.get('kind')=='year' for p in pages),
            'errors':[],'sha256':digest(path)}
    doc.close()
    return report

def validate_pngs(files):
    rows=[]
    for file in files:
        with Image.open(file) as im:
            im.load()
            assert im.format=='PNG' and im.mode=='RGBA'
            assert im.width>=1200 and im.height>=700
            low,high=im.getchannel('A').getextrema()
            assert low==0 and high==255
            rows.append({'file':file.name,'size':list(im.size),'alpha_range':[low,high]})
    return rows

def validate_legacy(root,baseline):
    for name,sha in baseline.items():
        assert digest(root/name)==sha,('Legacy changed',name)
    doc=fitz.open(root/'digital-planner-test.pdf')
    reader=PdfReader(root/'digital-planner-test.pdf',strict=True)
    assert len(doc)==8 and not doc.is_repaired
    refs={p.indirect_reference.idnum for p in reader.pages}
    count=0
    for p in reader.pages:
        for annot in p.get('/Annots',[]):
            assert annot.get_object()['/Dest'][0].idnum in refs
            count+=1
    assert count==86
    for page in doc:
        assert page.get_text().strip()
        page.get_pixmap(matrix=fitz.Matrix(.25,.25))
    return {'pages':8,'links':86,'original_files_unchanged':True,'hashes':baseline}
