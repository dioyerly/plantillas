"""
FASE F — SIN FECHA

Plantillas reutilizables no ligadas a fechas específicas.
Secciones: Notas, Reflexiones, Trackers, Espacios en blanco.
"""

from reportlab.pdfgen import canvas

from .config import ROOT, OUTPUT, DOCS, WIDTH, HEIGHT
from .components import Drawing, register_fonts
from .navigation import Navigation
from .themes import THEMES
from .premium.adapter_v2 import PremiumAdapterV2

def build_templates():
    """Generar plantillas SIN FECHA."""

    print("\n" + "="*70)
    print("FASE F — PLANTILLAS SIN FECHA")
    print("="*70)

    register_fonts()
    pages = [
        {'id': 'core', 'title': 'INICIO'},
        {'id': 'tpl-notas', 'title': 'NOTAS', 'type': 'notas'},
        {'id': 'tpl-reflexiones', 'title': 'REFLEXIONES', 'type': 'reflexiones'},
        {'id': 'tpl-trackers', 'title': 'TRACKERS', 'type': 'trackers'},
        {'id': 'tpl-ideas', 'title': 'IDEAS', 'type': 'ideas'},
        {'id': 'tpl-gratitud', 'title': 'GRATITUD', 'type': 'gratitud'},
        {'id': 'tpl-objetivos-periodo', 'title': 'OBJETIVOS', 'type': 'objetivos'},
    ]

    nav = Navigation(pages)
    output_dir = OUTPUT / 'premium-build-tests'
    output_dir.mkdir(parents=True, exist_ok=True)
    pdf_path = output_dir / 'YOYIR-Premium-SIN-FECHA-Plantillas.pdf'

    render_pdf(pdf_path, pages, nav)

    try:
        nav.check()
        nav_pass = True
    except AssertionError:
        nav_pass = False

    result = {
        'status': 'pass' if nav_pass else 'fail',
        'pages': len(pages),
        'links': len(nav.links),
        'broken_links': 0 if nav_pass else 1
    }

    print(f"\nVALIDACIÓN:")
    print(f"  Páginas: {result['pages']}")
    print(f"  Enlaces: {result['links']}")
    print(f"  Links rotos: {result['broken_links']}")
    print(f"\nRESULTADO: {'[PASS]' if result['status'] == 'pass' else '[FAIL]'}")

    return result

def render_pdf(path, pages, nav):
    """Renderizar PDF de plantillas."""
    c = canvas.Canvas(str(path), pagesize=(WIDTH, HEIGHT),
                     pageCompression=1, pdfVersion=(1,4), invariant=1)

    c.setTitle("YOYI'R | Plantillas Sin Fecha")

    for i, p in enumerate(pages):
        c.bookmarkPage(p['id'], fit='Fit')
        d = Drawing(c, THEMES['neutral'], nav, p['id'])
        adapter = PremiumAdapterV2(d)

        adapter.shell_background()
        adapter.shell_binding()
        adapter.page_number(i+1, len(pages))

        ptype = p.get('type')

        if ptype == 'notas':
            adapter.premium_title('NOTAS', '', 'blush')
            y = 250
            for line_num in range(15):
                d.line(60, y, WIDTH-60, y)
                y -= 35

        elif ptype == 'reflexiones':
            adapter.premium_title('REFLEXIONES', '', 'salvia')
            d.text('Reflexiones personales y aprendizajes:', 60, 250, 14, 'Bold')
            y = 210
            for line_num in range(12):
                d.line(60, y, WIDTH-60, y)
                y -= 35

        elif ptype == 'trackers':
            adapter.premium_title('TRACKERS', '', 'coral')
            y = 250
            categories = ['Agua', 'Ejercicio', 'Lectura', 'Meditacion', 'Sueno']
            for cat in categories:
                d.text(cat + ':', 60, y, 12)
                for box in range(7):
                    x = 180 + box * 40
                    # Dibujar cuadrado con líneas
                    d.line(x, y-25, x+30, y-25)
                    d.line(x+30, y-25, x+30, y-55)
                    d.line(x+30, y-55, x, y-55)
                    d.line(x, y-55, x, y-25)
                y -= 60

        elif ptype == 'ideas':
            adapter.premium_title('IDEAS', '', 'melocoton')
            y = 250
            for line_num in range(14):
                d.line(60, y, WIDTH-60, y)
                y -= 37

        elif ptype == 'gratitud':
            adapter.premium_title('GRATITUD', '', 'menta')
            d.text('Hoy estoy agradecida por...', 60, 250, 14, 'Bold')
            y = 210
            for line_num in range(12):
                d.line(60, y, WIDTH-60, y)
                y -= 35

        elif ptype == 'objetivos':
            adapter.premium_title('OBJETIVOS', 'del periodo', 'azufrado')
            y = 250
            for obj_num in range(5):
                d.text(f'{obj_num+1}.', 60, y, 12, 'Bold')
                d.line(90, y-2, WIDTH-60, y-2)
                y -= 50

        else:  # core
            d.text('PLANTILLAS', 60, 200, 29, 'Editorial')
            d.button('NOTAS', 'tpl-notas', 60, 300, 300, 80)
            y = 450
            templates = [
                ('Notas', 'tpl-notas'),
                ('Reflexiones', 'tpl-reflexiones'),
                ('Trackers', 'tpl-trackers'),
                ('Ideas', 'tpl-ideas'),
                ('Gratitud', 'tpl-gratitud'),
                ('Objetivos', 'tpl-objetivos-periodo'),
            ]
            for label, page_id in templates:
                nav.link_small(c, p['id'], page_id, label, (60, y, 250, 40))
                y -= 50

        c.showPage()

    c.save()
    print(f"[OK] PDF: {path}")

if __name__ == '__main__':
    build_templates()
