"""Fase 5: seis cuadernos digitales independientes, en español."""
import json, time
from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from pypdf import PdfReader
import fitz
from .config import ROOT, OUTPUT, DOCS, WIDTH, HEIGHT
from .components import Drawing, register_fonts
from .navigation import Navigation
from .themes import THEMES
from .phase3 import build_phase3
from .phase2 import panel

NOTEBOOKS=[
 ('notas','CUADERNO DE NOTAS',['NOTAS RÁPIDAS','NOTAS DETALLADAS','LISTAS','REUNIONES','IDEAS','REFERENCIAS','RESÚMENES','PREGUNTAS','BORRADORES','ARCHIVO'],['NOTA RÁPIDA','NOTA DETALLADA','LISTA','CHECKLIST','NOTA DE REUNIÓN','RESUMEN','IDEAS','PREGUNTAS']),
 ('estudio','CUADERNO DE ESTUDIO',['MATERIAS','CLASES','RESÚMENES','CORNELL','EXÁMENES','REPASO','LECTURA','PROYECTOS','FICHAS','ARCHIVO'],['NOTAS DE CLASE','CORNELL','RESUMEN DE TEMA','PLAN DE ESTUDIO','SESIÓN DE ESTUDIO','PREPARACIÓN DE EXAMEN','PREGUNTAS DE REPASO','VOCABULARIO','FÓRMULAS','MAPA CONCEPTUAL','LECTURA']),
 ('proyectos','CUADERNO DE PROYECTOS',[f'PROYECTO {i:02d}' for i in range(1,11)],['RESUMEN DEL PROYECTO','OBJETIVO','ALCANCE','IDEAS','TAREAS','PRIORIDADES','HITOS','CRONOGRAMA','RECURSOS','REUNIONES','DECISIONES','PROGRESO','PROBLEMAS','SOLUCIONES','REVISIÓN FINAL']),
 ('ideas','CUADERNO DE IDEAS',['IDEAS','INSPIRACIÓN','REFERENCIAS','BOCETOS','CONCEPTOS','ARCHIVO','FAVORITAS','EN DESARROLLO','PUBLICADAS','NOTAS'],['IDEA RÁPIDA','LLUVIA DE IDEAS','MAPA MENTAL','MAPA CONCEPTUAL','IDEAS RADIALES','PROBLEMA / SOLUCIÓN','¿QUÉ PASARÍA SI...?','INSPIRACIÓN','REFERENCIAS','BOCETO','CONCEPTO','IDEA → ACCIÓN','IDEA → PROYECTO']),
 ('bienestar','CUADERNO DE BIENESTAR',['REFLEXIÓN','GRATITUD','ESTADO DE ÁNIMO','ENERGÍA','SUEÑO','MOVIMIENTO','RUTINAS','AUTOCUIDADO','HÁBITOS','COMIDAS'],['REFLEXIÓN','GRATITUD','ESTADO DE ÁNIMO','ENERGÍA','SUEÑO','MOVIMIENTO','RUTINAS','AUTOCUIDADO','HÁBITOS','COMIDAS','NOTAS PERSONALES','PEQUEÑAS VICTORIAS']),
 ('personal','MI CUADERNO',['MI DÍA','MI SEMANA','PENSAMIENTOS','DIARIO','GRATITUD','LISTAS','IDEAS','RECUERDOS','FAVORITOS','PLANES'],['MI DÍA','MI SEMANA','PENSAMIENTOS','DIARIO','GRATITUD','LISTAS','IDEAS','RECUERDOS','FAVORITOS','PLANES','METAS','NOTAS LIBRES'])]
PAPERS=['BLANCO','RAYADO FINO','RAYADO MEDIO','RAYADO AMPLIO','CUADRÍCULA PEQUEÑA','CUADRÍCULA MEDIA','CUADRÍCULA GRANDE','PUNTOS PEQUEÑOS','PUNTOS MEDIOS','PUNTOS GRANDES','CORNELL','DOS COLUMNAS','TRES COLUMNAS','CHECKLIST','MITAD NOTAS / MITAD BLANCO','MITAD CUADRÍCULA / MITAD NOTAS','ESQUEMA','BORRADOR LIBRE']
THEME_KEYS=['lavender','blush','sage','sky','sand','neutral']; THEME_ES={'lavender':'LAVANDA','blush':'BLUSH','sage':'VERDE SUAVE','sky':'CIELO','sand':'ARENA','neutral':'NEUTRO'}

def nid(code, suffix): return f'{code}-{suffix}'
def nb_button(d,label,target,x,y,w=117,h=70,small=False):
    d.box(x,y,w,h,d.t.soft,radius=7); d.text(label,x+w/2,y+h/2+5,10 if len(label)>17 else 12,'Bold',center=True)
    (d.nav.link_small if small else d.nav.link)(d.c,d.page,target,label,(x,y,w,h))
def footer_nb(d,code,current):
    items=[('INICIO',nid(code,'inicio')),('ÍNDICE',nid(code,'indice')),('PAPELES',nid(code,'papeles')),('PLANTILLAS',nid(code,'plantillas'))]; w=(492-8*3)/4
    for i,(label,target) in enumerate(items): nb_button(d,label,target,24+i*(w+8),866,w,70)
def side_tabs(d,code):
    for i in range(10): nb_button(d,f'{i+1:02d}',nid(code,f'seccion-{i+1:02d}'),444,24+i*71,72,66,True)
def nb_header(d,code,title,kicker=''):
    nb_button(d,'INICIO',nid(code,'inicio'),24,24,117,66); nb_button(d,'ÍNDICE',nid(code,'indice'),149,24,117,66); nb_button(d,'PAPELES',nid(code,'papeles'),274,24,117,66); nb_button(d,'PLANTILLAS',nid(code,'plantillas'),399,24,117,66); side_tabs(d,code); d.text(title,24,139,25 if len(title)<28 else 21,'Editorial');
    if kicker: d.text(kicker,24,164,11,'Bold',d.t.accent)

def add_pages(code,title,sections,templates):
    pages=[]
    def add(s,t,k,**kw): pages.append(dict(id=nid(code,s),title=t,kind=k,code=code,theme='lavender',**kw))
    add('inicio',"YOYI'R · "+title,'cover'); add('uso','CÓMO USAR ESTE CUADERNO','howto'); add('identificacion','IDENTIFICACIÓN','identification'); add('indice','ÍNDICE','index'); add('portadas','ELIGE TU PORTADA','covers'); add('papeles','BIBLIOTECA DE PAPEL','papers'); add('plantillas','BIBLIOTECA DE PLANTILLAS','templates'); add('secciones','MIS SECCIONES','mysections')
    for i,paper in enumerate(PAPERS): add(f'papel-{i+1:02d}',paper,'paper',paper=paper)
    for i,t in enumerate(templates): add(f'plantilla-{i+1:02d}',t,'template',template=t)
    for i,section in enumerate(sections,1):
        add(f'seccion-{i:02d}',f'SECCIÓN {i:02d}','section',number=i,section=section)
        add(f'seccion-{i:02d}-notas-1','PÁGINA DE NOTAS','note',number=i,template='Rayado medio')
        add(f'seccion-{i:02d}-notas-2','PÁGINA DE NOTAS','note',number=i,template='Puntos medios')
    return pages

def draw_paper(d,p):
    kind=p['paper']; x,y,w,h=24,205,492,600; d.box(x,y,w,h,d.t.paper,stroke=True,radius=5)
    d.text(kind,x+12,y+25,13,'Bold',d.t.accent)
    if kind.startswith('RAYADO'):
        gap={'RAYADO FINO':22,'RAYADO MEDIO':31,'RAYADO AMPLIO':44}[kind]
        for yy in range(y+60,y+h-12,gap): d.line(x+18,yy,x+w-18,yy)
    elif kind.startswith('CUADRÍCULA'):
        gap={'CUADRÍCULA PEQUEÑA':18,'CUADRÍCULA MEDIA':28,'CUADRÍCULA GRANDE':42}[kind]
        for xx in range(x+18,x+w-10,gap): d.line(xx,y+50,xx,y+h-14)
        for yy in range(y+50,y+h-14,gap): d.line(x+18,yy,x+w-18,yy)
    elif kind.startswith('PUNTOS'):
        gap={'PUNTOS PEQUEÑOS':14,'PUNTOS MEDIOS':22,'PUNTOS GRANDES':32}[kind]
        for xx in range(x+20,x+w-12,gap):
            for yy in range(y+52,y+h-10,gap): d.c.circle(xx,HEIGHT-yy,1,fill=1,stroke=0)
    elif kind=='CORNELL': d.line(x+136,y+48,x+136,y+h-14); d.line(x+18,y+h-130,x+w-18,y+h-130)
    elif kind=='DOS COLUMNAS': d.line(x+w/2,y+48,x+w/2,y+h-14)
    elif kind=='TRES COLUMNAS': d.line(x+w/3,y+48,x+w/3,y+h-14); d.line(x+2*w/3,y+48,x+2*w/3,y+h-14)
    elif kind=='CHECKLIST':
        for yy in range(y+65,y+h-20,42): d.box(x+20,yy,17,17,d.t.paper,stroke=True); d.line(x+52,yy+10,x+w-20,yy+10)
    elif 'MITAD' in kind: d.line(x+18,y+h/2,x+w-18,y+h/2); d.text('ESPACIO DE ESCRITURA',x+28,y+h/2-18,11,'Bold')
    elif kind=='ESQUEMA':
        for i in range(6): d.line(x+28+i*24,y+75+i*70,x+w-30,y+75+i*70)
    else: d.text('Espacio libre para escribir, dibujar o pegar imágenes.',x+28,y+90,15,'Body')

def draw_nb(d,p,all_pages):
    code=p['code']; k=p['kind']
    if k=='cover':
        d.box(24,24,492,900,d.t.soft,radius=22); d.box(42,42,456,864,d.t.background,radius=18); d.text("YOYI'R",270,255,52,'Editorial',center=True); d.text(p['title'].split('·')[-1].strip(),270,320,25,'Bold',center=True); d.text('CUADERNO DIGITAL',270,365,15,'Bold',d.t.accent,center=True); nb_button(d,'ABRIR CUADERNO',nid(code,'uso'),92,510,356,76); d.text('Este cuaderno pertenece a',270,700,12,'Bold',center=True); d.line(110,745,430,745); return
    if k=='howto':
        nb_header(d,code,p['title'],'ORGANIZA, ESCRIBE Y CREA');
        lines=['Usa las pestañas numeradas para navegar.','Escribe o dibuja con las herramientas de tu aplicación.','Puedes insertar imágenes y elementos si tu aplicación lo permite.','Puedes duplicar páginas desde el administrador de páginas si tu aplicación ofrece esa función.','Los cambios se gestionan dentro de la aplicación que utilices.']
        for i,line in enumerate(lines): lib_y=220+i*95; d.text(f'{i+1:02d}',30,lib_y,20,'Editorial',d.t.accent); d.paragraph(line,78,lib_y,410,16,24)
        footer_nb(d,code,p['id']); return
    if k=='identification': nb_header(d,code,'IDENTIFICACIÓN'); d.text('NOMBRE',24,230,13,'Bold'); d.line(24,270,516,270); d.text('FECHA DE INICIO',24,340,13,'Bold'); d.line(24,380,270,380); d.text('PROPÓSITO DE ESTE CUADERNO',24,450,13,'Bold'); d.box(24,475,492,250,d.t.paper,stroke=True); footer_nb(d,code,p['id']); return
    if k=='index':
        nb_header(d,code,'ÍNDICE','10 SECCIONES PERSONALIZABLES'); sections=[x for x in all_pages if x['kind']=='section']
        for i,s in enumerate(sections): nb_button(d,f'{i+1:02d} · SECCIÓN',s['id'],24+(i%2)*252,200+(i//2)*90,240,70)
        nb_button(d,'MIS SECCIONES',nid(code,'secciones'),24,700,240,70); nb_button(d,'IDENTIFICACIÓN',nid(code,'identificacion'),276,700,240,70); nb_button(d,'ELIGE TU PORTADA',nid(code,'portadas'),24,780,240,70); footer_nb(d,code,p['id']); return
    if k=='mysections':
        nb_header(d,code,'MIS SECCIONES');
        for i in range(10): d.text(f'{i+1:02d}',30,215+i*58,13,'Bold',d.t.accent); d.line(75,215+i*58,500,215+i*58)
        footer_nb(d,code,p['id']); return
    if k=='covers':
        nb_header(d,code,'ELIGE TU PORTADA','RECURSOS INTERCAMBIABLES');
        for i,key in enumerate(THEME_KEYS): nb_button(d,THEME_ES[key],nid(code,'inicio'),24+(i%2)*252,210+(i//2)*100,240,72)
        d.paragraph('Estas opciones sirven para organizar recursos. Tocar una portada no cambia automáticamente el PDF.',24,760,480,14,22); footer_nb(d,code,p['id']); return
    if k=='papers':
        nb_header(d,code,'BIBLIOTECA DE PAPEL','ELIGE UNA PÁGINA PARA ESCRIBIR');
        for i,paper in enumerate(PAPERS): nb_button(d,f'{i+1:02d} · {paper}',nid(code,f'papel-{i+1:02d}'),24+(i%2)*252,195+(i//2)*74,240,66)
        footer_nb(d,code,p['id']); return
    if k=='templates':
        nb_header(d,code,'BIBLIOTECA DE PLANTILLAS','PLANTILLAS REUTILIZABLES'); templates=[x for x in all_pages if x['kind']=='template']
        for i,t in enumerate(templates): nb_button(d,f'{i+1:02d} · {t["title"]}',t['id'],24+(i%2)*252,195+(i//2)*82,240,70)
        footer_nb(d,code,p['id']); return
    if k=='paper': draw_paper(d,p); footer_nb(d,code,p['id']); return
    if k=='section':
        nb_header(d,code,p['title'],'ESCRIBE EL NOMBRE DE ESTA SECCIÓN'); d.text(f'{p["number"]:02d}',270,320,90,'Editorial',d.t.soft,center=True); d.line(90,470,430,470); d.text('DESCRIPCIÓN / PROPÓSITO',90,550,13,'Bold',d.t.accent); d.line(90,610,430,610); nb_button(d,'PÁGINA DE NOTAS',nid(code,f'seccion-{p["number"]:02d}-notas-1'),24,730,240,70); nb_button(d,'OTRA PÁGINA',nid(code,f'seccion-{p["number"]:02d}-notas-2'),276,730,240,70); footer_nb(d,code,p['id']); return
    if k=='note':
        nb_header(d,code,'PÁGINA DE NOTAS',f'SECCIÓN {p["number"]:02d}'); draw_paper(d,dict(p,paper=p['template'].upper())); footer_nb(d,code,nid(code,f'seccion-{p["number"]:02d}')); return
    if k=='template':
        nb_header(d,code,p['title'],'PLANTILLA REUTILIZABLE');
        for i,label in enumerate(['PROPÓSITO','IDEAS / CONTENIDO','PRÓXIMOS PASOS','NOTAS']): panel(d,label,24+(i%2)*252,205+(i//2)*180,240,155)
        d.paragraph('Puedes duplicar esta plantilla desde las herramientas de páginas de tu aplicación de anotación, cuando esta función esté disponible.',24,805,480,13,20); footer_nb(d,code,p['id']); return

def render_notebook(path,pages,theme_key):
    nav=Navigation(pages); c=canvas.Canvas(str(path),pagesize=(WIDTH,HEIGHT),pageCompression=1,pdfVersion=(1,4),invariant=1); c.setTitle("YOYI'R | Cuaderno digital | Español"); c.setAuthor("YOYI'R")
    byid={p['id']:p for p in pages}
    for i,p in enumerate(pages):
        c.bookmarkPage(p['id'],fit='Fit'); c.addOutlineEntry(p['title'],p['id'],0); d=Drawing(c,THEMES[theme_key],nav,p['id']); d.box(0,0,WIDTH,HEIGHT,d.t.background,radius=0); draw_nb(d,p,pages); d.text(f"YOYI'R  /  {i+1:03d}",24,955,8,color=d.t.accent); c.showPage()
    nav.check(); c.save(); return nav

def make_cover_resources(folder):
    folder.mkdir(parents=True,exist_ok=True); files=[]
    for code,title,_,_ in NOTEBOOKS:
        for key in THEME_KEYS:
            path=folder/f'YOYIR-{code}-{key}-portada.pdf'; c=canvas.Canvas(str(path),pagesize=(WIDTH,HEIGHT),pageCompression=1,pdfVersion=(1,4),invariant=1); t=THEMES[key]; c.setFillColor(HexColor(t.background)); c.rect(0,0,WIDTH,HEIGHT,fill=1,stroke=0); c.setFillColor(HexColor(t.soft)); c.roundRect(40,80,460,800,30,fill=1,stroke=0); c.setFillColor(HexColor(t.accent)); c.setFont('YEditorial',44); c.drawCentredString(270,570,"YOYI'R"); c.setFont('YBold',20); c.drawCentredString(270,520,title); c.setFont('YBody',13); c.drawCentredString(270,485,'CUADERNO DIGITAL'); c.showPage(); c.save(); files.append(path)
    return files

def build_phase5(output=None):
    started=time.time(); out=Path(output or OUTPUT); out.mkdir(parents=True,exist_ok=True); (out/'notebooks').mkdir(exist_ok=True); register_fonts(); build_phase3(out)
    covers=make_cover_resources(out/'notebook-covers'); reports=[]
    filenames={'notas':'YOYIR-Cuaderno-Notas-ES.pdf','estudio':'YOYIR-Cuaderno-Estudio-ES.pdf','proyectos':'YOYIR-Cuaderno-Proyectos-ES.pdf','ideas':'YOYIR-Cuaderno-Ideas-ES.pdf','bienestar':'YOYIR-Cuaderno-Bienestar-ES.pdf','personal':'YOYIR-Mi-Cuaderno-ES.pdf'}
    for code,title,sections,templates in NOTEBOOKS:
        pages=add_pages(code,title,sections,templates); path=out/'notebooks'/filenames[code]; nav=render_notebook(path,pages,'lavender'); reader=PdfReader(path,strict=True); doc=fitz.open(path); broken=sum(1 for pg in reader.pages for a in pg.get('/Annots',[]) if a.get_object().get('/Dest') is None); reports.append({'nombre':title,'archivo':str(path.relative_to(ROOT)),'paginas':len(pages),'secciones':10,'plantillas':len(templates),'papeles':len(PAPERS),'enlaces':len(nav.links),'enlaces_rotos':broken}); doc.close()
    (out/'notebook-validation.json').write_text(json.dumps({'notebooks':reports,'portadas':len(covers),'enlaces_rotos':sum(x['enlaces_rotos'] for x in reports)},ensure_ascii=False,indent=2)+'\n',encoding='utf-8'); write_notebook_inventory(reports,len(covers));
    from zipfile import ZipFile, ZIP_DEFLATED
    with ZipFile(out/'YOYIR-Phase5-Bundle.zip','w',ZIP_DEFLATED) as bundle:
        bundle.write(out/'YOYIR-Planificador-Digital-2026-2028-ES.pdf','YOYIR-Planificador-Digital-2026-2028-ES.pdf')
        for r in reports: bundle.write(ROOT/r['archivo'],r['archivo'])
        for cover in covers: bundle.write(cover,'notebook-covers/'+cover.name)
        for docfile in [DOCS/'BUILD-REPORT.md',DOCS/'NOTEBOOK-INVENTORY.md',out/'notebook-validation.json']:
            bundle.write(docfile,docfile.name)
    report_path=DOCS/'BUILD-REPORT.md'; marker='\n\n## FASE 5 — Sistema de seis cuadernos digitales'; old=report_path.read_text(encoding='utf-8'); old=old.split(marker,1)[0] if marker in old else old; report_path.write_text(old+marker+'\n\n'+json.dumps({'notebooks_generados':6,'portadas_notebook':len(covers),'total_paginas_notebooks':sum(x['paginas'] for x in reports),'total_hipervinculos_notebooks':sum(x['enlaces'] for x in reports),'enlaces_rotos':sum(x['enlaces_rotos'] for x in reports),'tamano_cada_pdf':{x['archivo']:Path(ROOT/x['archivo']).stat().st_size for x in reports},'paquete':'output/YOYIR-Phase5-Bundle.zip'},ensure_ascii=False,indent=2)+'\n',encoding='utf-8');
    with ZipFile(out/'YOYIR-Phase5-Bundle.zip','w',ZIP_DEFLATED) as bundle:
        bundle.write(out/'YOYIR-Planificador-Digital-2026-2028-ES.pdf','YOYIR-Planificador-Digital-2026-2028-ES.pdf')
        for r in reports: bundle.write(ROOT/r['archivo'],r['archivo'])
        for cover in covers: bundle.write(cover,'notebook-covers/'+cover.name)
        for docfile in [DOCS/'BUILD-REPORT.md',DOCS/'NOTEBOOK-INVENTORY.md',out/'notebook-validation.json']: bundle.write(docfile,docfile.name)
    return reports

def write_notebook_inventory(reports,covers):
    lines=['# Inventario de cuadernos YOYI\'R','','Todos los cuadernos están en español y funcionan como PDF independientes.','']
    for r in reports: lines += [f'## {r["nombre"]}','',f'- Archivo: `{r["archivo"]}`',f'- Páginas: {r["paginas"]}',f'- Secciones: {r["secciones"]}',f'- Plantillas: {r["plantillas"]}',f'- Papeles: {r["papeles"]}',f'- Enlaces internos: {r["enlaces"]}',f'- Enlaces rotos: {r["enlaces_rotos"]}',f'- Portadas disponibles: {covers // 6}', '']
    (DOCS/'NOTEBOOK-INVENTORY.md').write_text('\n'.join(lines),encoding='utf-8')

if __name__=='__main__': print(json.dumps(build_phase5(),ensure_ascii=False,indent=2))
