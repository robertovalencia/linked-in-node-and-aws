# 8 · GitHub publication and Study Desk setup

[Previous: building and review](07-building-and-reviewing-the-study-path.md) · [Walkthrough index](README.md) · [Main learning path](../README.md)

## 1. A commit identifies a reviewed snapshot

The existing remote is the private repository `robertovalencia/linked-in-node-and-aws`. We published reviewed curriculum source at `46a7c8893d4d392602e32cdd2f34e1e10db2501f` and the final reader audit at `7b6baff63dab4e1c117fdbf9c748d41e591e7400`. These are historical release identities, not a claim that main will always point there.

Before adding a change, run `git status --short` and inspect the diff. Stage only the intended files. This project shares infrastructure work with another chat; a blanket commit can accidentally publish someone else's unfinished change or private output. A clean status does not prove a remote push succeeded: verify the remote revision too.

## 2. Understand the pull-request delivery route

For normal feature work: create a small branch → implement a requirement → run affected checks → review the diff → open a PR → address review → merge under repository rules. A PR is the review conversation plus proposed source change. Branch protection and required reviewers are server settings, not merely YAML files.

The recorded curriculum release used direct commits/pushes to main under the user's publication request. We do not invent a PR number, Jira issue or branch-protection configuration for it. [The toolchain guide](https://github.com/robertovalencia/linked-in-node-and-aws/blob/8cb1c13bc3e42f06930ce8c7f1bb6a8aa3c08b61/docs/toolchain.md) describes the intended team workflow and pending owner integrations.

## 3. Keep different GitHub checks separate

[Verify](https://github.com/robertovalencia/linked-in-node-and-aws/blob/8cb1c13bc3e42f06930ce8c7f1bb6a8aa3c08b61/.github/workflows/verify.yml) checks application source/runtime/infrastructure preparation. The separate [quality workflow](https://github.com/robertovalencia/linked-in-node-and-aws/blob/8cb1c13bc3e42f06930ce8c7f1bb6a8aa3c08b61/.github/workflows/quality.yml) needs its actual hosted Sonar organization, project and token. A successful local Sonar scan does not configure those hosted values. The latest observed missing-configuration failure was not bypassed or called a pass.

A new main push can cancel an older Verify run under its concurrency rule. Record the exact revision/run status instead of treating cancellation as successful completion. This walkthrough update does not claim that all hosted gates are green. Configuration files demonstrate intended automation; artifacts establish a particular execution.

## 4. Markdown is the authoritative study content

Numbered source lessons live in [generated](../generated); the index is [README.md](../README.md). The schema/coverage map is [cloud-coverage.json](../cloud-coverage.json). “Generated” means managed study content; it does not mean unreviewed or safe to overwrite personal files.

These supplementary walkthroughs stay under `walkthroughs/`. They are linked from the index and included in the ZIP without renumbering the 84 lessons. In Study Desk their links open commit-pinned GitHub files; they are not additional numbered reader guides. This keeps existing guide IDs and saved notes stable.

## 5. Set up the independent reader environment

The existing reader application is `/Users/robertovalencia/Documents/Business/Interview process`. It has its own `AGENTS.md`, `README.md`, requirements and local virtual environment. It is not part of the Node runtime.

For a fresh reader environment, follow that application's README. It uses Homebrew Python 3.12:

```bash
cd '/Users/robertovalencia/Documents/Business/Interview process'
/opt/homebrew/opt/python@3.12/bin/python3.12 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

Those first-time commands are unnecessary when its working environment already exists. Reading/searching needs no AI API key. Optional AI tutoring requires separately configured credentials in the app's ignored `.env` and can incur charges; no paid calls are part of this setup walkthrough.

## 6. Import only published, committed inputs

Run from the reader application's root after the Node source commit has been published:

```bash
.venv/bin/python tools/import_nodejs_aws_study.py
.venv/bin/python tools/import_nodejs_aws_study.py --check
```

The importer checks managed files/manifest and directly linked file bytes against the Git commit used in links; directory targets must exist in that commit. It validates the complete import plan before writing. A missing or dirty managed input fails rather than publishing a misleading source link. Unrelated infrastructure edits do not block study imports.

It updates only the Node profile's managed index and 84 lessons. It rewrites internal lesson links into reader routes and source/lab/supplement links into commit-pinned GitHub links. `--check` reports drift without writing. A new HEAD can legitimately refresh link targets even when prose stays the same.

The reader tooling belongs to the separate app checkout; it is not secretly bundled as a standalone application in this repository's study ZIP. The ZIP is useful for offline Markdown/lab study without that app. The importer preserves personal notes, saved expansions/comments and other interview profiles; do not copy generated material over those directories manually.

## 7. Start and verify the reader

```bash
.venv/bin/python tools/study_app.py serve --port 8765
```

Open `http://127.0.0.1:8765` and choose **NodeJs/AWS**. The main syllabus is `/guide/nodejs-aws--44-cloud-complete-syllabus-and-mastery-map`; the index is `/guide/nodejs-aws--study-index`. Stop an old server normally before restarting on the same port; a bind error can mean another working instance already owns it.

Verify a foundation guide, a new professional guide, a walkthrough GitHub link and scoped search. Check that saved notes are still accessible. The recorded release's [independent audit](https://github.com/robertovalencia/linked-in-node-and-aws/blob/8cb1c13bc3e42f06930ce8c7f1bb6a8aa3c08b61/docs/evidence/cloud-study-release-2026-10-28/independent-audit.md) documents the 85-guide result and 166 preserved files. Source tests and a real reader audit provide different evidence.

## 8. Keep the setup reproducible

When lessons change: review source → validate links → rebuild ZIP → commit/push → import → run `--check` → inspect the reader → record evidence. If navigation code changes, restart the app. Keep infrastructure costs/deployment with the designated owner, and treat state/private plans as operational data rather than lesson attachments.

**Understanding check:** Why must a new linked lab file be committed before import? Why can the ZIP work without Study Desk? Which source files may be refreshed, and which saved content must remain untouched?


## Copyable command workbooks

Follow [09 · local Terraform commands](09-terraform-local-commands.md) for the executable learning sequence, then [10 · the AWS operator command workflow](10-terraform-aws-commands.md). Every step states its directory, purpose, expected result and execution boundary.
