from .art import COLORS,PAPER,INK,W,H

MONTHS=['ENE','FEB','MAR','ABR','MAY','JUN','JUL','AGO','SEP','OCT','NOV','DIC']
FULL_MONTHS=['ENERO','FEBRERO','MARZO','ABRIL','MAYO','JUNIO','JULIO','AGOSTO','SEPTIEMBRE','OCTUBRE','NOVIEMBRE','DICIEMBRE']

def month_target(year,month):
    if (year,month)==(2026,1):return 'enero'
    if (year,month)==(2028,2):return 'febrero'
    if (year,month)==(2026,3):return 'mes'
    return f'm-{year}-{month:02d}'

def digital_planner_shell(a,p,index,total):
    a.box(0,0,W,H,'#ECE8EF',r=0)
    # Three restrained layers create the notebook edge, not a heavy 3D shadow.
    a.box(33,79,439,864,'#DCD6DD',r=17)
    a.box(29,72,437,866,'#E9E3DE',r=15)
    a.box(25,65,435,867,PAPER,r=13)
    a.box(25,66,22,865,'#F0EBE6',r=12)
    a.line(46,82,46,914,'#DAD1C9',.8)
    for yy in range(117,866,94):
        a.circle(35,yy,3,fill='#D1C8C4',stroke='#D1C8C4')
        a.line(19,yy-2,36,yy-2,'#BBB2B0',2)
        a.line(19,yy,36,yy,'#FFFFFF',1)
    year=p.get('year',2026);month=p.get('month',3)
    targets=p.get('tab_targets',['inicio',f'year-{year}',month_target(year,month),'semana','dia'])
    tabs=list(zip(['INICIO','AÑO','MES','SEM','DÍA'],targets))
    active_tab=p.get('active_tab')
    for i,(label,target) in enumerate(tabs):
        active=label==active_tab if active_tab else p['id']==target
        a.tab(label,target,48+i*86,19 if active else 25,80,69 if active else 64,COLORS[[0,7,3,5,1][i]],active)
    if p.get('months'):
        for i,label in enumerate(MONTHS):
            active=i+1==p.get('month')
            target=p['month_targets'][i] if 'month_targets' in p else month_target(year,i+1)
            a.tab(label,target,456 if active else 460,96+i*68,72 if active else 68,64,COLORS[i%10],active)
    else:
        for i,(label,target,color) in enumerate([('METAS','objetivos',0),('VIDA','vida',3),('BIENESTAR','bienestar',5),('FINANZAS','finanzas',4),('NOTAS','notas',7),('EXTRAS','extras',1)]):
            a.tab(label,target,460,160+i*112,68,92,COLORS[color],p['id']==target)
    a.chip('MENÚ','menu',58,862,112,COLORS[0])
    a.chip('ANTERIOR',p.get('previous','inicio'),184,862,122,'#E9E5DD')
    a.chip('SIGUIENTE',p.get('next','inicio'),320,862,122,COLORS[6])
    a.text("YOYI'R",60,948,9,'Bold','#78707A')
    a.text(f'{index+1:02d} / {total:02d}',431,948,9,center=True)
