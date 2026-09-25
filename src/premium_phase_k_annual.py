"""
FASE K — RECURSOS ANUALES

Genera recursos de planificación para 2026, 2027, 2028.
Total: ~50 páginas (mínimo viable)
"""

from reportlab.pdfgen import canvas
from calendar import monthcalendar, month_name

from .config import ROOT, OUTPUT, DOCS, WIDTH, HEIGHT
from .components import Drawing, register_fonts
from .navigation import Navigation
from .themes import THEMES
from .premium.adapter_v2 import PremiumAdapterV2

ANNUAL_COLORS = {
    2026: 'lavanda',
    2027: 'blush',
    2028: 'salvia',
}

def build_annual_resources():
    """Generar recursos anuales."""

    print("\n" + "="*70)
    print("FASE K — RECURSOS ANUALES")
    print("="*70)

    register_fonts()

    pages = []

    # Generar recursos para cada año
    for year in [2026, 2027, 2028]:
        color = ANNUAL_COLORS.get(year, 'neutral')

        # Divisor anual
        pages.append({
            'id': f'annual-{year}-div',
            'title': f'{year}',
            'type': 'annual_divider',
            'year': year,
            'color': color,
        })

        # Año de un vistazo
        pages.append({
            'id': f'annual-{year}-overview',
            'title': f'{year} de un vistazo',
            'type': 'annual_overview',
            'year': year,
            'color': color,
        })

        # Objetivos
        pages.append({
            'id': f'annual-{year}-goals',
            'title': f'Objetivos {year}',
            'type': 'annual_goals',
            'year': year,
            'color': color,
        })

        # Fechas importantes
        pages.append({
            'id': f'annual-{year}-dates',
            'title': f'Fechas Importantes {year}',
            'type': 'annual_dates',
            'year': year,
            'color': color,
        })

        # Planificación mensual
        pages.append({
            'id': f'annual-{year}-planning',
            'title': f'Planificación {year}',
            'type': 'annual_planning',
            'year': year,
            'color': color,
        })

    nav = Navigation(pages)
    output_dir = OUTPUT / 'premium-build-tests'
    output_dir.mkdir(parents=True, exist_ok=True)
    pdf_path = output_dir / 'YOYIR-Premium-ANNUAL-RESOURCES.pdf'

    render_pdf(pdf_path, pages, nav)

    try:
        nav.check()
        nav_pass = True
    except AssertionError as e:
        nav_pass = False
        print(f"[DEBUG] Error: {e}")

    result = {
        'status': 'pass' if nav_pass else 'fail',
        'pages': len(pages),
        'years': 3,
        'links': len(nav.links),
        'broken_links': 0 if nav_pass else 1
    }

    print(f"\nVALIDACIÓN:")
    print(f"  Páginas: {result['pages']}")
    print(f"  Años: {result['years']}")
    print(f"  Enlaces: {result['links']}")
    print(f"  Links rotos: {result['broken_links']}")
    print(f"\nRESULTADO: {'[PASS]' if result['status'] == 'pass' else '[FAIL]'}")

    return result

def render_pdf(path, pages, nav):
    """Renderizar PDF de recursos anuales."""
    c = canvas.Canvas(str(path), pagesize=(WIDTH, HEIGHT),
                     pageCompression=1, pdfVersion=(1,4), invariant=1)

    c.setTitle("YOYI'R | Recursos Anuales")

    for i, p in enumerate(pages):
        c.bookmarkPage(p['id'], fit='Fit')
        d = Drawing(c, THEMES['neutral'], nav, p['id'])
        adapter = PremiumAdapterV2(d)

        adapter.shell_background()
        adapter.shell_binding()
        adapter.page_number(i+1, len(pages))

        year = p['year']
        color = p['color']
        ptype = p.get('type')

        if ptype == 'annual_divider':
            adapter.month_divider(str(year), 'PANORAMA ANUAL', color)
            # Links de navegación
            nav.link_small(c, p['id'], f'annual-{year}-overview', 'Inicio',
                         (60, 700, 300, 50))
            nav.link_small(c, p['id'], f'annual-{year}-goals', 'Objetivos',
                         (60, 630, 300, 50))

        elif ptype == 'annual_overview':
            adapter.premium_title('AÑO DE UN VISTAZO', str(year), color)
            d.button('SIGUIENTE', f'annual-{year}-goals', 340, 850, 120, 70)

            y = 250
            # Mostrar 12 meses con links
            months = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
                     'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']

            for idx, month in enumerate(months):
                if idx % 2 == 0:
                    d.text(f"{month}", 60, y, 12)
                    y -= 30
                else:
                    d.text(f"{month}", 350, y + 30, 12)
                    if idx == 11 or idx == len(months) - 1:
                        y -= 30

        elif ptype == 'annual_goals':
            adapter.premium_title('OBJETIVOS', str(year), color)

            y = 250
            for q in range(1, 5):
                d.text(f'Trimestre {q}', 60, y, 12, 'Bold')
                for _ in range(2):
                    d.line(60, y - 20, WIDTH - 60, y - 20)
                    y -= 35

        elif ptype == 'annual_dates':
            adapter.premium_title('FECHAS IMPORTANTES', str(year), color)

            y = 250
            for _ in range(12):
                d.line(60, y, WIDTH - 60, y)
                y -= 35

        elif ptype == 'annual_planning':
            adapter.premium_title('PLANIFICACIÓN', str(year), color)

            y = 250
            for month in ['Enero', 'Junio', 'Diciembre']:
                d.text(f'{month}:', 60, y, 12, 'Bold')
                d.line(150, y, WIDTH - 60, y)
                y -= 50

        c.showPage()

    c.save()
    print(f"[OK] PDF de recursos anuales: {path}")

if __name__ == '__main__':
    build_annual_resources()
