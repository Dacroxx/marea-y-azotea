import csv
import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('audit_media', ROOT/'tools/audit_media.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

class MediaAuditTests(unittest.TestCase):
    def test_folder_parser_retains_original_name_and_id(self):
        parser = module.FolderParser()
        parser.feed('<div class="flip-entry" id="entry-ABC"><a href="https://drive.google.com/file/d/ABC/view"><div class="flip-entry-title">Foto &amp; Mesa.JPG</div></a></div>')
        self.assertEqual(parser.entries, [{'id':'ABC','name':'Foto & Mesa.JPG','url':'https://drive.google.com/file/d/ABC/view'}])

    def test_current_page_references_match_only_verified_photos(self):
        refs = module.references((ROOT/'index.html').read_text(encoding='utf-8'))
        catalog = json.loads((ROOT/'audit/thematic-catalog.json').read_text(encoding='utf-8'))
        expected = [r for r in catalog if r['reviewStatus']=='verified' and r['mediaType']=='photo']
        self.assertEqual(len(refs), len(expected))
        self.assertEqual(refs, [{'id':r['sourceId'], 'name':r['originalName'], 'category':r['primaryCategory'], 'kind':'photo'} for r in expected])

    def test_historical_reference_snapshot_counts(self):
        # The snapshot describes the old three-chapter site, not today's selection.
        refs = json.loads((ROOT/'audit/page-references.json').read_text(encoding='utf-8'))
        self.assertEqual(len(refs), 50)
        self.assertEqual(len({r['id'] for r in refs}), 50)
        self.assertEqual(sum(r['kind']=='photo' for r in refs), 47)
        self.assertEqual(sum(r['kind']=='video' for r in refs), 3)
        self.assertEqual(sum(r['category']=='sensorial' for r in refs), 24)
        self.assertEqual(sum(r['category']=='agosto' for r in refs), 26)

    def test_legacy_reference_parser_remains_available(self):
        source = "const sensorialPhotos = [{id: 'A', name: 'A.HEIC'}]; const agostoPhotos = [{id: 'B', name: 'B.JPG'}]; const driveVideos = [{id: 'C', name: 'C.MOV', chapter: 'Taller Sensorial', localUrl: ''}];"
        self.assertEqual(module.references(source), [
            {'id':'A','name':'A.HEIC','category':'sensorial','kind':'photo'},
            {'id':'B','name':'B.JPG','category':'agosto','kind':'photo'},
            {'id':'C','name':'C.MOV','category':'sensorial','kind':'video'}])

    def test_snapshot_counts_are_consistent(self):
        summary = json.loads((ROOT/'audit/summary.json').read_text(encoding='utf-8'))
        inventory = json.loads((ROOT/'audit/inventory.json').read_text(encoding='utf-8'))
        media = [r for r in inventory if not r['isFolder']]
        self.assertEqual(len(media), summary['visibleMedia'])
        self.assertEqual(len({r['id'] for r in media}), len(media))
        self.assertEqual(sum(summary['mediaByFolder'].values()), len(media))
        self.assertEqual(sum(summary['mediaByCategory'].values()), len(media))
        self.assertEqual(sum(r['usedByPage'] for r in media), summary['pageReferences'])
        self.assertEqual(summary['missingPageIds'], [])
        self.assertTrue(all(r['pageNameMatches'] for r in media if r['usedByPage']))

    def test_csv_covers_every_visible_media_id(self):
        inventory = json.loads((ROOT/'audit/inventory.json').read_text(encoding='utf-8'))
        with (ROOT/'audit/media-catalog.csv').open(encoding='utf-8-sig',newline='') as stream:
            rows = list(csv.DictReader(stream))
        self.assertEqual({r['id'] for r in rows},{r['id'] for r in inventory if not r['isFolder']})
        self.assertEqual(len(rows),len({r['id'] for r in rows}))
        self.assertTrue(all(r['category']=='pending-review' for r in rows if r['categoryEvidence']=='none'))

if __name__ == '__main__':
    unittest.main()
