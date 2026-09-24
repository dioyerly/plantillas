"""python -m src.premium.month_proof — builds and validates the January 2026 premium block."""
import calendar
import json
import re
from datetime import date
import fitz
from PIL import Image,ImageChops
from pypdf import PdfReader
from .art import W,H
from .dated import build_month,WEEKDAYS
from .shell import FULL_MONTHS

YEAR,MONTH=2026,1
NAME='YOYIR-ENERO-2026-PREMIUM-APPROVED.pdf'
GOLDEN='YOYIR-DIA-PREMIUM-VISUAL-TEST.pdf'
DAY_TERMS=['ENFOQUE','HORARIO','TOP 3','POR HACER','COMIDAS','AGUA','MOVIMIENTO','ÁNIMO','GRATITUD','PARA MAÑANA']
WEEK_TERMS=['Mi semana','FOCO SEMANAL','LUNES','MARTES','MIÉRCOLES','JUEVES','VIERNES','SÁBADO','DOMINGO','TOP 3','HÁBITOS']
ENGLISH=['MONDAY','TUESDAY','WEDNESDAY','THURSDAY','FRIDAY','SATURDAY','SUNDAY','JANUARY','FEBRUARY','DECEMBER',
         'WEEK','TODAY','NOTES','HABITS','MOOD','WATER','GRATITUDE','TOMORROW','PLACEHOLDER']

def validate(pdf,pages,nav,future,arts):
    reader=PdfReader(pdf,strict=True);doc=fitz.open(pdf);index={p['id']:i for i,p in enumerate(pages)}
    r=dict(page_size=None,total_pages=len(doc),month_dividers=0,month_calendars=0,month_intention_pages=0,week_pages=0,
           daily_pages=0,complete_daily_pages=0,incomplete_daily_pages=0,dates_expected=calendar.monthrange(YEAR,MONTH)[1],
           dates_found=0,date_errors=0,internal_links=len(nav),broken_internal_links=0,duplicate_links=0,
           future_destinations=len({f['target'] for f in future}),blank_pages=0,clipping=0,overflow=0,
           english_visible_strings=0,week_coverage_missing=[],problems=[])
    sizes={(round(p.rect.width),round(p.rect.height)) for p in doc};r['page_size']=sorted(sizes)
    if sizes!={(W,H)}:r['problems'].append(('page size',sizes))
    covered=set()
    for i,(p,info) in enumerate(zip(doc,pages)):
        text=p.get_text();kind=info['kind']
        r[{'divider':'month_dividers','calendar':'month_calendars','plan':'month_intention_pages','week':'week_pages','day':'daily_pages'}[kind]]+=1
        pix=p.get_pixmap(matrix=fitz.Matrix(.3,.3),alpha=False)
        if len(text.strip())<25 or len(set(pix.samples))<8:r['blank_pages']+=1
        for b in p.get_text('dict')['blocks']:
            for ln in b.get('lines',[]):
                for s in ln['spans']:
                    if not p.rect.contains(fitz.Rect(s['bbox'])):r['overflow']+=1;r['problems'].append(('text overflow',i+1,s['text']))
        for dr in p.get_drawings():
            if not p.rect.contains(dr['rect']):r['clipping']+=1;r['problems'].append(('drawing outside page',i+1))
        upper=text.upper()
        hits=[w for w in ENGLISH if re.search(r'\b'+w+r'\b',upper)]
        r['english_visible_strings']+=len(hits)
        if kind=='day':
            d=info['date'];missing=[t for t in DAY_TERMS if t not in text]+[f'{h:02d}' for h in range(7,21) if not re.search(rf'(?m)^{h:02d}$',text)]
            missing+=[t for t in ['D','A','C','1','2','3','4','5'] if not re.search(rf'(?m)^{t}$',text)]
            if missing:r['incomplete_daily_pages']+=1;r['problems'].append(('incomplete day',i+1,missing))
            else:r['complete_daily_pages']+=1
            header=[WEEKDAYS[d.weekday()],f'{d.day:02d}',FULL_MONTHS[d.month-1],str(d.year)]
            if all(re.search(rf'(?m)^{re.escape(h)}$',text) for h in header):r['dates_found']+=1
            else:r['date_errors']+=1;r['problems'].append(('date header',i+1,header))
        if kind=='week':
            missing=[t for t in WEEK_TERMS if t not in text]
            if missing:r['problems'].append(('incomplete week',i+1,missing))
            covered|={e['target'] for e in nav if e['source']==info['id'] and e['target'].startswith('day-')}
        # links: annotation count, resolved destination, no overlaps
        links=[e for e in nav if e['source']==info['id']];annots=reader.pages[i].get('/Annots',[])
        if len(links)!=len(annots):r['broken_internal_links']+=abs(len(links)-len(annots))
        rects=[]
        for e,ref in zip(links,annots):
            dest=ref.get_object().get('/Dest')
            if not dest or dest[0].idnum!=reader.pages[index[e['target']]].indirect_reference.idnum:
                r['broken_internal_links']+=1;r['problems'].append(('broken link',i+1,e['label']))
            box=fitz.Rect(*e['rect'])
            if not p.rect.contains(box):r['problems'].append(('link outside page',i+1,e['label']))
            if any(box.intersects(o) for o in rects):r['duplicate_links']+=1;r['problems'].append(('overlapping link',i+1,e['label']))
            rects.append(box)
        for cal in arts[i].calendars:
            expected=list(range(1,calendar.monthrange(cal['year'],cal['month'])[1]+1))
            if [c[0] for c in cal['cells']]!=expected:r['date_errors']+=1
            for n,col,x,y in cal['cells']:
                if date(cal['year'],cal['month'],n).weekday()!=col:r['date_errors']+=1
                if str(n) not in p.get_text(clip=fitz.Rect(x-9,y-12,x+18,y+3)).split():r['date_errors']+=1;r['problems'].append(('calendar glyph',n))
    pairs=[(e['source'],e['target'],tuple(e['rect'])) for e in nav];r['duplicate_links']+=len(pairs)-len(set(pairs))
    for n in range(1,r['dates_expected']+1):
        if f'day-{YEAR}-{MONTH:02d}-{n:02d}' not in covered:r['week_coverage_missing'].append(n)
    reachable={pages[0]['id']}
    while True:
        grown=reachable|{e['target'] for e in nav if e['source'] in reachable}
        if grown==reachable:break
        reachable=grown
    r['unreachable_pages']=[p['id'] for p in pages if p['id'] not in reachable]
    for xref in range(1,doc.xref_length()):
        if any(t in doc.xref_object(xref) for t in ('/JavaScript','/URI','/GoToR','/Launch')):r['problems'].append(('unsafe object',xref))
    r['future_destination_list']=sorted({f['target'] for f in future})
    return r,doc

def golden_diff(doc,pages):
    golden=fitz.open(doc.name.replace(NAME,GOLDEN))[0]
    new=doc[[p['id'] for p in pages].index(f'day-{YEAR}-{MONTH:02d}-01')]
    m=fitz.Matrix(1.5,1.5)
    a=Image.frombytes('RGB',*[(x.width,x.height) for x in [golden.get_pixmap(matrix=m,alpha=False)]],golden.get_pixmap(matrix=m,alpha=False).samples)
    pb=new.get_pixmap(matrix=m,alpha=False);b=Image.frombytes('RGB',(pb.width,pb.height),pb.samples)
    diff=ImageChops.difference(a.convert('L'),b.convert('L')).point(lambda v:255 if v>40 else 0)
    changed=sum(1 for v in diff.getdata() if v)
    return round(100*changed/(a.width*a.height),3),diff.getbbox()

def previews(doc,pages):
    out=doc.name.rsplit('\\',1)[0].rsplit('/',1)[0];import os;folder=os.path.join(out,'previews');os.makedirs(folder,exist_ok=True)
    ids=[p['id'] for p in pages];weeks=[p['id'] for p in pages if p['kind']=='week']
    picks=[('01-divisor.png',ids[0]),('02-calendario.png',ids[1]),('03-intencion.png',ids[2]),('04-semana-1.png',weeks[0]),
           ('05-semana-media.png',weeks[len(weeks)//2]),('06-dia-01.png','day-2026-01-01'),('07-dia-15.png','day-2026-01-15'),
           ('08-dia-31.png','day-2026-01-31')]
    for name,key in picks:doc[ids.index(key)].get_pixmap(matrix=fitz.Matrix(3,3),alpha=False).save(os.path.join(folder,name))
    return [f'output/premium-proof/previews/{n}' for n,_ in picks]

if __name__=='__main__':
    pdf,pages,nav,future,arts=build_month(YEAR,MONTH,NAME)
    r,doc=validate(pdf,pages,nav,future,arts)
    r['golden_diff_percent'],r['golden_diff_bbox']=golden_diff(doc,pages)
    r['previews']=previews(doc,pages)
    (pdf.parent/'YOYIR-ENERO-2026-PREMIUM-APPROVED-validation.json').write_text(json.dumps(r,indent=2,ensure_ascii=False,default=str),encoding='utf-8')
    print(json.dumps(r,indent=1,ensure_ascii=False,default=str))
