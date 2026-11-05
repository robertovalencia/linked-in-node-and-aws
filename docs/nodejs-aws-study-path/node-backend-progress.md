# Node.js/backend questionnaire progress

Updated: 5 November 2026. This is an actual execution ledger. [Questionnaire](node-backend-questionnaire.md) · [Coverage](node-backend-coverage.md).

| Judgeable section | Builder | Executed state | Independent review |
|---|---|---|---|
| Both lesson inventories | inventory agent | 84 pairs;17 byte-identical;67 link-only differences;22 supplementary guides | full normalized lesson equality independently rechecked |
| Language and runtime | separate runtime builder | 43 questions,6 incidents; ten assertion groups | accepted after worker/error/stream/environment repairs; extra arrow-this card included in integrated review |
| Services, security, persistence and events | separate service builder | 54 questions,9 incidents;63 exact source mappings | accepted after stopped-consumer/manual-restart and prerequisite-label repairs |
| Setup, tests, client boundaries, delivery and extensions | coordinator builder | 40 questions,9 incidents; mixed backend/cloud omissions repaired | integrated content review accepted; clean rebuild independently passed |
| Anonymous equivalent explanations | fresh independent critic | five blinded pairs judged before identity inspection | ours selected in all five; full-bank superiority is not a measured claim |
| Source/render/lesson/coverage validation | coordinator and independent critic |137 questions,24 incidents;37 source files;28 absent examples;290 mapped mechanism rows;84 lesson dispositions | validator and source checks pass |
| Public official links | coordinator |157 GETs returned200; all requested fragments observed after parser/URL repair | technical relevance reviewed separately from reachability |
| Packaging and clean checkout | coordinator and independent critic |167 managed files;84 numbered lessons; private canaries tested | PASS: root and independent clean rebuilds; extracted lab and all-member/private-canary checks pass |

## Actual checks and limits

- `npm run check` and `npm run build`: passed.
- `npm test`: initial sandbox run failed three loopback TLS-server cases with EPERM. Rerun with local access passed88 backend tests and28 frontend tests. No test was removed or weakened.
- `node --unhandled-rejections=strict docs/nodejs-aws-study-path/labs/node-runtime/run.mjs`: ten assertion groups passed, including failed worker and failed pipeline cleanup. The independent runtime critic reran it.
- Node companion regression suite: all26 corrupt-input/index/private-asset controls passed. Existing AWS companion26 regressions passed.
- The legacy cloud/study checker passes with84 lessons,64 cloud lessons,321 cloud concepts,279 pinned source ranges and31 historical excerpts, plus the new companion validator.
- Docker daemon is not running. Full-stack HTTP acceptance/browser/outage recovery was not executed for this documentation change. Unit tests and the runtime lab do not establish broker outage recovery.
- Both agreements were read first. The external profile has no separate AGENTS.md; its project-root agreement applies. All numbered lessons and personal/profile files remain preserved.
- No original Java source, application behavior, infrastructure, secret values, hosted reader, external repository destination or cloud resource changed. No commit, push, publication or hosted integration execution is claimed.

## Largest gaps and repairs

The largest behavioral gap was assuming every KafkaJS consumer failure reconnects automatically. A non-retriable handler error can stop the consumer while the application retry loop remains asleep. Incidents now check CRASH restart state and actual progress, repair the cause, and require a controlled local restart with the same group/offset/event identity when needed. Poison records still require a designed policy; no dead-letter system is invented.

Runtime criticism exposed an unowned worker-event rejection; the lab now owns both observers together and asserts failed exit, and verifies both streams close on pipeline error. Child-process environment inheritance wording was corrected.

The inventory exposed backend concepts beyond the first ten lessons. Cache/queue/handler/trace/recovery cards were added; final semantic review then repaired management/data audit distinction, key-dependent restoration and denormalization/backfill consistency. Prerequisite lesson links are labeled separately from researched extensions.

Clean-checkout failures caught a missing copied navigation README and a contradiction between excluding private lab canaries and requiring them as archive assets. The repair retains mandatory real lab assets, private-state/environment exclusions and all-member byte verification. Root and independent repaired clean rebuilds now pass, including the extracted lab and byte/private-canary checks.

## Reproduce local validation

From the repository root:

```sh
python3 scripts/package-node-study.py
python3 scripts/check-cloud-study.py
python3 scripts/check-node-questionnaire.py --archive
python3 scripts/check-node-questionnaire.test.py
python3 scripts/check-aws-questionnaire.test.py
node --unhandled-rejections=strict docs/nodejs-aws-study-path/labs/node-runtime/run.mjs
python3 scripts/check-node-study-clean-checkout.py --output /private/tmp/node-study-clean.json
```

Public link checks are a separate optional network operation: `python3 scripts/check-node-study-links.py --output /private/tmp/node-study-links.json`. These commands validate study artifacts and do not invoke AWS APIs or start the full application. The canonical dated execution/review reports live under repository `docs/evidence/node-backend-*`; this ZIP includes the actual progress and portable source excerpts.
