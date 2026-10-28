# Independent process/setup walkthrough review — 28 October 2026

**Decision: APPROVE.** The supplementary walkthrough is suitable for publication without changing the 84 numbered lesson IDs. No blocking defect remains in the reviewed staging overlay.

## Scope and source verification

Reviewed all nine walkthrough Markdown files (index plus chapters 01–08), index/roadmap/syllabus/lesson80 links, requirement and traceability additions, and packaging/validation changes. Compared their claims with actual README, package.json, setup-local.sh, local.sh, local setup/testing/toolchain guides, the 28 October HTTPS review, free-hostname guide, certificate issuance receipt, three local-lab READMEs and the independent reader importer/README/serve CLI.

The main operational boundaries are accurate: the recorded certificate is ISSUED and unused; bootstrap has five proposed creates; HTTPS has 111 proposed creates and zero application tasks; neither new infrastructure plan is applied. The local-backend HTTPS preview is explicitly unsuitable for final apply. Certificate state remains separately preserved. Current costs and account operations belong to the deployment owner. The walkthrough performs no AWS operation or paid API call.

## Largest gap and repair

The first local-check sequence referred readers to backend/frontend dependency installation located only in the optional hot-reload route. A beginner following integrated containers could reach check/test/build with no host dependencies. Reported this to the builder. Chapter 02 now explicitly runs both `npm --prefix backend ci` and `npm --prefix frontend ci` before checks. Root `npm ci` and Chromium installation are separately explicit before browser checks. This resolves the reproducibility gap without changing runtime code or relaxing any check.

Also requested normal spacing around lesson/resource/test counts; the builder normalized the staged prose. The hostname chapter correctly labels the older guide’s price snapshots as historical and points to the newer 28 October report.

## Independently reproduced checks

- All 362 relative links in the initially completed changed Markdown overlay resolved against staged/source files.
- Ran the final overlay validator independently against real Git source: 84 lessons, 64 cloud lessons, 321 concept entries, 663 local links, 190 pinned source ranges and 31 exact historical excerpts passed.
- Independently opened the final ZIP: 123 unique members, including all nine walkthrough files and 84 numbered lessons. Every archived file byte-matched overlay source. No personal/saved/comment directories, Terraform cache/state/plans or Python caches were present.
- Confirmed the separate reader setup and serve commands against its actual README and CLI. Its importer retains 84 managed lessons plus index; supplementary walkthrough links intentionally become commit-pinned GitHub destinations. No importer/reader application change is required.

## Limits and remaining publication checks

This review is of the complete local publication overlay and source facts. It does not claim a remote push, new hosted CI result, final committed reader import, live AWS deployment or newly run application suite. After committing/pushing, the publisher must refresh the committed reader import, run `--check`, inspect the new pinned GitHub entry-point destinations and compare the protected study-file baseline. Those are publication checks, not outstanding content defects.
