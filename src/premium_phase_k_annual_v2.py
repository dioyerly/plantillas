"""
FASE K — RECURSOS ANUALES (V2)
Versión simplificada con navegación correcta.
"""

from reportlab.pdfgen import canvas
from .config import ROOT, OUTPUT, DOCS, WIDTH, HEIGHT
from .components import Drawing, register_fonts
from .navigation import Navigation
from .themes import THEMES
from .premium.adapter_v2 import PremiumAdapterV2

def build_annual_resources():
    """Generar recursos anuales con navegación completa."""

    print("\n" + "="*70)
    print("FASE K — RECURSOS ANUALES (V2)")
    print("="*70)

    register_fonts()

    pages = []

    # Generar para cada año
    for year in [2026, 2027, 2028]:
        for section in ['divisor', 'overview', 'goals', 'dates', 'planning']:
            pages.append({
                'id': f'annual-{year}-{section}',
                'title': f'{year} {section}',
                'type': section,
                'year': year,
            })

    nav = Navigation(pages)
    output_dir = OUTPUT / 'premium-build-tests'
    output_dir.mkdir(parents=True, exist_ok=True)
    pdf_path = output_dir / 'YOYIR-Premium-ANNUAL-RESOURCES.pdf'

    c = canvas.Canvas(str(pdf_path), pagesize=(WIDTH, HEIGHT),
                     pageCompression=1, pdfVersion=(1,4), invariant=1)
    c.setTitle("YOYI'R | Recursos Anuales")

    colors = {2026: 'lavanda', 2027: 'blush', 2028: 'salvia'}

    for i, p in enumerate(pages):
        year = p['year']
        section = p['type']
        color = colors.get(year, 'neutral')

        c.bookmarkPage(p['id'], fit='Fit')
        d = Drawing(c, THEMES['neutral'], nav, p['id'])
        adapter = PremiumAdapterV2(d)

        adapter.shell_background()
        adapter.shell_binding()
        adapter.page_number(i+1, len(pages))

        # Título
        if section == 'divisor':
            adapter.month_divider(str(year), 'RECURSO ANUAL', color)
        elif section == 'overview':
            adapter.premium_title('AÑO VISTAZO', str(year), color)
        elif section == 'goals':
            adapter.premium_title('OBJETIVOS', str(year), color)
        elif section == 'dates':
            adapter.premium_title('FECHAS', str(year), color)
        elif section == 'planning':
            adapter.premium_title('PLAN ANUAL', str(year), color)

        # Contenido simple
        d.text('Contenido de planificacion', 60, 300, 12)

        # Navegación
        year_pages = [p2 for p2 in pages if p2['year'] == year]
        page_index = year_pages.index(p) if p in year_pages else 0

        if page_index > 0:
            prev_page = year_pages[page_index - 1]
            d.button('ANTERIOR', prev_page['id'], 60, 850, 120, 70)

        if page_index < len(year_pages) - 1:
            next_page = year_pages[page_index + 1]
            d.button('SIGUIENTE', next_page['id'], 340, 850, 120, 70)

        c.showPage()

    c.save()
    print(f"[OK] PDF de recursos anuales generado")

    # Validar
    try:
        nav.check()
        status = 'pass'
    except:
        status = 'fail'

    print(f"\n[VALIDACION]")
    print(f"  Paginas: {len(pages)}")
    print(f"  Resultado: {status.upper()}")

    return {'status': status, 'pages': len(pages)}

if __name__ == '__main__':
    build_annual_resources()
