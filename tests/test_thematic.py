import importlib.util
import json
from pathlib import Path
import unittest
from copy import deepcopy
import hashlib
import contextlib
import io

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('thematic',ROOT/'tools/thematic_media.py')
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

class ThematicTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows=json.loads((ROOT/'audit/thematic-catalog.json').read_text(encoding='utf-8'))
    def test_full_contract_and_csv_json_parity(self):
        m.validate()
    def test_media_totals(self):
        self.assertEqual(sum(r['mediaType']=='photo' for r in self.rows),181)
        self.assertEqual(sum(r['mediaType']=='video' for r in self.rows),31)
    def test_offline_rebuild_is_byte_identical(self):
        paths=[ROOT/'audit'/name for name in ['thematic-catalog.json','thematic-catalog.csv','thematic-summary.json','thematic-observations.json','THEMATIC-REPORT.md']]
        before={p:hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
        with contextlib.redirect_stdout(io.StringIO()): m.build()
        self.assertEqual(before,{p:hashlib.sha256(p.read_bytes()).hexdigest() for p in paths})
    def test_no_video_claims(self):
        for r in self.rows:
            if r['mediaType']=='video':
                self.assertIsNone(r['primaryCategory'])
                self.assertEqual(r['reviewStatus'],'uninspected-video')
                self.assertIn('MOV no reproducido',r['visualDescription'])
    def test_traceability_and_observation_coverage(self):
        observations=json.loads((ROOT/'audit/thematic-observations.json').read_text(encoding='utf-8'))
        self.assertEqual({o['number'] for o in observations},set(range(1,213)))
        for r in self.rows:
            self.assertEqual(len(r['evidence']['thumbnailSha256']),64)
            self.assertEqual(r['evidence']['sheet'],f"sheet-{(r['evidence']['number']-1)//16+1:02}.jpg")
            self.assertEqual(r['evidence']['cell'],(r['evidence']['number']-1)%16+1)
    def test_independent_review_six_corrections(self):
        by_number={r['evidence']['number']:r for r in self.rows}
        expected={4:'mezcla-amarilla-fragmentos-sarten',26:'tallos-hojas-sobre-piedra',158:'tallos-hojas-sobre-piedra',71:'molino-metalico-granos-claros'}
        for number,label in expected.items():
            self.assertTrue(by_number[number]['proposedFilename'].startswith(label+'--'))
        for number in [26,158]:
            self.assertIn('Tallos y hojas verdes sobre piedra',by_number[number]['visualDescription'])
            self.assertNotIn('vainas',by_number[number]['visualDescription'])
            self.assertEqual(by_number[number]['reviewStatus'],'provisional')
        for number in [57,125]:
            self.assertIn('Mortero metálico con pasta clara',by_number[number]['visualDescription'])
            self.assertEqual(by_number[number]['reviewStatus'],'verified')
        self.assertEqual(by_number[71]['primaryCategory'],m.CATEGORIES[0])
        self.assertEqual(by_number[71]['reviewStatus'],'provisional')
        self.assertIn('ingrediente por confirmar',by_number[71]['visualDescription'])
        self.assertEqual(by_number[4]['reviewStatus'],'provisional')

    def test_no_forced_completion(self):
        self.assertTrue(any(r['mediaType']=='photo' and r['primaryCategory'] is None for r in self.rows))
        self.assertTrue(any(r['reviewStatus']=='provisional' for r in self.rows))
    def test_unknown_category_rejected(self):
        rows=deepcopy(self.rows)
        rows[0]['primaryCategory']='pending-review'
        with self.assertRaises(AssertionError): m.validate(rows)
    def test_tampered_evidence_rejected(self):
        rows=deepcopy(self.rows)
        rows[0]['evidence']['cell']=16
        with self.assertRaises(AssertionError): m.validate(rows)
    def test_missing_id_rejected(self):
        with self.assertRaises(AssertionError): m.validate(self.rows[:-1])
    def test_original_extension_preserved(self):
        rows=deepcopy(self.rows)
        rows[0]['proposedFilename']+='jpeg'
        with self.assertRaises(AssertionError): m.validate(rows)

if __name__=='__main__': unittest.main()
