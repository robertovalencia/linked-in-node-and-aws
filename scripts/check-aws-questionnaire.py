"""Validate the supplementary questionnaire against local lessons and public source; no cloud calls."""
from pathlib import Path
import argparse
import hashlib
import json
import re
from urllib.parse import unquote, urlsplit

QUESTIONNAIRE = 'aws-terraform-questionnaire.md'
MAPPING = 'aws-terraform-questionnaire-map.json'
CONTEXT = 'evidence/aws-terraform-project-context.md'
EXPECTED = [f'Q{i:02}' for i in range(1, 31)] + [f'I{i:02}' for i in range(1, 13)]
PRIMARY = {'docs.aws.amazon.com', 'developer.hashicorp.com', 'kafka.apache.org', 'www.postgresql.org'}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def anchors(text):
    """GitHub-compatible simple heading slugs plus explicit portable HTML anchors."""
    found = set(re.findall(r'<a\s+(?:id|name)="([^"]+)"\s*>', text))
    counts = {}
    for title in re.findall(r'^#{1,6}\s+(.+)$', text, re.M):
        title = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', title)
        slug = re.sub(r'[^\w\- ]', '', title.lower()).replace(' ', '-')
        count = counts.get(slug, 0)
        counts[slug] = count + 1
        found.add(slug + (f'-{count}' if count else ''))
    return found


def check_links(path, pack):
    count = 0
    for href in re.findall(r'\[[^\]]*\]\(([^)]+)\)', path.read_text()):
        parsed = urlsplit(href)
        if parsed.scheme:
            require(parsed.scheme == 'https', f'Non-HTTPS link: {href}')
            continue
        require(not href.startswith('/'), f'Absolute local link: {href}')
        target = (path.parent / unquote(parsed.path)).resolve() if parsed.path else path.resolve()
        require(target.is_relative_to(pack.resolve()), f'Link escapes managed pack: {href}')
        require(target.is_file(), f'Broken local file: {href}')
        if parsed.fragment:
            require(unquote(parsed.fragment) in anchors(target.read_text()), f'Broken local anchor: {href}')
        count += 1
    return count


def validate(pack, repo):
    guide = (pack / QUESTIONNAIRE).read_text()
    context = (pack / CONTEXT).read_text()
    data = json.loads((pack / MAPPING).read_text())
    require(data['schema_version'] == 1, 'Unsupported questionnaire map schema')
    rows = data['items']
    require([r['id'] for r in rows] == EXPECTED, 'Missing, duplicate or reordered item IDs')
    headings = re.findall(r'^### ([QI]\d{2}) · (.+)$', guide, re.M)
    require([ident for ident, _ in headings] == EXPECTED, 'Missing, duplicate or reordered rendered IDs')
    blocks = dict(zip(EXPECTED, re.split(r'^### [QI]\d{2} · .+$', guide, flags=re.M)[1:]))
    source_count = 0
    mapped = set()
    for row, (_, title) in zip(rows, headings):
        ident = row['id']; block = blocks[ident]
        require(row['title'] == title, f'{ident}: title/map differ')
        require(row['kind'] == ('question' if ident[0] == 'Q' else 'incident'), f'{ident}: wrong kind')
        require(row['priority'] in {'start now', 'next', 'extension'}, f'{ident}: missing priority')
        require(f'**Priority:** {row["priority"]}.' in block, f'{ident}: rendered priority differs')
        require(row['scope'] and f'**Evidence:** {row["scope"]}.' in block, f'{ident}: missing rendered evidence scope')
        require(row['lessons'], f'{ident}: missing lesson mapping')
        for lesson in row['lessons']:
            require(re.fullmatch(r'generated/[0-8][0-9]-[^/]+\.md', lesson), f'{ident}: invalid lesson path')
            require((pack / lesson).is_file(), f'{ident}: missing lesson {lesson}')
            require(f']({lesson})' in block, f'{ident}: rendered lesson missing {lesson}')
            mapped.add(lesson)
        src = row['source']; relative = Path(src['path'])
        target = (repo / relative).resolve()
        require(not relative.is_absolute() and target.is_relative_to(repo.resolve()), f'{ident}: source escape')
        require(relative.suffix in {'.md', '.tf', '.hcl', '.example', '.ts', '.mjs', '.yml', '.py'}, f'{ident}: non-public source type')
        if 'archived_file' in src:
            require(row['scope'].startswith('Dated execution:'), f'{ident}: only dated records may use an archive')
            archive_relative = Path(src['archived_file'])
            archive = (pack / archive_relative).resolve()
            require(not archive_relative.is_absolute() and archive.is_relative_to((pack / 'evidence/questionnaire-records').resolve()), f'{ident}: archive escape')
            require(archive.is_file(), f'{ident}: missing archived evidence')
            raw = archive.read_bytes()
            require(hashlib.sha256(raw).hexdigest() == src['sha256_at_inspection'], f'{ident}: archived evidence hash mismatch')
            if target.is_file():
                require(target.read_bytes() == raw, f'{ident}: local dated original differs from archived evidence')
            current = raw.decode()
        else:
            require(target.is_file(), f'{ident}: missing source file {relative}')
            current = target.read_text()
        require(src['symbol'] and src['symbol'] in current, f'{ident}: source symbol absent')
        require(src['excerpt'] and src['excerpt'] in current, f'{ident}: stale source excerpt')
        require(src['symbol'] in src['excerpt'], f'{ident}: excerpt omits selected symbol')
        context_match = re.search(r'<a id="source-' + ident.lower() + r'"></a>(.*?)(?=<a id="source-|\Z)', context, re.S)
        require(context_match is not None, f'{ident}: source context anchor missing')
        context_block = context_match[1]
        require(src['excerpt'] in context_block, f'{ident}: rendered excerpt missing')
        require(src['path'] in context_block and src['path'] in block, f'{ident}: rendered source path missing')
        require(src['symbol'] in block, f'{ident}: rendered source symbol missing')
        require(re.fullmatch(r'[a-f0-9]{64}', src['sha256_at_inspection']), f'{ident}: invalid historical file hash')
        require(src['href'] == f'{CONTEXT}#source-{ident.lower()}', f'{ident}: wrong source anchor mapping')
        require(f']({src["href"]})' in block, f'{ident}: rendered source link missing')
        require(ident.lower() in anchors(guide), f'{ident}: item anchor missing')
        url = row['official_reference']; parsed = urlsplit(url)
        require(parsed.scheme == 'https' and parsed.hostname in PRIMARY, f'{ident}: reference must be primary HTTPS')
        require(f']({url})' in block, f'{ident}: rendered primary reference missing')
        if ident in {'Q07', 'Q14', 'Q20', 'Q30'}:
            example = row.get('absent_feature_example', {})
            require(example.get('explanation') and example.get('url') == url, f'{ident}: absent feature needs a worked example')
            require(example['explanation'] in block and '**Absent feature / official worked example:**' in block, f'{ident}: absent feature not rendered')
        if row['kind'] == 'incident':
            for label in ('Diagnostic checks', 'Repair', 'Verify recovery'):
                require(f'**{label}:**' in block, f'{ident}: missing {label}')
        source_count += 1
    # These scope distinctions are contractual teaching requirements, not claims of live checks.
    for phrase in ('/health/live', '/health/serve', '/health/ready', 'October 31', 'November 7', 'local-only', 'at-least-once'):
        require(phrase in guide, f'Missing required evidence/contract distinction: {phrase}')
    for nav in (pack / 'README.md', pack.parents[1] / 'README.md'):
        # pack.parents[1] is docs' parent (repository root).
        if nav.is_file():
            require(QUESTIONNAIRE in nav.read_text(), f'Navigation missing in {nav}')
    local_links = sum(check_links(pack / p, pack) for p in (QUESTIONNAIRE, CONTEXT))
    archived_files = {row['source']['archived_file'] for row in rows if 'archived_file' in row['source']}
    local_links += sum(check_links(pack / name, pack) for name in archived_files)
    return {'questions': 30, 'incidents': 12, 'source_excerpts': source_count, 'distinct_mapped_lessons': len(mapped), 'questionnaire_local_links': local_links, 'absent_feature_examples': 4}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repository', type=Path, help='Source checkout for literal excerpt verification')
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    print(json.dumps(validate(root / 'docs/nodejs-aws-study-path', args.repository or root)))
