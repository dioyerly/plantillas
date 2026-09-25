"""
FASE G — COLECCIONES

Genera 10 colecciones premium:
OBJETIVOS, VIDA, PRODUCTIVIDAD, BIENESTAR, AUTOCUIDADO, FINANZAS,
ESTUDIO, ORGANIZACIÓN, NOTAS, EXTRAS
"""

from reportlab.pdfgen import canvas

from .config import ROOT, OUTPUT, DOCS, WIDTH, HEIGHT
from .components import Drawing, register_fonts
from .navigation import Navigation
from .themes import THEMES
from .premium.adapter_v2 import PremiumAdapterV2

COLLECTIONS = [
    ('OBJETIVOS', 'objetivos', 'lavanda'),
    ('VIDA', 'vida', 'blush'),
    ('PRODUCTIVIDAD', 'productividad', 'salvia'),
    ('BIENESTAR', 'bienestar', 'melocoton'),
    ('AUTOCUIDADO', 'autocuidado', 'menta'),
    ('FINANZAS', 'finanzas', 'coral'),
    ('ESTUDIO', 'estudio', 'azufrado'),
    ('ORGANIZACIÓN', 'organizacion', 'lavanda'),
    ('NOTAS', 'notas-col', 'blush'),
    ('EXTRAS', 'extras', 'salvia'),
]

def build_collections():
    """Generar colecciones."""

    print("\n" + "="*70)
    print("FASE G — COLECCIONES")
    print("="*70)

    register_fonts()
    pages = [{'id': 'core-col', 'title': 'COLECCIONES'}]

    # Crear 6 páginas por colección (contenido variado)
    for col_name, col_id, col_color in COLLECTIONS:
        pages.append({
            'id': f'col-{col_id}-index',
            'title': col_name,
            'type': 'col_index',
            'collection': col_name,
            'collection_id': col_id,
            'color': col_color
        })
        for pnum in range(1, 7):
            pages.append({
                'id': f'col-{col_id}-{pnum}',
                'title': f'{col_name} {pnum}',
                'type': 'col_page',
                'collection': col_name,
                'collection_id': col_id,
                'color': col_color,
                'page_num': pnum
            })

    nav = Navigation(pages)
    output_dir = OUTPUT / 'premium-build-tests'
    output_dir.mkdir(parents=True, exist_ok=True)
    pdf_path = output_dir / 'YOYIR-Premium-Colecciones.pdf'

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
        'collections': len(COLLECTIONS),
        'links': len(nav.links),
        'broken_links': 0 if nav_pass else 1
    }

    print(f"\nVALIDACIÓN:")
    print(f"  Páginas: {result['pages']}")
    print(f"  Colecciones: {result['collections']}")
    print(f"  Enlaces: {result['links']}")
    print(f"  Links rotos: {result['broken_links']}")
    print(f"\nRESULTADO: {'[PASS]' if result['status'] == 'pass' else '[FAIL]'}")

    return result

def render_pdf(path, pages, nav):
    """Renderizar PDF de colecciones."""
    c = canvas.Canvas(str(path), pagesize=(WIDTH, HEIGHT),
                     pageCompression=1, pdfVersion=(1,4), invariant=1)

    c.setTitle("YOYI'R | Colecciones")

    for i, p in enumerate(pages):
        c.bookmarkPage(p['id'], fit='Fit')
        d = Drawing(c, THEMES['neutral'], nav, p['id'])
        adapter = PremiumAdapterV2(d)

        adapter.shell_background()
        adapter.shell_binding()
        adapter.page_number(i+1, len(pages))

        ptype = p.get('type')

        if ptype == 'col_index':
            col_name = p['collection']
            col_id = p['collection_id']
            col_color = p['color']

            adapter.premium_title(col_name, 'COLECCIÓN', col_color)

            # Índice de subpáginas
            y = 250
            for pnum in range(1, 7):
                page_id = f'col-{col_id}-{pnum}'
                d.text(f'Página {pnum}', 60, y, 12)
                nav.link_small(c, p['id'], page_id, f'P{pnum}', (60, y-30, 250, 40))
                y -= 60

        elif ptype == 'col_page':
            col_name = p['collection']
            col_color = p['color']
            page_num = p['page_num']

            adapter.premium_title(f'{col_name}', f'Página {page_num}', col_color)

            # Contenido: líneas para notas
            y = 250
            for line in range(12):
                d.line(60, y, WIDTH-60, y)
                y -= 35

        else:  # core
            d.text('COLECCIONES', 60, 200, 29, 'Editorial')

            # Índice de colecciones
            y = 350
            for col_name, col_id, col_color in COLLECTIONS:
                nav.link_small(c, p['id'], f'col-{col_id}-index',
                             col_name, (60, y-25, 250, 40))
                y -= 60

        c.showPage()

    c.save()
    print(f"[OK] PDF: {path}")

if __name__ == '__main__':
    build_collections()
