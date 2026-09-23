from pathlib import Path
import json
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import fitz
from pypdf import PdfReader
from PIL import Image

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'digital-planner-test.pdf'
W, H = 450, 720
BG, INK, LINE = '#FCFAF5', '#41434B', '#DDDDE1'
PALETTE = ['#E8E1F3', '#F5E1E7', '#DDEDE5', '#DFECF6', '#F6E3D7', '#F5EED5', '#E0E4F6', '#EAE7F0']
KEYS = ['HOME', 'INDEX', 'MONTH', 'WEEK', 'DAY', 'GOALS', 'MONEY', 'NOTES']
TITLES = ['MY DIGITAL PLANNER', 'INDEX', 'MONTHLY PLANNER', 'WEEKLY PLANNER', 'DAILY PLANNER', 'MY GOALS', 'FINANCE', 'NOTES']
for name, file in [('Body', 'calibri.ttf'), ('Bold', 'calibrib.ttf'), ('Display', 'georgia.ttf')]:
    pdfmetrics.registerFont(TTFont(name, str(Path('C:/Windows/Fonts') / file)))
c = canvas.Canvas(str(OUT), pagesize=(W, H), pageCompression=1, pdfVersion=(1, 4))
c.setTitle('My Digital Planner | Compatibility Test')
c.setAuthor('Digital Planner')
expected = []

def rect(x, y, w, h, fill, radius=10, stroke=None):
    c.setFillColor(HexColor(fill))
    c.setStrokeColor(HexColor(stroke or fill))
    c.setLineWidth(.6)
    c.roundRect(x, H-y-h, w, h, radius, fill=1, stroke=bool(stroke))

def text(s, x, y, size=12, font='Body', center=False):
    c.setFillColor(HexColor(INK))
    c.setFont(font, size)
    (c.drawCentredString if center else c.drawString)(x, H-y, s)

def line(x, y, x2, y2):
    c.setStrokeColor(HexColor(LINE))
    c.setLineWidth(.55)
    c.line(x, H-y, x2, H-y2)

def button(label, key, x, y, w, h, color, active=False):
    rect(x, y, w, h, color, stroke=INK if active else None)
    text(label, x+w/2, y+h/2+4, 12, 'Bold', True)
    c.linkAbsolute(label, key, Rect=(x, H-y-h, x+w, H-y), thickness=0)
    expected.append({'source': page, 'target': KEYS.index(key), 'label': label, 'rect': [x,y,x+w,y+h]})

def panel(label, x, y, w, h, color, spacing=25):
    rect(x,y,w,h,'#FFFFFF',stroke=LINE)
    rect(x+1,y+1,w-2,30,color,8)
    text(label,x+12,y+21,11,'Bold')
    for yy in range(int(y+spacing+30),int(y+h-7),spacing):
        line(x+12,yy,x+w-12,yy)

def footer(items):
    gap = 8
    width = (402-gap*(len(items)-1))/len(items)
    for i,(label,key) in enumerate(items):
        button(label,key,24+i*(width+gap),632,width,56,PALETTE[KEYS.index(key)])

for page,key in enumerate(KEYS):
    rect(0,0,W,H,BG,0)
    c.bookmarkPage(key,fit='Fit')
    c.addOutlineEntry(TITLES[page],key,0)
    if page:
        for i,k in enumerate(KEYS):
            button(k,k,24+(i%4)*102.5,20+(i//4)*64,94.5,56,PALETTE[i],k==key)
        text(TITLES[page],24,182,25,'Display')
        text('UNDATED  /  MAKE ROOM FOR WHAT MATTERS',24,203,9)
    text(f'{page+1:02d} / 08',390,707,9)
    if page==0:
        rect(24,24,402,660,'#F0EAF5',18)
        rect(44,44,362,620,BG,14)
        text('A LITTLE SPACE FOR YOUR EVERYDAY',225,132,10,'Bold',True)
        line(185,175,265,175)
        text('MY DIGITAL',225,257,34,'Display',True)
        text('PLANNER',225,306,40,'Display',True)
        text('Plan • Organize • Focus',225,351,17,'Body',True)
        for i in range(7):
            rect(139+i*25,393,20,6,PALETTE[i],3)
        button('OPEN PLANNER','INDEX',89,465,272,64,PALETTE[0])
        text('THIS PLANNER BELONGS TO',225,580,10,'Bold',True)
        line(100,619,350,619)
    elif page==1:
        labels=['MONTH','WEEK','TODAY','GOALS','FINANCE','NOTES']
        for i,label in enumerate(labels):
            button(label,KEYS[i+2],24+(i%2)*209,238+(i//2)*112,193,96,PALETTE[i+2])
        text('Choose a section. Make it yours.',225,606,14,'Display',True)
        footer([('HOME','HOME'),('TODAY','DAY')])
    elif page==2:
        text('MONTH / YEAR',24,230,11,'Bold'); line(117,232,426,232)
        days=['MON','TUE','WED','THU','FRI','SAT','SUN']
        rect(24,248,402,30,PALETTE[2],5)
        for i,d in enumerate(days): text(d,24+(i+.5)*402/7,268,10,'Bold',True)
        for i in range(8): line(24+i*402/7,278,24+i*402/7,470)
        for i in range(7): line(24,278+i*32,426,278+i*32)
        for i,label in enumerate(['MONTHLY FOCUS','IMPORTANT','TO DO','NOTES']):
            panel(label,24+(i%2)*209,484+(i//2)*68,193,60,PALETTE[i],20)
        footer([('HOME','HOME'),('INDEX','INDEX'),('WEEK','WEEK'),('TODAY','DAY')])
    elif page==3:
        text('WEEK OF',24,228,11,'Bold'); line(82,230,426,230)
        for i,label in enumerate(['MONDAY','TUESDAY','WEDNESDAY','THURSDAY','FRIDAY','SATURDAY','SUNDAY']):
            panel(label,24,244+i*52,254,46,PALETTE[3],30)
        panel('TOP PRIORITIES',290,244,136,174,PALETTE[0])
        panel('NOTES',290,430,136,172,PALETTE[5])
        footer([('HOME','HOME'),('INDEX','INDEX'),('MONTH','MONTH'),('TODAY','DAY')])
    elif page==4:
        text('DATE',24,228,11,'Bold'); line(57,230,426,230)
        panel("TODAY'S FOCUS",24,244,402,65,PALETTE[4])
        panel('TOP 3 PRIORITIES',24,321,193,130,PALETTE[0],28)
        panel('TO DO',24,463,193,149,PALETTE[2])
        panel('SCHEDULE',233,321,193,198,PALETTE[3])
        panel('NOTES',233,531,193,81,PALETTE[5])
        footer([('HOME','HOME'),('INDEX','INDEX'),('MONTH','MONTH'),('WEEK','WEEK')])
    elif page==5:
        panel('GOAL',24,228,402,74,PALETTE[0])
        panel('WHY IT MATTERS',24,314,402,90,PALETTE[1])
        panel('ACTION STEPS',24,416,244,196,PALETTE[2])
        panel('PROGRESS',280,416,146,88,PALETTE[3])
        panel('NOTES',280,516,146,96,PALETTE[5])
        footer([('HOME','HOME'),('INDEX','INDEX'),('TODAY','DAY')])
    elif page==6:
        text('PERIOD / CURRENCY',24,228,11,'Bold'); line(126,230,426,230)
        for i,label in enumerate(['INCOME','EXPENSES','SAVINGS','BUDGET']):
            panel(label,24+(i%2)*209,244+(i//2)*142,193,130,PALETTE[i+2])
        panel('NOTES',24,528,402,84,PALETTE[0])
        footer([('HOME','HOME'),('INDEX','INDEX'),('TODAY','DAY')])
    elif page==7:
        rect(24,228,402,384,'#FFFFFF',stroke=LINE)
        for y in range(258,600,24): line(38,y,412,y)
        footer([('HOME','HOME'),('INDEX','INDEX'),('TODAY','DAY')])
    c.showPage()
c.save()

# Validate the actual serialized PDF with two independent PDF readers.
doc = fitz.open(OUT)
reader = PdfReader(OUT,strict=True)
assert len(doc)==len(reader.pages)==8
assert not doc.is_repaired and not doc.is_encrypted
assert '/AcroForm' not in reader.trailer['/Root']
assert OUT.read_bytes().startswith(b'%PDF-1.4')
counts=[]
thumbs=[]
for i,p in enumerate(doc):
    assert p.rect==fitz.Rect(0,0,W,H)
    assert TITLES[i] in p.get_text().replace('\n',' ') or i==0
    assert len(p.get_text().strip())>30
    links=p.get_links()
    wanted=[e for e in expected if e['source']==i]
    assert len(links)==len(wanted)
    for link,e,annotation in zip(links,wanted,reader.pages[i]['/Annots']):
        destination=annotation.get_object()['/Dest']
        assert destination[0].idnum==reader.pages[e['target']].indirect_reference.idnum
        assert destination[1]=='/Fit'
        # MuPDF exposes standard /Fit destinations as LINK_NAMED in some versions.
        assert (link['kind']==fitz.LINK_GOTO and link['page']==e['target']) or (link['kind']==fitz.LINK_NAMED and int(link['page'])==e['target']+1)
        assert p.rect.contains(link['from'])
        assert link['from'].width>=94 and link['from'].height>=56
        assert all(abs(a-b)<.1 for a,b in zip(link['from'],e['rect']))
    for block in p.get_text('dict')['blocks']:
        if 'lines' in block:
            for ln in block['lines']:
                for span in ln['spans']: assert p.rect.contains(fitz.Rect(span['bbox']))
    for drawing in p.get_drawings(): assert p.rect.contains(drawing['rect'])
    assert not list(p.widgets())
    pix=p.get_pixmap(matrix=fitz.Matrix(1,1),alpha=False)
    thumbs.append(Image.frombytes('RGB',[pix.width,pix.height],pix.samples))
    counts.append(len(links))
for xref in range(1,doc.xref_length()):
    obj=doc.xref_object(xref)
    assert not any(s in obj for s in ['/JavaScript','/JS ', '/Launch', '/EmbeddedFiles', '/URI'])
sheet=Image.new('RGB',(4*W,2*H),'#DDDDE1')
for i,im in enumerate(thumbs): sheet.paste(im,((i%4)*W,(i//4)*H))
sheet.save(ROOT/'planner-preview.png')
report={'file':OUT.name,'page_size_points':[W,H],'orientation':'portrait','pages':len(doc),'internal_links':sum(counts),'links_per_page':counts,'minimum_button_points':[94.5,56],'checks':'PASS: strict parse, render all pages, destinations match all buttons, nonempty pages, text/vector/link bounds, no forms, no JavaScript or external links','mobile_app_test':'Pending manual test on actual phone/tablet','generator':'Python + ReportLab','validators':['PyMuPDF','pypdf']}
(ROOT/'validation-report.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report,indent=2))
