# 7 · How we built and reviewed the learning path

[Previous: deployment](06-deployment-security-and-operations.md) · [Index](README.md) · [Next: publication and reader](08-publishing-and-study-desk.md)

This chapter records the process used to produce the study material. It distinguishes preserved history from checks newly performed for a particular release. The [independent release audit](../../../docs/evidence/cloud-study-release-2026-10-28/independent-audit.md) is the concrete evidence for the 84-lesson expansion.

## 1. Start from the working reference

The migration used existing product flows and architecture as its reference. For the curriculum, we read source, contracts, tests, existing Node study notes and the related project chat before setting the learning scope. A requirement such as “explain how inquiries survive retry” is more useful than “mention Kafka.” The first describes a mechanism the reviewer can inspect.

[Requirements](../../../docs/specs/requirements.md) define acceptance; [traceability](../../../docs/traceability.md) connects it to code/tests/evidence. Those documents also preserve earlier project stages. We do not treat an old Java-project test result as evidence for Node source.

## 2. Protect source and personal learning data

The Node project remains independent of Java and Python. Lesson work was staged in separate working directories, reviewed there, then copied only into owned source paths. Existing study notes, saved expansions, comments and other profiles were hashed before the reader import.

A **hash** is a compact content fingerprint. Comparing it before and after detects byte changes. The final audit compared 166 protected files and found none changed. This proves preservation for that captured set, not a general backup/recovery guarantee. Actual credentials/state were excluded from publication.

## 3. Expand the scope when the learning goal changes

The first 20 lessons cover application foundations;20–43 add AWS/Terraform foundations;44–83 extend the professional core. The [coverage manifest](../cloud-coverage.json) declares 84 numbered lessons, 64 cloud lessons and 321 concept entries. [Lesson 44](../generated/44-cloud-complete-syllabus-and-mastery-map.md) renders the concept checklist for a human reader.

The user asked to learn important concepts even without corresponding project resources. We therefore kept source-grounded walkthroughs and added explicitly illustrative examples, instead of claiming absent ALB/MSK resources were already deployed. Specialist follow-on topics remain explicit; a finite syllabus is not a promise to cover every future AWS feature.

## 4. Give each concept an observable learning task

Lessons combine a mechanism, an actual source anchor or labeled illustration, a practice task, expected observations, failure reasoning and answered recall. The distinction matters: “run Terraform” is vague; “change a map value and observe that the resource ID stays stable” gives a judgeable result.

The three local labs inspect Terraform lifecycle, module identity and partial network-permission reasoning. They require no cloud credentials. Their [source](../labs) is included so a learner can inspect what happens before executing it. Importantly, a built-in-provider test cannot prove an AWS permission or database failover.

## 5. Separate the builder and the critic

Builders drafted small lesson groups and examples. Separate critics inspected actual source, ran examples/labs and compared the expanded path against the prior path. The goal was to find the largest remaining gap and repair it, rather than have the author approve their own explanation.

Concrete repairs included ALB example paths that did not match the API contract, confusion between static `file()` loading and `templatefile()`, and stale cost/deployment status. See [reviews](../../../docs/reviews.md) and [the curriculum critic report](../evidence/full-curriculum-critic.md). This comparison was a reviewer judgment, not a measured learner exam score. A blind visual comparison was not claimed for text whose project links reveal its source.

## 6. Keep failures and their meaning

The advanced lab's first fixture accidentally inherited scenario inputs; its test exposed that problem, and the fixture was made explicit. Two reader tests initially failed because the sandbox blocked binding a local HTTP socket. They passed after a permitted loopback rerun; the checks were not removed. An attempted local example that required unavailable networking was replaced/labeled appropriately, rather than reported as passed.

Nineteen AWS-lesson example checks passed during the recorded expansion; the public DNS/TLS exercise was explicitly not run in that review. A command failing because of environment restrictions differs from a behavioral assertion failing. Both need honest records and an appropriate next step.

## 7. Validate the lesson pack before publication

From the repository root:

```bash
python3 scripts/check-cloud-study.py
python3 scripts/package-node-study.py
```

The validator checks contiguous lessons, coverage, Markdown targets, pinned source ranges and exact historical excerpts. The packager includes managed material, labs and evidence while excluding personal notes/state/plans/caches. A green validator proves those checks, not factual correctness of every sentence. Independent source review supplies a different form of evidence.

The recorded expansion audit passed 84 lessons, 547 local links, 190 pinned source ranges and 31 exact excerpts. Supplementary setup chapters can increase link counts without adding numbered lessons. Archive inspection separately compared every member with source.

## 8. Say precisely what was verified

The expansion's actual reader tests passed 36 general,12 Node and6 Python-profile regressions, plus 11 JavaScript navigation/editor checks. The independent reader audit verified 85 guides including the index, internal destinations, scoped search and note preservation. Those counts belong to that release; a later guide does not inherit proof automatically.

Live AWS operations remain the principal learning-evidence gap. The other chat owns the cost and deployment work needed to close selected gates. Local teaching material must not quietly rewrite “planned” into “deployed.”

**Understanding check:** Which check could catch a broken Markdown target? Which could catch a false claim about an AWS resource? Why is an independent reviewer useful even when every automated check passes?
