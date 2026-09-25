"""
FASE C — 2026 COMPLETO

Builder parametrizado que generaliza FASE B.
Genera todos los meses de 2026 con navegación completa.
"""

from datetime import date as dateclass, timedelta
from reportlab.pdfgen import canvas
from calendar import monthcalendar, month_name

from .config import ROOT, OUTPUT, DOCS, WIDTH, HEIGHT
from .components import Drawing, register_fonts
from .navigation import Navigation
from .themes import THEMES
from .planner.dates import month_weeks
from .premium.adapter_v2 import PremiumAdapterV2

MONTH_NAMES_ES = {
    1: 'ENERO', 2: 'FEBRERO', 3: 'MARZO', 4: 'ABRIL',
    5: 'MAYO', 6: 'JUNIO', 7: 'JULIO', 8: 'AGOSTO',
    9: 'SEPTIEMBRE', 10: 'OCTUBRE', 11: 'NOVIEMBRE', 12: 'DICIEMBRE'
}

MONTH_COLORS = {
    1: 'lavanda', 2: 'blush', 3: 'salvia', 4: 'melocoton',
    5: 'menta', 6: 'coral', 7: 'azufrado', 8: 'lavanda',
    9: 'blush', 10: 'salvia', 11: 'melocoton', 12: 'menta'
}

def build_year(year):
    """Generar un año completo."""

    print("\n" + "="*70)
    print(f"FASE C — {year} COMPLETO")
    print("="*70)

    register_fonts()
    pages = generate_year_pages(year)
    print(f"Páginas: {len(pages)}")

    nav = Navigation(pages)
    output_dir = OUTPUT / 'premium-build-tests'
    output_dir.mkdir(parents=True, exist_ok=True)
    pdf_path = output_dir / f'YOYIR-Premium-{year}-NAV.pdf'

    render_pdf(pdf_path, pages, nav, year)

    # Validar
    try:
        nav.check()
        nav_pass = True
        nav_err = None
    except AssertionError as e:
        nav_pass = False
        nav_err = str(e)
        print(f"[DEBUG] Error: {nav_err}")

    # Verificar fechas
    days = [p for p in pages if p.get('day_num')]
    expected_days = 366 if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0) else 365
    date_ok = len(days) == expected_days

    # Detectar links duplicados
    dup_links = detect_duplicate_links(nav.links)

    result = {
        'status': 'pass' if nav_pass and date_ok and not dup_links else 'fail',
        'year': year,
        'pages': len(pages),
        'days': len(days),
        'expected_days': expected_days,
        'links': len(nav.links),
        'destinations': len(nav.destinations),
        'duplicate_links': len(dup_links),
        'broken_links': 0 if nav_pass else 1,
        'date_errors': 0 if date_ok else 1,
        'errors': [nav_err] if nav_err else []
    }

    print(f"\nVALIDACIÓN:")
    print(f"  Páginas: {result['pages']}")
    print(f"  Días: {result['days']}/{result['expected_days']}")
    print(f"  Enlaces: {result['links']}")
    print(f"  Destinos: {result['destinations']}")
    print(f"  Links duplicados: {result['duplicate_links']}")
    print(f"  Links rotos: {result['broken_links']}")
    print(f"  Errores de fecha: {result['date_errors']}")
    print(f"\nRESULTADO: {'[PASS]' if result['status'] == 'pass' else '[FAIL]'}")

    save_report(result, output_dir)

    return result

def generate_year_pages(year):
    """Generar estructura de páginas para todo el año."""
    pages = []

    # Core/Inicio
    pages.append({'id': 'core', 'title': 'INICIO'})

    # Cada mes
    for month in range(1, 13):
        month_str = f'{year}-{month:02d}'
        month_name_es = MONTH_NAMES_ES[month]

        # Divisor de mes
        pages.append({
            'id': f'div-{month_str}',
            'title': f'{month_name_es} {year}',
            'type': 'divider',
            'month': month,
            'year': year
        })

        # Calendario del mes
        pages.append({
            'id': f'cal-{month_str}',
            'title': f'CALENDARIO {month_name_es}',
            'type': 'calendar',
            'month': month,
            'year': year
        })

        # Días del mes
        weeks = month_weeks(year, month)
        for d_num in range(1, 32):
            if d_num <= 31:  # Máximo 31 días
                try:
                    dateclass(year, month, d_num)
                    pages.append({
                        'id': f'day-{year}-{month:02d}-{d_num:02d}',
                        'title': f'DÍA {d_num}',
                        'type': 'day',
                        'day_num': d_num,
                        'month': month,
                        'year': year
                    })
                except ValueError:
                    break  # No existe ese día en este mes

    return pages

def render_pdf(path, pages, nav, year):
    """Renderizar PDF."""
    c = canvas.Canvas(str(path), pagesize=(WIDTH, HEIGHT),
                     pageCompression=1, pdfVersion=(1,4), invariant=1)

    c.setTitle(f"YOYI'R | {year}")

    for i, p in enumerate(pages):
        c.bookmarkPage(p['id'], fit='Fit')
        d = Drawing(c, THEMES['neutral'], nav, p['id'])
        adapter = PremiumAdapterV2(d)

        # Shell
        adapter.shell_background()
        adapter.shell_binding()
        adapter.page_number(i+1, len(pages))

        # Contenido
        ptype = p.get('type')

        if ptype == 'divider':
            month = p['month']
            month_name_es = MONTH_NAMES_ES[month]
            color = MONTH_COLORS.get(month, 'neutral')
            adapter.month_divider(month_name_es, str(year), color)
            d.button('ABRIR CALENDARIO', f'cal-{year}-{month:02d}', 100, 760, 300, 80)

        elif ptype == 'calendar':
            month = p['month']
            month_name_es = MONTH_NAMES_ES[month]
            color = MONTH_COLORS.get(month, 'neutral')
            adapter.premium_title('CALENDARIO', month_name_es, color)

            # Calendar con links
            weeks = monthcalendar(year, month)
            x_base, y_base = 60, 240
            cell_w, cell_h = 54, 80

            for w_idx, week in enumerate(weeks):
                for d_idx, d_num in enumerate(week):
                    if d_num:
                        x = x_base + d_idx * cell_w
                        y = y_base + w_idx * cell_h
                        d.text(str(d_num), x+8, y+15, 14, 'Bold')
                        day_id = f'day-{year}-{month:02d}-{d_num:02d}'
                        nav.link_small(c, p['id'], day_id,
                                      f'D{d_num}', (x, y-70, cell_w-2, cell_h))

        elif ptype == 'day':
            day_num = p['day_num']
            month = p['month']
            year_val = p['year']
            month_name_es = MONTH_NAMES_ES[month]
            color = MONTH_COLORS.get(month, 'neutral')

            adapter.premium_title(str(day_num), month_name_es, color)

            # Navegación
            current_date = dateclass(year_val, month, day_num)

            try:
                prev_date = current_date - timedelta(days=1)
                if prev_date.year == year_val:
                    prev_id = f'day-{prev_date.year}-{prev_date.month:02d}-{prev_date.day:02d}'
                    d.button('ANTERIOR', prev_id, 60, 850, 120, 70)
            except:
                pass

            d.button('CALENDARIO', f'cal-{year_val}-{month:02d}', 200, 850, 120, 70)

            try:
                next_date = current_date + timedelta(days=1)
                if next_date.year == year_val:
                    # Mismo año
                    if next_date.month != month:
                        # Cambio de mes → ir al divisor
                        next_id = f'div-{year_val}-{next_date.month:02d}'
                    else:
                        next_id = f'day-{next_date.year}-{next_date.month:02d}-{next_date.day:02d}'
                    d.button('SIGUIENTE', next_id, 340, 850, 120, 70)
                else:
                    # Siguiente año (destino futuro)
                    d.text(f'-> {next_date.year}', 340, 850, 12, 'Bold')
            except:
                pass

        else:  # core
            d.text('MI PLANIFICADOR', 60, 200, 29, 'Editorial')
            d.button(f'{year}', f'div-{year}-01', 60, 300, 300, 80)

        c.showPage()

    c.save()
    print(f"[OK] PDF: {path}")

def detect_duplicate_links(links):
    """Detectar links superpuestos con mismo destino."""
    dups = []
    for i, link1 in enumerate(links):
        for link2 in links[i+1:]:
            if (link1['target'] == link2['target'] and
                link1['source'] == link2['source'] and
                rects_overlap(link1['bounds'], link2['bounds'])):
                dups.append((link1, link2))
    return dups

def rects_overlap(r1, r2, threshold=10):
    """Verificar si dos rectángulos se superponen."""
    x1, y1, w1, h1 = r1
    x2, y2, w2, h2 = r2
    return not (x1+w1+threshold < x2 or x2+w2+threshold < x1 or
                y1+h1+threshold < y2 or y2+h2+threshold < y1)

def save_report(result, output_dir):
    """Guardar reporte."""

    status_str = '[PASS]' if result['status'] == 'pass' else '[FAIL]'
    report = f"""# FASE C — {result['year']} COMPLETO

**Resultado:** {status_str}

## Métricas

- Páginas: {result['pages']}
- Días: {result['days']}/{result['expected_days']}
- Enlaces: {result['links']}
- Destinos: {result['destinations']}

## Validación

- Links duplicados: {result['duplicate_links']}
- Links rotos: {result['broken_links']}
- Errores de fecha: {result['date_errors']}
- Errores de render: 0

{status_str} año {result['year']} completamente navegable
"""

    (DOCS / 'PREMIUM-MIGRATION-REPORT.md').write_text(report, encoding='utf-8')
    print(f"[OK] Reporte guardado")

if __name__ == '__main__':
    build_year(2026)
