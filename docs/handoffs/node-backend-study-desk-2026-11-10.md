# Fresh-chat handoff: add the Node.js/backend questionnaire to Study Desk

**Final continuation checkpoint, November10:** user explicitly approved the named Study Desk integration. Installation/import/check/repeat and actual destination suites succeeded, preservation was checked, a visible anchor/header issue was repaired, and an independent fresh-context installed-output critic accepted it. The local questionnaire entry is `http://127.0.0.1:8765/guide/nodejs-aws--node-backend-questionnaire`. Read the [actual execution record](../evidence/node-backend-reader-2026-11-10/README.md) for final patch/tests/HTTP/preservation and scoped browser coverage before repeating any work. The original read-only handoff below is historical.

## Request and current status

The user asked to add the existing Node.js/backend interview questionnaire to **Interview process → NodeJs/AWS**, and to perform that integration in a clean chat. This handoff prepares that work; **the reader integration has not been performed**. The destination project was inspected read only on November 10, 2026. No destination file, saved note, profile, server or workflow was changed.

Start the new chat with `/Users/robertovalencia/Documents/Business/Interview process` as its project/workspace. The user has authorized the integration; proceed with the concrete work rather than asking again. Recheck current files and instructions before editing.

## Instructions and source of truth

Read these first:

- Destination: `/Users/robertovalencia/Documents/Business/Interview process/AGENTS.md`.
- Source: `/Users/robertovalencia/Documents/Business/linked-in-node-and-aws/AGENTS.md`.
- Source README, CONTRACT.md, docs/specs/requirements.md and docs/architecture.md if changing source-project behavior.
- Destination `README.md`, relevant existing workflows, `tools/import_nodejs_aws_study.py`, `tools/study_app.py`, and `tests/test_nodejs_aws_import.py`.

Use the destination’s `.venv/bin/python`. Preserve its WAT separation and reuse/extend existing deterministic tools. Do not create or overwrite a workflow without the approval required by its AGENTS.md; no new workflow is needed for this import. No paid API calls, backup uploads, Git publication or cloud operations are part of the request.

The canonical questionnaire is in source `docs/nodejs-aws-study-path/`:

| File | Role |
|---|---|
| `node-backend-questionnaire.md` | Entry page and stable question/incident navigation |
| `node-backend-runtime.md` | JavaScript, TypeScript and Node runtime |
| `node-backend-services.md` | NestJS, security, persistence and events |
| `node-backend-operations.md` | Setup, tests, delivery and backend extensions |
| `node-backend-questionnaire-map.json` | 137 questions,24 incidents; source/lesson/reference mappings |
| `node-backend-coverage.md` and `.json` | Concept/disposition coverage |
| `evidence/node-backend-source-context.md` | Portable literal source excerpts and stable source anchors |
| `labs/node-runtime/README.md` and `run.mjs` | Credential-free runnable examples |
| `node-backend-progress.md` | Dated source-project validation/review record |

Existing source reviews/results: `docs/evidence/node-backend-final-critic-2026-11-05.md`, `docs/evidence/node-backend-validation-2026-11-05.json`, and `docs/reviews.md`. Those checks are historical; they do not establish a successful reader import. Source HEAD at handoff inspection was `841f0cf6484d6d6e4d7d752c2fcde9341a2f635f`; source worktree was clean before adding this handoff. Re-resolve HEAD rather than treating this revision as a required future target.

## Findings that determine the implementation

1. The destination profile currently has its index and84 numbered lessons, but no questionnaire or its section pages. The source main README already links the questionnaire; that is distinct from importing it into the local reader.
2. `import_nodejs_aws_study.import_plan()` currently maps only `generated/[0-9][0-9]-*.md` and the pack README. Other linked files become revision-pinned GitHub links. **Rerunning the existing importer alone will not make these companion pages searchable local guides.**
3. `StudyLibrary._discover()` discovers profile guides from `study/profiles/nodejs-aws/generated/*.md`; it does not recursively discover arbitrary companion directories. `NODEJS_AWS_GROUPS` controls the visible groups, with ungrouped pages falling into “More guides.”
4. Keep the84 numbered lessons and their existing IDs. Add supplementary slugs such as `nodejs-aws--node-backend-questionnaire`, `nodejs-aws--node-backend-runtime`, `nodejs-aws--node-backend-services` and `nodejs-aws--node-backend-operations`. Use an explicit allowlist for other companion pages that must be local, especially coverage and portable source context.
5. Preserve current committed-source integrity checks: managed inputs and linked assets must match the exact commit used by rewritten URLs; incomplete/modified bundles must fail before destination writes. Do not import personal content or simply copy every Markdown file recursively. Preserve existing44-lesson legacy compatibility and84-lesson completeness validation.
6. Preserve `#nr01`, `#ns01`, `#no01` and incident/source fragments. The companions use explicit HTML anchors; the reader generates its own heading IDs and sanitizes rendered HTML. **Known blocker:** `markdown_engine()` currently sets `html=False`, so explicit `<a id="nr01"></a>` anchors become escaped text before sanitization. Implement safe stable targets and verify the actual final HTML; link rewriting alone is insufficient. Preserve existing protection against arbitrary embedded HTML rather than enabling it globally.
7. The destination has substantial preexisting uncommitted app/resume work, deleted CV files and untracked notes/profiles/tools. Record current status and protected hashes first. Do not stage, restore, delete, reformat, or claim ownership of that work. Extend the existing working versions of importer/app/test files with small focused diffs. Never overwrite personal progress, saved expansions, comments or other profiles.

## Actual read-only check from this chat

Executed with `PYTHONDONTWRITEBYTECODE=1` to avoid bytecode writes:

```sh
cd "/Users/robertovalencia/Documents/Business/Interview process"
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python tools/import_nodejs_aws_study.py --check
```

Exit1: `Node guides need refresh` for the index and13 numbered guides. This reports source-to-reader drift, not an import failure after writes. The destination virtual-environment interpreter exists. No import, app restart, browser check or destination test suite was run here. A separate fresh-context critic reviewed this handoff against the source map, destination importer and reader: accurate/actionable, with the concrete disabled-HTML anchor blocker above incorporated. That review does not approve an unimplemented import.

## Work to complete in the fresh chat

1. Extend the importer’s managed companion mapping and link rewriting, keeping the numbered curriculum assertion separate from supplementary-guide count. Preserve stable card IDs, priority, answers, implementation labels, lesson relationships, official references and recovery criteria. Do not rewrite or regenerate the questionnaire itself.
2. Add a clear “Node.js/backend interview and troubleshooting” group to the NodeJs/AWS path and a reader-local index link. Update the destination main README/import instructions. Links among companions and lessons should stay inside the reader where those guides are imported; external source/lab/download links must retain real commit provenance.
3. Add meaningful importer and rendering/navigation regressions: complete bundle; missing/modified companion rejected before writes; consistent committed asset links; stable existing IDs; destination preservation; read-only/idempotent `--check`; profile-scoped discovery/search; correct question/incident counts; and actual fragment targets after Markdown rendering/sanitization. Keep prior tests intact, including legacy behavior.
4. Run focused tests first, then the documented destination suites as appropriate:

```sh
.venv/bin/python -m unittest discover -s tests -p 'test_nodejs_aws_import.py' -v
.venv/bin/python -m unittest discover -s tests -p 'test_study_app.py' -v
.venv/bin/python -m unittest discover -s tests -v
node --test tests/test_app_navigation.js tests/test_comment_paste.js tests/test_resume_ui.js
```

5. Run the reviewed importer, then `--check`; a second run must be unchanged. Inspect `StudyLibrary`, actual rendered guide HTML, search and profile navigation. If the app is already running, establish its owner/process before restarting; do not kill an unrelated listener. Use a separate temporary local port for verification if necessary. Check the visible NodeJs/AWS reader and the questionnaire’s lesson/source/incident links without calling paid AI features.
6. Use an independent fresh-context critic to review the actual imported output, security/sanitization, failure paths, source integrity, profile isolation and preservation. Record actual results and the largest gap/repair. Only then describe the reader integration as complete and provide the observed local entry URL.

## Paste-ready new-chat prompt

> Work in `/Users/robertovalencia/Documents/Business/Interview process`. Read both projects’ AGENTS.md instructions, then read `/Users/robertovalencia/Documents/Business/linked-in-node-and-aws/docs/handoffs/node-backend-study-desk-2026-11-10.md`. Complete the authorized import of the existing137-question/24-incident Node.js/backend questionnaire into the searchable NodeJs/AWS Study Desk path. Extend the existing importer and navigation, preserve all lesson IDs/personal notes/other profiles/unrelated work, verify source integrity and real rendered anchors, run appropriate tests/import/check/browser verification, and obtain independent review. This is a fresh-chat implementation task; the previous chat only inspected the destination and prepared the handoff. Do not stop at a plan or a remote README link.
