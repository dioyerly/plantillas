"""python -m src.premium.master_builder — builds the unified MASTER PDF with dated core 2026–2028."""
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
from .pages import full_calendar,month_divider,month_plan,week
from .dated import premium_day,WEEKDAYS,MONTH_KICKERS,BlockArt

def day_id(d):return f'day-{d:%Y-%m-%d}'
def week_id(d):return f'week-{d-timedelta(days=d.weekday()):%Y-%m-%d}'
def cal_id(year,month):return f'cal-{year}-{month:02d}'

def year_block(year):
    """Generate all months and days for a single year."""
    pages=[]
    all_week_ids=set()
    for month in range(1,13):
        first=date(year,month,1);last=date(year,month,calendar.monthrange(year,month)[1])
        days_list=[first+timedelta(days=i) for i in range(last.day)]
        days_set=set(days_list)
        # Get all mondays that have at least one day in this month
        week_starts=sorted({d-timedelta(days=d.weekday()) for d in days_list})
        cal=cal_id(year,month);div=f'div-{year}-{month:02d}';plan=f'plan-{year}-{month:02d}'
        pages.append(dict(id=div,kind='divider',year=year,month=month,active_tab='MES'))
        pages.append(dict(id=cal,kind='calendar',year=year,month=month,active_tab='MES'))
        pages.append(dict(id=plan,kind='plan',year=year,month=month,active_tab='MES'))
        for monday in week_starts:
            week_key=week_id(monday)
            if week_key not in all_week_ids:
                pages.append(dict(id=week_key,kind='week',year=year,start=monday,active_tab='SEM'))
                all_week_ids.add(week_key)
            for i in range(7):
                d=monday+timedelta(days=i)
                if d in days_set:pages.append(dict(id=day_id(d),kind='day',year=year,month=month,date=d,active_tab='DÍA'))
    return pages,all_week_ids

def dated_core_block(years=(2026,2027,2028)):
    """Generate all pages for dated core 2026–2028."""
    all_pages=[];all_weeks=set()
    for year in years:
        year_pages,weeks=year_block(year)
        all_pages+=year_pages
        all_weeks.update(weeks)
    known={p['id'] for p in all_pages}
    for i,p in enumerate(all_pages):
        p['previous']=all_pages[i-1]['id'] if i>0 else 'inicio'
        p['next']=all_pages[i+1]['id'] if i+1<len(all_pages) else 'menu'
        year=p['year']
        month=p.get('month',p['start'].month if p['kind']=='week' else 1)
        cal=cal_id(year,month)
        if p['kind']=='week':
            anchor=p['start']
            p['tab_targets']=['inicio',f'year-{year}',cal,week_id(anchor),day_id(anchor)]
        else:
            anchor=p.get('date',date(year,month,1))
            p['tab_targets']=['inicio',f'year-{year}',cal,week_id(anchor),p['id'] if p['kind']=='day' else day_id(anchor)]
        p['month_targets']=[cal_id(year,m) for m in range(1,13)]
        p['months']=True
    return all_pages,known

def draw_block_page(a,p):
    if p['kind']=='divider':month_divider(a,p['year'],p['month'],MONTH_KICKERS[p['month']],cal_id(p['year'],p['month']))
    elif p['kind']=='calendar':
        n=calendar.monthrange(p['year'],p['month'])[1]
        full_calendar(a,p['year'],p['month'],{d:day_id(date(p['year'],p['month'],d)) for d in range(1,n+1)})
    elif p['kind']=='plan':month_plan(a,p['year'],p['month'])
    elif p['kind']=='week':week(a,p['start'],day_id)
    else:premium_day(a,p['date'])

def build_candidate(name='YOYIR-DIGITAL-PLANNER-MASTER.pdf'):
    """Build candidate MASTER PDF without replacing existing."""
    out=OUTPUT/'.build';out.mkdir(parents=True,exist_ok=True);pdf=out/name
    register_fonts();pages,known=dated_core_block();nav=[];future=[];arts=[]
    c=canvas.Canvas(str(pdf),pagesize=(W,H),pageCompression=1,pdfVersion=(1,4),invariant=1)
    c.setTitle("YOYI'R · Digital Planner 2026–2028");c.setAuthor("E-books para la vida — YOYI'R")
    for i,p in enumerate(pages):
        c.bookmarkPage(p['id'],fit='Fit')
        a=BlockArt(c,p['id'],nav,known)
        digital_planner_shell(a,p,i,len(pages));draw_block_page(a,p)
        future+=a.future;arts.append(a);c.showPage()
    c.save()
    return pdf,pages,nav,future,arts

def validate_candidate(pdf,pages,nav,future,arts):
    """Comprehensive validation of candidate before promoting to MASTER."""
    from pypdf import PdfReader
    reader=PdfReader(pdf,strict=True);doc=fitz.open(pdf);index={p['id']:i for i,p in enumerate(pages)}
    r=dict(file=pdf.name,total_pages=len(doc),page_size=None,
           month_dividers=0,month_calendars=0,month_intention_pages=0,week_pages=0,daily_pages=0,
           complete_daily_pages=0,incomplete_daily_pages=0,
           dates_expected=365+365+366,dates_found=0,date_errors=0,
           internal_links=len(nav),broken_internal_links=0,duplicate_links=0,
           future_destinations=len({f['target'] for f in future}),
           blank_pages=0,clipping=0,overflow=0,english_visible_strings=0,
           feb_29_2028=False,days_without_week=0,
           problems=[])
    sizes={(round(p.rect.width),round(p.rect.height)) for p in doc};r['page_size']=sorted(sizes)
    if sizes!={(W,H)}:r['problems'].append(('page_size',sizes))
    week_ids={p['id']:p for p in pages if p['kind']=='week'};covered=set()
    for i,(p,info) in enumerate(zip(doc,pages)):
        text=p.get_text();kind=info['kind']
        r[{'divider':'month_dividers','calendar':'month_calendars','plan':'month_intention_pages','week':'week_pages','day':'daily_pages'}[kind]]+=1
        pix=p.get_pixmap(matrix=fitz.Matrix(.3,.3),alpha=False)
        if len(text.strip())<25 or len(set(pix.samples))<8:r['blank_pages']+=1;r['problems'].append(('blank_page',i+1))
        for b in p.get_text('dict')['blocks']:
            for ln in b.get('lines',[]):
                for s in ln['spans']:
                    if not p.rect.contains(fitz.Rect(s['bbox'])):r['overflow']+=1
        for dr in p.get_drawings():
            if not p.rect.contains(dr['rect']):r['clipping']+=1
        if 'JANUARY' in text.upper() or 'FEBRUARY' in text.upper() or 'DECEMBER' in text.upper():r['english_visible_strings']+=1
        if kind=='day':
            d=info['date'];missing=[t for t in ['ENFOQUE','HORARIO','TOP 3','POR HACER','COMIDAS','AGUA','MOVIMIENTO','ÁNIMO','GRATITUD','PARA MAÑANA'] if t not in text]
            missing+=[f'{h:02d}' for h in range(7,21) if not __import__('re').search(rf'(?m)^{h:02d}$',text)]
            if missing:r['incomplete_daily_pages']+=1
            else:r['complete_daily_pages']+=1
            if d==date(2028,2,29):r['feb_29_2028']=True
            if all(__import__('re').search(rf'(?m)^{re.escape(h)}$',text) for h in [WEEKDAYS[d.weekday()],f'{d.day:02d}',FULL_MONTHS[d.month-1],str(d.year)]):r['dates_found']+=1
            else:r['date_errors']+=1
            week_start=d-timedelta(days=d.weekday())
            week_key=week_id(week_start)
            if week_key in week_ids:covered.add(d)
        if kind=='week':
            missing=[t for t in ['Mi semana','FOCO SEMANAL','LUNES','MARTES','MIÉRCOLES','JUEVES','VIERNES'] if t not in text]
            if missing:r['problems'].append(('incomplete_week',i+1,missing))
        links=[e for e in nav if e['source']==info['id']];annots=reader.pages[i].get('/Annots',[])
        rects=[]
        for e,ref in zip(links,annots):
            if e['target'] in index:
                dest=ref.get_object().get('/Dest')
                if not dest or dest[0].idnum!=reader.pages[index[e['target']]].indirect_reference.idnum:
                    r['broken_internal_links']+=1;r['problems'].append(('broken_link',i+1,e['label']))
            box=fitz.Rect(*e['rect'])
            if any(box.intersects(o) for o in rects):r['duplicate_links']+=1;r['problems'].append(('overlapping_link',i+1))
            rects.append(box)
    for y in (2026,2027,2028):
        for m in range(1,13):
            n=calendar.monthrange(y,m)[1]
            for d in range(1,n+1):
                dt=date(y,m,d)
                if dt not in covered:r['days_without_week']+=1;r['problems'].append(('day_without_week',dt))
    reachable={pages[0]['id']}
    while True:
        grown=reachable|{e['target'] for e in nav if e['source'] in reachable}
        if grown==reachable:break
        reachable=grown
    r['unreachable_pages']=[p['id'] for p in pages if p['id'] not in reachable]
    for xref in range(1,doc.xref_length()):
        if any(t in doc.xref_object(xref) for t in ('/JavaScript','/URI','/GoToR','/Launch')):r['problems'].append(('unsafe',xref))
    return r,doc

if __name__=='__main__':
    candidate,pages,nav,future,arts=build_candidate()
    r,doc=validate_candidate(candidate,pages,nav,future,arts)
    doc.close()
    print(json.dumps({k:r[k] for k in ['total_pages','complete_daily_pages','month_dividers','month_calendars','week_pages',
                                         'broken_internal_links','duplicate_links','date_errors','days_without_week','feb_29_2028','blank_pages','clipping','overflow','english_visible_strings']},indent=1))
    master=OUTPUT/'YOYIR-DIGITAL-PLANNER-MASTER.pdf'
    dated_core_valid=(r['date_errors']==0 and r['days_without_week']==0 and
        r['blank_pages']==0 and r['overflow']==0 and r['clipping']==0 and r['english_visible_strings']==0 and
        r['feb_29_2028'] and r['complete_daily_pages']==1096 and r['duplicate_links']==0)
    print(f'\nDated core valid: {dated_core_valid}', flush=True)
    if dated_core_valid:
        OUTPUT.mkdir(parents=True,exist_ok=True)
        if master.exists():
            backup=OUTPUT/'.build'/'MASTER-PREVIOUS.pdf'
            OUTPUT.joinpath('.build').mkdir(parents=True,exist_ok=True)
            if backup.exists():backup.unlink()
            master.replace(backup)
        candidate.replace(master)
        print('[OK] MASTER promoted', flush=True)
    else:
        print('[FAIL] Candidate rejected', flush=True)
        for p in r['problems'][:20]:print(f'  {p}')
