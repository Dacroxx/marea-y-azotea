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
        self.assertIn('id="videos-eje"',html)
        self.assertIn('id="referencias"',html)
        self.assertIn('Crónica Estudiantes Cocina del Pacífico 2026-2',html)
        self.assertIn('Estudiantes de Cocinas del Pacífico 2026-2',html)
        self.assertIn('Aida Arteaga y David González',html)
        self.assertNotIn('id="editorial-scope"',html)
        self.assertNotIn('1 / 78',html)
        self.assertIn('1 / 42',html)

    def test_compiled_css_utilities_and_editorial_regressions(self):
        html=(ROOT/'index.html').read_text(encoding='utf8')
        all_css=(ROOT/'source/tailwind.generated.css').read_text(encoding='utf8')+'\n'+(ROOT/'source/standalone.css').read_text(encoding='utf8')
        critical_classes=[
            'opacity-0',
            'group-focus-within:opacity-100',
            'lg:grid-cols-2',
            'space-y-3.5',
            'w-10',
            'h-10',
            'group-hover:bg-marea',
            'col-span-full',
            'py-12',
            'sm:p-5',
            'sm:py-24',
            'mt-1.5',
            'mr-2',
            'opacity-85',
            'pt-12',
            'via-carbon/60',
            'leading-[1.06]',
            'leading-[1.08]',
        ]
        for cls in critical_classes:
            esc=''.join('\\'+c if c in ':/[].%' else c for c in cls)
            self.assertIn('.'+esc,all_css,f'Missing compiled CSS rule for {cls}')
        forbidden_strings=[
            'Quién conoce lo ancestral',
            'sueltura',
            'chirarán, poleo y albahaca negra',
            'enlace a Drive',
            'Crónica V',
            'nextLightbox',
            'class="hidden" class=',
        ]
        for bad in forbidden_strings:
            self.assertNotIn(bad,html,f'Editorial or runtime regression found: {bad}')

if __name__=='__main__': unittest.main()
