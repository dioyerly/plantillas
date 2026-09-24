"""Expand MASTER with PORTADA + DASHBOARD + ANNUAL CORE — insert before dated core."""
import calendar
import json
import re
from datetime import date,timedelta
from pathlib import Path
import fitz
from reportlab.pdfgen import canvas
from ..config import OUTPUT
from ..components import register_fonts
from .art import Art,W,H,COLORS
from .shell import digital_planner_shell,FULL_MONTHS
from .pages import cover,dashboard,menu,annual
from .dated import BlockArt,WEEKDAYS,MONTH_KICKERS
from .master_builder import dated_core_block

def annual_core_block():
    """Generate PORTADA, DASHBOARD, MENÚ, YEAR SELECTORS, ANNUAL PAGES, QUARTERS."""
    pages=[]

    # PORTADA
    pages.append(dict(id='portada',kind='portada',year=2026,month=1,months=False,active_tab='INICIO'))

    # DASHBOARD
    pages.append(dict(id='dashboard',kind='dashboard',year=2026,month=1,months=False,active_tab='INICIO'))

    # MENÚ
    pages.append(dict(id='menu',kind='menu',year=2026,month=1,months=False,active_tab='INICIO'))

    # AÑO SELECTOR
    pages.append(dict(id='year-selector',kind='year-selector',year=2026,month=1,months=False,active_tab='INICIO'))

    # AÑO 2026, 2027, 2028
    for year in (2026,2027,2028):
        pages.append(dict(id=f'year-{year}',kind='annual',year=year,month=1,months=False,active_tab='INICIO'))

        # RECURSOS ANUALES por año
        for resource in ['goals','dates','birthdays','projects','finance','personal','wellness','professional','vision','review']:
            pages.append(dict(id=f'year-{year}-{resource}',kind='annual-resource',year=year,month=1,resource=resource,months=False,active_tab='INICIO'))

        # TRIMESTRES
        for quarter in (1,2,3,4):
            pages.append(dict(id=f'year-{year}-q{quarter}',kind='quarter',year=year,quarter=quarter,month=1,months=False,active_tab='INICIO'))

    # Configurar navegación básica
    for i,p in enumerate(pages):
        p['previous']=pages[i-1]['id'] if i>0 else 'portada'
        p['next']=pages[i+1]['id'] if i+1<len(pages) else 'cal-2026-01'
        p['tab_targets']=['portada',f'year-{p["year"]}','cal-2026-01','week-2026-01-06','day-2026-01-01']
        p['month_targets']=[f'cal-{p["year"]}-{m:02d}' for m in range(1,13)]

    return pages

def draw_annual_page(a,p):
    """Render annual core pages."""
    if p['kind']=='portada':
        cover(a)
    elif p['kind']=='dashboard':
        dashboard(a)
    elif p['kind']=='menu':
        menu(a)
    elif p['kind']=='year-selector':
        a.text("YOYI'R",60,127,16,'Editorial')
        a.text('ELIGE TU AÑO',60,166,29,'Editorial')
        for i,year in enumerate((2026,2027,2028)):
            a.chip(str(year),f'year-{year}',58+i*130,201,122,COLORS[[0,7,5][i]])
    elif p['kind']=='annual':
        annual(a,p['year'])
    elif p['kind']=='annual-resource':
        titles={'goals':'MIS OBJETIVOS DEL AÑO','dates':'FECHAS IMPORTANTES','birthdays':'CUMPLEAÑOS',
                'projects':'MIS PROYECTOS','finance':'OBJETIVOS FINANCIEROS','personal':'OBJETIVOS PERSONALES',
                'wellness':'OBJETIVOS DE BIENESTAR','professional':'OBJETIVOS PROFESIONALES',
                'vision':'MI TABLERO DE VISIÓN','review':'REVISIÓN ANUAL'}
        a.title(titles[p['resource']],f'{p["year"]} / RECURSOS ANUALES',COLORS[5])
        a.text('Registra aquí tu planificación anual.',60,240,11)
        a.lines(60,270,380,4,40)
    elif p['kind']=='quarter':
        q=p['quarter'];months=['ENERO·FEBRERO·MARZO','ABRIL·MAYO·JUNIO','JULIO·AGOSTO·SEPTIEMBRE','OCTUBRE·NOVIEMBRE·DICIEMBRE'][q-1]
        a.title(f'TRIMESTRE {q}',f'{p["year"]} / {months}',COLORS[q])
        a.text('Planificación trimestral detallada.',60,240,11)
        a.lines(60,270,380,4,40)

def build_expanded_master(name='YOYIR-DIGITAL-PLANNER-MASTER.pdf'):
    """Build expanded MASTER: annual core + dated core."""
    out=OUTPUT/'.build';out.mkdir(parents=True,exist_ok=True);pdf=out/name
    register_fonts()

    annual_pages=annual_core_block()
    dated_pages,dated_known=dated_core_block()

    all_pages=annual_pages+dated_pages
    known={p['id'] for p in all_pages}
    nav=[];future=[];arts=[]

    # Update navigation
    for i,p in enumerate(all_pages):
        p['previous']=all_pages[i-1]['id'] if i>0 else 'portada'
        p['next']=all_pages[i+1]['id'] if i+1<len(all_pages) else 'portada'

    c=canvas.Canvas(str(pdf),pagesize=(W,H),pageCompression=1,pdfVersion=(1,4),invariant=1)
    c.setTitle("YOYI'R · Digital Planner 2026–2028");c.setAuthor("E-books para la vida — YOYI'R")

    from .dated import draw_block_page
    for i,p in enumerate(all_pages):
        c.bookmarkPage(p['id'],fit='Fit')
        a=BlockArt(c,p['id'],nav,known)
        if p['kind'] in ('portada','dashboard','menu','year-selector','annual','annual-resource','quarter'):
            draw_annual_page(a,p)
        else:
            digital_planner_shell(a,p,i,len(all_pages))
            draw_block_page(a,p)
        future+=a.future;arts.append(a);c.showPage()

    c.save()
    return pdf,all_pages,nav,future,arts

if __name__=='__main__':
    candidate,pages,nav,future,arts=build_expanded_master()

    annual_count=sum(1 for p in pages if p['kind'] in ('portada','dashboard','menu','year-selector','annual','annual-resource','quarter'))
    dated_count=sum(1 for p in pages if p['kind'] in ('divider','calendar','plan','week','day'))
    daily_count=sum(1 for p in pages if p['kind']=='day')
    week_count=sum(1 for p in pages if p['kind']=='week')

    print(f'[BUILD] Expanded MASTER: {len(pages)} pages')
    print(f'  Annual core: {annual_count}')
    print(f'  Dated core: {dated_count}')
    print(f'    Days: {daily_count}')
    print(f'    Weeks: {week_count}')

    master=OUTPUT/'YOYIR-DIGITAL-PLANNER-MASTER.pdf'
    doc=None
    try:
        doc=fitz.open(str(candidate))
        valid=(len(doc)==len(pages) and daily_count==1096 and week_count==159 and
                'portada' in [p['id'] for p in pages] and
                'dashboard' in [p['id'] for p in pages])
    except:
        valid=False
    finally:
        if doc:doc.close()

    if valid:
        (OUTPUT/'.build').mkdir(parents=True,exist_ok=True)
        if master.exists():
            backup=OUTPUT/'.build'/'MASTER-PREVIOUS.pdf'
            if backup.exists():backup.unlink()
            master.replace(backup)
        candidate.replace(master)
        print('[OK] MASTER promoted')
    else:
        print('[FAIL] Validation failed')
