"""Render reviewed structured cards into portable Markdown. No network or application changes."""
from pathlib import Path
import json
import subprocess

ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / 'docs/nodejs-aws-study-path'
SECTIONS = [('runtime', 'JavaScript, TypeScript and the Node runtime'),
            ('services', 'NestJS, contracts, security, databases and events'),
            ('operations', 'Setup, testing, client boundaries, delivery and extensions')]


def render():
    items = []
    context = ['# Inspected Node/backend source excerpts\n',
               'Inspected 5 November 2026. These literal excerpts describe source, not a new deployment. '
               'Paths are repository-relative. Hashes bind the full inspected file; validators require current source to match. '
               'Absent-feature cards show a related boundary for contrast and label their external example separately.\n']
    for key, title in SECTIONS:
        rows = json.loads((PACK / f'node-{key}-items.json').read_text())
        lines = [f'# {title}\n', '[Questionnaire and routes](node-backend-questionnaire.md) · '
                 '[Acronym glossary](node-backend-questionnaire.md#acronyms-at-a-glance) · '
                 '[Source excerpts](evidence/node-backend-source-context.md) · [Runtime lab](labs/node-runtime/README.md)\n']
        for row in rows:
            ident = row['id']
            source = row['source']
            source['href'] = f'evidence/node-backend-source-context.md#source-{ident.lower()}'
            row['section'] = key
            lines += [f'<a id="{ident.lower()}"></a>\n', f'### {ident} · {row["title"]}\n',
                      f'**Priority:** {row["priority"]}. **Implementation:** {row["scope"]}.\n', row['answer'] + '\n']
            if row['kind'] == 'incident':
                for field in ('symptom', 'checks', 'repair', 'recovery'):
                    label = 'Recovery verification' if field == 'recovery' else field.title()
                    lines.append(f'**{label}:** {row[field]}\n')
            if row['scope'] == 'Absent implementation':
                lines += [f'**External worked example (not installed here):** {row["worked_example"]} '
                          f'[Official example]({row["worked_example_url"]}).\n']
            lines += [f'**Project:** [{source["path"]}]({source["href"]}) · symbol: `{source["symbol"]}`.\n',
                      '**Lessons:** ' + ' · '.join(f'[{p[10:12]} · {p[13:-3].replace("-", " ")}]({p})' for p in row['lessons']) + '.\n',
                      '**Lesson relationship:** ' + row.get('lesson_relation', 'The linked lessons teach this mechanism or its project boundary; current details come from the inspected source and official references.') + '\n',
                      '**Official documentation:** ' + ' · '.join(f'[{u.split("/")[2]} · reference {n}]({u})' for n,u in enumerate(row['official_references'], 1)) + '.\n']
            context += [f'<a id="source-{ident.lower()}"></a>\n', f'## {ident} · {source["path"]}\n',
                        f'Symbol: `{source["symbol"]}`. Full-file SHA-256: `{source["sha256_at_inspection"]}`.\n',
                        '```text\n' + source['excerpt'].rstrip('\n') + '\n```\n']
            items.append(row)
        (PACK/f'node-backend-{key}.md').write_text('\n'.join(lines))
    (PACK/'evidence/node-backend-source-context.md').write_text('\n'.join(context))
    try:
        head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
    except subprocess.CalledProcessError:
        head=None
    data=dict(schema_version=1,inspected_on='2026-11-05',source_head=head,items=items)
    (PACK/'node-backend-questionnaire-map.json').write_text(json.dumps(data,indent=2)+'\n')
    count=sum(i['kind']=='question' for i in items); incidents=len(items)-count
    intro=f'''# Node.js/backend interview questionnaire and troubleshooting

{count} questions and {incidents} incidents, chosen from concept coverage across both lesson sets and researched gaps. Existing lesson IDs and personal progress stay unchanged. Researched 5 November 2026.

[Study path](README.md) · [AWS/Terraform companion](aws-terraform-questionnaire.md) · [Coverage ledger](node-backend-coverage.md) · [Live progress](node-backend-progress.md) · [Download](NodeJs-AWS-study-pack.zip)

Use **start now** for first-interview foundations, **next** for mechanisms and **extension** for alternatives. Read the answer aloud, explain its project symbol, then describe one failure and how you would verify recovery. The incidents are rehearsals unless the progress/evidence record explicitly says a check ran. An implementation label establishes source presence, not a verified running service.

Start locally: use Node within the backend’s declared `>=22 <25` range and Docker Desktop/Compose v2. From the repository root run `npm run setup`, then `npm run up`; open http://localhost:8180. For host hot reload, stop containers with `npm run down`, run `bash scripts/local.sh deps`, install backend/frontend dependencies and run `npm run dev`; open http://localhost:5183. The source-linked setup section explains credentials, host/container addresses and expected health. These local scripts do not invoke AWS.

## Choose a small session

- First 30 minutes: NO01–NO07 (setup), NR01/NR14–NR17/NR22 (runtime), NS01–NS10 (service boundaries).
- One request: NS25–NS34, then NSI05 and NSI06 (authentication → durable inquiry → eventual notification).
- One failure drill: choose an incident below, predict its checks, repair and recovery observations, then run only the stated local exercise.
- Runnable mechanics: from the repository root, `node docs/nodejs-aws-study-path/labs/node-runtime/run.mjs`. The same lab runs from the extracted ZIP; [instructions and expected groups](labs/node-runtime/README.md).
- Advanced backend design: the operations extensions connect the cloud lessons to cache/queue/handler/trace/recovery behavior. Infrastructure detail remains in the AWS/Terraform companion.

## Read evidence carefully

Four capability processes own separate databases: Identity, Catalog, Inquiries and Notifications. Shared image/code does not mean shared domain tables. The older handbooks and some numbered lesson excerpts describe historical source checkpoints; this companion’s literal source excerpts were inspected for this task. The selected ECS infrastructure source is separate from application activation. No current AWS inventory, release, hosted CI, Jira or Study Desk publication is established here.

The requested [reference repository](https://github.com/Devinterview-io/node-interview-questions) was fetched before drafting. Its public README contains 15 expanded answers and advertises a larger question bank. This companion is original project-specific teaching, with independent section reviews and anonymous equivalent-explanation comparisons recorded separately; counts alone do not establish a quality win.

## Acronyms at a glance

| Term | Meaning |
|---|---|
| API / HTTP / JSON | Application programming interface / Hypertext Transfer Protocol / JavaScript Object Notation |
| URL / HTTPS / REST / HTML | Uniform Resource Locator / HTTP secured by TLS / Representational State Transfer / Hypertext Markup Language |
| I/O / CPU / RAM | Input/output / central processing unit / random-access memory |
| IP / ID / TCP / UDP | Internet Protocol / identifier / Transmission Control Protocol / User Datagram Protocol |
| ESM / CJS / DI | ECMAScript modules / CommonJS modules / dependency injection |
| SQL / JSONB / ACID | Structured Query Language / PostgreSQL binary JSON / atomicity, consistency, isolation, durability |
| JWT / HMAC / HS256 | JSON Web Token / hash-based message authentication code / HMAC using SHA-256 |
| TLS / CA / DNS | Transport Layer Security / certificate authority / Domain Name System |
| CORS / CSRF / XSS | Cross-Origin Resource Sharing / cross-site request forgery / cross-site scripting |
| OAuth / OIDC | OAuth authorization framework / OpenID Connect identity layer |
| PKCE / LTS / VM | Proof Key for Code Exchange / long-term support / virtual machine |
| UTC / ISO | Coordinated Universal Time / International Organization for Standardization (here, standardized date format) |
| UUID / SHA / UTF-8 | Universally unique identifier / Secure Hash Algorithm / Unicode Transformation Format using 8-bit units |
| CI / ADR / ORM | Continuous integration / architecture decision record / object-relational mapper |
| TTL / DLQ / FIFO | Time to live / dead-letter queue / first in, first out |
| SLI / SLO / SLA | Service-level indicator / objective / agreement |
| RPO / RTO | Recovery point objective (allowed data loss) / recovery time objective (allowed recovery duration) |
| AWS / ECS / RDS / SQS / SNS | Amazon Web Services / Elastic Container Service / Relational Database Service / Simple Queue Service / Simple Notification Service |
| EC2 / S3 / KMS | Elastic Compute Cloud / Simple Storage Service / Key Management Service |
| SCRAM / ACL / ISR | Salted Challenge Response Authentication Mechanism / access control list / in-sync replicas |

## Sections and stable IDs
'''
    for key,title in SECTIONS:
        intro+=f'\n### {title}\n\n'
        for row in items:
            if row['section']==key:
                intro+=f'- [{row["id"]} · {row["title"]}](node-backend-{key}.md#{row["id"].lower()}) — {row["priority"]}' + ('; incident' if row['kind']=='incident' else '')+'\n'
    (PACK/'node-backend-questionnaire.md').write_text(intro)
    print(json.dumps(dict(questions=count,incidents=incidents,sections=len(SECTIONS))))

if __name__ == '__main__':
    render()
