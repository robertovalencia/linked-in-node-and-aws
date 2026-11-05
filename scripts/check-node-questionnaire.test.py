"""Meaningful corruption regressions for portable teaching contracts; no cloud calls."""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
import importlib.util
import json
import shutil
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('node_checker',ROOT/'scripts/check-node-questionnaire.py')
checker=importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)


class CompanionContract(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(prefix='node-study-contract-')
        self.repo=Path(self.temp.name)
        self.pack=self.repo/'docs/nodejs-aws-study-path'
        shutil.copytree(checker.PACK,self.pack)
        for rel in ['README.md','docs/nodejs-beginner/README.md']:
            target=self.repo/rel;target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(ROOT/rel,target)
        self.data=json.loads((self.pack/'node-backend-questionnaire-map.json').read_text())
        for row in self.data['items']:
            rel=row['source']['path'];target=self.repo/rel
            target.parent.mkdir(parents=True,exist_ok=True)
            shutil.copy2(ROOT/rel,target)

    def tearDown(self):
        self.temp.cleanup()

    def save(self):
        (self.pack/'node-backend-questionnaire-map.json').write_text(json.dumps(self.data))

    def bad(self,pattern):
        with self.assertRaisesRegex(ValueError,pattern):checker.validate(self.pack,self.repo)

    def replace(self,rel,a,b):
        p=self.pack/rel;s=p.read_text();self.assertIn(a,s);p.write_text(s.replace(a,b,1))

    def test_actual_candidate(self):
        result=checker.validate(self.pack,self.repo,archive=True)
        self.assertEqual(result['questions'],137)
        self.assertEqual(result['incidents'],24)

    def test_missing_card(self):
        self.data['items'].pop();self.save();self.bad('IDs')

    def test_duplicate_id(self):
        self.data['items'][1]['id']=self.data['items'][0]['id'];self.save();self.bad('IDs')

    def test_input_map_drift(self):
        self.data['items'][0]['answer']='unreviewed answer';self.save();self.bad('input/map content mismatch')

    def test_current_source_required(self):
        (self.repo/self.data['items'][0]['source']['path']).unlink();self.bad('missing actual source')

    def test_stale_source_hash(self):
        p=self.repo/self.data['items'][0]['source']['path'];p.write_text(p.read_text()+'\n// drift\n');self.bad('stale source hash')

    def test_own_excerpt_required_even_if_other_card_matches(self):
        ident=self.data['items'][0]['id'].lower();p=self.pack/'evidence/node-backend-source-context.md';s=p.read_text()
        start=s.index(f'<a id="source-{ident}">');end=s.index('<a id="source-',start+1)
        p.write_text(s[:start]+s[start:end].replace(self.data['items'][0]['source']['excerpt'],'corrupt excerpt')+s[end:]);self.bad('own source context differs')

    def test_missing_rendered_answer(self):
        self.replace('node-backend-runtime.md',self.data['items'][0]['answer'],'removed');self.bad('rendered answer')

    def test_missing_rendered_priority(self):
        self.replace('node-backend-runtime.md','**Priority:** start now','**Priority:** later');self.bad('rendered priority')

    def test_missing_rendered_symbol(self):
        symbol=self.data['items'][0]['source']['symbol'];self.replace('node-backend-runtime.md',f'`{symbol}`','`wrong symbol`');self.bad('source not rendered')

    def test_missing_rendered_recovery(self):
        row=next(r for r in self.data['items'] if r['kind']=='incident');self.replace(f'node-backend-{row["section"]}.md',row['recovery'],'removed');self.bad('missing recovery')

    def test_missing_absent_example(self):
        row=next(r for r in self.data['items'] if r['scope']=='Absent implementation');self.replace(f'node-backend-{row["section"]}.md',row['worked_example'],'removed');self.bad('worked example not rendered')

    def test_bad_local_fragment(self):
        with (self.pack/'node-backend-runtime.md').open('a') as f:f.write('\n[broken](README.md#no-such-anchor)\n')
        self.bad('Broken local anchor')

    def test_pack_escape(self):
        with (self.pack/'node-backend-runtime.md').open('a') as f:f.write('\n[escape](../../README.md)\n')
        self.bad('escapes managed pack')

    def test_missing_lesson_link(self):
        lesson=self.data['items'][0]['lessons'][0];self.replace('node-backend-runtime.md',f']({lesson})','](README.md)');self.bad('missing lesson link')

    def test_missing_concept(self):
        p=self.pack/'node-backend-coverage.json';d=json.loads(p.read_text());d['concepts'].pop(0);p.write_text(json.dumps(d));self.bad('Incomplete concept mapping')

    def test_unknown_coverage_card(self):
        p=self.pack/'node-backend-coverage.json';d=json.loads(p.read_text());d['concepts'][0]['item_ids']=['NR99'];p.write_text(json.dumps(d));self.bad('Unmapped backend concept')

    def test_missing_supplement(self):
        p=self.pack/'node-backend-coverage.json';d=json.loads(p.read_text());d['supplementary_guides'].pop();p.write_text(json.dumps(d));self.bad('supplementary disposition')

    def test_protected_lesson_changed(self):
        p=next((self.pack/'generated').glob('01-*.md'));p.write_text(p.read_text()+'\nchanged\n');self.bad('Protected lesson changed')

    def test_navigation_missing(self):
        (self.repo/'README.md').write_text('missing nav');self.bad('Missing navigation')

    def test_archive_corrupt_bytes(self):
        archive=self.pack/'NodeJs-AWS-study-pack.zip'
        with ZipFile(archive) as z:rows=[(i,z.read(i)) for i in z.namelist()]
        with ZipFile(archive,'w',compression=ZIP_DEFLATED) as z:
            for name,content in rows:z.writestr(name,b'corrupt' if name.endswith('/node-backend-runtime.md') else content)
        with self.assertRaisesRegex(ValueError,'Archive byte mismatch'):checker.validate(self.pack,self.repo,archive=True)

    def test_archive_personal_canary(self):
        archive=self.pack/'NodeJs-AWS-study-pack.zip'
        with ZipFile(archive,'a') as z:z.writestr('NodeJs-AWS/personal/canary.md','private')
        with self.assertRaisesRegex(ValueError,'Private/cache'):checker.validate(self.pack,self.repo,archive=True)

    def test_archive_missing_lab(self):
        archive=self.pack/'NodeJs-AWS-study-pack.zip'
        with ZipFile(archive) as z:rows=[(n,z.read(n)) for n in z.namelist() if not n.endswith('labs/node-runtime/run.mjs')]
        with ZipFile(archive,'w') as z:
            for name,content in rows:z.writestr(name,content)
        with self.assertRaisesRegex(ValueError,'Missing Node companion'):checker.validate(self.pack,self.repo,archive=True)

    def test_private_lab_files_are_not_required_assets(self):
        for name in ('private.tfstate','private.tfplan','.env','.env.local'):
            (self.pack/'labs/node-runtime'/name).write_text('private canary')
        checker.validate(self.pack,self.repo,archive=True)

    def test_archive_environment_canary(self):
        with ZipFile(self.pack/'NodeJs-AWS-study-pack.zip','a') as z:
            z.writestr('NodeJs-AWS/labs/node-runtime/.env','private')
        with self.assertRaisesRegex(ValueError,'Environment archive entry'):checker.validate(self.pack,self.repo,archive=True)

    def test_wrong_rendered_index_count(self):
        self.replace('node-backend-questionnaire.md','137 questions and 24 incidents','999 questions and 24 incidents')
        self.bad('Wrong rendered question/incident counts')


if __name__=='__main__':unittest.main()
