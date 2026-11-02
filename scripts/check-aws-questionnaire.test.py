"""Offline regression checks for broken questionnaire evidence and archive inclusion/exclusion."""
from pathlib import Path
from tempfile import TemporaryDirectory
from zipfile import ZipFile
import argparse
import importlib.util
import json
import shutil
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--repository', type=Path, default=ROOT)
args, remaining = parser.parse_known_args()
REPOSITORY = args.repository
spec = importlib.util.spec_from_file_location('questionnaire_check', ROOT / 'scripts/check-aws-questionnaire.py')
check = importlib.util.module_from_spec(spec)
spec.loader.exec_module(check)


class QuestionnaireEvidenceTests(unittest.TestCase):
    def setUp(self):
        self.temp = TemporaryDirectory(prefix='questionnaire-regression-')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.pack = self.root / 'docs/nodejs-aws-study-path'
        shutil.copytree(ROOT / 'docs/nodejs-aws-study-path', self.pack, ignore=shutil.ignore_patterns('*.zip', 'personal', 'saved', 'comments', '__pycache__'))
        shutil.copy2(ROOT / 'README.md', self.root / 'README.md')
        self.repository = self.root / 'source-checkout'
        for row in json.loads((self.pack / check.MAPPING).read_text())['items']:
            path = row['source']['path']
            if (REPOSITORY / path).is_file():
                destination = self.repository / path
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(REPOSITORY / path, destination)

    def mapping(self, mutate):
        path = self.pack / check.MAPPING
        data = json.loads(path.read_text())
        mutate(data)
        path.write_text(json.dumps(data))

    def guide(self, old, new):
        path = self.pack / check.QUESTIONNAIRE
        original = path.read_text()
        self.assertIn(old, original)
        path.write_text(original.replace(old, new, 1))

    def rejected(self, message):
        with self.assertRaisesRegex(ValueError, message):
            check.validate(self.pack, self.repository)

    def test_complete_evidence(self):
        result = check.validate(self.pack, self.repository)
        self.assertEqual((result['questions'], result['incidents'], result['source_excerpts']), (30, 12, 42))

    def archived_row(self):
        return next(row for row in json.loads((self.pack / check.MAPPING).read_text())['items'] if 'archived_file' in row['source'])

    def test_missing_dated_original_uses_verified_full_archive(self):
        for row in json.loads((self.pack / check.MAPPING).read_text())['items']:
            if 'archived_file' in row['source']:
                (self.repository / row['source']['path']).unlink(missing_ok=True)
        self.assertEqual(check.validate(self.pack, self.repository)['source_excerpts'], 42)

    def test_missing_current_source_is_still_rejected(self):
        (self.repository / 'infra/aws-ecs-dev/network.tf').unlink()
        self.rejected('missing source file')

    def test_missing_archived_record(self):
        (self.pack / self.archived_row()['source']['archived_file']).unlink()
        self.rejected('missing archived evidence')

    def test_corrupt_archived_record(self):
        path = self.pack / self.archived_row()['source']['archived_file']
        path.write_text(path.read_text() + '\nAltered evidence\n')
        self.rejected('archived evidence hash mismatch')

    def test_present_original_must_match_archived_record(self):
        path = self.repository / self.archived_row()['source']['path']
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text('Conflicting dated original')
        self.rejected('local dated original differs')

    def test_archive_is_disallowed_for_current_source(self):
        self.mapping(lambda d: d['items'][0]['source'].update(archived_file=self.archived_row()['source']['archived_file']))
        self.rejected('only dated records may use an archive')

    def test_duplicate_manifest_id(self):
        self.mapping(lambda d: d['items'][1].update(id='Q01'))
        self.rejected('item IDs')

    def test_missing_rendered_card(self):
        self.guide('### Q30 ·', '### Removed ·')
        self.rejected('rendered IDs')

    def test_missing_lesson_file(self):
        lesson = json.loads((self.pack / check.MAPPING).read_text())['items'][0]['lessons'][0]
        (self.pack / lesson).unlink()
        self.rejected('missing lesson')

    def test_mismatched_lesson_mapping(self):
        self.mapping(lambda d: d['items'][0].update(lessons=['generated/21-aws-accounts-regions-and-cli.md']))
        self.rejected('rendered lesson missing')

    def test_broken_existing_file_fragment(self):
        path = self.pack / check.CONTEXT
        path.write_text(path.read_text().replace('<a id="source-q01"></a>', ''))
        self.rejected('source context anchor missing')

    def test_unlisted_broken_link(self):
        self.guide('## Choose a starting point', '[Extra](generated/21-aws-accounts-regions-and-cli.md#does-not-exist)\n\n## Choose a starting point')
        self.rejected('Broken local anchor')

    def test_pack_escape_to_existing_file(self):
        self.guide('## Choose a starting point', '[Escape](../../README.md)\n\n## Choose a starting point')
        self.rejected('escapes managed pack')

    def test_stale_source_excerpt(self):
        self.mapping(lambda d: d['items'][0]['source'].update(excerpt='invented Terraform source'))
        self.rejected('stale source excerpt')

    def test_nonexistent_source_symbol(self):
        self.mapping(lambda d: d['items'][0]['source'].update(symbol='invented_symbol'))
        self.rejected('source symbol absent')

    def test_source_path_escape(self):
        self.mapping(lambda d: d['items'][0]['source'].update(path='../README.md'))
        self.rejected('source escape')

    def test_absent_feature_without_worked_example(self):
        self.mapping(lambda d: d['items'][6].pop('absent_feature_example'))
        self.rejected('absent feature needs a worked example')

    def test_nonprimary_reference(self):
        self.mapping(lambda d: d['items'][0].update(official_reference='https://example.com/interview'))
        self.rejected('reference must be primary')

    def test_incident_without_recovery_criterion(self):
        self.guide('**Verify recovery:**', '**Expected:**')
        self.rejected('missing Verify recovery')

    def test_wrong_rendered_evidence_scope(self):
        self.guide('**Evidence:** Current source.', '**Evidence:** Verified AWS.')
        self.rejected('rendered evidence scope')

    def test_source_snapshot_missing_actual_excerpt(self):
        row = json.loads((self.pack / check.MAPPING).read_text())['items'][0]
        path = self.pack / check.CONTEXT
        path.write_text(path.read_text().replace(row['source']['excerpt'], 'invented excerpt'))
        self.rejected('rendered excerpt missing')

    def test_source_symbol_must_render_in_its_card(self):
        self.guide('setting/symbol: `capabilities     =`', 'setting/symbol: `wrong`')
        self.rejected('rendered source symbol missing')

    def test_excerpt_cannot_be_borrowed_from_another_card(self):
        path = self.pack / check.CONTEXT
        text = path.read_text()
        begin = text.index('<a id="source-i01">')
        end = text.index('<a id="source-i02">')
        # I01 and Q11 use the same excerpt: the other intact copy must not mask corruption.
        text = text[:begin] + text[begin:end].replace("'--platform', 'linux/amd64'", "'--platform', 'invented'") + text[end:]
        path.write_text(text)
        self.rejected('rendered excerpt missing')

    def test_readme_navigation_is_required(self):
        path = self.pack / 'README.md'
        path.write_text(path.read_text().replace(check.QUESTIONNAIRE, 'removed.md'))
        self.rejected('Navigation missing')

    def test_managed_archive_bytes_and_personal_exclusions(self):
        scripts = self.root / 'scripts'; scripts.mkdir()
        shutil.copy2(ROOT / 'scripts/package-node-study.py', scripts / 'package-node-study.py')
        for folder in ('personal', 'saved', 'comments'):
            (self.pack / folder).mkdir(exist_ok=True)
            (self.pack / folder / 'private-note.md').write_text('personal canary')
        (self.pack / 'private-root-note.md').write_text('unmanaged canary')
        subprocess.run([sys.executable, str(scripts / 'package-node-study.py')], check=True, capture_output=True, text=True)
        with ZipFile(self.pack / 'NodeJs-AWS-study-pack.zip') as archive:
            names = archive.namelist()
            self.assertEqual(len(names), len(set(names)))
            for relative in (check.QUESTIONNAIRE, check.MAPPING, check.CONTEXT):
                self.assertIn('NodeJs-AWS/' + relative, names)
            self.assertFalse(any('private-note' in n or 'private-root-note' in n for n in names))
            for name in names:
                path = self.pack / name.removeprefix('NodeJs-AWS/')
                self.assertEqual(archive.read(name), path.read_bytes(), name)


if __name__ == '__main__':
    unittest.main(argv=[sys.argv[0], *remaining])
