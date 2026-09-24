"""python -m src.premium.build — renders only the art-direction prototype."""
import calendar
import hashlib
import json
from pathlib import Path
import fitz
from PIL import Image,ImageDraw
from pypdf import PdfReader
from reportlab.pdfgen import canvas
from ..config import ROOT,OUTPUT,DOCS
from ..components import register_fonts
from .art import Art,W,H,COLORS,NAMES
from .shell import digital_planner_shell
from .pages import manifest,draw

NAME='YOYIR-Premium-High-Fidelity-Prototype.pdf'
PREVIEW_PAGES=[1,2,5,10,11,15,19,22,24,28,29]

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def build():
    OUTPUT.mkdir(exist_ok=True);DOCS.mkdir(exist_ok=True)
    before={p.name:sha(p) for p in OUTPUT.glob('*.pdf') if p.name!=NAME}
    register_fonts()
    path=OUTPUT/NAME;pages=manifest();nav=[];art=[]
    c=canvas.Canvas(str(path),pagesize=(W,H),pageCompression=1,pdfVersion=(1,4),invariant=1)
    c.setTitle("YOYI'R · Planificador digital 2026–2028")
    c.setAuthor("E-books para la vida — YOYI'R")
    for i,p in enumerate(pages):
        c.bookmarkPage(p['id'],fit='Fit');c.addOutlineEntry(p['title'],p['id'],level=0)
        a=Art(c,p['id'],nav)
        if p['id']!='portada':digital_planner_shell(a,p,i,len(pages))
        draw(a,p)
        art.append({'page':i,'id':p['id'],'icons':a.icons,'stickers':a.stickers,'calendars':a.calendars})
        c.showPage()
    c.save()
    result=validate(path,pages,nav,art,before)
    (OUTPUT/'premium-validation.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    (OUTPUT/'premium-navigation.json').write_text(json.dumps(nav,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    report(result,pages,art)
    print(json.dumps({k:result[k] for k in ['pages','links','calendars','stickers','errors']},ensure_ascii=False),flush=True)

def validate(path,pages,nav,art,before):
    reader=PdfReader(path,strict=True);doc=fitz.open(path)
    assert len(doc)==len(pages)==33 and not doc.is_repaired and not doc.is_encrypted
    assert '/AcroForm' not in reader.trailer['/Root']
    page_ids={p['id']:i for i,p in enumerate(pages)}
    destinations=dict(page_ids)
    for year in (2026,2027,2028):
        for month in range(1,13):destinations[f'm-{year}-{month:02d}']=page_ids[f'year-{year}']
    for key in ('vision','metas','accion','progreso','revision'):destinations['smart-'+key]=page_ids['smart']
    reachable={'portada'}
    while True:
        expanded=reachable|{pages[destinations[e['target']]]['id'] for e in nav if e['source'] in reachable}
        if expanded==reachable:break
        reachable=expanded
    assert len(reachable)==len(pages)
    for i,p in enumerate(doc):
        assert p.rect==fitz.Rect(0,0,W,H)
        text=p.get_text()
        assert len(text.strip())>25
        assert all(term not in text.upper() for term in ('ESPACIO PARA ESCRIBIR','PLACEHOLDER','PREVIEW','TODAY'))
        links=[e for e in nav if e['source']==pages[i]['id']]
        annotations=reader.pages[i].get('/Annots',[])
        assert len(links)==len(annotations)>0
        rects=[]
        for link,ref in zip(links,annotations):
            annotation=ref.get_object();dest=annotation['/Dest']
            target=destinations[link['target']]
            assert dest[0].idnum==reader.pages[target].indirect_reference.idnum
            x,y,x2,y2=link['rect'];box=fitz.Rect(x,y,x2,y2)
            assert x2-x>=64 and y2-y>=64
            assert p.rect.contains(box)
            assert all(abs(float(u)-v)<.01 for u,v in zip(annotation['/Rect'],[x,H-y2,x2,H-y]))
            for other in rects:assert not box.intersects(other),('Overlapping links',i,link)
            rects.append(box)
        for block in p.get_text('dict')['blocks']:
            for ln in block.get('lines',[]):
                for span in ln['spans']:
                    assert p.rect.contains(fitz.Rect(span['bbox'])),('Text overflow',i+1,span['text'],span['bbox'])
        for drawing in p.get_drawings():assert p.rect.contains(drawing['rect']),('Drawing overflow',i+1,drawing['rect'])
        p.get_pixmap(matrix=fitz.Matrix(.25,.25),alpha=False)
        for info in art[i]['calendars']:
            expected=list(range(1,calendar.monthrange(info['year'],info['month'])[1]+1))
            assert [cell[0] for cell in info['cells']]==expected
            for number,col,x,y in info['cells']:
                from datetime import date
                assert date(info['year'],info['month'],number).weekday()==col
                # Verify the printed glyph in its local date cell.
                nearby=p.get_text(clip=fitz.Rect(x-9,y-10,x+17,y+3)).split()
                assert str(number) in nearby,('Missing printed date',i+1,number,nearby)
    for xref in range(1,doc.xref_length()):
        obj=doc.xref_object(xref)
        assert not any(term in obj for term in ('/JavaScript','/JS ','/URI','/GoToR','/Launch','/EmbeddedFiles'))
    for name,old in before.items():assert sha(OUTPUT/name)==old,('Existing PDF changed',name)
    preview=OUTPUT/'premium-preview-images';preview.mkdir(exist_ok=True)
    generated=[]
    for num in PREVIEW_PAGES:
        file=preview/f'{num:02d}-{pages[num-1]["id"]}.png'
        doc[num-1].get_pixmap(matrix=fitz.Matrix(3,3),alpha=False).save(file)
        generated.append(file.name)
    for start in range(0,len(pages),12):
        sheet=Image.new('RGB',(1120,1512),'#E4E0E3');dd=ImageDraw.Draw(sheet)
        for j in range(min(12,len(pages)-start)):
            pix=doc[start+j].get_pixmap(matrix=fitz.Matrix(.5,.5),alpha=False)
            x=(j%4)*280+5;y=(j//4)*504+5
            sheet.paste(Image.frombytes('RGB',(pix.width,pix.height),pix.samples),(x,y))
            dd.text((x+4,y+481),f'{start+j+1:02d} / {pages[start+j]["id"]}',fill='#383940')
        sheet.save(preview/f'contact-{start//12+1:02d}.png')
    return {'file':NAME,'pages':len(pages),'links':len(nav),'dimensions_pt':[W,H],
            'minimum_target_pt':64,'minimum_target_at_360px':64*360/W,
            'calendars':sum(len(p['calendars']) for p in art),
            'stickers':sum(p['stickers'] for p in art),'functional_stickers':art[27]['stickers'],'life_stickers':art[28]['stickers'],
            'icon_names':sorted({name for p in art for name in p['icons']}),
            'layout_families':sorted({p['family'] for p in pages}),
            'pngs':generated,'png_dimensions':[1620,2880],
            'unchanged_existing_pdfs':before,'errors':[],'sha256':sha(path)}

def report(r,pages,art):
    lines=["# YOYI'R · Dirección de arte de alta fidelidad",'',
           f'**PÁGINAS:** {r["pages"]}: las 30 páginas solicitadas más 2027, 2028 y sin fecha para resolver los accesos del inicio.',
           f'**PDF:** `output/{NAME}`. {W} × {H} pt, vertical. {r["links"]} enlaces internos reales.',
           '',f'**LAYOUT FAMILIES:** {len(r["layout_families"])} familias diferenciadas.','',
           '| Página | Diseño | Familia |','| ---: | --- | --- |']
    for i,p in enumerate(pages):lines.append(f'| {i+1:02d} | {p["title"]} | {p["family"]} |')
    lines += ['', '**COLORES:** '+', '.join(f'{name} `{color}`' for name,color in zip(NAMES,COLORS))+'.',
              '', '**COMPONENTES:** DIGITAL_PLANNER_SHELL, papel interior, borde de hojas, sombra de papel, margen de encuadernación, cinco pestañas superiores, pestañas laterales mensuales/de sección, estado activo, menú, cinta washi, nota adhesiva, clip vectorial, renglones, checklist, mini calendarios, timeline, escala de ánimo, gotas, barra segmentada, matriz, collage y stickers troquelados.',
              '', '**ICONOS:** '+', '.join(r['icon_names'])+'. Todos dibujados con vectores propios; sin emojis, imágenes descargadas ni clipart externo.',
              '',f'**STICKERS VISIBLES:** {r["stickers"]} instancias: {r["functional_stickers"]} en la hoja funcional, {r["life_stickers"]} en la hoja de vida y el resto integrado en dashboards/páginas. Son arte vectorial real. Las hojas no simulan una función de inserción al tocarlas.',
              '', '**TRACKERS:** agua con 8 gotas; ánimo/energía con escalas; hábitos con puntos; sueño con línea temporal por día; ahorro y progreso con barras segmentadas; movimiento con icono y registro. Los indicadores se marcan usando la aplicación de anotación, sin cálculos ni automatización.',
              '', f'**CALENDARIOS VALIDADOS:** {r["calendars"]}: 36 mini calendarios anuales, enero 2026, febrero 2028, marzo 2026 y mini marzo de estudio. Fechas calculadas con calendar/datetime y verificadas sobre el texto realmente dibujado. Enero 2026 empieza en jueves; febrero 2028 incluye el martes 29. Sin números de día 32–35.',
              '', '**NAVEGACIÓN:** destinos PDF /Fit y /FitR. El mes con página desarrollada abre esa página; el resto abre su mini calendario del mismo año. Los cinco accesos SMART apuntan a sus áreas reales. Los accesos semana/día muestran las páginas de ejemplo 16–22/03/2026 y 18/03/2026. No existen páginas fechadas completas fuera de este prototipo.',
              '', '**PLACEHOLDERS:** 0 textos de relleno; no aparece “ESPACIO PARA ESCRIBIR”. Los renglones y campos en blanco son áreas de anotación intencionales, no contenido pendiente.',
              '', '**ERRORES AUTOMÁTICOS:** 0. PDFs leídos por PyMuPDF y pypdf estricto; se renderizan todas las páginas; se comprueban límites de textos/trazos, enlaces no superpuestos, destinos, fechas dibujadas, alcance de todas las páginas desde portada y ausencia de JavaScript/enlaces externos.',
              '', '**OBJETIVOS TÁCTILES:** mínimo 64 × 64 pt (42,7 × 42,7 píxeles al ajustar a 360 px de ancho). Revisar tamaño físico y comodidad en la app de teléfono/tablet elegida; no se declara compatibilidad probada con aplicaciones específicas. Los calendarios anuales requieren ampliar para leer/anotar.',
              '', '**ARCHIVOS PNG GENERADOS:** 11 previews a 1620 × 2880 px, más 3 hojas de contacto de todas las páginas.', '']
    lines += [f'- `output/premium-preview-images/{name}`' for name in r['pngs']]
    lines += ['', '**PRESERVACIÓN:** se verificó SHA-256 de todos los PDFs preexistentes antes y después; no se modificó ni regeneró el master ni el preview V2.',
              '', '**CÓDIGO:** `src/premium/` separa arte vectorial, shell, composiciones y build/validación. Generar únicamente este archivo con `python -m src.premium.build`.',
              '', '**REVISIÓN MANUAL:** revisar previews y probar navegación, /FitR, tamaño de pestañas, escritura y guardado en teléfono/tablet. La aprobación estética corresponde a la usuaria; los checks automáticos no certifican una valoración visual.',
              '', '**ESTADO:** se entrega solo este prototipo y sus previews. No se inicia otra fase ni se aplica el diseño al master.','']
    (DOCS/'HIGH-FIDELITY-DESIGN-REPORT.md').write_text('\n'.join(lines),encoding='utf-8')

if __name__=='__main__':build()
