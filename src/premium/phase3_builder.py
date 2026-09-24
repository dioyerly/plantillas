"""PHASE 3: Add improved annual resources + Objectives collection to MASTER."""
from datetime import date
import fitz
from reportlab.pdfgen import canvas
from ..config import OUTPUT
from ..components import register_fonts
from .art import W, H, COLORS
from .shell import digital_planner_shell
from .master_builder import dated_core_block, draw_block_page
from .dated import BlockArt

def improved_resources():
    """Generate 30 improved annual resources (10 templates × 3 years)."""
    pages = []
    for year in (2026, 2027, 2028):
        resources = [
            {'resource': 'goals', 'title': 'MIS OBJETIVOS DEL AÑO'},
            {'resource': 'dates', 'title': 'FECHAS IMPORTANTES'},
            {'resource': 'birthdays', 'title': 'CUMPLEAÑOS'},
            {'resource': 'projects', 'title': 'MIS PROYECTOS'},
            {'resource': 'finance', 'title': 'OBJETIVOS FINANCIEROS'},
            {'resource': 'personal', 'title': 'OBJETIVOS PERSONALES'},
            {'resource': 'wellness', 'title': 'OBJETIVOS DE BIENESTAR'},
            {'resource': 'professional', 'title': 'OBJETIVOS PROFESIONALES'},
            {'resource': 'vision', 'title': 'MI TABLERO DE VISIÓN'},
            {'resource': 'review', 'title': 'REVISIÓN ANUAL'},
        ]
        for r in resources:
            pages.append({
                'id': f'res-{year}-{r["resource"]}',
                'kind': 'resource',
                'year': year,
                'resource': r['resource'],
                'title': r['title']
            })
    return pages

def objectives_collection():
    """Generate 12-page Objectives collection."""
    return [
        {'id': 'obj-div', 'kind': 'obj-divisor'},
        {'id': 'obj-vision', 'kind': 'obj-page', 'template': 'vision'},
        {'id': 'obj-overview', 'kind': 'obj-page', 'template': 'overview'},
        {'id': 'obj-smart', 'kind': 'obj-page', 'template': 'smart'},
        {'id': 'obj-plan', 'kind': 'obj-page', 'template': 'plan'},
        {'id': 'obj-action', 'kind': 'obj-page', 'template': 'action'},
        {'id': 'obj-milestones', 'kind': 'obj-page', 'template': 'milestones'},
        {'id': 'obj-progress', 'kind': 'obj-page', 'template': 'progress'},
        {'id': 'obj-obstacles', 'kind': 'obj-page', 'template': 'obstacles'},
        {'id': 'obj-checkin', 'kind': 'obj-page', 'template': 'checkin'},
        {'id': 'obj-victories', 'kind': 'obj-page', 'template': 'victories'},
        {'id': 'obj-review', 'kind': 'obj-page', 'template': 'review'},
    ]

def draw_resource_page(a, p):
    """Draw improved resource pages with real structure."""
    title = p['title']
    year = p['year']
    resource = p['resource']

    a.box(0, 0, W, H, '#ECE8EF', r=0)
    a.box(25, 65, 435, 867, '#F8F5F0', r=13)
    a.text(title, 60, 130, 18, 'Bold')
    a.text(f'{year}', 60, 155, 12)

    if resource == 'goals':
        a.text('OBJETIVO', 60, 280, 9, 'Bold')
        a.lines(60, 270, 380, 3, 45)
    elif resource == 'dates':
        a.text('FECHA', 60, 295, 9, 'Bold')
        a.text('EVENTO', 150, 295, 9, 'Bold')
        a.text('CATEGORÍA', 280, 295, 9, 'Bold')
        a.lines(60, 265, 380, 6, 35)
    elif resource == 'birthdays':
        a.text('NOMBRE', 60, 295, 9, 'Bold')
        a.text('FECHA', 200, 295, 9, 'Bold')
        a.text('REGALO', 300, 295, 9, 'Bold')
        a.lines(60, 265, 380, 6, 35)
    elif resource == 'projects':
        a.text('PROYECTO', 60, 295, 9, 'Bold')
        a.text('PRÓXIMO PASO', 240, 295, 9, 'Bold')
        a.text('FECHA', 380, 295, 9, 'Bold')
        a.lines(60, 265, 380, 5, 40)
    elif resource == 'finance':
        a.text('META', 60, 295, 9, 'Bold')
        a.text('OBJETIVO', 160, 295, 9, 'Bold')
        a.text('ACTUAL', 280, 295, 9, 'Bold')
        a.text('%', 360, 295, 9, 'Bold')
        a.lines(60, 265, 380, 5, 40)
    elif resource == 'personal':
        a.text('QUIERO', 60, 295, 9, 'Bold')
        a.text('POR QUÉ', 220, 295, 9, 'Bold')
        a.text('PRIMER PASO', 340, 295, 9, 'Bold')
        a.lines(60, 265, 380, 5, 40)
    elif resource == 'wellness':
        a.text('ÁREA', 60, 295, 9, 'Bold')
        a.text('MEJORAR', 160, 295, 9, 'Bold')
        a.text('ACCIÓN', 280, 295, 9, 'Bold')
        a.text('FRECUENCIA', 370, 295, 9, 'Bold')
        a.lines(60, 265, 380, 4, 45)
    elif resource == 'professional':
        a.text('OBJETIVO', 60, 295, 9, 'Bold')
        a.text('HABILIDAD', 200, 295, 9, 'Bold')
        a.text('FECHA', 330, 295, 9, 'Bold')
        a.lines(60, 265, 380, 5, 40)
    elif resource == 'vision':
        for i, label in enumerate(['VIVIR', 'CREAR', 'APRENDER', 'SENTIR', 'CONSEGUIR']):
            a.text(label, 60, 260 - i * 50, 10, 'Bold')
            a.lines(60, 240 - i * 50, 380, 1, 40)
    elif resource == 'review':
        for i, label in enumerate(['LOGRÉ', 'APRENDÍ', 'CAMBIÓ', 'MOMENTOS', 'ORGULLOSA', 'SUELTO', 'LLEVO', 'PALABRA']):
            a.text(label, 60, 280 - i * 40, 10, 'Bold')
            a.lines(60, 250 - i * 40, 380, 1, 35)

def draw_objectives_page(a, p):
    """Draw objectives collection pages."""
    a.box(0, 0, W, H, '#ECE8EF', r=0)
    a.box(25, 65, 435, 867, '#F8F5F0', r=13)

    if p['kind'] == 'obj-divisor':
        a.text('OBJETIVOS', 250, 400, 38, 'Editorial', center=True)
        a.text('Lo que quiero construir', 250, 450, 16, 'Editorial', center=True)
    else:
        template = p.get('template')
        titles = {
            'vision': ('Mi visión', 'UNA IDEA CON DIRECCIÓN'),
            'overview': ('Mis objetivos', 'RESUMEN POR ÁREA'),
            'smart': ('Objetivo SMART', 'ESPECÍFICA, MEDIBLE, ALCANZABLE'),
            'plan': ('De meta a plan', 'ESTRUCTURA CLARA'),
            'action': ('Plan de acción', 'PASOS CONCRETOS'),
            'milestones': ('Hitos', 'PUNTOS DE REFERENCIA'),
            'progress': ('Seguimiento', 'MONITOREO CONTINUO'),
            'obstacles': ('Obstáculos', 'ANTICIPAR Y RESOLVER'),
            'checkin': ('Check-in', 'REVISIÓN PERIÓDICA'),
            'victories': ('Pequeñas victorias', 'CELEBRAR AVANCES'),
            'review': ('Revisión', 'REFLEXIÓN FINAL'),
        }
        if template in titles:
            title, subtitle = titles[template]
            a.text(title, 60, 130, 18, 'Bold')
            a.text(subtitle, 60, 155, 12)
            a.lines(60, 250, 380, 8, 40)

def build_phase3():
    """Build complete MASTER with improved resources + Objectives."""
    register_fonts()

    dated_pages, dated_known = dated_core_block()
    improved_res = improved_resources()
    objectives = objectives_collection()

    all_pages = improved_res + objectives + dated_pages
    known = {p['id'] for p in all_pages}
    nav = []
    future = []
    arts = []

    for i, p in enumerate(all_pages):
        p['previous'] = all_pages[i - 1]['id'] if i > 0 else 'menu'
        p['next'] = all_pages[i + 1]['id'] if i + 1 < len(all_pages) else 'menu'

    out = OUTPUT / '.build'
    out.mkdir(parents=True, exist_ok=True)
    pdf = out / 'YOYIR-DIGITAL-PLANNER-MASTER.pdf'

    c = canvas.Canvas(str(pdf), pagesize=(W, H), pageCompression=1, pdfVersion=(1, 4), invariant=1)
    c.setTitle("YOYI'R · Digital Planner 2026–2028")
    c.setAuthor("E-books para la vida — YOYI'R")

    for i, p in enumerate(all_pages):
        c.bookmarkPage(p['id'], fit='Fit')
        a = BlockArt(c, p['id'], nav, known)

        if p['kind'] == 'resource':
            draw_resource_page(a, p)
        elif p['kind'] in ('obj-divisor', 'obj-page'):
            draw_objectives_page(a, p)
        else:
            digital_planner_shell(a, p, i, len(all_pages))
            draw_block_page(a, p)

        future += a.future
        arts.append(a)
        c.showPage()

    c.save()
    return pdf, all_pages, nav, future, arts

if __name__ == '__main__':
    candidate, pages, nav, future, arts = build_phase3()

    print(f'\n[BUILD] PHASE 3 MASTER')
    print(f'  Total pages: {len(pages)}')

    try:
        doc = fitz.open(str(candidate))
        daily = sum(1 for p in pages if p['kind'] == 'day')
        resources = sum(1 for p in pages if p['kind'] == 'resource')
        objectives = sum(1 for p in pages if p['kind'] in ('obj-divisor', 'obj-page'))

        print(f'  Days: {daily}')
        print(f'  Resources: {resources}')
        print(f'  Objectives: {objectives}')
        print(f'  PDF: {candidate.name}')

        master = OUTPUT / 'YOYIR-DIGITAL-PLANNER-MASTER.pdf'
        if master.exists():
            backup = OUTPUT / '.build' / 'MASTER-PREVIOUS.pdf'
            if backup.exists():
                backup.unlink()
            master.rename(backup)
        candidate.replace(master)
        print(f'  [OK] MASTER promoted')

        doc.close()
    except Exception as e:
        print(f'  [ERROR] {e}')
