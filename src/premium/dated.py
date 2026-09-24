"""Parametrized dated layouts built on the approved Prototype V2 components."""
import calendar
from datetime import date,timedelta
import fitz
from reportlab.pdfgen import canvas
from ..config import OUTPUT
from ..components import register_fonts
from .art import Art,W,H,COLORS
from .shell import digital_planner_shell,FULL_MONTHS
from .pages import full_calendar,month_divider,month_plan,week

WEEKDAYS=['LUNES','MARTES','MIÉRCOLES','JUEVES','VIERNES','SÁBADO','DOMINGO']
MONTH_KICKERS={1:'UN AÑO QUE EMPIEZA',2:'PEQUEÑOS PASOS',3:'UNA NUEVA ESTACIÓN',4:'DEJAR CRECER',5:'TIEMPO DE FLORECER',
               6:'MITAD DEL CAMINO',7:'RESPIRAR Y SEGUIR',8:'DÍAS LARGOS',9:'VOLVER A EMPEZAR',10:'COSECHAR',
               11:'AGRADECER',12:'CERRAR CON CARIÑO'}

class BlockArt(Art):
    """Art that only emits annotations for destinations present in the current PDF."""
    def __init__(self,c,page,nav,known):
        super().__init__(c,page,nav);self.known=known;self.future=[]
    def link(self,target,x,y,w,h,label,minimum=64):
        if target in self.known:
            return super().link(target,x,y,w,h,label,minimum)
        if not any(str(target).startswith(t) for t in ['cal-','week-','day-','div-','plan-']):
            return
        self.future.append({'source':self.page,'target':target,'label':label})

def premium_day(a,d):
    a.text(WEEKDAYS[d.weekday()],60,123,12,'Bold');a.text(f'{d.day:02d}',58,183,63,'Editorial')
    a.text(FULL_MONTHS[d.month-1],146,154,25,'Editorial');a.text(str(d.year),148,180,15)
    a.sticker('sol',368,115,62,COLORS[4])
    a.label('ENFOQUE',58,220,COLORS[3]);a.lines(151,220,290,1)
    a.label('HORARIO',58,267,COLORS[7]);a.line(86,291,86,694,'#B6C6D3',1.6)
    for i,hour in enumerate(range(7,21)):
        yy=294+i*29;a.text(f'{hour:02d}',61,yy+3,9);a.circle(86,yy,2.3,fill=COLORS[7],stroke=COLORS[7]);a.line(99,yy+3,218,yy+3)
    a.label('TOP 3',242,267,COLORS[0]);a.check(245,287,192,3,28)
    a.label('POR HACER',242,397,COLORS[5]);a.check(245,416,192,3,27)
    a.label('COMIDAS',242,523,COLORS[3])
    for i,t in enumerate(['D','A','C']):a.text(t,247,550+i*25,10,'Bold');a.line(264,553+i*25,438,553+i*25)
    a.text('AGUA',243,639,10,'Bold')
    for i in range(8):a.icon('gota',241+i*24,651,21,'#6D91A7')
    a.text('MOVIMIENTO',59,730,11,'Bold');a.icon('zapatilla',60,748,28);a.line(100,770,222,770)
    a.text('ÁNIMO',242,730,11,'Bold')
    for i in range(5):a.circle(260+i*35,754,9,stroke='#9D8AA5');a.text(i+1,260+i*35,758,9,center=True)
    a.text('GRATITUD',60,805,11,'Bold');a.line(60,831,224,831)
    a.text('PARA MAÑANA',242,805,11,'Bold');a.line(242,831,440,831)

def day_page(d):
    key=f'day-{d:%Y-%m-%d}'
    return dict(id=key,year=d.year,month=d.month,months=True,active_tab='DÍA',
                tab_targets=['inicio',f'year-{d.year}',f'cal-{d:%Y-%m}',f'week-{d:%G-W%V}',key],
                previous=f'day-{date.fromordinal(d.toordinal()-1):%Y-%m-%d}',
                next=f'day-{date.fromordinal(d.toordinal()+1):%Y-%m-%d}')

def build_day_test(d=date(2026,1,1)):
    out=OUTPUT/'premium-proof';out.mkdir(parents=True,exist_ok=True)
    pdf=out/'YOYIR-DIA-PREMIUM-VISUAL-TEST.pdf';png=pdf.with_suffix('.png')
    register_fonts()
    p=day_page(d);nav=[]
    c=canvas.Canvas(str(pdf),pagesize=(W,H),pageCompression=1,pdfVersion=(1,4),invariant=1)
    c.setTitle(f"YOYI'R · {WEEKDAYS[d.weekday()].title()} {d.day} de {FULL_MONTHS[d.month-1].lower()} de {d.year}")
    c.bookmarkPage(p['id'],fit='Fit')
    a=BlockArt(c,p['id'],nav,{p['id']})
    digital_planner_shell(a,p,0,1);premium_day(a,d)
    c.showPage();c.save()
    fitz.open(pdf)[0].get_pixmap(matrix=fitz.Matrix(3,3),alpha=False).save(png)
    return pdf,png,a.future

def day_id(d):return f'day-{d:%Y-%m-%d}'
def week_id(d):return f'week-{d-timedelta(days=d.weekday()):%Y-%m-%d}'
def cal_id(year,month):return f'cal-{year}-{month:02d}'

def month_block(year,month):
    first=date(year,month,1);last=date(year,month,calendar.monthrange(year,month)[1])
    days_list=[first+timedelta(days=i) for i in range(last.day)]
    days_set=set(days_list)
    week_starts=sorted({d-timedelta(days=d.weekday()) for d in days_list})
    cal=cal_id(year,month);div=f'div-{year}-{month:02d}';plan=f'plan-{year}-{month:02d}'
    pages=[dict(id=div,kind='divider',active_tab='MES'),dict(id=cal,kind='calendar',active_tab='MES'),
           dict(id=plan,kind='plan',active_tab='MES')]
    for monday in week_starts:
        pages.append(dict(id=week_id(monday),kind='week',start=monday,active_tab='SEM'))
        for i in range(7):
            d=monday+timedelta(days=i)
            if d in days_set:pages.append(dict(id=day_id(d),kind='day',date=d,active_tab='DÍA'))
    for i,p in enumerate(pages):
        p.update(year=year,month=month,months=True,
                 month_targets=[cal_id(year,m) for m in range(1,13)],
                 previous=pages[i-1]['id'] if i else f'year-{year}',
                 next=pages[i+1]['id'] if i+1<len(pages) else day_id(last+timedelta(days=1)))
        anchor=p.get('date',p.get('start',first))
        p['tab_targets']=['inicio',f'year-{year}',cal,week_id(anchor if p['kind']!='week' else p['start']),
                          p['id'] if p['kind']=='day' else day_id(max(anchor,first))]
        if p['kind']=='day':
            d=p['date'];p['previous']=day_id(d-timedelta(days=1));p['next']=day_id(d+timedelta(days=1))
    return pages

def draw_block_page(a,p):
    if p['kind']=='divider':month_divider(a,p['year'],p['month'],MONTH_KICKERS[p['month']],cal_id(p['year'],p['month']))
    elif p['kind']=='calendar':
        n=calendar.monthrange(p['year'],p['month'])[1]
        full_calendar(a,p['year'],p['month'],{d:day_id(date(p['year'],p['month'],d)) for d in range(1,n+1)})
    elif p['kind']=='plan':month_plan(a,p['year'],p['month'])
    elif p['kind']=='week':week(a,p['start'],day_id)
    else:premium_day(a,p['date'])

def build_month(year,month,name):
    out=OUTPUT/'premium-proof';out.mkdir(parents=True,exist_ok=True);pdf=out/name
    register_fonts();pages=month_block(year,month);known={p['id'] for p in pages};nav=[];future=[];arts=[]
    c=canvas.Canvas(str(pdf),pagesize=(W,H),pageCompression=1,pdfVersion=(1,4),invariant=1)
    c.setTitle(f"YOYI'R · {FULL_MONTHS[month-1].title()} {year}");c.setAuthor("E-books para la vida — YOYI'R")
    for i,p in enumerate(pages):
        c.bookmarkPage(p['id'],fit='Fit')
        a=BlockArt(c,p['id'],nav,known)
        digital_planner_shell(a,p,i,len(pages));draw_block_page(a,p)
        future+=a.future;arts.append(a);c.showPage()
    c.save()
    return pdf,pages,nav,future,arts
