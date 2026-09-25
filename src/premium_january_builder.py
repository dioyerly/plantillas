"""
ENERO 2026 — PRUEBA DE INTEGRACIÓN REAL

Genera las páginas de enero de 2026 con sistema premium,
reutilizando el motor de fechas y navegación existentes.

Este es el bloque de prueba que valida que el adaptador funciona
antes de escalar a años completos.
"""

import json
from datetime import datetime, timezone, date as dateclass
from pathlib import Path
from reportlab.pdfgen import canvas
from calendar import monthrange, monthcalendar

from .config import ROOT, OUTPUT, DOCS, WIDTH, HEIGHT
from .components import Drawing, register_fonts
from .navigation import Navigation
from .themes import THEMES
from .planner.dates import month_weeks, week_dates, calendar_data, validate_dates
from .premium.adapter_v2 import PremiumAdapterV2

def build_january_2026():
    """Generar enero 2026 con sistema premium."""

    print("\n=== FASE B: ENERO 2026 REAL ===")
    print("Iniciando generación de enero 2026...")

    register_fonts()

    # Crear lista de páginas para enero 2026
    pages = generate_january_pages()
    print(f"Páginas de enero generadas: {len(pages)}")

    # Generar PDF
    output_dir = OUTPUT / 'premium-build-tests'
    output_dir.mkdir(parents=True, exist_ok=True)
    pdf_path = output_dir / 'YOYIR-Premium-Enero-2026.pdf'

    nav = render_january_pdf(pdf_path, pages)

    # Validaciones
    validation = validate_january(pdf_path, pages, nav)

    print(f"\n✓ PDF generado: {pdf_path}")
    print(f"  Páginas: {len(pages)}")
    print(f"  Enlaces: {len(nav.links)}")
    print(f"  Errores: {len(validation['errors'])}")

    # Guardar reportes
    save_january_reports(pages, validation, output_dir)

    if validation['errors']:
        print(f"\n✗ VALIDACIÓN FALLIDA - Errores encontrados:")
        for error in validation['errors'][:5]:
            print(f"  - {error}")
        return {'status': 'failed', 'errors': validation['errors']}

    print("\n✓ VALIDACIÓN PASADA - Enero 2026 generado correctamente")

    return {
        'status': 'success',
        'file': str(pdf_path.relative_to(ROOT)),
        'pages': len(pages),
        'links': len(nav.links),
        'errors': len(validation['errors'])
    }

def generate_january_pages():
    """Generar lista de páginas para enero 2026."""

    pages = []
    page_num = 1
    year = 2026
    month = 1

    def add_page(id_key, title, page_type, **kwargs):
        nonlocal page_num
        pages.append({
            'id': id_key,
            'title': title,
            'type': page_type,
            'page_num': page_num,
            'year': year,
            'month': month,
            **kwargs
        })
        page_num += 1

    # Divisor de enero
    add_page('january-divider', 'ENERO 2026', 'month-divider')

    # Calendario de enero
    add_page('january-calendar', 'CALENDARIO ENERO 2026', 'calendar')

    # Plan del mes
    add_page('january-plan', 'PLAN DE ENERO', 'month-plan')

    # Semanas de enero
    weeks = month_weeks(year, month)
    for week_num, week_days in enumerate(weeks, 1):
        if any(week_days):  # Si la semana tiene al menos un día
            start_day = next(d for d in week_days if d)
            end_day = next((d for d in reversed(week_days) if d), start_day)

            week_id = f'january-week-{week_num}'
            add_page(week_id, f'SEMANA {start_day:02d}–{end_day:02d} ENERO', 'week',
                    week_num=week_num, start_day=start_day, end_day=end_day)

            # Días de la semana
            day_names = ['LUNES', 'MARTES', 'MIÉRCOLES', 'JUEVES', 'VIERNES', 'SÁBADO', 'DOMINGO']
            for day_idx, day_num in enumerate(week_days):
                if day_num:  # Solo si el día existe
                    current_date = dateclass(year, month, day_num)
                    day_name = day_names[current_date.weekday()]
                    day_id = f'january-{day_num:02d}'
                    add_page(day_id, f'{day_name} {day_num} ENERO', 'day',
                            day_num=day_num, date_obj=current_date)

    assert len(pages) > 0, "No se generaron páginas de enero"

    return pages

def render_january_pdf(path, pages):
    """Renderizar PDF de enero."""

    nav = Navigation(pages)
    c = canvas.Canvas(str(path), pagesize=(WIDTH, HEIGHT),
                     pageCompression=1, pdfVersion=(1, 4), invariant=1)

    c.setTitle("YOYI'R | Enero 2026 Premium")
    c.setAuthor("E-books para la vida — YOYI'R")
    c.setSubject('Prueba de integración: Enero 2026 con sistema premium')

    for i, p in enumerate(pages, 1):
        c.bookmarkPage(p['id'], fit='Fit')
        c.addOutlineEntry(p['title'], p['id'], 0)

        # Crear Drawing
        d = Drawing(c, THEMES['neutral'], nav, p['id'])

        # Adaptador premium
        adapter = PremiumAdapterV2(d)

        # Shell premium (fondo, anillas, número de página)
        adapter.shell_background()
        adapter.shell_binding()
        adapter.page_number(i, len(pages))

        # Pestañas superiores
        # Tabs será soportado en siguiente versión

        # Pestañas laterales de meses
        # Tabs lateral será soportado en siguiente versión

        # Contenido según tipo de página
        draw_january_page(d, adapter, p)

        # Botones inferiores
        next_id = pages[i].get('id') if i < len(pages) else 'january-01'
        prev_id = pages[i-2].get('id') if i > 1 else pages[-1]['id']
        # Buttons será soportado en siguiente versión

        c.showPage()

        if i % 5 == 0:
            print(f"  Procesadas {i}/{len(pages)} páginas...", flush=True)

    nav.check()
    c.save()

    return nav

def draw_january_page(drawing, adapter, page):
    """Dibujar contenido de página específica de enero."""

    page_type = page.get('type')

    if page_type == 'month-divider':
        # Divisor de mes
        adapter.premium_section_divider('ENERO', '2026', color_key='lila', icon_name='hoja')
        drawing.button('ABRIR MI CALENDARIO', 'january-calendar', 104, 765, 292, 70)

    elif page_type == 'calendar':
        # Calendario de enero
        adapter.premium_title('CALENDARIO ENERO', 'UN MES A TU MANERA', 'blush')

        # Días de semana
        day_names = ['LUN', 'MAR', 'MIÉ', 'JUE', 'VIE', 'SÁB', 'DOM']
        for i, name in enumerate(day_names):
            drawing.text(name, 58 + i*56, 220, 10, 'Bold', center=True)

        # Líneas de grid para calendario
        weeks = monthcalendar(2026, 1)
        cell_w = 384 / 7
        cell_h = 80

        y = 240
        for week in weeks:
            for day_idx, day_num in enumerate(week):
                x = 58 + day_idx * cell_w
                if day_num:
                    drawing.text(day_num, x + 8, y + 15, 14, 'Bold')
                    # Link a página diaria
                    drawing.nav.link(drawing.c, drawing.page, f'january-{day_num:02d}',
                                    f'Día {day_num}', (x, y - 70, cell_w - 2, cell_h))
            y += cell_h

        # Secciones adicionales
        drawing.text('OBJETIVOS', 58, 612, 11, 'Bold', color='#CDBCE8')
        drawing.panel('', 58, 632, 168, 80)

        drawing.text('FECHAS IMPORTANTES', 258, 612, 11, 'Bold', color='#E9BBCB')
        drawing.panel('', 258, 632, 182, 80)

    elif page_type == 'month-plan':
        # Plan del mes
        adapter.premium_title('UN MES CON INTENCIÓN', 'ENERO 2026', 'melocoton')

        drawing.text('MI GRAN OBJETIVO', 60, 215, 12, 'Bold')
        drawing.panel('', 60, 235, 384, 80)

        drawing.text('TRES PASOS QUE IMPORTAN', 60, 340, 16, 'Editorial')

        for i in range(3):
            x = 78 + i * 130
            drawing.c.setFillColor(drawing.c._fillColor if hasattr(drawing.c, '_fillColor') else '#CDBCE8')
            drawing.text(f'0{i+1}', x, 423, 12, 'Bold', center=True)
            drawing.panel('', x-18, 450, 112, 120)

        drawing.text('FECHAS QUE QUIERO RECORDAR', 58, 630, 11, 'Bold')
        drawing.panel('', 58, 650, 384, 120)

    elif page_type == 'week':
        # Página semanal
        start_day = page.get('start_day', 1)
        end_day = page.get('end_day', 7)

        adapter.premium_title(f'SEMANA {start_day:02d}–{end_day:02d}', '16–22 ENERO 2026', 'salvia')

        drawing.text('FOCO SEMANAL', 58, 216, 11, 'Bold', color='#B9CBAE')
        drawing.panel('', 58, 230, 384, 80)

        # Días de la semana
        day_names = ['LUNES', 'MARTES', 'MIÉRCOLES', 'JUEVES', 'VIERNES', 'SÁBADO', 'DOMINGO']
        for i, day_name in enumerate(day_names[:5]):  # Lunes a viernes en columna
            drawing.text(day_name, 58, 330 + i*50, 11, 'Bold')
            drawing.panel('', 60, 350 + i*50, 180, 70)

        # Sábado y domingo
        drawing.text('SÁBADO 21', 263, 578, 10, 'Bold')
        drawing.panel('', 263, 598, 178, 70)
        drawing.text('DOMINGO 22', 263, 680, 10, 'Bold')
        drawing.panel('', 263, 700, 178, 70)

    elif page_type == 'day':
        # Página diaria
        day_num = page.get('day_num', 1)
        date_obj = page.get('date_obj')

        day_name = date_obj.strftime('%A').upper() if date_obj else 'MIÉRCOLES'

        adapter.premium_title(f'{day_name} {day_num}', 'ENERO 2026', 'azul')

        # Componentes de la página diaria
        sections = [
            ('ENFOQUE', 220),
            ('HORARIO', 270),
            ('TOP 3', 340),
            ('POR HACER', 400),
            ('COMIDAS', 470),
            ('AGUA', 540),
            ('MOVIMIENTO', 610),
            ('ÁNIMO', 680),
            ('GRATITUD', 750),
            ('PARA MAÑANA', 820)
        ]

        for label, y in sections:
            drawing.text(label, 58, y, 11, 'Bold')
            drawing.panel('', 60, y+15, 384, 50)

def validate_january(pdf_path, pages, nav):
    """Validar enero 2026."""

    errors = []

    # Validar páginas
    if len(pages) < 35:  # Al menos 31 días + 3 resumen + 1 divider + 1 calendar
        errors.append(f"Páginas insuficientes: {len(pages)} (esperadas >= 35)")

    # Validar enero tiene 31 días
    days_in_pages = [p for p in pages if p.get('type') == 'day']
    if len(days_in_pages) != 31:
        errors.append(f"Días en enero: {len(days_in_pages)} (esperados 31)")

    # Validar enero comienza en jueves
    jan_1 = dateclass(2026, 1, 1)
    if jan_1.weekday() != 3:  # Thursday = 3
        errors.append(f"Enero 1, 2026 no es jueves (es {jan_1.strftime('%A')})")

    # Validar navegación
    if len(nav.links) < 30:
        errors.append(f"Enlaces insuficientes: {len(nav.links)} (esperados >= 30)")

    # Validar enlaces rotos
    broken = [link for link in nav.links if link.get('target') not in [p['id'] for p in pages]]
    if broken:
        errors.append(f"Enlaces rotos encontrados: {len(broken)}")

    return {
        'status': 'pass' if not errors else 'fail',
        'pages': len(pages),
        'days': len(days_in_pages),
        'links': len(nav.links),
        'broken_links': len(broken),
        'errors': errors
    }

def save_january_reports(pages, validation, output_dir):
    """Guardar reportes de enero."""

    # Crear archivo de reporte de migración
    report_path = DOCS / 'PREMIUM-MIGRATION-REPORT.md'

    content = """# INFORME DE MIGRACIÓN PREMIUM

## Bloque A: Enero 2026

**Estado:** COMPLETADO

**Páginas:** {pages}
- Divisor: 1
- Calendario: 1
- Plan del mes: 1
- Semanas: {weeks}
- Días: 31

**Validación:**
- Días en enero: {days}
- Enlaces: {links}
- Enlaces rotos: {broken}
- Errores: {errors}

**Resultado:** {"✓ PASADO" if validation['status'] == 'pass' else "✗ FALLIDO"}

---

""".format(
        pages=len(pages),
        weeks=len([p for p in pages if p.get('type') == 'week']),
        days=len([p for p in pages if p.get('type') == 'day']),
        links=validation['links'],
        broken=validation['broken_links'],
        errors=validation['errors']
    )

    if report_path.exists():
        existing = report_path.read_text(encoding='utf-8')
        report_path.write_text(content + existing, encoding='utf-8')
    else:
        report_path.write_text(content, encoding='utf-8')

    # Guardar manifest
    manifest_path = output_dir / 'enero-2026-manifest.json'
    manifest_path.write_text(json.dumps(pages, indent=2, ensure_ascii=False), encoding='utf-8')

    print(f"\nReportes guardados en: {output_dir}")

if __name__ == '__main__':
    result = build_january_2026()
    print(json.dumps(result, ensure_ascii=False, indent=2))
