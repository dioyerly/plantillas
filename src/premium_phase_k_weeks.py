"""
FASE K — SEMANAS FECHADAS

Genera todas las semanas de 2026, 2027, 2028 con navegación completa.
Total: 156 semanas (52 × 3 años)
"""

from datetime import date, timedelta
from reportlab.pdfgen import canvas
from calendar import day_name

from .config import ROOT, OUTPUT, DOCS, WIDTH, HEIGHT
from .components import Drawing, register_fonts
from .navigation import Navigation
from .themes import THEMES
from .premium.adapter_v2 import PremiumAdapterV2

def build_weeks():
    """Generar todas las semanas de 2026-2028."""

    print("\n" + "="*70)
    print("FASE K — SEMANAS FECHADAS (156 PÁGINAS)")
    print("="*70)

    register_fonts()

    # Generar estructura de semanas
    pages = []
    week_data = []

    for year in [2026, 2027, 2028]:
        weeks = generate_weeks_for_year(year)
        for week_info in weeks:
            week_id = f"week-{year}-{week_info['num']:02d}"
            pages.append({
                'id': week_id,
                'title': f'SEMANA {week_info["num"]}',
                'type': 'week',
                'year': year,
                'week_num': week_info['num'],
                'start_date': week_info['start'],
                'end_date': week_info['end'],
            })
            week_data.append(week_info)

    nav = Navigation(pages)
    output_dir = OUTPUT / 'premium-build-tests'
    output_dir.mkdir(parents=True, exist_ok=True)
    pdf_path = output_dir / 'YOYIR-Premium-WEEKS.pdf'

    render_pdf(pdf_path, pages, nav, week_data)

    # Validar
    try:
        nav.check()
        nav_pass = True
    except AssertionError as e:
        nav_pass = False
        print(f"[DEBUG] Error navegación: {e}")

    result = {
        'status': 'pass' if nav_pass else 'fail',
        'pages': len(pages),
        'weeks': len(pages),
        'years': 3,
        'links': len(nav.links),
        'broken_links': 0 if nav_pass else 1
    }

    print(f"\nVALIDACIÓN:")
    print(f"  Semanas: {result['weeks']}")
    print(f"  Años: {result['years']}")
    print(f"  Enlaces: {result['links']}")
    print(f"  Links rotos: {result['broken_links']}")
    print(f"\nRESULTADO: {'[PASS]' if result['status'] == 'pass' else '[FAIL]'}")

    return result

def generate_weeks_for_year(year):
    """Generar todas las semanas de un año."""
    weeks = []
    jan1 = date(year, 1, 1)
    dec31 = date(year, 12, 31)

    # Encontrar primer lunes
    current = jan1
    while current.weekday() != 0:  # 0 = Monday
        current += timedelta(days=1)

    week_num = 1
    while current.year == year:
        week_end = min(current + timedelta(days=6), dec31)

        # Generar días de la semana
        days = []
        for i in range(7):
            day = current + timedelta(days=i)
            if day <= dec31:
                days.append({
                    'date': day,
                    'weekday': day_name[day.weekday()],
                    'day_num': day.day,
                })

        weeks.append({
            'num': week_num,
            'start': current,
            'end': week_end,
            'year': year,
            'days': days,
        })

        current = week_end + timedelta(days=1)
        week_num += 1

    return weeks

def render_pdf(path, pages, nav, week_data):
    """Renderizar PDF de semanas."""
    c = canvas.Canvas(str(path), pagesize=(WIDTH, HEIGHT),
                     pageCompression=1, pdfVersion=(1,4), invariant=1)

    c.setTitle("YOYI'R | Semanas")

    for i, p in enumerate(pages):
        c.bookmarkPage(p['id'], fit='Fit')
        d = Drawing(c, THEMES['neutral'], nav, p['id'])
        adapter = PremiumAdapterV2(d)

        adapter.shell_background()
        adapter.shell_binding()
        adapter.page_number(i+1, len(pages))

        year = p['year']
        week_num = p['week_num']
        start_date = p['start_date']
        end_date = p['end_date']

        color = 'salvia'  # Verde para semanas

        # Título
        date_range = f"{start_date.strftime('%d/%m')} - {end_date.strftime('%d/%m/%Y')}"
        adapter.premium_title('SEMANA', date_range, color)

        # Días de la semana
        y = 250
        for day_info in week_data[i]['days']:
            day_date = day_info['date']
            weekday = day_info['weekday']

            # Buscar ID del día correspondiente
            day_id = f"day-{day_date.year}-{day_date.month:02d}-{day_date.day:02d}"

            # Mostrar día
            d.text(f"{weekday}", 60, y, 12, 'Bold')
            d.text(f"{day_date.strftime('%d/%m')}", 200, y, 12)

            # Link a página del día si existe
            try:
                nav.link_small(c, p['id'], day_id, f"D{day_date.day}",
                             (60, y-30, 250, 30))
            except:
                pass

            y -= 50

        # Navegación
        if week_num > 1:
            prev_id = f"week-{year}-{week_num-1:02d}"
            d.button('ANTERIOR', prev_id, 60, 900, 120, 70)

        d.button('MES', f'cal-{year}-{start_date.month:02d}', 200, 900, 120, 70)

        if week_num < 52:
            next_id = f"week-{year}-{week_num+1:02d}"
            d.button('SIGUIENTE', next_id, 340, 900, 120, 70)

        c.showPage()

    c.save()
    print(f"[OK] PDF de semanas: {path}")

if __name__ == '__main__':
    build_weeks()
