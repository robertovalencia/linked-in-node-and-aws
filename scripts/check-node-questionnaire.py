"""Offline contract checks for the Node/backend companion and managed ZIP."""
from pathlib import Path
from urllib.parse import urlsplit
from zipfile import ZipFile
import argparse
import hashlib
import importlib.util
import json
import re

ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / 'docs/nodejs-aws-study-path'
spec = importlib.util.spec_from_file_location('aws_checker', ROOT/'scripts/check-aws-questionnaire.py')
aws_checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(aws_checker)
PRIMARY = {'nodejs.org','docs.nestjs.com','www.typescriptlang.org','typescriptlang.org',
           'tc39.es','docs.npmjs.com','docs.docker.com','node-postgres.com',
           'www.postgresql.org','postgresql.org','zod.dev','kafka.js.org','kafkajs.com','kafka.apache.org',
           'github.com','react.dev','jestjs.io','vitest.dev','playwright.dev','testing-library.com',
           'fetch.spec.whatwg.org','dom.spec.whatwg.org','html.spec.whatwg.org',
           'www.rfc-editor.org','datatracker.ietf.org','openid.net','oauth.net','cheatsheetseries.owasp.org',
           'owasp.org','docs.aws.amazon.com','docs.github.com','docs.sonarsource.com',
           'opentelemetry.io','prometheus.io','sre.google','www.w3.org','w3c.github.io',
           'rxjs.dev','helmet.js.org','helmetjs.github.io','expressjs.com'}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def read_items(pack):
    return json.loads((pack/'node-backend-questionnaire-map.json').read_text())['items']


def validate(pack=PACK, repo=ROOT, archive=False):
    data=json.loads((pack/'node-backend-questionnaire-map.json').read_text())
    require(data['schema_version']==1,'Unsupported schema')
    rows=data['items']; ids=[r['id'] for r in rows]
    ledger=json.loads((pack/'node-backend-coverage.json').read_text())
    # This manifest fixes reviewed identity/counts independently from the renderer.
    require(ids==ledger['reviewed_item_ids'],'Missing, duplicate, reordered or unreviewed IDs')
    require(len(ids)==len(set(ids)),'Duplicate ID')
    index=(pack/'node-backend-questionnaire.md').read_text()
    require(f'{sum(r["kind"]=="question" for r in rows)} questions and {sum(r["kind"]=="incident" for r in rows)} incidents' in index,'Wrong rendered question/incident counts')
    for row in rows:
        require(f'](node-backend-{row["section"]}.md#{row["id"].lower()})' in index,f'{row["id"]}: missing index link')
    context=(pack/'evidence/node-backend-source-context.md').read_text()
    source_blocks=dict(re.findall(r'<a id="source-([a-z0-9]+)"></a>\n(.*?)(?=<a id="source-|\Z)',context,re.S))
    sources=set(); absent=0
    for section in ['runtime','services','operations']:
        expected=[r for r in rows if r['section']==section]
        original=json.loads((pack/f'node-{section}-items.json').read_text())
        require([r['id'] for r in original]==[r['id'] for r in expected],f'{section}: data/render mismatch')
        for a,b in zip(original,expected):
            b={k:v for k,v in b.items() if k!='section'}
            b['source']={k:v for k,v in b['source'].items() if k!='href'}
            require(a==b,f'{a["id"]}: input/map content mismatch')
        guide=(pack/f'node-backend-{section}.md').read_text()
        headings=re.findall(r'^### ([A-Z]+\d{2}) · (.+)$',guide,re.M)
        require(headings==[(r['id'],r['title']) for r in expected],f'{section}: rendered IDs/titles differ')
        blocks=dict(zip([r['id'] for r in expected],re.split(r'^### [A-Z]+\d{2} · .+$',guide,flags=re.M)[1:]))
        for row in expected:
            ident=row['id']; block=blocks[ident]; source=row['source']
            require(row['kind'] in ('question','incident'),f'{ident}: invalid kind')
            require(row['priority'] in ('start now','next','extension'),f'{ident}: invalid priority')
            require(row['answer'].strip() and row['answer'] in block,f'{ident}: missing rendered answer')
            require(f'**Priority:** {row["priority"]}' in block,f'{ident}: missing rendered priority')
            require(row['scope'] in ('Current source','Absent implementation'),f'{ident}: invalid scope')
            require(row['scope'] in block,f'{ident}: scope not rendered')
            require(row['concepts'] and row['lessons'],f'{ident}: missing concepts/lessons')
            if 'lesson_relation' in row:
                require(row['lesson_relation'] in block,f'{ident}: missing lesson relationship')
            for lesson in row['lessons']:
                require(re.fullmatch(r'generated/\d{2}-[a-z0-9-]+\.md',lesson),f'{ident}: invalid lesson')
                require((pack/lesson).is_file() and f']({lesson})' in block,f'{ident}: missing lesson link')
            path=(repo/source['path']).resolve()
            require(path.is_relative_to(repo.resolve()),f'{ident}: source path escape')
            require(path.is_file(),f'{ident}: missing actual source')
            raw=path.read_bytes(); content=raw.decode()
            require(hashlib.sha256(raw).hexdigest()==source['sha256_at_inspection'],f'{ident}: stale source hash')
            require(source['symbol'] in content and source['symbol'] in source['excerpt'],f'{ident}: missing symbol')
            require(source['excerpt'] in content,f'{ident}: stale source excerpt')
            require(f'`{source["symbol"]}`' in block and f']({source["href"]})' in block,f'{ident}: source not rendered')
            own=source_blocks.get(ident.lower(),'')
            require(source['excerpt'].rstrip('\n') in own and source['sha256_at_inspection'] in own,f'{ident}: own source context differs')
            require(source['path'] in own and source['symbol'] in own,f'{ident}: own source label missing')
            sources.add(source['path'])
            for url in row['official_references']:
                parsed=urlsplit(url)
                require(parsed.scheme=='https' and parsed.hostname in PRIMARY,f'{ident}: non-primary reference {url}')
                require(f']({url})' in block,f'{ident}: official reference not rendered')
            require(row['official_references'],f'{ident}: no references')
            if row['scope']=='Absent implementation':
                absent+=1
                require(row.get('worked_example') and row.get('worked_example_url'),f'{ident}: absent feature lacks worked example')
                require(row['worked_example'] in block and f']({row["worked_example_url"]})' in block,f'{ident}: worked example not rendered')
                require(urlsplit(row['worked_example_url']).hostname in PRIMARY,f'{ident}: non-primary worked example')
            if row['kind']=='incident':
                for field in ['symptom','checks','repair','recovery']:
                    require(row.get(field,'').strip() and row[field] in block,f'{ident}: missing {field}')
    require([l['lesson_id'] for l in ledger['lessons']]==[f'{n:02}' for n in range(84)],'Incomplete lesson disposition')
    require(len(ledger['concepts'])>=150,'Backend concept coverage lost')
    for row in ledger['concepts']:
        require(row['item_ids'] and all(i in ids for i in row['item_ids']),f'Unmapped backend concept {row["concept"]}')
    inventory=json.loads((pack/'node-backend-lesson-inventory.json').read_text())
    for lesson in inventory['lessons']:
        require(hashlib.sha256((pack/lesson['pack_path']).read_bytes()).hexdigest()==lesson['sha256'],f'Protected lesson changed {lesson["lesson_id"]}')
        if lesson['lesson_id'] not in ('00','19','20','44'):
            mapped=[r['concept'] for r in ledger['concepts'] if r['lesson']==lesson['pack_path']]
            require(mapped==lesson['node_backend_concepts'],f'Incomplete concept mapping for lesson {lesson["lesson_id"]}')
    require([r['path'] for r in ledger['supplementary_guides']]==[r['path'] for r in inventory['supplementary_guides']],'Incomplete supplementary disposition')
    managed=[*pack.glob('node-backend-*.md'),pack/'evidence/node-backend-source-context.md',pack/'labs/node-runtime/README.md']
    local_links=sum(aws_checker.check_links(p,pack) for p in managed)
    for nav in [repo/'README.md',pack/'README.md',repo/'docs/nodejs-beginner/README.md']:
        require('node-backend-questionnaire.md' in nav.read_text(),f'Missing navigation {nav}')
    archive_members=None
    if archive:
        with ZipFile(pack/'NodeJs-AWS-study-pack.zip') as z:
            names=z.namelist();require(len(names)==len(set(names)),'Duplicate archive members')
            for name in names:
                require(name.startswith('NodeJs-AWS/'),'Archive root escape')
                rel=Path(name).relative_to('NodeJs-AWS')
                require('..' not in rel.parts and not rel.is_absolute(),'Archive path escape')
                require(not any(p in ('personal','saved','comments','.terraform','__pycache__') for p in rel.parts),'Private/cache archive entry')
                require(not rel.name.endswith(('.tfstate','.tfstate.backup','.tfplan','.pyc','.zip')),'Private archive suffix')
                require(not (rel.name=='.env' or rel.name.startswith('.env.')),'Environment archive entry')
                require((pack/rel).is_file() and z.read(name)==(pack/rel).read_bytes(),f'Archive byte mismatch: {rel}')
            required=[*pack.glob('node-*.md'),*pack.glob('node-*.json'),pack/'evidence/node-backend-source-context.md',pack/'labs/node-runtime/README.md',pack/'labs/node-runtime/run.mjs']
            require(all('NodeJs-AWS/'+p.relative_to(pack).as_posix() in names for p in required if p.is_file()),'Missing Node companion archive file')
            require(sum(bool(re.fullmatch(r'NodeJs-AWS/generated/\d{2}-.+\.md',n)) for n in names)==84,'Archive lesson loss')
            archive_members=len(names)
    return dict(questions=sum(r['kind']=='question' for r in rows),incidents=sum(r['kind']=='incident' for r in rows),
                source_files=len(sources),absent_examples=absent,concept_rows=len(ledger['concepts']),local_links=local_links,archive_members=archive_members)


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repository',type=Path,default=ROOT)
    parser.add_argument('--archive',action='store_true')
    args=parser.parse_args()
    print(json.dumps(validate(PACK,args.repository,args.archive)))
