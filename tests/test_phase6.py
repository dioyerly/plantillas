import json
import unittest
from pathlib import Path

class PhaseSixTests(unittest.TestCase):
    def test_sticker_library_report(self):
        report_path=Path('output/sticker-validation.json')
        self.assertTrue(report_path.is_file())
        report=json.loads(report_path.read_text(encoding='utf-8'))
        self.assertGreaterEqual(report['total_png'],1600)
        self.assertEqual(report['png_error'],0)
        self.assertEqual(report['duplicados_exactos'],0)
        self.assertEqual(report['enlaces_rotos'],0)
        self.assertEqual(report['categorias'],25)

    def test_sticker_book_exists(self):
        self.assertTrue(Path('output/YOYIR-Libro-de-Stickers-ES.pdf').is_file())
        self.assertTrue(Path('docs/STICKER-INVENTORY.csv').is_file())
        self.assertTrue(Path('docs/STICKER-INVENTORY.md').is_file())

if __name__ == '__main__':
    unittest.main()
