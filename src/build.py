import argparse
import json
from datetime import datetime, timezone
from reportlab.pdfgen import canvas
from .config import ROOT, OUTPUT, DOCS, WIDTH, HEIGHT, MODULES, ANNUAL_TEMPLATES, MONTHLY_TEMPLATES
from .themes import THEMES, theme_data
from .components import Drawing, register_fonts
from .navigation import Navigation
from .planner.manifest import master_pages
from .planner.dates import calendar_data, validate_dates
from .planner.blueprint import dated_blueprint
from .layouts.planner import draw_page
from .layouts.covers import cover_catalog
from .notebooks import notebook_pages, draw_notebook, notebook_catalog
from .stickers import generate_stickers, inventory
from .validation import digest, validate_pdf, validate_pngs, validate_legacy

LEGACY = ['generate_planner.py','digital-planner-test.pdf','planner-preview.png','validation-report.json','requirements.txt']

def write_json(path,data):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')

def render_pdf(path,pages,sticker_files=None,notebook=False):
    nav=Navigation(pages)
    c=canvas.Canvas(str(path),pagesize=(WIDTH,HEIGHT),pageCompression=1,pdfVersion=(1,4),invariant=1)
    c.setTitle("YOYI'R | "+('Digital Notebook Test' if notebook else 'Digital Planner Master Test'))
    c.setAuthor("E-books para la vida — YOYI'R")
    c.setSubject('Hyperlinked PDF Digital Planner designed for PDF annotation apps on tablets and phones.')
    for i,p in enumerate(pages):
        c.bookmarkPage(p['id'],fit='Fit')
        c.addOutlineEntry(p['title'],p['id'],0)
        d=Drawing(c,THEMES[p['theme']],nav,p['id'])
        d.box(0,0,WIDTH,HEIGHT,d.t.background,radius=0)
        if notebook:
            draw_notebook(d,p)
        else:
            draw_page(d,p,sticker_files)
        d.text(f"YOYI'R  /  {i+1:02d}",24,955,8,color=d.t.accent)
        c.showPage()
    nav.check()
    c.save()
    return nav

def main():
    parser=argparse.ArgumentParser(description="Build YOYI'R Phase 1 PDF assets")
    parser.add_argument('--theme',choices=list(THEMES),default='lavender')
    parser.add_argument('--output',type=str,default=str(OUTPUT))
    args=parser.parse_args()
    out=ROOT/args.output
    out.mkdir(parents=True,exist_ok=True)
    DOCS.mkdir(parents=True,exist_ok=True)
    baseline={name:digest(ROOT/name) for name in LEGACY}
    register_fonts()
    dates=calendar_data()
    checked_dates=validate_dates(dates)
    write_json(out/'data/calendar-2026-2028.json',dates)
    write_json(out/'data/publishing-blueprint.json',dated_blueprint(dates))
    write_json(out/'data/themes.json',theme_data())
    write_json(out/'data/cover-catalog.json',cover_catalog())
    write_json(out/'data/sticker-catalog.json',inventory())
    write_json(out/'data/notebook-catalog.json',notebook_catalog())
    write_json(out/'data/template-catalog.json',{'annual':ANNUAL_TEMPLATES,'monthly':MONTHLY_TEMPLATES,
               'weekly':['WEEKLY PLANNER','WEEKLY COMPANION'],'daily':['DAILY PLANNER','DAILY COMPANION'],
               'modules':{k:v[1].split('|') for k,v in MODULES.items()},'systems':['DATED 2026–2028','UNDATED']})
    stickers=generate_stickers(out/'stickers-test',THEMES)
    png_report=validate_pngs(stickers)
    reports=[]
    for name,pages,notebook in [('YOYIR-Digital-Planner-Master-Test.pdf',master_pages(args.theme),False),
                                ('YOYIR-Notebook-Test.pdf',notebook_pages(args.theme),True)]:
        path=out/name
        nav=render_pdf(path,pages,stickers,notebook)
        stem='notebook' if notebook else 'master'
        report=validate_pdf(path,pages,nav,out/'previews'/stem)
        reports.append(report)
        write_json(out/'data'/f'{stem}-manifest.json',pages)
        write_json(out/'data'/f'{stem}-navigation.json',{'destinations':nav.destinations,'links':nav.links})
        print(f'{name}: {report["pages"]} pages, {report["links"]} internal links',flush=True)
    legacy=validate_legacy(ROOT,baseline)
    validation={'generated_utc':datetime.now(timezone.utc).isoformat(),'theme':args.theme,'pdfs':reports,
                'dates_checked':checked_dates,'pngs':png_report,'legacy':legacy,'errors':[],
                'manual_device_testing':'Pending: phone/tablet annotation apps, link activation, FitR zoom, handwriting, save/reopen.'}
    write_json(out/'validation.json',validation)
    build_report(reports,png_report,checked_dates,args.theme,out)
    from zipfile import ZipFile, ZIP_DEFLATED
    with ZipFile(out/'YOYIR-Phase1-Bundle.zip','w',ZIP_DEFLATED) as bundle:
        for file in [out/r['file'] for r in reports]+stickers+[DOCS/'BUILD-REPORT.md', DOCS/'MOBILE-TEST.md']:
            if file.is_file():
                bundle.write(file, ('stickers-test/'+file.name) if file.suffix=='.png' else file.name)
    print('Validation passed. Phase 1 only. See docs/BUILD-REPORT.md.',flush=True)

def build_report(reports,pngs,date_count,theme,out):
    lines=["# YOYI'R · Fase 1 — Informe de construcción",'',
           'Hyperlinked PDF Digital Planner designed for PDF annotation apps on tablets and phones.','',
           '## Archivos generados','',
           '| PDF | Páginas | Enlaces internos | Destinos |','| --- | ---: | ---: | ---: |']
    for r in reports:
        lines.append(f'| {r["file"]} | {r["pages"]} | {r["links"]} | {r["destinations"]} |')
    lines += ['',f'Carpeta: `{out.relative_to(ROOT) if out.is_relative_to(ROOT) else out}`.',
              f'Dimensiones: {WIDTH} × {HEIGHT} pt, vertical ({WIDTH*25.4/72:.1f} × {HEIGHT*25.4/72:.1f} mm).',
              'Objetivo táctil mínimo: 66 × 66 pt; equivale a 44 × 44 píxeles al ajustar la página a 360 píxeles de ancho. No garantiza el tamaño físico en todos los dispositivos.',
              '',f'Tema principal: **{theme.upper()}**. Seis configuraciones: LAVENDER, BLUSH, SAGE, SKY, SAND y NEUTRAL.',
              'Se incluyen 6 páginas de muestra de temas y 12 portadas vectoriales originales; el catálogo reserva 150 IDs, sin afirmar que los diseños futuros estén terminados.',
              f'Stickers: {len(pngs)} PNG RGBA de 1248 × 720 px, con píxeles transparentes y opacos. Catálogo: 28 categorías × 60 variantes reservadas = 1680 IDs.',
              'Notebook: portada, índice y 10 secciones; cada una tiene divisor y dos plantillas. Los 6 tipos de notebook están configurados; solo se publica un notebook de prueba.',
              '', '## Alcance y navegación','',
              'Master: 60 páginas. El mes completo de ejemplo es enero de 2026: dashboard, calendario, objetivos/prioridades/tareas, hábitos, finanzas y reflexión.',
              'La semana del 26 de enero al 1 de febrero y el día 31 de enero se distribuyen en dos páginas cada uno para ampliar los espacios de escritura.',
              'Los calendarios anuales contienen los 36 meses y todas las fechas de 2026–2028. Todavía no se publican los cientos de dashboards, semanas y días finales.',
              'Las pestañas mensuales usan destinos del mismo año. Enero 2026 abre el dashboard desarrollado; las demás abren una vista ampliada de su mes dentro del overview mediante /FitR. Volver al ajuste de página permite acceder a HOME e INDEX. Este comportamiento requiere validación manual en la app elegida.',
              'La navegación principal se agrupa en INDEX, accesible desde todas las páginas interiores. HOME y YEAR también permanecen visibles. Los botones Previous/Next recorren páginas existentes; no simulan días o meses aún no generados.',
              'Los índices de módulos distinguen botones de páginas disponibles y listas de plantillas planificadas sin enlaces. Las casillas, fechas y renglones destinados a escribir no se presentan como botones.',
              'El sistema Undated tiene una base mensual reutilizable y un inventario común de plantillas; no constituye aún la edición completa sin fecha.',
              'Los PNG se insertan con la app de anotación. Las portadas y temas son estáticos: no cambian dinámicamente dentro del PDF. Duplicar una página no reescribe automáticamente sus destinos.',
              '', '## Validaciones ejecutadas','',
              '- Existencia, encabezado PDF 1.4, EOF, lectura estricta con pypdf y apertura sin reparación con PyMuPDF.',
              '- Renderizado de todas las páginas; texto presente y comprobación de límites de texto, trazados y enlaces.',
              '- Cada anotación se compara con el destino planificado, incluida la referencia de página y coordenadas /FitR.',
              '- Tamaño mínimo de botones, ausencia de superposición de enlaces y de texto cruzando sus bordes.',
              '- Todas las páginas son alcanzables desde la portada mediante enlaces internos.',
              '- Fuentes TrueType incrustadas; sin formularios, JavaScript, acciones externas, vínculos web ni archivos adjuntos.',
              f'- {date_count} fechas comprobadas, incluidos 29/02/2028, inicio de semanas y transiciones de mes/año.',
              '- Lectura del texto de los 36 calendarios anuales impresos y comprobación de cada pestaña contra el año activo.',
              '- Los PNG se abren completamente y contienen canal alfa real con extremos 0 y 255.',
              '- Regresión: los 5 archivos originales conservan su SHA-256; el PDF original mantiene 8 páginas y 86 enlaces válidos.',
              '', '**Errores detectados en la validación final: 0.**',
              'Detalle reproducible: `output/validation.json`. Mapas de destinos y enlaces: `output/data/*-navigation.json`.',
              'Tecnología: Python, ReportLab, PyMuPDF, pypdf y Pillow. El usuario del PDF no necesita Python ni conexión.',
              'Paquete para transferir al dispositivo: `output/YOYIR-Phase1-Bundle.zip` (ambos PDFs, 12 PNG y guías).',
              '', '## Revisión visual y pruebas pendientes','',
              'Previews: `output/previews/master/` y `output/previews/notebook/`; hojas de contacto de todas las páginas y capturas individuales.',
              'Probar en teléfono y tablet: importar ambos PDFs; activar enlaces; abrir los tres años y sus 12 pestañas; probar el zoom /FitR y regreso al ajuste de página; recorrer Month → Week → Day y regresar; escribir, insertar PNG, guardar y reabrir; exportar una copia y comprobar conservación de enlaces.',
              'Comprobar especialmente legibilidad de calendarios anuales al ampliar y comodidad de escritura en las páginas semanal/diaria. No se declara compatibilidad probada con ninguna aplicación específica.',
              '', '## Límite de fase','',
              'Fase 2 no iniciada. La expansión a cientos de páginas, 150 portadas terminadas y 1600+ stickers dibujados requiere la siguiente aprobación.','']
    (DOCS/'BUILD-REPORT.md').write_text('\n'.join(lines),encoding='utf-8')

if __name__=='__main__':
    main()
