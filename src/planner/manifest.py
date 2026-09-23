from ..config import MODULES
from ..themes import THEMES

SAMPLES = {
    'life': [('DREAM LIFE','vision'),('BOOK LOG','reading')],
    'wellness': [('WEEKLY CHECK-IN','wellbeing'),('MOVEMENT PLAN','movement')],
    'selfcare': [('DAILY GRATITUDE','gratitude'),('SELF-COMPASSION','reflection')],
    'productivity': [('PROJECT PLANNER','project'),('FOCUS SESSION','focus')],
    'money': [('MONTHLY BUDGET','budget'),('EXPENSE TRACKER','expenses')],
    'notes': [('BLANK','blank'),('GRID','grid')],
}

def master_pages(theme='lavender'):
    pages=[]
    def add(id,title,kind,**kwargs):
        pages.append(dict(id=id,title=title,kind=kind,theme=theme,**kwargs))
    add('home',"YOYI'R DIGITAL PLANNER",'cover')
    add('welcome','Welcome to your space','welcome')
    add('quick','A calm beginning','quick')
    add('index','Your planner, connected','index')
    add('years','Choose your year','years')
    for year in (2026,2027,2028):
        add(f'year-{year}',f'{year} / Year overview','year',year=year)
    add('undated','An open beginning','undated')
    for id,title,kind in [('month','January 2026','month'),('calendar','Monthly calendar','calendar'),('month-goals','Focus & priorities','month_goals'),('month-habits','Small things, often','month_habits'),('month-money','Money, with intention','month_money'),('month-reflection','January / Looking back','month_reflection')]:
        add(id,title,kind,year=2026,month=1)
    add('week','A week with intention','week',year=2026,month=1)
    add('week-life','The rest of the week','week_life',year=2026,month=1)
    add('day','Saturday, January 31','day',year=2026,month=1)
    add('day-life','A little room for you','day_life',year=2026,month=1)
    add('goals','From intention to action','goals')
    for key,(title,_) in MODULES.items():
        add(key,title,'module',module=key)
    for key,samples in SAMPLES.items():
        for i,(title,template) in enumerate(samples):
            add(f'{key}-{i+1}',title,'template',module=key,template=template)
    for key,t in THEMES.items():
        add('theme-'+key,t.name,'theme')
        pages[-1]['theme']=key
    for i in range(12):
        add(f'cover-{i+1:02d}',f'Cover {i+1:02d}','cover_sample',variant=i)
        pages[-1]['theme']=list(THEMES)[i%6]
    for key,title in [('lined','Lined notes'),('dot','Dot grid notes'),('cornell','Cornell notes')]:
        add(key,title,'note',template=key)
    add('stickers','Little markers, clear meaning','stickers')
    assert len(pages)==60
    return pages
