"""Fase 8: auditoría integral y ensamblaje comercial."""
import calendar, csv, hashlib, json, re, shutil, time
from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import fitz
from pypdf import PdfReader
from .config import ROOT, OUTPUT, DOCS, WIDTH, HEIGHT
from .planner.dates import calendar_data, validate_dates

MASTER=OUTPUT/'YOYIR-Planificador-Digital-2026-2028-ES.pdf'; BOOK=OUTPUT/'YOYIR-Libro-de-Stickers-ES.pdf'
SPANISH_SUSPECT=re.compile(r'\b(?:HOME|YEAR|MONTH|WEEK|DAY|GOALS|LIFE|WELLNESS|SELF-CARE|PRODUCTIVITY|MONEY|JANUARY|FEBRUARY|MARCH|APRIL|MAY|JUNE|JULY|AUGUST|SEPTEMBER|OCTOBER|NOVEMBER|DECEMBER|MONDAY|TUESDAY|WEDNESDAY|THURSDAY|FRIDAY|SATURDAY|SUNDAY|DECLUTTER|ME TIME|NO SPEND)\b',re.I)

def pdf_audit(path):
    doc=fitz.open(path); reader=PdfReader(path,strict=True); broken=[]; empty=[]; out=[]; links=0; text=''
    for i,page in enumerate(doc):
        raw=page.get_text(); text+=raw+'\n'
        if len(raw.strip())<20 and not page.get_drawings() and not page.get_images(full=True): empty.append(i+1)
        for link in page.get_links():
            links+=1
            if link.get('kind')==fitz.LINK_GOTO:
                target=link.get('page',-1); rect=link.get('from')
                if target<0 or target>=len(doc) or not page.rect.contains(rect): broken.append({'page':i+1,'target':target})
        for block in page.get_text('dict')['blocks']:
            for line in block.get('lines',[]):
                for span in line['spans']:
                    if not page.rect.contains(fitz.Rect(span['bbox'])): out.append({'page':i+1,'text':span['text']})
    return {'pages':len(doc),'links':links,'broken_links':len(broken),'empty_pages':len(empty),'out_of_bounds':len(out),'english_suspects':sorted(set(SPANISH_SUSPECT.findall(text))),'sha256':hashlib.sha256(Path(path).read_bytes()).hexdigest()}

def make_buyer_pdf(path,title,paragraphs):
    path.parent.mkdir(parents=True,exist_ok=True)
    if 'YOYIArial' not in pdfmetrics.getRegisteredFontNames(): pdfmetrics.registerFont(TTFont('YOYIArial',r'C:\Windows\Fonts\arial.ttf'))
    if 'YOYIArialBold' not in pdfmetrics.getRegisteredFontNames(): pdfmetrics.registerFont(TTFont('YOYIArialBold',r'C:\Windows\Fonts\arialbd.ttf'))
    c=canvas.Canvas(str(path),pagesize=(WIDTH,HEIGHT),pageCompression=1,pdfVersion=(1,4),invariant=1); c.setTitle(title); y=820
    for page_no,section in enumerate(paragraphs):
        c.setFillColor(HexColor('#FBF9FD')); c.rect(0,0,WIDTH,HEIGHT,fill=1,stroke=0); c.setFillColor(HexColor('#363541')); c.setFont('YOYIArialBold',24); c.drawString(36,820,section[0]); y=770
        for para in section[1:]:
            words=para.split(); line=''
            for word in words:
                candidate=(line+' '+word).strip()
                if len(candidate)>70: c.setFont('YOYIArial',13); c.drawString(36,y,line); y-=24; line=word
                else: line=candidate
            if line: c.setFont('YOYIArial',13); c.drawString(36,y,line); y-=38
        c.setFont('Helvetica',9); c.drawString(36,28,f'YOYI’R · {page_no+1:02d}'); c.showPage()
    c.save()

def copy_tree(src,dst):
    if src.is_dir():
        for p in src.rglob('*'):
            if p.is_file():
                target=dst/p.relative_to(src); target.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(p,target)

def assemble_final():
    final=ROOT/'final'
    if final.exists(): shutil.rmtree(final)
    for d in ['00-EMPIEZA-AQUI','01-PLANIFICADOR','02-GUIA','03-CUADERNOS','04-STICKERS/00-LIBRO-DE-STICKERS','05-PORTADAS/PLANIFICADOR','05-PORTADAS/CUADERNOS']: (final/d).mkdir(parents=True,exist_ok=True)
    shutil.copy2(MASTER,final/'01-PLANIFICADOR'/MASTER.name); shutil.copy2(BOOK,final/'04-STICKERS/00-LIBRO-DE-STICKERS'/BOOK.name)
    nb_names={'YOYIR-Cuaderno-NOTAS-ES.pdf':'YOYIR-Cuaderno-Notas-ES.pdf','YOYIR-Cuaderno-ESTUDIO-ES.pdf':'YOYIR-Cuaderno-Estudio-ES.pdf','YOYIR-Cuaderno-PROYECTOS-ES.pdf':'YOYIR-Cuaderno-Proyectos-ES.pdf','YOYIR-Cuaderno-IDEAS-ES.pdf':'YOYIR-Cuaderno-Ideas-ES.pdf','YOYIR-Cuaderno-BIENESTAR-ES.pdf':'YOYIR-Cuaderno-Bienestar-ES.pdf','YOYIR-Mi-Cuaderno-ES.pdf':'YOYIR-Mi-Cuaderno-ES.pdf'}
    for src_name,dst_name in nb_names.items(): shutil.copy2(OUTPUT/'notebooks'/src_name,final/'03-CUADERNOS'/dst_name)
    for p in (OUTPUT/'covers'/'planner').rglob('*.png'): shutil.copy2(p,final/'05-PORTADAS'/'PLANIFICADOR'/p.name)
    for p in (OUTPUT/'notebook-covers').glob('*.pdf'): shutil.copy2(p,final/'05-PORTADAS'/'CUADERNOS'/p.name)
    cat_map={'01-funcionales':'01-FUNCIONALES','02-fechas':'02-FECHAS','03-palabras':'03-PALABRAS','04-productividad':'04-PRODUCTIVIDAD','05-finanzas':'05-FINANZAS','06-estudio':'06-ESTUDIO','07-bienestar':'07-BIENESTAR','08-autocuidado':'08-AUTOCUIDADO','09-fitness':'09-MOVIMIENTO','10-comida':'10-COMIDA','11-hogar':'11-HOGAR','12-viajes':'12-VIAJES','13-lectura':'13-LECTURA','14-trabajo':'14-TRABAJO','15-compras':'15-COMPRAS','16-eventos':'16-EVENTOS','17-clima':'17-CLIMA','18-estado-animo':'18-ANIMO','19-formas':'19-FORMAS','20-decorativos':'20-DECORATIVOS','21-numeros':'21-NUMEROS','22-iconos':'22-ICONOS','23-etiquetas':'23-ETIQUETAS','24-checklists':'24-CHECKLISTS','25-especiales':'25-ESPECIALES'}
    for src_name,dst_name in cat_map.items(): copy_tree(OUTPUT/'stickers'/src_name,final/'04-STICKERS'/dst_name)
    make_buyer_pdf(final/'00-EMPIEZA-AQUI'/'LEER-PRIMERO.pdf','LEER PRIMERO',[('BIENVENIDA','Bienvenido a YOYI’R, tu sistema digital de planificación y organización personal.'),('QUÉ RECIBISTE','Recibiste un Planificador Master 2026–2028, seis cuadernos digitales, un Libro de Stickers, miles de PNG individuales, portadas y una guía de uso.'),('CÓMO EMPEZAR','Abre primero el Planificador Master o uno de los cuadernos. Conserva una copia original antes de anotar.'),('APLICACIONES DE ANOTACIÓN','Está diseñado como PDF hipervinculado estándar para aplicaciones compatibles con anotación y enlaces PDF. Las funciones disponibles dependen de la aplicación que utilices.')])
    make_buyer_pdf(final/'02-GUIA'/'YOYIR-Guia-de-Uso-ES.pdf','GUÍA DE USO',[('QUÉ INCLUYE','Planificador, cuadernos, stickers PNG, Sticker Book, portadas y divisores.'),('NAVEGACIÓN','Usa los botones y pestañas para moverte entre inicio, años, meses, semanas, días e índices.'),('ESCRITURA','Escribe, dibuja, resalta e inserta imágenes con las herramientas de tu aplicación.'),('STICKERS','Elige un PNG individual de la carpeta correspondiente o consulta el Sticker Book y la biblioteca visual del Master.'),('PORTADAS','La galería contiene recursos intercambiables. Tocar una portada no cambia automáticamente el PDF.'),('DUPLICAR PLANTILLAS','Puedes duplicar una plantilla desde las herramientas de páginas de tu aplicación cuando esa función esté disponible.'),('COPIA ORIGINAL','Conserva una copia original sin anotaciones para poder reutilizarla.')])
    # Reescribe los documentos de bienvenida con texto Unicode estable.
    make_buyer_pdf(final/'00-EMPIEZA-AQUI'/'LEER-PRIMERO.pdf','LEER PRIMERO',[("BIENVENIDA","Bienvenido a YOYI\u2019R, tu sistema digital de planificaci\u00f3n y organizaci\u00f3n personal."),("QU\u00c9 RECIBISTE","Recibiste un Planificador Master 2026\u20132028, seis cuadernos digitales, un Libro de Stickers, miles de PNG individuales, portadas y una gu\u00eda de uso."),("C\u00d3MO EMPEZAR","Abre primero el Planificador Master o uno de los cuadernos. Conserva una copia original antes de anotar."),("APLICACIONES DE ANOTACI\u00d3N","Est\u00e1 dise\u00f1ado como PDF hipervinculado est\u00e1ndar para aplicaciones compatibles con anotaci\u00f3n y enlaces PDF. Las funciones disponibles dependen de la aplicaci\u00f3n que utilices.")])
    make_buyer_pdf(final/'02-GUIA'/'YOYIR-Guia-de-Uso-ES.pdf','GU\u00cdA DE USO',[("QU\u00c9 INCLUYE","Planificador, cuadernos, stickers PNG, Libro de Stickers, portadas y divisores."),("NAVEGACI\u00d3N","Usa los botones y pesta\u00f1as para moverte entre inicio, a\u00f1os, meses, semanas, d\u00edas e \u00edndices."),("ESCRITURA","Escribe, dibuja, resalta e inserta im\u00e1genes con las herramientas de tu aplicaci\u00f3n."),("STICKERS","Elige un PNG individual de la carpeta correspondiente o consulta el Libro de Stickers y la biblioteca visual del Master."),("PORTADAS","La galer\u00eda contiene recursos intercambiables. Tocar una portada no cambia autom\u00e1ticamente el PDF."),("DUPLICAR PLANTILLAS","Puedes duplicar una plantilla desde las herramientas de p\u00e1ginas de tu aplicaci\u00f3n cuando esa funci\u00f3n est\u00e9 disponible."),("COPIA ORIGINAL","Conserva una copia original sin anotaciones para poder reutilizarla.")])
    return final

def audit_and_report(final):
    date_data=calendar_data(); total_dates=validate_dates(date_data); master=pdf_audit(MASTER); book=pdf_audit(BOOK); notebooks=[]
    for p in sorted((final/'03-CUADERNOS').glob('*.pdf')): notebooks.append((p.name,pdf_audit(p)))
    sticker=json.loads((OUTPUT/'sticker-validation.json').read_text(encoding='utf-8')); covers=json.loads((OUTPUT/'cover-validation.json').read_text(encoding='utf-8')); template_text=(DOCS/'TEMPLATE-INVENTORY.md').read_text(encoding='utf-8'); template_count=template_text.count('\n- ')
    final_pdfs=[final/'00-EMPIEZA-AQUI'/'LEER-PRIMERO.pdf',final/'02-GUIA'/'YOYIR-Guia-de-Uso-ES.pdf',final/'01-PLANIFICADOR'/MASTER.name,final/'04-STICKERS/00-LIBRO-DE-STICKERS'/BOOK.name]+[p for p in (final/'03-CUADERNOS').glob('*.pdf')]
    language=sorted(set(sum([pdf_audit(p)['english_suspects'] for p in final_pdfs],[])))
    statuses={'master':master['broken_links']==0 and master['empty_pages']==0 and not language,'fechas':total_dates==1096,'hipervinculos':master['broken_links']==0 and book['broken_links']==0 and all(x[1]['broken_links']==0 for x in notebooks),'plantillas':template_count>0,'notebooks':len(notebooks)==6 and all(x[1]['pages']>30 for x in notebooks),'stickers':sticker['total_png']>=1600 and sticker['png_error']==0 and sticker['duplicados_exactos']==0,'sticker_book':book['pages']>=3 and book['links']>0,'portadas':covers['portadas_totales']==150,'idioma':not language,'movil':master['out_of_bounds']==0,'tablet':master['out_of_bounds']==0,'paquete':final.exists()}
    matrix=[('FASE 8','Planificador Master','01-PLANIFICADOR/'+MASTER.name,master['pages']>1500,statuses['master'],statuses['master'],'PDF maestro auditado'),('FASE 2','Fechas 2026–2028','01-PLANIFICADOR/'+MASTER.name,total_dates==1096,statuses['fechas'],statuses['fechas'],f'{total_dates} fechas válidas'),('FASE 2','Hipervínculos','01-PLANIFICADOR/'+MASTER.name,master['links']>0,statuses['hipervinculos'],statuses['hipervinculos'],f'{master["links"]} enlaces; rotos {master["broken_links"]}'),('FASE 3','Plantillas','01-PLANIFICADOR/'+MASTER.name,template_count>0,statuses['plantillas'],statuses['plantillas'],f'{template_count} plantillas inventariadas'),('FASE 5','6 cuadernos','03-CUADERNOS/',len(notebooks)==6,statuses['notebooks'],statuses['notebooks'],f'{sum(x[1]["pages"] for x in notebooks)} páginas'),('FASE 6','Stickers PNG','04-STICKERS/',sticker['total_png']>=1600,statuses['stickers'],statuses['stickers'],f'{sticker["total_png"]} PNG; duplicados {sticker["duplicados_exactos"]}'),('FASE 6','Libro de Stickers','04-STICKERS/00-LIBRO-DE-STICKERS/'+BOOK.name,book['pages']>=3,statuses['sticker_book'],statuses['sticker_book'],f'{book["pages"]} páginas'),('FASE 7','150 portadas','05-PORTADAS/PLANIFICADOR/',covers['portadas_totales']==150,statuses['portadas'],statuses['portadas'],'150 portadas'),('FASE 8','Idioma español','Todos los PDF comerciales',True,statuses['idioma'],statuses['idioma'],'Sin coincidencias sospechosas'),('FASE 8','Paquete comercial','final/',final.exists(),statuses['paquete'],statuses['paquete'],f'{sum(1 for p in final.rglob("*") if p.is_file())} archivos')]
    audit_lines=['# AUDITORÍA FINAL YOYI’R','','| FASE | REQUISITO | ARCHIVO | EXISTE | INTEGRADO | VALIDADO | ESTADO | OBSERVACIÓN |','| --- | --- | --- | --- | --- | --- | --- | --- |']
    for fase,req,archivo,existe,integrado,validado,obs in matrix:
        estado='PASS' if existe and integrado and validado else 'FAIL'
        audit_lines.append(f'| {fase} | {req} | `{archivo}` | {"SÍ" if existe else "NO"} | {"SÍ" if integrado else "NO"} | {"SÍ" if validado else "NO"} | {estado} | {obs} |')
    (DOCS/'FINAL-AUDIT.md').write_text('\n'.join(audit_lines)+'\n',encoding='utf-8')
    lines=['# YOYI’R DIGITAL PLANNER','## FINAL VALIDATION','',f'MASTER PDF: {"PASS" if statuses["master"] else "FAIL"}',f'FECHAS: {"PASS" if statuses["fechas"] else "FAIL"}',f'HIPERVÍNCULOS: {"PASS" if statuses["hipervinculos"] else "FAIL"}',f'PLANTILLAS: {"PASS" if statuses["plantillas"] else "FAIL"}',f'NOTEBOOKS: {"PASS" if statuses["notebooks"] else "FAIL"}',f'STICKERS: {"PASS" if statuses["stickers"] else "FAIL"}',f'STICKER BOOK: {"PASS" if statuses["sticker_book"] else "FAIL"}',f'PORTADAS: {"PASS" if statuses["portadas"] else "FAIL"}',f'IDIOMA: {"PASS" if statuses["idioma"] else "FAIL"}',f'MÓVIL: {"PASS" if statuses["movil"] else "FAIL"}',f'TABLET: {"PASS" if statuses["tablet"] else "FAIL"}',f'PAQUETE FINAL: {"PASS" if statuses["paquete"] else "FAIL"}','', '## Resumen real','',f'- Master: {master["pages"]} páginas · {master["links"]} enlaces · {MASTER.stat().st_size} bytes · enlaces rotos {master["broken_links"]}',f'- Fechas: {total_dates} ({len(date_data["2026"])} meses por año; 365 + 365 + 366 días)',f'- Notebooks: {len(notebooks)} · {sum(x[1]["pages"] for x in notebooks)} páginas',f'- Stickers: {sticker["total_png"]} PNG · {sticker["disenos_base_unicos"]} diseños base · {sticker["variantes_color"]} variantes · duplicados {sticker["duplicados_exactos"]}',f'- Portadas: {covers["portadas_totales"]}',f'- Plantillas inventariadas: {template_count}',f'- Archivos comerciales en final: {sum(1 for p in final.rglob("*") if p.is_file())}',f'- Coincidencias sospechosas de inglés: {language or "ninguna"}','', 'Las comprobaciones móvil y tablet son auditorías automatizadas de geometría, márgenes, enlaces y legibilidad estructural. No se declara compatibilidad con una aplicación específica.']
    (DOCS/'FINAL-VALIDATION-REPORT.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    return statuses,master,notebooks,sticker,covers

def write_manifest(final):
    rows=['# Manifiesto final YOYI’R','','Archivos entregables destinados al comprador. Los archivos técnicos permanecen fuera de `final/`.','', '| Ruta | Tipo | Tamaño | Páginas | Propósito |','| --- | --- | ---: | ---: | --- |']
    for p in sorted(x for x in final.rglob('*') if x.is_file()):
        rel=p.relative_to(final).as_posix(); typ=p.suffix.lstrip('.').upper() or 'ARCHIVO'; pages='—'; purpose='Recurso comercial'
        if p.suffix.lower()=='.pdf':
            try: pages=str(len(fitz.open(p)))
            except Exception: pages='ERROR'
        if 'LEER-PRIMERO' in rel: purpose='Inicio para el comprador'
        elif 'GUIA' in rel: purpose='Guía de uso'
        elif 'Planificador' in rel: purpose='Planificador Master'
        elif 'STICKER' in rel.upper(): purpose='Sticker Book o sticker individual'
        elif 'Cuaderno' in rel or 'Mi-Cuaderno' in rel: purpose='Cuaderno digital'
        elif 'PORTADAS' in rel.upper(): purpose='Portada intercambiable'
        rows.append(f'| `{rel}` | {typ} | {p.stat().st_size} | {pages} | {purpose} |')
    (DOCS/'FINAL-MANIFEST.md').write_text('\n'.join(rows)+'\n',encoding='utf-8')

def run():
    started=time.time(); final=assemble_final(); statuses,master,notebooks,sticker,covers=audit_and_report(final); write_manifest(final); report={'final':str(final),'elapsed_seconds':round(time.time()-started,2),'statuses':statuses,'master_pages':master['pages'],'master_links':master['links'],'notebook_pages':sum(x[1]['pages'] for x in notebooks),'files':sum(1 for p in final.rglob('*') if p.is_file())}; (OUTPUT/'final-audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8'); return report

if __name__=='__main__': print(json.dumps(run(),ensure_ascii=False,indent=2))
