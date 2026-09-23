import calendar
from datetime import date, timedelta
from ..config import YEARS

def month_weeks(year, month):
    return calendar.Calendar(firstweekday=0).monthdayscalendar(year, month)

def week_dates(day):
    start = day - timedelta(days=day.weekday())
    return [start + timedelta(days=n) for n in range(7)]

def calendar_data():
    result = {}
    for year in YEARS:
        months = []
        for month in range(1, 13):
            days = []
            for number in range(1, calendar.monthrange(year, month)[1]+1):
                value = date(year, month, number)
                week = week_dates(value)
                days.append({'date': value.isoformat(), 'weekday': value.weekday(),
                             'week_start': week[0].isoformat(), 'week_end': week[-1].isoformat(),
                             'previous': (value-timedelta(days=1)).isoformat(),
                             'next': (value+timedelta(days=1)).isoformat()})
            months.append({'month': month, 'weeks': month_weeks(year, month), 'days': days})
        result[str(year)] = months
    return result

def validate_dates(data):
    count = 0
    for year, months in data.items():
        flattened = []
        for month in months:
            values = [n for week in month['weeks'] for n in week if n]
            assert values == list(range(1, len(month['days'])+1))
            for row, week in enumerate(month['weeks']):
                for col, number in enumerate(week):
                    if number:
                        d = date(int(year), month['month'], number)
                        # Independent weekday check using ordinal arithmetic.
                        assert (d.toordinal()-1) % 7 == col
            for entry in month['days']:
                d = date.fromisoformat(entry['date'])
                assert d.weekday() == entry['weekday']
                assert date.fromisoformat(entry['next'])-d == timedelta(days=1)
                assert d-date.fromisoformat(entry['previous']) == timedelta(days=1)
                assert date.fromisoformat(entry['week_start']).weekday() == 0
                assert date.fromisoformat(entry['week_end']).weekday() == 6
                assert date.fromisoformat(entry['week_start']) <= d <= date.fromisoformat(entry['week_end'])
                flattened.append(d)
        assert len(flattened) == (366 if calendar.isleap(int(year)) else 365)
        assert flattened[0] == date(int(year),1,1) and flattened[-1] == date(int(year),12,31)
        count += len(flattened)
    assert date(2026,1,1).weekday()==3
    assert date(2027,1,1).weekday()==4
    assert date(2028,2,29).weekday()==1
    assert week_dates(date(2027,1,1))[0]==date(2026,12,28)
    assert week_dates(date(2028,1,1))[0]==date(2027,12,27)
    return count
