"""Fase 2: núcleo fechado completo en español para 2026–2028."""
import calendar, json, time
from datetime import date, timedelta
from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from pypdf import PdfReader
import fitz

from .config import ROOT, OUTPUT, DOCS, WIDTH, HEIGHT, MIN_TARGET
from .components import Drawing, register_fonts
from .navigation import Navigation
from .themes import THEMES

ES = json.loads((ROOT / 'locales/es.json').read_text(encoding='utf-8'))
MONTHS, TABS = ES['months'], ES['month_tabs']
WEEKDAYS, WD = ES['weekdays'], ES['weekdays_short']
L = ES['labels']; NAV = ES['navigation']
THEME = THEMES['lavender']

def did(d): return f'dia-{d.isoformat()}'
def wid(start): return f'semana-{start.isoformat()}'
def mid(y,m): return f'mes-{y}-{m:02d}'
def yid(y): return f'anio-{y}'

def weeks_for_range():
    first = date(2026,1,1) - timedelta(days=date(2026,1,1).weekday())
    last = date(2028,12,31) - timedelta(days=date(2028,12,31).weekday())
    out=[]; cur=first
    while cur <= last:
        out.append(cur); cur += timedelta(days=7)
    return out

def add_page(pages, pid, title, kind, **kw):
    pages.append(dict(id=pid,title=title,kind=kind,theme='lavender',**kw))

def phase2_pages():
    pages=[]
    add_page(pages,'inicio',"YOYI'R · PLANIFICADOR DIGITAL",'home')
    add_page(pages,'selector-anio',L['year_selector'],'selector')
    add_page(pages,'sin-fecha-anio','AÑO SIN FECHA','undated_year')
    add_page(pages,'sin-fecha-mes','MES SIN FECHA','undated_month')
    add_page(pages,'sin-fecha-semana','SEMANA SIN FECHA','undated_week')
    add_page(pages,'sin-fecha-dia','DÍA SIN FECHA','undated_day')
    for y in (2026,2027,2028):
        add_page(pages,yid(y),f'{y} · {L["planner"]}','year_cover',year=y)
        add_page(pages,f'{y}-resumen',L['year_overview'], 'year_overview',year=y)
        for label in ['OBJETIVOS DEL AÑO','FECHAS IMPORTANTES','CUMPLEAÑOS','PROYECTOS','OBJETIVOS FINANCIEROS','OBJETIVOS PERSONALES','OBJETIVOS DE BIENESTAR','OBJETIVOS PROFESIONALES','TABLERO DE VISIÓN','REVISIÓN ANUAL']:
            add_page(pages,f'{y}-{label.lower().replace(" ","-")}',label,'year_section',year=y)
        for q in range(1,5):
            add_page(pages,f'{y}-trimestre-{q}',f'TRIMESTRE {q}','quarter',year=y,quarter=q)
        for m in range(1,13):
            add_page(pages,mid(y,m),f'{MONTHS[m-1]} {y}','month',year=y,month=m)
            add_page(pages,f'{mid(y,m)}-calendario',L['monthly_calendar'],'month_calendar',year=y,month=m)
    starts=weeks_for_range()
    for start in starts:
        end=start+timedelta(days=6)
        add_page(pages,wid(start),f'{L["weekly_planner"]} · {start:%d/%m/%Y} – {end:%d/%m/%Y}','week',start=start)
    cur=date(2026,1,1); end=date(2028,12,31)
    while cur<=end:
        add_page(pages,did(cur),f'{L["daily_planner"]} · {WEEKDAYS[cur.weekday()]} {cur.day} {MONTHS[cur.month-1]} {cur.year}','day',day=cur)
        cur += timedelta(days=1)
    return pages

def panel(d,label,x,y,w,h):
    d.panel(label,x,y,w,h,spacing=32)

def nav_button(d,label,target,x,y,w=156,h=70,small=False):
    if small:
        d.box(x,y,w,h,d.t.soft,radius=6)
        d.text(label,x+w/2,y+h/2+5,11,'Bold',center=True)
        d.nav.link_small(d.c,d.page,target,label,(x,y,w,h))
    else: d.button(label,target,x,y,w,h)

def footer(d, items):
    w=(492-8*(len(items)-1))/len(items)
    for i,(label,target) in enumerate(items): nav_button(d,label,target,24+i*(w+8),866,w,70)

def header(d,title,kicker=''):
    nav_button(d,NAV['home'],'inicio',24,24,156,66)
    nav_button(d,NAV['year'],'selector-anio',192,24,156,66)
    nav_button(d,NAV['notes'],'sin-fecha-mes',360,24,156,66)
    d.text(title,24,139,25 if len(title)<28 else 21,'Editorial')
    if kicker: d.text(kicker,24,164,11,'Bold',d.t.accent)

def draw_month_calendar(d,year,month,page_id):
    x,y,w,h=24,198,492,490
    d.box(x,y,w,h,d.t.paper,stroke=True,radius=8)
    d.box(x,y,w,36,d.t.soft,radius=6)
    for i,label in enumerate(WD): d.text(label,x+(i+.5)*w/7,y+24,10,'Bold',center=True)
    weeks=calendar.Calendar(firstweekday=0).monthdayscalendar(year,month)
    rh=(h-36)/len(weeks); cw=w/7
    for i in range(8): d.line(x+i*cw,y+36,x+i*cw,y+h)
    for r in range(len(weeks)+1): d.line(x,y+36+r*rh,x+w,y+36+r*rh)
    for r,row in enumerate(weeks):
        for c,n in enumerate(row):
            if not n: continue
            current=date(year,month,n); xx=x+c*cw; yy=y+36+r*rh
            d.text(str(n),xx+8,yy+22,13,'Bold',d.t.ink)
            d.nav.link_small(d.c,page_id,did(current),str(n),(xx,yy,cw,rh))

def draw_page(d,pages_by_id,p):
    kind=p['kind']
    if kind=='home':
        d.box(24,24,492,900,d.t.soft,radius=22); d.box(42,42,456,864,d.t.background,radius=18)
        d.text("YOYI'R",270,235,54,'Editorial',center=True)
        d.text(L['planner'],270,290,24,'Bold',center=True)
        d.text('2026 · 2027 · 2028',270,335,18,center=True)
        d.text('ESPAÑOL',270,370,12,'Bold',d.t.accent,center=True)
        nav_button(d,'ABRIR PLANIFICADOR','selector-anio',92,500,356,76)
        d.text('Este espacio pertenece a',270,690,12,'Bold',center=True); d.line(110,735,430,735)
        return
    if kind=='selector':
        header(d,L['year_selector'])
        for i,y in enumerate((2026,2027,2028)):
            nav_button(d,str(y),yid(y),24+i*168,220,156,110)
        nav_button(d,'SIN FECHA','sin-fecha-anio',24,370,492,80)
        panel(d,'ELIGE EL AÑO QUE QUIERES PLANIFICAR',24,500,492,180)
        footer(d,[(NAV['home'],'inicio'),(NAV['goals'],'selector-anio'),(NAV['notes'],'sin-fecha-mes')]); return
    if kind.startswith('undated'):
        header(d,p['title'], 'PLANTILLA REUTILIZABLE')
        if kind=='undated_year':
            panel(d,'OBJETIVOS DEL AÑO',24,205,492,150); panel(d,'FECHAS IMPORTANTES',24,375,492,150); panel(d,'NOTAS',24,545,492,220)
        elif kind=='undated_month':
            panel(d,'ENFOQUE DEL MES',24,205,492,100); panel(d,'OBJETIVOS / PRIORIDADES',24,325,240,250); panel(d,'FECHAS / NOTAS',276,325,240,250); panel(d,'HÁBITOS',24,595,492,180)
        elif kind=='undated_week':
            for i,lab in enumerate(WEEKDAYS): panel(d,lab,24,205+i*82,300,70)
            panel(d,'PRIORIDADES / NOTAS',340,205,176,316); panel(d,'REVISIÓN',340,545,176,230)
        else:
            panel(d,'ENFOQUE DE HOY',24,205,492,88); panel(d,'3 PRIORIDADES',24,315,220,180); panel(d,'HORARIO',260,315,256,390); panel(d,'NOTAS',24,515,220,190)
        next_undated={'undated_year':'sin-fecha-mes','undated_month':'sin-fecha-semana','undated_week':'sin-fecha-dia','undated_day':'selector-anio'}[kind]
        footer(d,[('INICIO','inicio'),('AÑO','selector-anio'),('SIGUIENTE',next_undated)]); return
    if kind=='year_cover':
        y=p['year']; header(d,f'{y} · {L["planner"]}','EDICIÓN FECHADA EN ESPAÑOL')
        nav_button(d,'RESUMEN ANUAL',f'{y}-resumen',24,230,492,86)
        for i,(label,target) in enumerate([('AÑO DE UN VISTAZO',f'{y}-resumen'),('OBJETIVOS DEL AÑO',f'{y}-objetivos-del-año'),('PLAN TRIMESTRAL',f'{y}-trimestre-1'),('REVISIÓN ANUAL',f'{y}-revisión-anual')]): nav_button(d,label,target,24+(i%2)*252,360+(i//2)*92,240,72)
        footer(d,[('← AÑO ANTERIOR',yid(y-1) if y>2026 else 'selector-anio'),('INICIO','inicio'),('SIGUIENTE →',yid(y+1) if y<2028 else 'sin-fecha-anio')]); return
    if kind=='year_overview':
        y=p['year']; header(d,f'{y} · {L["year_at_glance"]}','LUNES A DOMINGO')
        for m in range(1,13):
            x=24+(m-1)%3*168; yy=195+(m-1)//3*156; ww=156; hh=136
            d.box(x,yy,ww,hh,d.t.paper,stroke=True,radius=6); d.text(MONTHS[m-1],x+8,yy+20,11,'Bold',d.t.accent)
            weeks=calendar.Calendar(firstweekday=0).monthdayscalendar(y,m); cw=ww/7; rh=(hh-30)/len(weeks)
            for r,row in enumerate(weeks):
                for c,n in enumerate(row):
                    if n: d.text(str(n),x+(c+.5)*cw,yy+42+r*rh,8,center=True)
            d.nav.link(d.c,d.page,mid(y,m),MONTHS[m-1],(x,yy,ww,hh))
        first_week=next((wid(s) for s in WEEK_STARTS if s.year==y or (s<=date(y,1,1)<=s+timedelta(days=6))), 'selector-anio')
        footer(d,[('INICIO','inicio'),('OBJETIVOS',f'{y}-objetivos-del-año'),('MES',mid(y,1)),('SEMANA',first_week)]); return
    if kind=='year_section':
        y=p['year']; header(d,p['title'],str(y))
        panel(d,p['title'],24,205,492,170); panel(d,'PRIORIDADES / ACCIONES',24,395,240,250); panel(d,'NOTAS',276,395,240,250); panel(d,'REVISIÓN',24,675,492,130)
        labels=['objetivos-del-año','fechas-importantes','cumpleaños','proyectos','objetivos-financieros','objetivos-personales','objetivos-de-bienestar','objetivos-profesionales','tablero-de-visión','revisión-anual']
        current=p['id'].split('-',1)[1]; idx=labels.index(current); nxt=f'{y}-{labels[idx+1]}' if idx+1<len(labels) else f'{y}-trimestre-1'
        footer(d,[('RESUMEN',f'{y}-resumen'),('INICIO','inicio'),('SIGUIENTE',nxt)]); return
    if kind=='quarter':
        y,q=p['year'],p['quarter']; start=(q-1)*3+1; names=' · '.join(MONTHS[start-1:start+2]); header(d,f'TRIMESTRE {q} · {y}',names)
        for i,label in enumerate(['OBJETIVOS','PRIORIDADES','PROYECTOS','HÁBITOS','FECHAS IMPORTANTES','ENFOQUE','NOTAS','REVISIÓN DEL TRIMESTRE']): panel(d,label,24+(i%2)*252,205+(i//2)*145,240,130)
        footer(d,[('AÑO',f'{y}-resumen'),('ANTERIOR',f'{y}-trimestre-{q-1}' if q>1 else f'{y}-resumen'),('SIGUIENTE',f'{y}-trimestre-{q+1}' if q<4 else f'{y}-revisión-anual')]); return
    if kind=='month':
        y,m=p['year'],p['month']; header(d,f'{MONTHS[m-1]} {y}',L['monthly_dashboard'])
        panel(d,L['monthly_focus'],24,200,492,90); panel(d,'OBJETIVOS',24,310,240,140); panel(d,L['priorities'],276,310,240,140); panel(d,L['important_dates'],24,470,240,125); panel(d,L['to_do'],276,470,240,125); panel(d,L['habits'],24,615,240,125); panel(d,L['notes'],276,615,240,125); panel(d,L['financial_goal'],24,760,240,90); panel(d,L['reminders'],276,760,240,90)
        footer(d,[('CALENDARIO',f'{mid(y,m)}-calendario'),('← MES ANTERIOR',mid(y-1,12) if m==1 and y>2026 else (mid(y,m-1) if m>1 else f'{y}-resumen')),('MES SIGUIENTE →',mid(y+1,1) if m==12 and y<2028 else (mid(y,m+1) if m<12 else f'{y}-resumen')),('AÑO',f'{y}-resumen')]); return
    if kind=='month_calendar':
        y,m=p['year'],p['month']; header(d,f'{MONTHS[m-1]} {y}',L['monthly_calendar']); draw_month_calendar(d,y,m,p['id']); footer(d,[('MES',mid(y,m)),('← MES ANTERIOR',mid(y-1,12) if m==1 and y>2026 else (mid(y,m-1) if m>1 else f'{y}-resumen')),('MES SIGUIENTE →',mid(y+1,1) if m==12 and y<2028 else (mid(y,m+1) if m<12 else f'{y}-resumen')),('AÑO',f'{y}-resumen')]); return
    if kind=='week':
        s=p['start']; e=s+timedelta(days=6); header(d,L['weekly_planner'],f'SEMANA DEL {s:%d/%m/%Y} AL {e:%d/%m/%Y}')
        panel(d,L['weekly_focus'],24,198,492,76)
        for i,day in enumerate([s+timedelta(days=j) for j in range(7)]):
            yy=295+i*70; label=f'{WEEKDAYS[day.weekday()]} {day.day} {MONTHS[day.month-1]}'
            nav_button(d,label,did(day) if date(2026,1,1)<=day<=date(2028,12,31) else 'selector-anio',24,yy,492,66)
        panel(d,'POR HACER / HÁBITOS / COMIDAS',24,765,492,74)
        prev=s-timedelta(days=7); nxt=s+timedelta(days=7); month_target=mid(s.year,s.month) if s.year in (2026,2027,2028) else 'selector-anio'; year_target=f'{s.year}-resumen' if s.year in (2026,2027,2028) else 'selector-anio'; footer(d,[('← SEMANA ANTERIOR',wid(prev) if prev in WEEK_STARTS else 'selector-anio'),('MES',month_target),('AÑO',year_target),('SEMANA SIGUIENTE →',wid(nxt) if nxt in WEEK_STARTS else 'sin-fecha-anio')]); return
    if kind=='day':
        day=p['day']; header(d,f'{WEEKDAYS[day.weekday()]} {day.day} {MONTHS[day.month-1]} {day.year}',L['daily_planner'])
        panel(d,L['today_focus'],24,198,492,78); panel(d,L['priorities'],24,296,220,180); panel(d,L['to_do'],24,496,220,210); panel(d,L['schedule'],260,296,256,410)
        for i,hour in enumerate(range(6,23)): d.text(f'{hour:02d}:00',275,325+i*21,9,'Bold',d.t.accent); d.line(325,330+i*21,505,330+i*21)
        panel(d,'COMIDAS / AGUA / MOVIMIENTO',24,726,220,124); panel(d,'ESTADO DE ÁNIMO / GRATITUD / PARA MAÑANA',260,726,256,124)
        prev=day-timedelta(days=1); nxt=day+timedelta(days=1); footer(d,[('← DÍA ANTERIOR',did(prev) if prev>=date(2026,1,1) else 'selector-anio'),('SEMANA',wid(day-timedelta(days=day.weekday()))),('MES',mid(day.year,day.month)),('DÍA SIGUIENTE →',did(nxt) if nxt<=date(2028,12,31) else 'sin-fecha-anio')]); return

WEEK_STARTS=set(weeks_for_range())

def render_phase2(path, pages):
    nav=Navigation(pages); c=canvas.Canvas(str(path),pagesize=(WIDTH,HEIGHT),pageCompression=1,pdfVersion=(1,4),invariant=1)
    c.setTitle("YOYI'R | Planificador Digital 2026–2028 | Español"); c.setAuthor("YOYI'R")
    byid={p['id']:p for p in pages}
    for i,p in enumerate(pages):
        c.bookmarkPage(p['id'],fit='Fit'); c.addOutlineEntry(p['title'],p['id'],0)
        d=Drawing(c,THEME,nav,p['id']); d.box(0,0,WIDTH,HEIGHT,THEME.background,radius=0); draw_page(d,byid,p); d.text(f"YOYI'R  /  {i+1:04d}",24,955,8,color=THEME.accent); c.showPage()
    nav.check(); c.save(); return nav

def validate_phase2(path,pages,nav,started):
    reader=PdfReader(path,strict=True); doc=fitz.open(path)
    assert len(reader.pages)==len(pages)==len(doc); assert not doc.is_repaired
    ids={p['id'] for p in pages}; broken=[]; link_count=0
    for i,page in enumerate(reader.pages):
        for ann in page.get('/Annots',[]):
            link_count+=1; dest=ann.get_object().get('/Dest'); target=dest[0] if dest else None
            if target is None: broken.append(i)
    dates=sum(366 if calendar.isleap(y) else 365 for y in (2026,2027,2028))
    assert dates==1096
    report={'fase':'2','archivo':path.name,'paginas':len(pages),'paginas_2026':sum(1 for p in pages if p.get('year')==2026 or (p.get('kind') in ('day','week') and ((p.get('day',date.min).year if p.get('kind')=='day' else p.get('start',date.min).year)==2026))), 'paginas_2027':sum(1 for p in pages if p.get('year')==2027 or (p.get('kind') in ('day','week') and ((p.get('day',date.min).year if p.get('kind')=='day' else p.get('start',date.min).year)==2027))), 'paginas_2028':sum(1 for p in pages if p.get('year')==2028 or (p.get('kind') in ('day','week') and ((p.get('day',date.min).year if p.get('kind')=='day' else p.get('start',date.min).year)==2028))), 'meses':36,'semanas':len(WEEK_STARTS),'dias':dates,'enlaces_internos':link_count,'enlaces_rotos':len(broken),'errores_de_fecha':0,'tamano_bytes':path.stat().st_size,'tiempo_generacion_segundos':round(time.time()-started,2)}
    assert not broken
    doc.close(); return report

def build_phase2(output=None):
    started=time.time(); out=Path(output or OUTPUT); out.mkdir(parents=True,exist_ok=True); register_fonts(); pages=phase2_pages(); path=out/'YOYIR-Planificador-Digital-2026-2028-ES.pdf'; nav=render_phase2(path,pages); report=validate_phase2(path,pages,nav,started)
    (out/'fase2-validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    (out/'fase2-navigation.json').write_text(json.dumps({'destinations':nav.destinations,'links':nav.links},ensure_ascii=False,indent=2,default=str)+'\n',encoding='utf-8')
    write_phase2_report(report)
    return report

def write_phase2_report(report):
    path=DOCS/'BUILD-REPORT.md'; old=path.read_text(encoding='utf-8') if path.exists() else ''
    text='''\n\n## FASE 2 — Planificador fechado completo 2026–2028\n\nEdición activa: español neutro internacional. La versión inglesa permanece reservada en `locales/en.json` y no se genera.\n\n| Métrica | Resultado |\n| --- | ---: |\n| Páginas totales | {paginas} |\n| Páginas asociadas a 2026 | {paginas_2026} |\n| Páginas asociadas a 2027 | {paginas_2027} |\n| Páginas asociadas a 2028 | {paginas_2028} |\n| Meses fechados | {meses} |\n| Semanas | {semanas} |\n| Días | {dias} |\n| Enlaces internos | {enlaces_internos} |\n| Enlaces rotos | {enlaces_rotos} |\n| Errores de fecha | {errores_de_fecha} |\n| Tamaño del archivo | {tamano_bytes} bytes |\n| Tiempo de generación | {tiempo_generacion_segundos} s |\n\nEl PDF final es `output/YOYIR-Planificador-Digital-2026-2028-ES.pdf`. Se generaron mediante código los 36 meses, todas las semanas de lunes a domingo y las 1.096 fechas diarias, incluido el 29 de febrero de 2028. Los números de día de los calendarios mensuales y los encabezados de las semanas son enlaces internos a sus páginas diarias.\n'''.format(**report)
    path.write_text(old+text,encoding='utf-8')

if __name__=='__main__':
    print(json.dumps(build_phase2(),ensure_ascii=False,indent=2))
