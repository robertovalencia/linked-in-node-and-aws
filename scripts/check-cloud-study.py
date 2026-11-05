"""Validate managed cloud curriculum, links and exact historical excerpts offline."""
from pathlib import Path
import argparse
import json
import re
import subprocess
from urllib.parse import unquote, urlsplit

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--repository', type=Path, help='Full Git source checkout')
args = parser.parse_args()
root = Path(__file__).resolve().parents[1]
repo = args.repository or root
pack = root / 'docs/nodejs-aws-study-path'
coverage = json.loads((pack / 'cloud-coverage.json').read_text())
assert coverage['schema_version'] == 2
count = coverage['lesson_count']
all_lessons = sorted((pack / 'generated').glob('[0-9][0-9]-*.md'))
assert [int(p.name[:2]) for p in all_lessons] == list(range(count)), 'Missing/duplicate lesson'
first, last = coverage['cloud_first'], coverage['cloud_last']
lessons = all_lessons[first:last + 1]
assert [r['lesson'] for r in coverage['coverage']] == list(range(first, last + 1))
for row, path in zip(coverage['coverage'], lessons):
    assert row['slug'] == path.stem and row['concepts']
cache = {}
def source(commit, path):
    key = commit, path
    if key not in cache:
        cache[key] = subprocess.check_output(['git', '-C', str(repo), 'show', f'{commit}:{unquote(path)}'], text=True).splitlines()
    return cache[key]
links = 0
pinned = set()
for path in [*all_lessons, pack / 'README.md', pack / 'deployment-handoff.md', pack / 'aws-terraform-questionnaire.md', pack / 'evidence/aws-terraform-project-context.md', *(pack / 'evidence/questionnaire-records').glob('*.md'), *(pack / 'labs').rglob('*.md'), *(pack / 'walkthroughs').glob('*.md'), *(pack / 'visuals').glob('*.md')]:
    text = path.read_text()
    for href in re.findall(r'\[[^\]]*\]\(([^)]+)\)', text):
        parsed = urlsplit(href)
        if parsed.scheme or href.startswith(('/', '#')) or not parsed.path:
            continue
        target = (path.parent / unquote(parsed.path)).resolve()
        assert target.is_relative_to(pack.resolve()), f'{path.name}: link escapes downloadable pack; use a pinned source URL: {href}'
        assert target.exists(), f'{path.name}: broken local link {href}'
        links += 1
    refs = re.findall(r'https://github.com/robertovalencia/linked-in-node-and-aws/blob/([0-9a-f]{40})/([^\s)#]+)(?:#L(\d+)(?:-L(\d+))?)?', text)
    if path in lessons and int(path.name[:2]) < 44:
        assert refs, f'{path.name}: foundation needs its pinned project example'
    if path in lessons and int(path.name[:2]) >= 44:
        assert re.search(r'^## (?:Mastery|.*mastery|Practice and expected results|Evidence limits and interview application)' , text, re.M), f'{path.name}: missing mastery gate'
        assert re.search(r'^- \[[^\]]+\]\(https://(?:docs\.aws\.amazon\.com|aws\.amazon\.com|developer\.hashicorp\.com|registry\.terraform\.io|github\.com/hashicorp|opentelemetry\.io)',text,re.M), f'{path.name}: missing primary reference'
    for commit, filename, begin, end in refs:
        lines = source(commit, filename)
        if begin:
            assert 1 <= int(begin) <= int(end or begin) <= len(lines), f'{path.name}: invalid source lines'
        pinned.add((commit, filename, begin, end))
manifest = json.loads((pack / 'cloud-source-excerpts.json').read_text())
for row in manifest['excerpts']:
    actual = '\n'.join(source(manifest['source_commit'], row['path'])[row['start']-1:row['end']])
    assert actual == row['excerpt'], f"Stale source excerpt: {row['path']}"
questionnaire = json.loads(subprocess.check_output(['python3', str(root / 'scripts/check-aws-questionnaire.py'), '--repository', str(repo)], text=True))
node_questionnaire = json.loads(subprocess.check_output(['python3', str(root / 'scripts/check-node-questionnaire.py'), '--repository', str(repo)], text=True))
print(json.dumps({'questionnaire':questionnaire,'node_questionnaire':node_questionnaire,'lessons':count,'cloud_lessons':len(lessons),'mapped_concepts':sum(len(r['concepts']) for r in coverage['coverage']),'local_links':links,'unique_pinned_source_ranges':len(pinned),'exact_manifest_excerpts':len(manifest['excerpts'])}))
