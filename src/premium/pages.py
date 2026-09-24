import calendar
from datetime import date,timedelta
from .art import COLORS,PAPER,INK,RULE,H
from .shell import FULL_MONTHS

PAGE_DEFS=[
('portada','PORTADA','cover'),('inicio','INICIO','dashboard'),('menu','MENÚ','directory'),
('year-2026','2026','annual'),('enero','ENERO 2026','calendar'),('febrero','FEBRERO 2028','calendar'),
('mes','MARZO','divider'),('calendario','MARZO 2026','calendar'),('plan-mes','PLAN DEL MES','roadmap'),
('semana','MI SEMANA','split-page'),('dia','MIÉRCOLES','timeline'),
('objetivos','OBJETIVOS','editorial-divider'),('smart','MI META SMART','goal-map'),
('vida','VIDA','editorial-divider'),('mi-vida','MI VIDA','collage'),
('productividad','PRODUCTIVIDAD','editorial-divider'),('plan-productividad','MENOS RUIDO, MÁS FOCO','matrix'),
('bienestar','BIENESTAR','editorial-divider'),('tracker','MI SEMANA DE BIENESTAR','tracker'),
('autocuidado','VOLVER A MÍ','journal'),('finanzas','FINANZAS','editorial-divider'),
('presupuesto','PRESUPUESTO MENSUAL','table'),('estudio','ESTUDIO','editorial-divider'),
('plan-estudio','PLAN DE ESTUDIO','study-plan'),('organizacion','UN LUGAR PARA CADA COSA','checklist'),
('notas','IDEAS QUE MERECEN QUEDARSE','dot-grid'),('extras','PEQUEÑOS EXTRAS','resource-board'),
('funcionales','STICKERS FUNCIONALES','sticker-sheet'),('stickers-vida','STICKERS DE VIDA','illustration-sheet'),
('cierre','TU TIEMPO, TU RITMO','freeform'),('year-2027','2027','annual'),('year-2028','2028','annual'),
('sin-fecha','UN NUEVO COMIENZO','undated')]

def manifest():
    pages=[]
    for i,(key,title,family) in enumerate(PAGE_DEFS):
        p=dict(id=key,title=title,family=family,previous=PAGE_DEFS[i-1][0] if i else 'inicio',next=PAGE_DEFS[i+1][0] if i+1<len(PAGE_DEFS) else 'inicio')
        if family in ('annual','calendar') or key in ('mes','plan-mes','semana','dia'):
            p.update(year=2028 if key=='febrero' else int(key[-4:]) if key.startswith('year-') else 2026,months=True)
            if family!='annual':p['month']=1 if key=='enero' else 2 if key=='febrero' else 3
        pages.append(p)
    return pages

def mini_calendar(a,year,month,x,y,w=120,h=110,anchor=False):
    color=COLORS[(month-1)%10]
    a.box(x,y,w,h,'#FAF7F1',r=4)
    a.label(FULL_MONTHS[month-1],x+3,y+17,color,w-6)
    for col,name in enumerate(['L','M','X','J','V','S','D']):a.text(name,x+(col+.5)*w/7,y+37,7.5,'Bold',center=True)
    cells=[]
    for row,week in enumerate(calendar.Calendar(0).monthdayscalendar(year,month)):
        for col,n in enumerate(week):
            if n:
                xx=x+(col+.5)*w/7;yy=y+49+row*10
                a.text(n,xx,yy,8,center=True);cells.append((n,col,xx,yy))
    a.calendars.append(dict(year=year,month=month,bounds=[x,y,w,h],cells=cells))
    if anchor:
        key=f'm-{year}-{month:02d}'
        a.c.bookmarkPage(key,fit='FitR',left=x,bottom=H-y-h,right=x+w,top=H-y)
    return cells

def full_calendar(a,year,month,day_targets=None):
    color=COLORS[(month-1)%10]
    a.title(FULL_MONTHS[month-1].title(),str(year)+' / UN MES A TU MANERA',color)
    a.sticker('hoja' if month==3 else 'estrella',366,111, sixty:=62,color)
    x,y,w,h=58,220,384,355
    weeks=calendar.Calendar(0).monthdayscalendar(year,month);cw=w/7;rh=(h-30)/len(weeks)
    a.box(x,y,w,30,color,r=3)
    a.box(x+5*cw,y+30,2*cw,h-30,'#F4F0F4',r=0)
    for col,name in enumerate(['LUN','MAR','MIÉ','JUE','VIE','SÁB','DOM']):a.text(name,x+(col+.5)*cw,y+20,9,'Bold',center=True)
    for col in range(8):a.line(x+col*cw,y+30,x+col*cw,y+h)
    for row in range(len(weeks)+1):a.line(x,y+30+row*rh,x+w,y+30+row*rh)
    cells=[]
    for row,week in enumerate(weeks):
        for col,n in enumerate(week):
            if n:
                xx=x+col*cw+8;yy=y+48+row*rh
                a.text(n,xx,yy,12,'Bold');cells.append((n,col,xx,yy))
    a.calendars.append(dict(year=year,month=month,bounds=[x,y,w,h],cells=cells))
    a.label('OBJETIVOS',58,612,COLORS[5]);a.check(60,632,168,3,28)
    a.label('FECHAS IMPORTANTES',258,612,COLORS[1]);a.lines(258,647,182,3,28)
    a.label('NOTAS',58,760,COLORS[7]);a.lines(60,786,168,2,28)
    a.label('HÁBITOS',258,760,COLORS[4]);a.dots(268,782,7,2,24)

def cover(a):
    a.box(0,0,540,960,'#EAE4EB',r=0)
    a.box(40,32,469,900,'#C6BEC9',r=22)
    a.box(32,24,469,900,'#C6B3DE',r=21)
    a.box(32,25,28,898,'#AFA0C6',r=14)
    a.line(66,46,66,900,'#E6DAEF',1)
    a.box(82,69,365,758,'#F8F1E9',r=140)
    a.circle(251,251,100,fill=COLORS[3],stroke=COLORS[3])
    a.circle(305,211,68,fill=COLORS[1],stroke=COLORS[1])
    a.circle(216,293,62,fill=COLORS[7],stroke=COLORS[7])
    a.line(139,331,354,157,INK,.8)
    a.icon('estrella',325,129,38);a.icon('estrella',148,340,24)
    a.text("YOYI'R",266,458,55,'Editorial',center=True)
    a.text('PLANIFICADOR',266,504,22,'Bold',center=True)
    a.text('DIGITAL',266,537,22,'Bold',center=True)
    a.text('2026 · 2027 · 2028',266,589,20,'Editorial',center=True)
    a.line(210,625,320,625,'#9D8CA7',1)
    a.text('Un lugar para tu vida.',266,669,17,'Editorial',center=True)
    a.chip('ABRIR MI AGENDA','inicio',141,726,250,COLORS[5],72)
    a.text('E-books para la vida',270,865,12,'Body',center=True)
    a.box(466,60,17,830,'#9D8CB1',r=7)

def dashboard(a):
    a.text("YOYI'R",60,127,16,'Editorial');a.text('MI PLANIFICADOR',60,166,29,'Editorial')
    a.icon('agenda',374,110,56)
    for i,year in enumerate((2026,2027,2028)):a.chip(str(year),f'year-{year}',58+i*130,201,122,COLORS[[0,7,5][i]])
    a.chip('SIN FECHA','sin-fecha',58,282,162,COLORS[9])
    a.text('A tu manera.',258,322,21,'Editorial')
    # Asymmetric editorial tiles; the full colored surface is a real link.
    a.sticky(58,374,236,154,COLORS[0]);a.icon('estrella',224,389,46)
    a.text('OBJETIVOS',75,414,19,'Bold');a.text('Lo que quiero construir',75,444,13)
    a.lines(76,480,176,2,24);a.link('objetivos',58,374,236,154,'OBJETIVOS')
    a.box(309,374,133,154,COLORS[3],r=55);a.icon('hoja',351,398,47)
    a.text('VIDA',375,492,17,'Bold',center=True);a.link('vida',309,374,133,154,'VIDA')
    a.box(58,545,133,139,COLORS[5],r=7);a.icon('sol',103,558,44)
    a.text('BIENESTAR',124,647,13,'Bold',center=True);a.link('bienestar',58,545,133,139,'BIENESTAR')
    a.box(207,545,235,139,'#EEF1F8',r=10);a.tape(285,538,77,COLORS[7])
    a.text('PRODUCTIVIDAD',224,589,18,'Bold');a.check(225,614,177,2,27)
    a.link('productividad',207,545,235,139,'PRODUCTIVIDAD')
    for i,(label,key) in enumerate([('FINANZAS','finanzas'),('ESTUDIO','estudio'),('NOTAS','notas'),('EXTRAS','extras')]):
        a.chip(label,key,58+(i%2)*200,700+(i//2)*73,184,COLORS[[4,8,7,1][i]])

def menu(a):
    a.title('Todo tiene su lugar','TU AGENDA / MENÚ',COLORS[7])
    entries=[('OBJETIVOS','objetivos','estrella'),('VIDA','vida','hoja'),('PRODUCTIVIDAD','productividad','reloj'),('BIENESTAR','bienestar','sol'),('AUTOCUIDADO','autocuidado','corazon'),('FINANZAS','finanzas','cartera'),('ESTUDIO','estudio','libro'),('ORGANIZACIÓN','organizacion','casa'),('NOTAS','notas','lapiz'),('EXTRAS','extras','regalo')]
    for i,(label,key,icon) in enumerate(entries):
        yy=200+i*64
        # Adjacent nonoverlapping 64 pt tap targets, each a ruled index entry.
        a.circle(81,yy+27,22,fill=COLORS[i],stroke=COLORS[i]);a.icon(icon,65,yy+11,32)
        a.text(label,119,yy+33,16,'Bold');a.text(f'{i+1:02d}',426,yy+33,12,center=True)
        a.line(114,yy+57,438,yy+57);a.link(key,58,yy,384,64,label)

def annual(a,year):
    a.title(str(year),'EL AÑO DE UN VISTAZO',COLORS[7])
    a.text('Un año de posibilidades.',188,159,15,'Editorial')
    for month in range(1,13):mini_calendar(a,year,month,58+(month-1)%3*130,204+(month-1)//3*121,124,111,True)
    a.label('PALABRA DEL AÑO',58,714,COLORS[3]);a.lines(60,744,174,1)
    a.label('OBJETIVO DEL AÑO',260,714,COLORS[5]);a.lines(260,744,180,1)
    a.label('MIS FECHAS CLAVE',58,786,COLORS[1]);a.lines(60,816,380,1)

DIVIDERS={
'objetivos':('Lo que quiero construir','estrella',0,'smart',[('VISIÓN','smart-vision'),('METAS','smart-metas'),('PLAN DE ACCIÓN','smart-accion'),('PROGRESO','smart-progreso'),('REVISIÓN','smart-revision')]),
'vida':('Lo que hace mi vida mía','hoja',3,'mi-vida',[('MI TABLERO','mi-vida'),('SUEÑOS & AVENTURAS','mi-vida')]),
'productividad':('Hacer espacio para lo importante','reloj',8,'plan-productividad',[('MI PLAN DE FOCO','plan-productividad'),('PRIORIDADES','plan-productividad')]),
'bienestar':('Escuchar mi propio ritmo','sol',5,'tracker',[('MI SEMANA','tracker'),('MI AUTOCUIDADO','autocuidado')]),
'finanzas':('Decisiones con intención','cartera',4,'presupuesto',[('MI PRESUPUESTO','presupuesto'),('AHORRO & FACTURAS','presupuesto')]),
'estudio':('Aprender, conectar, crecer','libro',7,'plan-estudio',[('PLAN DE ESTUDIO','plan-estudio'),('MIS APUNTES','notas')])}

def divider(a,key,title):
    caption,icon,ci,target,links=DIVIDERS[key];color=COLORS[ci]
    a.text(f'COLECCIÓN PERSONAL / {title}',60,129,10,'Bold')
    a.box(87,190,326,294,color,r=135)
    a.circle(334,268,55,fill=COLORS[(ci+3)%10],stroke=COLORS[(ci+3)%10])
    a.icon(icon,168,238,148)
    a.icon('estrella',358,401,29)
    size=29 if len(title)>12 else 38
    a.text(title,250,518,size,'Editorial',center=True)
    a.text(caption,250,554,16,'Editorial',center=True)
    if len(links)==5:
        for i,(label,to) in enumerate(links[:4]):a.chip(label,to,58+(i%2)*200,588+(i//2)*80,184,COLORS[(ci+i)%10])
        a.chip(links[4][0],links[4][1],158,748,184,COLORS[6])
    else:
        for i,(label,to) in enumerate(links):a.chip(label,to,82,605+i*92,336,COLORS[(ci+i)%10],72)
        a.text('Abre una página. Empieza por algo pequeño.',250,822,12,center=True)

def month_divider(a,year=2026,month=3,kicker='UNA NUEVA ESTACIÓN',target='calendario'):
    a.text(f'{month:02d} / {kicker}',60,128,11,'Bold')
    a.box(85,189,330,318,COLORS[3],r=160)
    a.circle(330,288,64,fill=COLORS[4],stroke=COLORS[4]);a.icon('planta',156,227,175)
    a.text(FULL_MONTHS[month-1],250,548,52,'Editorial',center=True);a.text(str(year),250,587,24,'Body',center=True)
    a.text('Este mes quiero…',77,657,21,'Editorial');a.lines(78,692,344,2,35)
    a.chip('ABRIR MI MES',target,104,765,292,COLORS[5],70)

def month_plan(a,year=2026,month=3):
    a.title('Un mes con intención',f'{FULL_MONTHS[month-1]} {year} / MIS PRIORIDADES',COLORS[3])
    a.sticky(58,215,384,115,COLORS[4]);a.text('MI GRAN OBJETIVO',76,249,13,'Bold');a.lines(76,284,340,1)
    a.text('Tres pasos que importan',60,378,21,'Editorial')
    for i in range(3):
        x=78+i*130;a.circle(x,423,19,fill=COLORS[i],stroke=COLORS[i]);a.text(f'0{i+1}',x,428,12,'Bold',center=True)
        if i<2:a.line(x+23,423,x+104,423,'#A69FA4',1)
        a.lines(x-18,466,112,3,27)
    a.label('FECHAS QUE QUIERO RECORDAR',58,578,COLORS[1]);a.check(62,601,376,3,31)
    a.label('UN HÁBITO PEQUEÑO',58,738,COLORS[5]);a.lines(60,773,160,1)
    a.dots(263,765,7,3,25)

def week_range(start):
    end=start+timedelta(days=6)
    if (start.year,start.month)==(end.year,end.month):return f'{start.day}—{end.day} {FULL_MONTHS[end.month-1]} {end.year}'
    if start.year==end.year:return f'{start.day} {FULL_MONTHS[start.month-1]}—{end.day} {FULL_MONTHS[end.month-1]} {end.year}'
    return f'{start.day} {FULL_MONTHS[start.month-1]} {start.year}—{end.day} {FULL_MONTHS[end.month-1]} {end.year}'

def week(a,start=date(2026,3,16),day_target=None):
    a.title('Mi semana',week_range(start),COLORS[5])
    a.label('FOCO SEMANAL',58,216,COLORS[4]);a.lines(61,244,380,1)
    a.line(250,279,250,676,'#CFC5C1',1)
    for i in range(5):
        col=i%2;row=i//2;x=58+col*204;y=282+row*137
        day=start+timedelta(days=i)
        a.text(['LUNES','MARTES','MIÉRCOLES','JUEVES','VIERNES'][i],x,y+17,12,'Bold')
        a.circle(x+166,y+12,15,fill=COLORS[i],stroke=COLORS[i]);a.text(day.day,x+166,y+17,11,'Bold',center=True)
        a.lines(x,y+49,180,3,27)
        if day_target:a.link(day_target(day),x+128,y-20,64,64,f'DIA {day:%d/%m}')
    a.box(263,558,178,115,'#F3EEE7',r=8)
    for i,name in enumerate(['SÁBADO','DOMINGO']):
        day=start+timedelta(days=5+i)
        a.text(f'{name} {day.day}',274,578+i*52,10,'Bold');a.line(275,601+i*52,429,601+i*52)
        if day_target:a.link(day_target(day),263,550+i*64,178,64,f'DIA {day:%d/%m}')
    a.label('TOP 3',58,720,COLORS[0]);a.check(61,744,178,3,29)
    a.label('HÁBITOS',263,720,COLORS[6]);a.text('L   M   X   J   V   S   D',269,749,9,'Bold');a.dots(273,770,7,3,24)

def day(a):
    a.text('MIÉRCOLES',60,123,12,'Bold');a.text('18',58,183,63,'Editorial')
    a.text('MARZO',146,154,25,'Editorial');a.text('2026',148,180,15)
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

def smart(a):
    a.title('Mi meta SMART','UNA IDEA CON DIRECCIÓN',COLORS[0])
    rows=[('S','ESPECÍFICA','¿Qué quiero conseguir exactamente?','vision'),('M','MEDIBLE','¿Cómo voy a medir mi progreso?','metas'),('A','ALCANZABLE','¿Qué necesito para conseguirlo?','accion'),('R','RELEVANTE','¿Por qué es importante para mí?','progreso'),('T','TEMPORAL','¿Cuándo quiero conseguirlo?','revision')]
    for i,(letter,title,prompt,key) in enumerate(rows):
        yy=210+i*123
        a.circle(82,yy+24,24,fill=COLORS[i],stroke=COLORS[i]);a.text(letter,82,yy+31,21,'Editorial',center=True)
        a.text(title,122,yy+16,12,'Bold');a.text(prompt,122,yy+40,12);a.lines(124,yy+72,311,1)
        if key=='progreso':a.bar(126,yy+88,277,10)
        a.c.bookmarkPage('smart-'+key,fit='FitR',left=55,bottom=H-yy-121,right=442,top=H-yy+5)

def life(a):
    a.title('Mi vida','COSAS QUE QUIERO VIVIR',COLORS[3])
    a.box(62,223,210,245,'#E7DFD5',r=1);a.box(58,217,210,245,'#FFFFFF',r=1)
    a.box(71,231,184,174,'#F0E6EF',r=0);a.tape(115,207,89,COLORS[0])
    a.icon('camara',143,280,51);a.text('MI VISIÓN',163,436,14,'Editorial',center=True)
    a.sticky(286,242,151,188,COLORS[4]);a.text('MIS SUEÑOS',299,278,12,'Bold');a.check(301,305,118,3,31)
    a.label('PRÓXIMA AVENTURA',58,514,COLORS[7]);a.sticker('maleta',363,490,67,COLORS[3])
    a.text('Destino / fecha',60,550,12);a.lines(60,578,370,2,29)
    a.icon('avion',349,603,53)
    a.label('FAVORITOS',58,683,COLORS[1]);a.icon('auriculares',58,705,29);a.lines(98,725,140,3,29)
    a.label('QUIERO APRENDER',263,683,COLORS[5]);a.icon('libro',269,707,29);a.lines(306,730,132,3,27)

def productivity(a):
    a.title('Menos ruido, más foco','MI PLAN DE PRODUCTIVIDAD',COLORS[8])
    a.label('UNA COSA IMPORTANTE',58,218,COLORS[4]);a.lines(60,252,380,1)
    for i,label in enumerate(['HACER','PLANIFICAR','DELEGAR','SOLTAR']):
        x=58+(i%2)*198;y=292+(i//2)*145
        a.box(x,y,186,132,['#EFE8F6','#E7F0E3','#E8F0F6','#F7E7E2'][i],r=4)
        a.text(label,x+12,y+24,12,'Bold');a.check(x+12,y+43,160,3,27)
    a.text('Mi sesión de concentración',60,630,20,'Editorial');a.icon('reloj',394,603,37)
    for i,label in enumerate(['PREPARAR','ENFOCAR','PAUSAR']):
        x=78+i*132;a.circle(x,679,13,fill=COLORS[i+5],stroke=COLORS[i+5])
        if i<2:a.line(x+15,679,x+117,679)
        a.text(label,x-15,714,10,'Bold');a.line(x-17,751,x+95,751)
    a.label('LO QUE LOGRÉ',58,804,COLORS[0]);a.lines(182,806,258,1)

def wellbeing(a):
    a.title('Mi semana de bienestar','16—22 MARZO / OBSERVAR SIN JUZGAR',COLORS[5])
    for i,t in enumerate(['L','M','X','J','V','S','D']):a.text(t,184+i*38,220,12,'Bold',center=True)
    for row,label in enumerate(['ÁNIMO','ENERGÍA']):
        yy=257+row*105;a.text(label,59,yy+7,12,'Bold')
        for col in range(7):
            for k in range(5):a.circle(184+col*38,yy-12+k*13,3,stroke='#A49AA4',width=.7)
        a.text('1 → 5',60,yy+33,10)
    a.label('SUEÑO / HORAS',58,471,COLORS[8])
    for i,t in enumerate(['L','M','X','J','V','S','D']):
        yy=495+i*20;a.text(t,65,yy+4,10,'Bold');a.line(94,yy,433,yy)
        for j in range(9):a.line(94+j*42,yy-3,94+j*42,yy+3,'#B7ADB8')
    a.text('0',91,640,9);a.text('4',257,640,9);a.text('8+',424,640,9)
    a.label('AGUA',58,684,COLORS[7]);
    for i in range(8):a.icon('gota',58+i*22,701,21,'#6D91A7')
    a.label('MOVIMIENTO',263,684,COLORS[3]);a.icon('zapatilla',266,704,32);a.lines(306,729,132,1)
    a.label('MI PAUSA',58,788,COLORS[1]);a.icon('luna', sixty:=60,805,30);a.lines(106,830,331,1)

def selfcare(a):
    a.title('Volver a mí','UN MOMENTO DE AUTOCUIDADO',COLORS[1])
    a.circle(250,292,79,fill=COLORS[1],stroke=COLORS[1]);a.circle(250,292,57,stroke=PAPER,width=1)
    a.icon('corazon',220,259, sixty:=60)
    a.text('¿Qué necesito hoy?',250,417,25,'Editorial',center=True)
    a.lines(74,457,350,3,33)
    a.sticky(58,581,177,177,COLORS[4]);a.text('ME DOY PERMISO',72,617,11,'Bold');a.lines(73,651,147,3,30)
    a.text('Un gesto amable',262,608,18,'Editorial');a.check(263,632,175,4,32)
    a.label('ALGO QUE AGRADEZCO',58,809,COLORS[6]);a.lines(257,815,180,1)

def budget(a):
    a.title('Presupuesto mensual','MARZO 2026 / MONEDA: __________',COLORS[4])
    for i,label in enumerate(['INGRESOS','GASTOS','AHORRO']):
        x=58+i*130;a.box(x,205,122,86,COLORS[[5,1,4][i]],r=6);a.text(label,x+11,230,11,'Bold');a.line(x+12,270,x+110,270,'#9A9190')
    a.label('MI PRESUPUESTO',58,331,COLORS[4])
    for x,t in [(60,'CATEGORÍA'),(270,'PREVISTO'),(369,'REAL')]:a.text(t,x,366,10,'Bold')
    for r in range(7):
        yy=388+r*34
        if r%2==0:a.box(58,yy-17,384,33,'#F5F1E8',r=0)
        a.line(58,yy+16,442,yy+16)
    a.line(253,346,253,610);a.line(353,346,353,610)
    a.label('FACTURAS',58,655,COLORS[1]);a.check( sixty:=60,678,175,4,30)
    a.label('MI META DE AHORRO',259,655,COLORS[5]);a.icon('cartera',264,674,38)
    a.lines(310,704,126,1);a.bar(265,737,167,10,COLORS[5]);a.text('Meta / fecha',266,815,11);a.line(335,817,437,817)

def study(a):
    a.title('Plan de estudio','APRENDER CON INTENCIÓN',COLORS[7])
    a.label('MATERIA',58,216,COLORS[7]);a.line(147,220,438,220)
    a.text('Mi objetivo',60,262,19,'Editorial');a.lines(61,291,213,2,28)
    mini_calendar(a,2026,3,308,243,132,111)
    a.label('TEMAS',58,386,COLORS[0]);a.check(61,409,376,4,32)
    a.label('SESIONES / FECHAS',58,578,COLORS[7])
    a.line(86,622,410,622,'#A9C1D1',2)
    for i in range(4):
        x=86+i*108;a.circle(x,622,9,fill=COLORS[[7,0,5,3][i]],stroke=INK);a.text(f'0{i+1}',x,652,10,center=True);a.line(x-24,682,x+25,682)
    a.label('PROGRESO',58,733,COLORS[5]);a.bar(185,717,247,10)
    a.label('NOTAS',58,794,COLORS[4]);a.lines( sixty:=60,827,380,1)

def organization(a):
    a.title('Un lugar para cada cosa','MI ORGANIZACIÓN',COLORS[9])
    a.sticker('casa',367,195,65,COLORS[9])
    for i,(title,color) in enumerate([('HOY',4),('ESTA SEMANA',5),('CUANDO PUEDA',7)]):
        yy=225+i*182;a.label(title,58,yy,COLORS[color]);a.check(63,yy+23,374,4,29)
    a.tape( ninety:=95,770,83,COLORS[3]);a.text('Menos cosas. Más calma.',250,817,22,'Editorial',center=True)

def note_page(a):
    a.title('Ideas que merecen quedarse','NOTAS / FECHA: ______________',COLORS[7])
    a.icon('clip',382,187, forty:=40)
    for yy in range(226,832,19):
        for xx in range(65,436,19):a.circle(xx,yy,.6,fill='#CAC3BF',stroke='#CAC3BF',width=.2)
    a.label('UNA IDEA PARA RECORDAR',58,815,COLORS[4],224)

def extras(a):
    a.title('Pequeños extras','PAPELERÍA PARA HACERLO TUYO',COLORS[1])
    a.sticky(65,222,367,205,COLORS[4]);a.tape(184,211,92,COLORS[3])
    a.sticker('estrella',91,248,70,COLORS[0]);a.sticker('lapiz',187,272,76,COLORS[7]);a.sticker('agenda',295,241,80,COLORS[5])
    a.text('Tu papelería digital',248,399,24,'Editorial',center=True)
    a.chip('STICKERS FUNCIONALES','funcionales',70,475,360,COLORS[0],80)
    a.chip('STICKERS DE VIDA','stickers-vida',70,579,360,COLORS[3],80)
    a.chip('MI PÁGINA DE NOTAS','notas',70,683,360,COLORS[7],80)
    a.text('Ilustraciones originales para acompañar tus días.',250,814,12,center=True)

def sticker_label(a,label,x,y,w,h,color,shape=0):
    a.stickers+=1
    a.box(x+2,y+3,w,h,'#E2DAD4',r=14 if shape==0 else 3)
    a.box(x,y,w,h,'#FFFFFF',r=14 if shape==0 else 3)
    a.box(x+3,y+3,w-6,h-6,color,r=12 if shape==0 else 2)
    a.text(label,x+w/2,y+h/2+4,11 if len(label)>12 else 13,'Bold',center=True)

def functional_stickers(a):
    a.title('Stickers funcionales','PEQUEÑAS SEÑALES PARA TU DÍA',COLORS[0])
    labels=['HOY','IMPORTANTE','CITA','PAGO','ESTUDIO','DESCANSO','VIAJE','CUMPLEAÑOS','COMPRAS','ENTRENAMIENTO']
    for i,t in enumerate(labels):sticker_label(a,t,60+(i%2)*198,210+(i//2)* sixty if False else 210+(i//2)*63,184,49,COLORS[i],i%2)
    for i,name in enumerate(['check','flecha','reloj','estrella','lapiz','corazon']):a.sticker(name,62+i*64,550,55,COLORS[i])
    for i in range(10):sticker_label(a,str(i+1),60+(i%5)*77,640+(i//5)*61, sixty:=62,48,COLORS[i])
    for i,t in enumerate(['PRIORIDAD','HECHO','RECORDAR']):sticker_label(a,t,60+i*130,787,122,44,COLORS[i+4],1)

def life_stickers(a):
    a.title('Stickers de vida','PEQUEÑAS COSAS, GRANDES DÍAS',COLORS[3])
    icons=['libro','maleta','avion','casa','regalo','pastel','auriculares','zapatilla','botella','estrella','sol','luna','planta','comida','camara','corazon','sobre','agenda','hoja','taza']
    for i,name in enumerate(icons):
        x=62+(i%4)*96;y=215+(i//4)*123
        a.sticker(name,x,y, eighty:=78,COLORS[i%10])
        a.text({'avion':'AVIÓN','camara':'CÁMARA','corazon':'CORAZÓN','lapiz':'LÁPIZ'}.get(name,name.upper()),x+39,y+98,9,'Bold',center=True)

def closing(a):
    a.text('UNA PÁGINA A LA VEZ',250,147,12,'Bold',center=True)
    a.circle(250,348,133,fill=COLORS[3],stroke=COLORS[3]);a.circle(304,297,70,fill=COLORS[4],stroke=COLORS[4]);a.icon('planta',160,244,171)
    a.text('Tu tiempo,',250,557,39,'Editorial',center=True);a.text('tu ritmo.',250,608,39,'Editorial',center=True)
    a.text('Lo importante también crece despacio.',250,666,15,'Body',center=True)
    a.chip('VOLVER A MI AGENDA','inicio',89,747,322,COLORS[5],76)

def undated(a):
    a.title('Un nuevo comienzo','SIN FECHA / TU PROPIO RITMO',COLORS[9])
    a.text('MES: __________________',60,219,14,'Bold')
    for col,name in enumerate(['L','M','X','J','V','S','D']):a.text(name,58+(col+.5)*384/7,261,12,'Bold',center=True)
    for col in range(8):a.line(58+col*384/7,279,58+col*384/7,639)
    for row in range(7):a.line(58,279+row*60,442,279+row*60)
    a.label('MI INTENCIÓN',58,698,COLORS[3]);a.lines(60,732,380,2,30)
    a.label('ALGO QUE QUIERO RECORDAR',58,804,COLORS[5]);a.lines( sixty:=60,832,380,1)

def draw(a,p):
    key=p['id']
    if key=='portada':cover(a)
    elif key=='inicio':dashboard(a)
    elif key=='menu':menu(a)
    elif key.startswith('year-'):annual(a,int(key[-4:]))
    elif key in ('enero','febrero','calendario'):full_calendar(a,p['year'],p['month'])
    elif key in DIVIDERS:divider(a,key,p['title'])
    else:
        {'mes':month_divider,'plan-mes':month_plan,'semana':week,'dia':day,'smart':smart,'mi-vida':life,
         'plan-productividad':productivity,'tracker':wellbeing,'autocuidado':selfcare,'presupuesto':budget,
         'plan-estudio':study,'organizacion':organization,'notas':note_page,'extras':extras,
         'funcionales':functional_stickers,'stickers-vida':life_stickers,'cierre':closing,'sin-fecha':undated}[key](a)
