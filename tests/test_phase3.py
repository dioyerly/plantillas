import unittest
from src.phase3 import library_pages, MODULES, tid

class PhaseThreeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pages = library_pages()
        cls.ids = {p['id'] for p in cls.pages}

    def test_library_inventory_and_unique_destinations(self):
        expected = sum(len(v[1]) for v in MODULES.values())
        actual = sum(1 for p in self.pages if p['kind'] == 'template')
        self.assertEqual(actual, expected)
        self.assertEqual(len(self.ids), len(self.pages))
        self.assertIn(tid('objetivos','META SMART'), self.ids)
        self.assertIn(tid('bienestar','RECETAS'), self.ids)

    def test_spanish_replaces_internal_term(self):
        titles = ' '.join(p['title'] for p in self.pages)
        self.assertIn('DEPURACIÓN DEL HOGAR', titles)
        self.assertNotIn('DECLUTTER', titles)
        self.assertNotIn('SMART GOAL', titles)

if __name__ == '__main__':
    unittest.main()
