"""Portable offline build and editorial-source provenance contracts."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import unittest
ROOT=Path(__file__).resolve().parents[1]

class EditorialBuildTests(unittest.TestCase):
    def test_source_attachment_exact_bytes(self):
        self.assertEqual(hashlib.sha256((ROOT/'source/editorial-template.html').read_bytes()).hexdigest(),'7bd51e2854517647430d5d64a197a49d230a8298027c76c9a2daf6c4dfaa3c15')

    def test_committed_css_build_checksum(self):
        record=json.loads((ROOT/'source/css-build.json').read_text(encoding='utf8'))
        self.assertEqual(hashlib.sha256((ROOT/'source/tailwind.generated.css').read_bytes()).hexdigest(),record['cssSha256'])

    def test_offline_rebuild_identical_and_catalog_untouched(self):
        paths=[ROOT/'index.html',ROOT/'audit/thematic-catalog.json',ROOT/'audit/thematic-catalog.csv']
        before={p:hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
        subprocess.run([sys.executable,str(ROOT/'tools/build_magazine.py')],check=True,capture_output=True)
        self.assertEqual(before,{p:hashlib.sha256(p.read_bytes()).hexdigest() for p in paths})

    def test_no_external_runtime_or_obsolete_media_counts(self):
        html=(ROOT/'index.html').read_text(encoding='utf8')
        self.assertNotIn('<script src=',html)
        self.assertNotIn('cdn.tailwindcss.com',html)
        self.assertNotIn('href="assets/',html)
        self.assertNotRegex(html,r'[1-9]\d* registros audiovisuales')
        self.assertIn('0 videos publicados · 29 en carpeta de revisión',html)
        self.assertNotIn('1 / 78',html)
        self.assertIn('1 / 39',html)

if __name__=='__main__': unittest.main()
