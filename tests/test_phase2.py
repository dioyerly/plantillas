import unittest
from datetime import date
from src.phase2 import phase2_pages, did, mid, wid, WEEK_STARTS

class PhaseTwoTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pages = phase2_pages()
        cls.ids = {p['id'] for p in cls.pages}

    def test_complete_page_inventory(self):
        self.assertEqual(len(self.pages), 1379)
        self.assertEqual(sum(1 for p in self.pages if p['kind'] == 'month'), 36)
        self.assertEqual(sum(1 for p in self.pages if p['kind'] == 'day'), 1096)
        self.assertEqual(sum(1 for p in self.pages if p['kind'] == 'week'), 157)
        self.assertEqual(len(self.ids), len(self.pages))

    def test_date_boundaries_and_leap_day(self):
        self.assertIn(did(date(2026, 1, 1)), self.ids)
        self.assertIn(did(date(2026, 12, 31)), self.ids)
        self.assertIn(did(date(2027, 1, 1)), self.ids)
        self.assertIn(did(date(2027, 12, 31)), self.ids)
        self.assertIn(did(date(2028, 1, 1)), self.ids)
        self.assertIn(did(date(2028, 2, 29)), self.ids)
        self.assertIn(did(date(2028, 12, 31)), self.ids)
        self.assertIn(mid(2027, 3), self.ids)
        self.assertIn(wid(date(2026, 12, 28)), self.ids)

    def test_spanish_visible_inventory(self):
        titles = ' '.join(p['title'] for p in self.pages)
        for word in ('ENERO', 'FEBRERO', 'MIÉRCOLES', 'PLANIFICADOR', 'SIN FECHA'):
            self.assertIn(word, titles)
        for word in ('JANUARY', 'MONDAY', 'HOME', 'WEEKLY PLANNER'):
            self.assertNotIn(word, titles)

if __name__ == '__main__':
    unittest.main()
