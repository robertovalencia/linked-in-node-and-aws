"""Validate curriculum links and exact source excerpts without network or AWS access."""
from pathlib import Path
import argparse
import json
import re
import subprocess
from urllib.parse import unquote, urlsplit

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--repository', type=Path, help='Full Git source checkout (default: this repository)')
args = parser.parse_args()
root = Path(__file__).resolve().parents[1]
repo = args.repository or root
pack = root / 'docs/nodejs-aws-study-path'
lessons = sorted(p for p in (pack / 'generated').glob('*.md') if 20 <= int(p.name[:2]) <= 43)
assert [int(p.name[:2]) for p in lessons] == list(range(20, 44)), 'Expected all 24 cloud lessons'
cache = {}
def source(commit, path):
    key = commit, path
    if key not in cache:
        cache[key] = subprocess.check_output(['git', '-C', str(repo), 'show', f'{commit}:{path}'], text=True).splitlines()
    return cache[key]
links = 0
pinned = set()
for path in [*lessons, pack / 'README.md', *(pack / 'labs').rglob('*.md')]:
    text = path.read_text()
    for href in re.findall(r'\[[^\]]*\]\(([^)]+)\)', text):
        parsed = urlsplit(href)
        if parsed.scheme or href.startswith(('/', '#')):
            continue
        if not parsed.path:
            continue
        target = path.parent / unquote(parsed.path)
        fallback = repo / target.relative_to(root) if target.is_relative_to(root) else target
        assert target.exists() or fallback.exists(), f'{path.name}: broken local link {href}'
        links += 1
    refs = re.findall(r'https://github.com/robertovalencia/linked-in-node-and-aws/blob/([0-9a-f]{40})/([^\s)#]+)(?:#L(\d+)(?:-L(\d+))?)?', text)
    if path in lessons:
        assert refs, f'{path.name}: no pinned real project example'
    for commit, filename, begin, end in refs:
        lines = source(commit, filename)
        if begin:
            assert 1 <= int(begin) <= int(end or begin) <= len(lines), f'{path.name}: invalid source lines'
        pinned.add((commit, filename, begin, end))
manifest = json.loads((pack / 'cloud-source-excerpts.json').read_text())
for row in manifest['excerpts']:
    actual = '\n'.join(source(manifest['source_commit'], row['path'])[row['start']-1:row['end']])
    assert actual == row['excerpt'], f"Stale source excerpt: {row['path']}"
print(json.dumps({'cloud_lessons': len(lessons), 'local_links': links, 'unique_pinned_source_ranges':len(pinned), 'exact_manifest_excerpts':len(manifest['excerpts'])}))
