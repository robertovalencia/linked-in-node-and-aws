# Independent curriculum review

Review dates: 2026-10-27–28. Reviewers: separate critic agents, not lesson builders. Status: source release approved after final repairs; expanded curriculum wins the content comparison. Actual Study Desk import, running-reader, preservation and final archive checks remain release gates.

## Scope and evidence boundaries

The review compares the proposed 84-lesson curriculum with the actual project, its working agreement, API contract, requirements and architecture. It checks broad AWS/Terraform coverage, clear prerequisites, mechanisms, practice and answered recall, accurate source attribution, and the distinction between existing implementation and new teaching examples. The review does not establish that cloud resources exist or that account-backed designs have been deployed.

The current pinned infrastructure has one EC2 host, a public subnet with outbound routing, a security group with no ingress rules, SSM access, ECR repositories, S3 artifacts and runtime-secret metadata. New service designs must remain explicitly illustrative. Adding an ingress rule is a grant of permission; a proposed public entry path needs narrow ALB-to-application-to-database trust and a requirement that justifies it.

## Findings and repairs

- Lesson 70 initially called the existing static shell script a template. The critic compared actual `user_data = file(...)` with the teaching text and requested a repair. The builder changed the text to explain that current `file()` reads a static script and that `templatefile()` is a separate new illustration.
- Lesson 65 used a universal alarm description for a metric-alarm example. After the critic checked current AWS alarm types, the builder labeled M-of-N/metric settings as a metric-alarm example; the repair was re-read and verified.
- Baseline assertions in lessons 68, 69, 80 and 81 lacked direct pinned project anchors. The builder added the requested source links, including a baseline architecture anchor in the capstone, and the critic verified the repairs.
- The handoff initially had no delivery evidence and correctly said it was only prepared. Subsequently the deployment owner acknowledged the user-delivered request and reported that its cost-first comparison had begun. The handoff and lesson 80 were updated to acknowledge delivery while retaining the pending cost report and expired-login re-verification limits. This does not establish approved implementation or provisioned resources. The handoff assigns actual costs/infrastructure to that owner and rejects deploying every named service merely to complete a learning checklist.

## Independently executed checks

- Existing foundation Terraform lab: passed create, idempotence, in-place update, replacement, moved address with preserved identity, three Terraform test runs and empty-state cleanup under Terraform 1.17.0.
- New advanced Terraform lab: passed 24 Terraform commands, 11 runner assertions and five Terraform test runs under Terraform 1.17.0. Structured plans confirm stable-key updates and a child-module address migration preserving all three resource identities. Cleanup leaves no managed local resources.
- Source review of both runners confirms credential-free local built-in-provider practice. The advanced runner copies its configuration to a temporary directory and removes ambient Terraform/cloud configuration variables. Neither lab exercises AWS provider behavior, remote backend authorization or live availability.
- New network reasoning lab: source reviewed and independently executed; 14 positive/negative checks passed with the source rule file unchanged. The test proves behavior of a deliberately partial TCP permission model; actual AWS group attachment, routing/NACL rules, listeners, TLS and application authorization remain untested.
- The earlier independent review read all forty new lessons in full. It executed nineteen credential-free lesson examples (44–63, excluding the public-network DNS/TLS exercise); the task-definition illustration was parsed as JSON without claiming semantic or deployment completeness. The DNS/TLS public-network example was not run. Final integration checks remain pending.
- Baseline hashes captured for 101 existing personal, comment and saved-expansion files before the final Study Desk refresh. Post-refresh comparison remains pending.

Raw critic evidence is retained outside the downloadable lesson pack in the working evidence directory: `work/cloud-full-curriculum-evidence/critic/`. It includes foundation command JSON, advanced command output, the saved-content baseline and a GET-only reader audit script.

## Primary documentation checked independently

The critic checked provider-module mappings and lifetime, optional non-null attribute defaults, sensitive redaction versus omission, and feature/version requirements against official HashiCorp documentation. Ephemeral variables, child outputs and resources require Terraform 1.10 or later; managed-resource write-only arguments require Terraform 1.11 or later and supporting resource/provider schemas. Current `terraform_data.store` documentation explicitly describes storing a write-only input in a resulting output, so an input flag alone cannot establish that all related values stay out of state.

- [Provider configurations in modules](https://developer.hashicorp.com/terraform/language/modules/develop/providers)
- [Type constraints and optional defaults](https://developer.hashicorp.com/terraform/language/expressions/type-constraints)
- [Sensitive and ephemeral mechanisms](https://developer.hashicorp.com/terraform/language/manage-sensitive-data)
- [Write-only requirements](https://developer.hashicorp.com/terraform/language/manage-sensitive-data/write-only)
- [Built-in data resource retention](https://developer.hashicorp.com/terraform/language/resources/terraform-data)
- [ALB security-group target trust](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/load-balancer-update-security-groups.html)


## Final independent comparison · 2026-10-28

The expanded curriculum wins against the previous 44-lesson path for the user's stated goal. The baseline gave useful project-grounded AWS/Terraform foundations but left major professional mechanisms outside its repository-limited scope. The expansion keeps those foundations and explicitly teaches governance/policy evaluation, ingress and private connectivity, DNS/TLS/ALB/CDN, managed compute/data/messaging, security/observability/recovery, and Terraform module/provider/state/team practices even when the old baseline did not implement them. It supplies labeled examples, failure reasoning, recall answers and local practice rather than treating absent resources as absent learning requirements. The finite core and specialist follow-on topics are explicit; the comparison is a review judgment, not a measured learner competency score.

The final critic independently confirmed:

- All 64 cloud lesson rows and 321 mapped concept entries exist. Lesson 44 now exposes the concept map as a readable 64-row linked checklist. These counts establish coverage structure, not mastery or equal depth for every concept.
- The repaired lesson 51 includes both collection and descendant paths for inquiries/providers and uses `/health/ready`, matching the contract at its pinned source commit. The small local route exercise produces 200/404 and clearly states its transport/runtime limits.
- The refreshed validator passes 84 lessons, 64 cloud lessons, 321 mapped concepts, 547 local links, 190 unique pinned source ranges and 31 exact excerpts. The packager selects all 84 numbered lessons and excludes personal notes and state/plan/cache files by its managed-input rules. Archive output still needs its release check.
- Seven importer shape/link/preservation regressions and three real-Git commit-integrity regressions were independently rerun successfully. They cover stable legacy IDs, complete managed input validation before writes, dirty managed documents/linked assets, unpublished linked assets and unrelated infrastructure edits. The importer verifies managed file bytes against the commit used for links; a directory link verifies its committed tree, without claiming every unlinked working-tree descendant is imported.
- The new navigation groups intentionally partition lessons 44–83 and preserve existing guide IDs. Actual running-reader verification after import remains pending and must not be inferred from source inspection.

The final pass requested removal of stale pending-cost/status wording in lessons 50, 80 and 83. The critic re-read those repairs: lesson 50 now identifies its historical pinned baseline, lesson 80 acknowledges the published cost report, and lesson 83 identifies bootstrap/final-plan approval and runtime gates as pending. The owner update establishes reported certificate issuance and published planning evidence only; it must not be broadened into applied application infrastructure or successful HTTPS/recovery/teardown evidence. Cost calculations and deployment remain owned by the other chat. The critic also inspected the release owner’s fresh full-app output: 48 tests passed; this is reviewed execution evidence, distinct from the ten importer regressions independently run by this final critic.

### Largest remaining gap

The largest learning-evidence gap is live AWS operational verification: most managed-service practice is intentionally small local models, code inspection or written design. These activities cannot establish effective IAM, actual ALB/ECS connectivity, RDS failover/restore, managed Kafka operation, or regional recovery. The curriculum truthfully marks those limits. Closing them requires separately authorized, selected runtime exercises and evidence from the deployment owner, rather than provisioning a service for every syllabus item. Reader/package/preservation checks are release gates, not substitutes for that future operational learning.

Source decision: approved for committing/publishing and importing the repaired curriculum. This approval does not pre-approve unrun reader or final archive checks; the final critic must review their actual results after import.
