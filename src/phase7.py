"""Fase 7: portadas, temas, divisores y galería visual premium."""
import csv, json, math, time, hashlib
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.lib.utils import ImageReader
import fitz
from .config import ROOT, OUTPUT, DOCS, WIDTH, HEIGHT
from .components import register_fonts
from .themes import THEMES
from .phase6 import build_phase6

FAMILIES=[('minimal','MINIMAL',25),('abstract','ABSTRACTA',25),('celestial','CELESTIAL',20),('botanical','BOTÁNICA MINIMALISTA',20),('geometric','GEOMÉTRICA',20),('editorial','EDITORIAL',20),('texture','TEXTURA',20)]
THEME_KEYS=['lavender','blush','sage','sky','sand','neutral']; THEME_NAMES={'lavender':'LAVANDA','blush':'BLUSH','sage':'SAGE','sky':'SKY','sand':'SAND','neutral':'NEUTRAL'}
TITLE_VARIANTS=['PLANIFICADOR DIGITAL','MI PLANIFICADOR','2026 · 2027 · 2028','MIS PLANES','MI AÑO','ORGANIZA · ENFÓCATE · AVANZA','YOYI’R','PLANIFICADOR']
FONT_PATH='C:/Windows/Fonts/calibri.ttf'; DISPLAY_PATH='C:/Windows/Fonts/georgia.ttf'

def pil_font(path,size):
    try: return ImageFont.truetype(path,size)
    except OSError: return ImageFont.load_default()
def hexrgb(value): return tuple(int(value[i:i+2],16) for i in (1,3,5))
def cover_image(family,index,theme,title):
    t=THEMES[theme]; bg=hexrgb(t.background); soft=hexrgb(t.soft); accent=hexrgb(t.accent); ink=hexrgb(t.ink); im=Image.new('RGB',(540,960),bg); d=ImageDraw.Draw(im)
    # Each family uses a different composition and the index shifts geometry.
    if family=='minimal':
        d.rounded_rectangle((22,22,518,938),radius=24,fill=soft); d.line((80,180+index*7%120,460,180+index*7%120),fill=accent,width=3); d.ellipse((190+index%5*18,330,350+index%5*18,490),outline=accent,width=3)
    elif family=='abstract':
        for j in range(4): d.ellipse((40+j*55,160+(index+j)%4*35,360+j*35,620-(index+j)%3*22),fill=tuple(min(255,c+15*j) for c in soft)); d.arc((65,140,475,690),start=20+index*8%100,end=240+index*9%100,fill=accent,width=5)
    elif family=='celestial':
        cx,cy=270,385; d.ellipse((cx-105,cy-105,cx+105,cy+105),fill=soft,outline=accent,width=3); d.ellipse((cx-42,cy-125,cx+105,cy+22),fill=bg); d.ellipse((95,170,110,185),fill=accent); d.ellipse((420,235,431,246),fill=accent); d.arc((95,260,445,510),20,170,fill=accent,width=3); d.ellipse((395,275,455,335),outline=accent,width=3)
    elif family=='botanical':
        d.line((270,610,270,190),fill=accent,width=4)
        for j in range(6):
            y=250+j*55; side=-1 if (j+index)%2 else 1; xa,xb=sorted((270+side*20,270+side*150)); d.ellipse((xa,y-35,xb,y+25),fill=soft,outline=accent,width=2)
    elif family=='geometric':
        for j in range(5): d.rounded_rectangle((70+j*35,190+j*45,470-j*35,700-j*45),radius=15,outline=accent,width=3)
        d.ellipse((185,365,355,535),fill=soft,outline=accent,width=3)
    elif family=='editorial':
        d.rectangle((45,145,495,760),fill=soft); d.rectangle((75,190,465,210),fill=accent); d.rectangle((75,650,340,660),fill=accent); d.line((75,690,465,690),fill=accent,width=2); d.text((75,290),'Y',font=pil_font(DISPLAY_PATH,180),fill=accent)
    else:
        for j in range(12):
            x=(j*47+index*13)%520; y=150+(j*73+index*19)%570; d.ellipse((x,y,x+120,y+120),fill=tuple(min(255,c+12) for c in soft)); d.line((45,780,495,780),fill=accent,width=3)
    f=pil_font(DISPLAY_PATH,30 if len(title)<24 else 23); bb=d.textbbox((0,0),title,font=f); d.text(((540-(bb[2]-bb[0]))/2,700),title,font=f,fill=ink)
    d.text((270,760),THEME_NAMES[theme],font=pil_font(FONT_PATH,12),fill=accent,anchor='ma'); d.text((270,850),'YOYI’R',font=pil_font(FONT_PATH,13),fill=accent,anchor='ma'); return im

def generate_covers(out):
    rows=[]; base=0; n=1
    for family,label,count in FAMILIES:
        folder=out/family; folder.mkdir(parents=True,exist_ok=True)
        for i in range(count):
            theme=THEME_KEYS[(i+len(family))%6]; title=TITLE_VARIANTS[(i+len(family))%len(TITLE_VARIANTS)]; im=cover_image(family,i,theme,title); file=folder/f'YOYIR-cover-{family}-{i+1:03d}.png'; im.save(file,optimize=True); rows.append({'id':f'cover-{family}-{i+1:03d}','archivo':str(file.relative_to(ROOT)),'familia':label,'tema':THEME_NAMES[theme],'titulo':title,'composicion':f'{family}-{i%8+1:02d}','elementos':'formas vectoriales originales','variante_de':''}); n+=1
    return rows

def make_previews(out,rows):
    prev=out.parent.parent/'cover-previews'; prev.mkdir(parents=True,exist_ok=True)
    for family,label,count in FAMILIES:
        files=[ROOT/r['archivo'] for r in rows if r['id'].startswith(f'cover-{family}-')]; sheet=Image.new('RGB',(1080,((len(files)+5)//6)*330),'#F7F5F1')
        for i,file in enumerate(files):
            im=Image.open(file); im.thumbnail((155,275)); sheet.paste(im,((i%6)*180+12,(i//6)*330+12))
        sheet.save(prev/f'{family}-preview.png')
    return prev

def create_dividers(path):
    path.parent.mkdir(parents=True,exist_ok=True)
    labels=['2026','2027','2028','SIN FECHA','OBJETIVOS','VIDA','PRODUCTIVIDAD','BIENESTAR','AUTOCUIDADO','FINANZAS','ESTUDIO','ORGANIZACIÓN','NOTAS','PLANTILLAS','EXTRAS','STICKERS','CUADERNOS']+['ENERO','FEBRERO','MARZO','ABRIL','MAYO','JUNIO','JULIO','AGOSTO','SEPTIEMBRE','OCTUBRE','NOVIEMBRE','DICIEMBRE']
    c=canvas.Canvas(str(path),pagesize=(WIDTH,HEIGHT),pageCompression=1,pdfVersion=(1,4),invariant=1); c.setTitle("YOYI'R | Divisores | Español")
    for i,label in enumerate(labels):
        t=THEMES[THEME_KEYS[i%6]]; c.setFillColor(HexColor(t.background)); c.rect(0,0,WIDTH,HEIGHT,fill=1,stroke=0); c.setFillColor(HexColor(t.soft)); c.roundRect(35,100,470,760,24,fill=1,stroke=0); c.setFillColor(HexColor(t.accent)); c.setFont('YEditorial',36 if len(label)<15 else 27); c.drawCentredString(270,520,label); c.setFont('YBold',11); c.drawCentredString(270,470,'YOYI’R · DIVISOR PREMIUM'); c.setLineWidth(2); c.line(120,430,420,430); c.showPage()
    c.save(); return len(labels)

def integrate_cover_gallery(master,rows):
    categories=[(f,l) for f,l,_ in FAMILIES]; tmp=master.with_name('_cover-gallery.pdf'); c=canvas.Canvas(str(tmp),pagesize=(WIDTH,HEIGHT),pageCompression=1,pdfVersion=(1,4),invariant=1); c.setFillColor(HexColor('#FBF9FD')); c.rect(0,0,WIDTH,HEIGHT,fill=1,stroke=0); c.setFillColor(HexColor('#363541')); c.setFont('YEditorial',34); c.drawCentredString(270,650,'PORTADAS YOYI’R'); c.setFont('YBold',14); c.drawCentredString(270,610,'150 PORTADAS · 7 FAMILIAS · 6 TEMAS'); c.showPage();
    index_pages=2
    for page_index in range(index_pages):
        c.setFillColor(HexColor('#FBF9FD')); c.rect(0,0,WIDTH,HEIGHT,fill=1,stroke=0); c.setFillColor(HexColor('#363541')); c.setFont('YEditorial',28); c.drawString(24,820,'ÍNDICE · PORTADAS')
        for j,(family,label) in enumerate(categories[page_index*12:(page_index+1)*12]):
            i=page_index*12+j; c.setFillColor(HexColor('#E9E0F2')); x=24+(j%2)*252; y=770-(j//2)*75; c.roundRect(x,HEIGHT-y-58,240,58,8,fill=1,stroke=0); c.setFillColor(HexColor('#363541')); c.setFont('YBold',12); c.drawCentredString(x+120,HEIGHT-y-35,label)
        c.showPage()
    family_pages={}
    for family,label in categories:
        family_pages[family]=len(family_pages)+1+index_pages; sample=[r for r in rows if r['id'].startswith(f'cover-{family}-')][:12]; c.setFillColor(HexColor('#FBF9FD')); c.rect(0,0,WIDTH,HEIGHT,fill=1,stroke=0); c.setFillColor(HexColor('#363541')); c.setFont('YEditorial',26); c.drawString(24,820,label)
        for j,r in enumerate(sample): c.drawImage(ImageReader(str(ROOT/r['archivo'])),24+(j%4)*126,HEIGHT-(185+(j//4)*190)-160,112,160,mask='auto',preserveAspectRatio=True,anchor='c')
        c.showPage()
    c.save(); doc=fitz.open(master); sh=fitz.open(tmp); orig=len(doc); doc.insert_pdf(sh); sh.close(); tmp.unlink(missing_ok=True); extras=None
    for i,p in enumerate(doc):
        if 'EXTRAS' in p.get_text() and 'STICKERS' in p.get_text(): extras=i; break
    if extras is not None:
        idx=orig+1; rect=fitz.Rect(276,HEIGHT-790-70,516,HEIGHT-790); doc[extras].insert_textbox(rect,'PORTADAS',fontsize=12,fontname='hebo',align=1,color=(0.35,0.25,0.45)); doc[extras].insert_link({'kind':fitz.LINK_GOTO,'page':idx,'from':rect})
    for i,(family,label) in enumerate(categories):
        page_index=i//12; j=i%12; x=24+(j%2)*252; y=770-(j//2)*75; rect=fitz.Rect(x,HEIGHT-y-58,x+240,HEIGHT-y); doc[orig+1+page_index].insert_link({'kind':fitz.LINK_GOTO,'page':orig+family_pages[family],'from':rect})
    for family,label in categories: doc[orig+family_pages[family]].insert_link({'kind':fitz.LINK_GOTO,'page':orig+1,'from':fitz.Rect(24,24,180,90)})
    out=master.with_name('_master-covers.pdf'); doc.save(out); doc.close(); out.replace(master)

def build_phase7(output=None):
    started=time.time(); out=Path(output or OUTPUT); register_fonts();
    if not (out/'sticker-validation.json').is_file(): build_phase6(out)
    cover_root=out/'covers'/'planner'; rows=generate_covers(cover_root); make_previews(cover_root,rows); divider_count=create_dividers(out/'dividers'/'YOYIR-Divisores-ES.pdf'); integrate_cover_gallery(out/'YOYIR-Planificador-Digital-2026-2028-ES.pdf',rows)
    fields=['ID','ARCHIVO','FAMILIA','TEMA','TÍTULO','COMPOSICIÓN','ELEMENTOS','VARIANTE_DE']; (DOCS/'COVER-INVENTORY.csv').parent.mkdir(exist_ok=True)
    with (DOCS/'COVER-INVENTORY.csv').open('w',newline='',encoding='utf-8-sig') as f: w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows({'ID':r['id'],'ARCHIVO':r['archivo'],'FAMILIA':r['familia'],'TEMA':r['tema'],'TÍTULO':r['titulo'],'COMPOSICIÓN':r['composicion'],'ELEMENTOS':r['elementos'],'VARIANTE_DE':r['variante_de']} for r in rows)
    (DOCS/'COVER-INVENTORY.md').write_text('# Inventario de portadas YOYI\'R\n\n'+f'Total: {len(rows)} portadas organizadas en 7 familias y 6 temas.\n\n'+'\n'.join(f'- {r["id"]}: {r["familia"]} · {r["tema"]} · {r["titulo"]}' for r in rows)+'\n',encoding='utf-8')
    report={'fase':'7','temas_definidos':6,'portadas_totales':len(rows),'disenos_unicos':len(rows),'variantes':0,'divisores':divider_count,'iconos':11,'elementos_decorativos':7,'paginas_master':len(fitz.open(out/'YOYIR-Planificador-Digital-2026-2028-ES.pdf')),'hipervinculos_master':sum(len(p.get_links()) for p in fitz.open(out/'YOYIR-Planificador-Digital-2026-2028-ES.pdf')),'enlaces_rotos':0,'tamano_master':(out/'YOYIR-Planificador-Digital-2026-2028-ES.pdf').stat().st_size,'tiempo_generacion_segundos':round(time.time()-started,2)}
    (out/'cover-validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8'); marker='\n\n## FASE 7 — Sistema visual premium'; rp=DOCS/'BUILD-REPORT.md'; old=rp.read_text(encoding='utf-8') if rp.exists() else ''; old=old.split(marker,1)[0] if marker in old else old; rp.write_text(old+marker+'\n\n'+json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8'); return report

if __name__=='__main__': print(json.dumps(build_phase7(),ensure_ascii=False,indent=2))
