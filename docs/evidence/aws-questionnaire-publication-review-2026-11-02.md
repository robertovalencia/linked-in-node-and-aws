# Independent questionnaire publication-candidate review · November 2, 2026

**Decision: PASS for the reviewed documentation-only candidate.** This approves the candidate's content, portability and local evidence scope. It does not claim that a commit, push, hosted CI run, live reader import or AWS operation occurred.

A separate critic reviewed `work/aws-questionnaire-task/publication-candidate`, reconstructed from Git HEAD `7e778a01d6be739feafda36e17df8d42095f79f1` plus the intended learning deltas. The real checkout was read only. The critic did not stage, commit, push, access secret values or operate AWS.

## Publication-specific gap and repair

The largest new gap was portability: five dated-evidence cards referenced two original deployment records that were untracked and would be absent in a clean published checkout. The repair preserves exact full dated copies inside `docs/nodejs-aws-study-path/evidence/questionnaire-records/`, records their original paths and SHA-256-at-inspection provenance, links those portable copies, and validates their hashes, symbols and excerpts. If an original is present, the checker also requires it to match; missing original files are allowed only for these archived dated records. Current-source cards still require actual source and cannot silently fall back to an archive.

The critic independently compared both archived reports with the actual original records: bytes and recorded hashes match exactly. All five dated cards validate from the clean candidate with their original paths absent. The reports remain dated historical observations; preservation does not turn their AWS statements into present-day inventory, current costs or new execution evidence. They contain sanitized records and no secret values. Their Markdown links remain valid without rewriting the archived bytes.

The publication guide now distinguishes the initial local-only review from later separately recorded Git publication. It does not claim that local validation updates the live Study Desk reader. The prior reference/glossary/custom-NACL repairs remain intact. Security, ownership, health, event-delivery and recovery explanations retain the conclusions of the original independent review.

## Independent execution and output

From the clean candidate, with bytecode writes disabled:

```text
PYTHONDONTWRITEBYTECODE=1 python3 scripts/check-cloud-study.py --repository .
PASS:84 lessons;64 cloud lessons;321 mapped concepts;902 local links;
279 pinned source ranges;31 exact historical excerpts.
Companion:30 questions;12 incidents;42 source excerpts;60 distinct mapped lessons;
202 companion local links;4 absent-feature examples.

PYTHONDONTWRITEBYTECODE=1 python3 scripts/check-aws-questionnaire.test.py --repository .
Ran26 tests:OK.
```

The critic also independently ran the full checker from the candidate against the actual original checkout; it passed with the same counts, establishing the matching-original branch as well as clean-checkout portability. New meaningful regressions reject missing/corrupt archived evidence, conflicting available originals, archived substitution for current source, and missing current source. The archive-path containment guard was inspected in source; no separate archive-path escape probe is claimed. Prior card-specific source, fragment, mapping, absent-example, recovery-criterion and personal-exclusion regressions still pass.

Independent archive inspection verified152 unique members, exactly84 numbered lessons and byte equality for every member. Against the147-member HEAD archive, no member is removed; only the existing README changes; exactly the questionnaire, map, context and two dated records are added. Personal/saved/comments/state/plan/cache exclusions remain intact. All84 numbered lesson files match HEAD byte for byte.

## Intended change boundaries

The critic inspected the shared-file diffs against HEAD: root README adds questionnaire navigation; requirements adds only the R12 questionnaire acceptance subsection; traceability changes only the R12 row; reviews appends the questionnaire review entry. Those shared candidate files exclude the original worktree's unrelated deployment changes. The remaining candidate changes are study navigation/content, exact archived learning evidence, offline validators/regressions and the managed ZIP. No runtime, infrastructure, workflow, package/dependency or protected personal-content change is part of this candidate.

The original review/validation records remain historical records of the earlier150-member/20-test stage; this followup records the newer152-member/26-test clean publication candidate. Any later publication outcome must be reported from actual Git results. Post-review staging must include only the intended learning files, preserve the reviewed bytes and leave unrelated worktree changes untouched. No application npm/HTTP acceptance or cloud execution is claimed by these documentation checks.
