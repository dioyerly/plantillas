import json
import unittest
from pathlib import Path

class PhaseSevenTests(unittest.TestCase):
    def test_cover_inventory(self):
        report=json.loads(Path('output/cover-validation.json').read_text(encoding='utf-8'))
        self.assertEqual(report['temas_definidos'],6)
        self.assertEqual(report['portadas_totales'],150)
        self.assertEqual(report['divisores'],29)
        self.assertEqual(report['enlaces_rotos'],0)
        self.assertEqual(len(list(Path('output/covers/planner').rglob('*.png'))),150)

    def test_family_previews_and_inventory(self):
        self.assertEqual(len(list(Path('output/cover-previews').glob('*.png'))),7)
        self.assertTrue(Path('docs/COVER-INVENTORY.csv').is_file())
        self.assertTrue(Path('docs/COVER-INVENTORY.md').is_file())
        self.assertTrue(Path('output/dividers/YOYIR-Divisores-ES.pdf').is_file())

if __name__ == '__main__':
    unittest.main()
