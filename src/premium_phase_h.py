"""
FASE H — CORE

Portada, Dashboard, Menú e Índices.
"""

from reportlab.pdfgen import canvas

from .config import ROOT, OUTPUT, DOCS, WIDTH, HEIGHT
from .components import Drawing, register_fonts
from .navigation import Navigation
from .themes import THEMES
from .premium.adapter_v2 import PremiumAdapterV2

def build_core():
    """Generar core del planificador."""

    print("\n" + "="*70)
    print("FASE H — CORE")
    print("="*70)

    register_fonts()
    pages = [
        {'id': 'portada', 'title': 'PORTADA', 'type': 'portada'},
        {'id': 'dashboard', 'title': 'DASHBOARD', 'type': 'dashboard'},
        {'id': 'menu-principal', 'title': 'MENÚ', 'type': 'menu'},
        {'id': 'indice-anios', 'title': 'ÍNDICE AÑOS', 'type': 'indice_anios'},
        {'id': 'indice-meses', 'title': 'ÍNDICE MESES', 'type': 'indice_meses'},
        {'id': 'indice-colecciones', 'title': 'ÍNDICE COLECCIONES', 'type': 'indice_col'},
    ]

    nav = Navigation(pages)
    output_dir = OUTPUT / 'premium-build-tests'
    output_dir.mkdir(parents=True, exist_ok=True)
    pdf_path = output_dir / 'YOYIR-Premium-CORE.pdf'

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
    """Renderizar PDF de core."""
    c = canvas.Canvas(str(path), pagesize=(WIDTH, HEIGHT),
                     pageCompression=1, pdfVersion=(1,4), invariant=1)

    c.setTitle("YOYI'R | Premium Core")

    for i, p in enumerate(pages):
        c.bookmarkPage(p['id'], fit='Fit')
        d = Drawing(c, THEMES['neutral'], nav, p['id'])
        adapter = PremiumAdapterV2(d)

        adapter.shell_background()
        adapter.shell_binding()
        adapter.page_number(i+1, len(pages))

        ptype = p.get('type')

        if ptype == 'portada':
            d.text('YOYI\'R', 60, 300, 48, 'Editorial')
            d.text('PLANIFICADOR DIGITAL PREMIUM', 60, 250, 24, 'Bold')
            d.text('2026-2028', 60, 200, 18)
            nav.link_small(c, p['id'], 'dashboard', 'Inicio',
                         (60, 100, 300, 60))

        elif ptype == 'dashboard':
            adapter.premium_title('DASHBOARD', 'Inicio', 'blush')
            y = 250
            items = [
                ('Años', 'indice-anios'),
                ('Meses', 'indice-meses'),
                ('Colecciones', 'indice-colecciones'),
                ('Menú', 'menu-principal'),
            ]
            for label, page_id in items:
                nav.link_small(c, p['id'], page_id, label,
                             (60, y-30, 250, 40))
                y -= 70

        elif ptype == 'menu':
            adapter.premium_title('MENÚ', 'Principal', 'salvia')
            d.text('Acceso rápido:', 60, 250, 14, 'Bold')
            y = 210
            menu_items = [
                ('Años', 'indice-anios'),
                ('Meses', 'indice-meses'),
                ('Colecciones', 'indice-colecciones'),
                ('Dashboard', 'dashboard'),
            ]
            for label, page_id in menu_items:
                d.text(f'• {label}', 60, y, 12)
                nav.link_small(c, p['id'], page_id, label,
                             (60, y-30, 250, 30))
                y -= 50

        elif ptype == 'indice_anios':
            adapter.premium_title('ÍNDICE', 'Años', 'melocoton')
            years = ['2026', '2027', '2028']
            y = 250
            for year in years:
                d.text(f'{year}', 60, y, 14, 'Bold')
                d.text('Disponible en PDF separado', 90, y, 11)
                y -= 60

        elif ptype == 'indice_meses':
            adapter.premium_title('ÍNDICE', 'Meses', 'coral')
            months_es = ['Enero', 'Febrero', 'Marzo', 'Abril',
                        'Mayo', 'Junio', 'Julio', 'Agosto',
                        'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
            y = 250
            for month_num, month_name in enumerate(months_es[:6], 1):
                d.text(f'{month_name} 2026', 60, y, 12)
                y -= 35
            y = 250
            for month_num, month_name in enumerate(months_es[6:], 7):
                d.text(f'{month_name} 2026', 400, y, 12)
                y -= 35

        elif ptype == 'indice_col':
            adapter.premium_title('ÍNDICE', 'Colecciones', 'azufrado')
            collections = ['Objetivos', 'Vida', 'Productividad', 'Bienestar',
                          'Autocuidado', 'Finanzas', 'Estudio', 'Organización',
                          'Notas', 'Extras']
            y = 250
            for col in collections[:5]:
                d.text(f'• {col}', 60, y, 12)
                y -= 35
            y = 250
            for col in collections[5:]:
                d.text(f'• {col}', 400, y, 12)
                y -= 35

        c.showPage()

    c.save()
    print(f"[OK] PDF: {path}")

if __name__ == '__main__':
    build_core()
