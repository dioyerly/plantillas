import unittest
from datetime import date
from src.planner.dates import calendar_data, validate_dates, week_dates
from src.planner.blueprint import dated_blueprint
from src.planner.manifest import master_pages
from src.notebooks import notebook_pages
from src.navigation import Navigation

class CalendarAndNavigationTests(unittest.TestCase):
    def test_complete_range_and_leap_day(self):
        data=calendar_data()
        self.assertEqual(validate_dates(data),1096)
        self.assertEqual(len(data['2028'][1]['days']),29)
        self.assertEqual(len(data['2027'][1]['days']),28)

    def test_weeks_cross_months_and_years(self):
        self.assertEqual(week_dates(date(2026,1,31))[-1],date(2026,2,1))
        self.assertEqual(week_dates(date(2027,1,1))[0],date(2026,12,28))
        self.assertEqual(week_dates(date(2028,1,1))[0],date(2027,12,27))

    def test_future_daily_navigation_at_year_boundary(self):
        plan=dated_blueprint(calendar_data())
        rows={r['id']:r for records in plan['years'].values() for r in records}
        self.assertEqual(rows['2026/day/2026-12-31']['next'],'2027/day/2027-01-01')
        day=rows['2027/day/2027-01-01']
        self.assertEqual(day['previous'],'2026/day/2026-12-31')
        self.assertEqual(day['week'],'2027/week/2026-12-28')
        self.assertEqual(day['month_tabs']['1'],'2027/01/monthly-dashboard')
        self.assertIsNone(rows['2028/day/2028-12-31']['next'])

    def test_phase_one_stays_bounded(self):
        pages=master_pages()
        self.assertEqual(len(pages),60)
        self.assertEqual(len({p['id'] for p in pages}),60)
        self.assertEqual(len(notebook_pages()),32)

    def test_navigation_rejects_missing_destinations_and_isolated_pages(self):
        nav=Navigation([{'id':'home'},{'id':'index'}])
        nav.links=[{'source':0,'target':'missing'}]
        with self.assertRaises(AssertionError): nav.check()
        nav.links=[]
        with self.assertRaises(AssertionError): nav.check()

if __name__=='__main__':
    unittest.main()
