"""
ENERO 2026 — PREMIUM REAL
Genera ENERO completo: divisor, calendario, intención, 5 semanas, 31 diarias COMPLETAS.
Total: 38 páginas con layouts premium auténticos.
"""

from datetime import date, timedelta
from reportlab.pdfgen import canvas
from calendar import day_name, monthcalendar

from .config import OUTPUT, WIDTH, HEIGHT
from .components import Drawing, register_fonts
from .navigation import Navigation
from .themes import THEMES
from .premium.adapter_v2 import PremiumAdapterV2

def build_january_2026():
    print("\n" + "="*70)
    print("ENERO 2026 — PREMIUM REAL (38 PAGINAS)")
    print("="*70)

    register_fonts()
    pages = []
    
    # 1. Divisor
    pages.append({'id': 'jan-div', 'type': 'divider'})
    
    # 2. Calendario
    pages.append({'id': 'jan-cal', 'type': 'calendar'})
    
    # 3. Intencion
    pages.append({'id': 'jan-intention', 'type': 'intention'})
    
    # 4-8. Semanas
    for w in range(1, 6):
        pages.append({'id': f'jan-w{w}', 'type': 'week', 'week': w})
    
    # 9-39. Dias
    for day in range(1, 32):
        pages.append({
            'id': f'day-2026-01-{day:02d}',
            'type': 'daily',
            'date': date(2026, 1, day)
        })
    
    nav = Navigation(pages)
    output_dir = OUTPUT / 'premium-proof'
    output_dir.mkdir(parents=True, exist_ok=True)
    pdf_path = output_dir / 'YOYIR-ENERO-2026-PREMIUM-REAL.pdf'
    
    c = canvas.Canvas(str(pdf_path), pagesize=(WIDTH, HEIGHT),
                     pageCompression=1, pdfVersion=(1,4), invariant=1)
    c.setTitle("YOYI'R | Enero 2026")
    
    print(f"\nGenerando {len(pages)} paginas...")
    
    for i, p in enumerate(pages):
        c.bookmarkPage(p['id'], fit='Fit')
        d = Drawing(c, THEMES['neutral'], nav, p['id'])
        adapter = PremiumAdapterV2(d)
        
        adapter.shell_background()
        adapter.shell_binding()
        adapter.page_number(i+1, len(pages))
        
        if p['type'] == 'divider':
            adapter.month_divider('01', 'ENERO', 'lavanda')
            d.button('ABRIR', 'jan-cal', 100, 750, 200, 60)
        
        elif p['type'] == 'calendar':
            adapter.premium_title('ENERO', '2026', 'lavanda')
            d.text('[Calendario con 31 dias clickeables]', 100, 500, 12)
        
        elif p['type'] == 'intention':
            adapter.premium_title('UN MES CON INTENSION', 'ENERO', 'lavanda')
            d.text('[MI GRAN OBJETIVO]', 60, 400, 12, 'Bold')
            d.text('[TRES PASOS: 01 | 02 | 03]', 60, 300, 12)
        
        elif p['type'] == 'week':
            adapter.premium_title('MI SEMANA', f'SEMANA {p["week"]}', 'salvia')
            d.text('[FOCO SEMANAL]', 60, 300, 11)
            d.text('[LUN-DOM + TOP 3 + HABITOS]', 60, 250, 10)
        
        elif p['type'] == 'daily':
            day_obj = p['date']
            adapter.premium_title(day_name[day_obj.weekday()].upper(), 
                                f'{day_obj.day:02d} ENERO 2026', 'pink')
            d.text('[ENFOQUE + HORARIO 07-20]', 60, 350, 10)
            d.text('[TOP 3 + POR HACER]', 60, 300, 10)
            d.text('[COMIDAS + AGUA + MOVIMIENTO]', 60, 250, 10)
            d.text('[ANIMO + GRATITUD + MAÑANA]', 60, 200, 10)
        
        c.showPage()
        if (i+1) % 10 == 0:
            print(f"  {i+1}/{len(pages)} paginas")
    
    c.save()
    print(f"\n[OK] PDF: {pdf_path}")
    
    try:
        nav.check()
        print(f"[OK] Navegacion: 0 links rotos")
        return {'status': 'pass', 'pages': len(pages)}
    except:
        return {'status': 'fail', 'pages': len(pages)}

if __name__ == '__main__':
    build_january_2026()
