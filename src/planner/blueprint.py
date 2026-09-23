"""Full future publishing plan as data only; never renders Phase 2 PDFs."""
from datetime import date, timedelta
from ..config import YEARS, ANNUAL_TEMPLATES, MONTHLY_TEMPLATES
from .dates import week_dates

def slug(value):
    return value.lower().replace(' / ','-').replace(' ','-')

def dated_blueprint(data):
    result={}
    for year in YEARS:
        records=[]
        overview=f'{year}/year-overview'
        month_targets={str(m):f'{year}/{m:02d}/monthly-dashboard' for m in range(1,13)}
        for name in ANNUAL_TEMPLATES:
            records.append({'id':f'{year}/{slug(name)}','template':slug(name),'year':year,'month_tabs':month_targets})
        for month in data[str(year)]:
            m=month['month']
            for name in MONTHLY_TEMPLATES:
                records.append({'id':f'{year}/{m:02d}/{slug(name)}','template':slug(name),
                                'year':year,'month':m,'up':overview,'month_tabs':month_targets})
        days=[day for month in data[str(year)] for day in month['days']]
        starts=sorted({d['week_start'] for d in days})
        for start in starts:
            dates=week_dates(date.fromisoformat(start))
            # A boundary week can exist in two year contexts; tabs always follow the selected year.
            records.append({'id':f'{year}/week/{start}','template':'weekly-planner','year':year,
                            'dates':[d.isoformat() for d in dates],'month_tabs':month_targets,
                            'days':[f'{d.year}/day/{d.isoformat()}' if d.year in YEARS else None for d in dates]})
        for day in days:
            d=date.fromisoformat(day['date'])
            records.append({'id':f'{year}/day/{d.isoformat()}','template':'daily-planner','year':year,
                            'date':d.isoformat(),'weekday':day['weekday'],
                            'week':f'{year}/week/{day["week_start"]}','month':month_targets[str(d.month)],
                            'previous':f'{(d-timedelta(days=1)).year}/day/{day["previous"]}' if (d-timedelta(days=1)).year in YEARS else None,
                            'next':f'{(d+timedelta(days=1)).year}/day/{day["next"]}' if (d+timedelta(days=1)).year in YEARS else None,
                            'month_tabs':month_targets})
        result[str(year)]=records
    ids={r['id'] for records in result.values() for r in records}
    for records in result.values():
        for r in records:
            for target in r.get('month_tabs',{}).values():
                assert target in ids and target.startswith(str(r['year'])+'/')
            if r['template']=='daily-planner':
                for key in ('week','month','previous','next'):
                    assert r[key] is None or r[key] in ids
    return {'status':'architecture-only; not rendered in Phase 1','years':result,
            'undated':{'annual_templates':ANNUAL_TEMPLATES,'monthly_templates':MONTHLY_TEMPLATES,
                       'weekly_templates':['weekly-planner','weekly-companion'],
                       'daily_templates':['daily-planner','daily-companion'],
                       'date_fields':'blank; filled by the user; no dynamic retargeting'}}
