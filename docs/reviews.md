# Builder and independent critic record

The migration was split into backend, frontend and infrastructure pieces. A separate critic inspected each piece with the real reference contract, executable evidence and running software where available. The reviewers named defects before the final pass; the root and builders repaired them without weakening the 48-check baseline. A visual comparison was handled separately because screenshots require matching viewport and scroll state.

| Piece | Builder result | Independent critic decision and evidence | Largest remaining gap |
|---|---|---|---|
| NestJS/PostgreSQL/Kafka | Four service processes, versioned migrations, owner checks, transactional inquiry/outbox and deduplicated notification inbox | **Win for migrated local backend.** [Review](evidence/backend-critic.md), [48-check API result](evidence/local-acceptance.json), [adversarial probes](evidence/backend-adversarial.json), [restart drill](evidence/failure-drill.json) | Production key rotation, poison-event operations and high availability are outside this dev portfolio |
| React/TypeScript | Separate components, services, routes, types, contexts and hooks with controlled regressions and real desktop/mobile journeys | **Win for repaired source and regression scope.** [Original findings](evidence/frontend-critic.md), [recheck](evidence/frontend-critic-recheck.md), [browser result](evidence/browser-smoke.json) | Assistive-technology testing and a real browser provider editing/status journey remain for a later pass |
| Terraform/CI/release | Isolated AWS dev definitions, OIDC, ECR images, release automation and setup guides | **Win for prepared infrastructure scope only.** [Review](evidence/infra-critic.md), [Terraform test](evidence/terraform.txt), [release fixtures](evidence/infra-remote-orchestration.json) | Real account plan, provisioning, SSM deployment, cloud smoke and rollback await an AWS account and approved billable plan |
| Visual comparison | Preserved the reference visual language and refactored presentation code | See the [blind visual review](evidence/visual-critic.md) for its separate verdict | Still screenshots cannot prove interaction or accessibility |
| Local SonarQube repair | 24 new failure-path and lifecycle tests, pinned scanner image, exact CE/analysis gate lookup and short-lived token cleanup | **Win against the unchanged local 80% gate.** Independent critic queried live analysis `bff6bec1-c67f-4b1b-900e-fc63d704c5ea`: 82.3% new coverage, 0% duplication, 0 new violations; 64/64 Jest and 48/48 HTTP checks pass. [Review](evidence/local-sonar-critic.md) | Hosted Sonar Cloud main/PR analysis is pending account setup; frontend editor has 25 uncovered lines |
| Hosted SonarQube setup | Free EU Cloud URL, variable-driven project identity, token gate and same-repository PR trigger | Independent critic found no static blocker after the PR trigger repair; local scanner remains separate | Cloud organization/project/token and actual hosted main/PR gate runs remain unverified |

The fresh Git-aware local Sonar scan first failed at 62.6% new coverage. The builder added meaningful authentication, ownership, transaction, migration and Kafka failure-path tests; the critic checked the running server and token lifecycle. The final scan passed the same 80% threshold. The failed gate is retained as evidence, and local success is not treated as a hosted result.

The hosted SonarQube critique found that the first workflow ran only on `main`, leaving PR feedback absent. A same-repository PR trigger was added with a fork guard so untrusted fork code cannot receive the token. The critic rechecked the static workflow and documentation; the actual hosted gate is still pending account setup.

The first frontend critique found late login completion after dismissal, lost-response inquiry retries that could change idempotency identity, stale notifications and dead-end editor loading. The recheck identified two further inquiry reconciliation errors: historical same-content inquiries were treated as proof of current delivery, and an auth failure on a later retry could discard the original key. Both were repaired and covered with focused regressions. The critic's 18/18 focused rerun and the root's full 28/28 suite are recorded separately.

The backend critic reproduced the stale nginx upstream failure after container recreation. The repaired DNS resolution passed the unchanged nine-check drill. The infrastructure critic reproduced retained fetched secret JSON after a failed remote deployment. The absolute cleanup trap now passes both fake-CLI scenarios; a separate Amazon Linux package probe corrected the `awscli-2` bootstrap package name. These review records show the correction path and the limits of each check.

The [requirements](specs/requirements.md), [implementation plan](specs/implementation-plan.md), [acceptance contract](../CONTRACT.md), [traceability table](traceability.md), [raw results](results.md), and [Codex prompts](prompts/builder.md) make the chain from requirement to implementation and test inspectable. No percentage of AI-authored code was measured; the role's approximately 95% target is presented as a workflow target, not an attribution claim.


## 2026-10-22: NodeJs/AWS study path and beginner service documentation

Added twenty sequenced lessons, the roadmap, coverage matrices, an unchecked progress template, and the complete offline ZIP. The main README links both the browsable study path and download. Six service guides explain runtime wiring, each capability, browser/event/AWS flow, debugging labs, and vocabulary.

The completed independent content reviews found missing concurrent-request teaching and a missing authored UI-to-API exercise. Repairs added the two-request lock/commit trace and local retry lab, plus a proposed minimum-rate UI-to-Zod/SQL feature. Final source and coverage reviews accepted the materials; the review loop was stopped at the user's request. The architecture summary now accurately describes temporary inquiry recovery data in sessionStorage and notification-table event deduplication.

Publication checks: the ZIP integrity test passed, the browsable lessons and source links were checked locally, and no application behavior or infrastructure was changed. Learner Docker/AWS labs remain instructions rather than execution claims.


## 2026-10-22: Technical concept revision requested by the learner

Rewrote the twenty lesson files around individual mechanisms, with short What/How explanations, actual code excerpts, common traps and recall questions. Added four service-specific technical handbooks. The Interview Process lessons and repository lessons use identical content. Existing personal notes, saved expansions and comments were preserved.

Code links use a fixed inspected commit and verified line ranges. Existing practical walkthrough code blocks were preserved while their long prose was split. The new archive mirrors the repository documentation layout. The earlier critic loop remains stopped; this revision uses direct source, rendering, link and synchronization checks, with no claim of a new independent review or executed cloud lab.


## 2026-10-23: Free plan AWS preparation

The user selected a 24-hour demonstration using available Free plan credits, followed by complete teardown. Account-specific inspection confirmed the usable region as `us-east-2` and `m7i-flex.large` as Free Tier eligible with 8 GiB RAM. IAM OIDC-provider operations were denied by an AWS-managed service control policy. Rather than changing account plan or trust, the user selected GitHub source/runtime/Sonar verification and deployment from a temporary local AWS login.

The Terraform builder replaced the `t3.medium` default/example with `m7i-flex.large`, omitted CPU-credit options for non-T families, and retained `standard` mode for explicit T-family overrides. The critic reviewed the default/T3 tests and requested an exact GitHub trust assertion; it now checks the repository dev environment and STS audience. The builder also corrected a misleading “fixed-performance” comment to “non-T,” because Flex instances have baseline/burst behavior. Optional GitHub deployment remains the default compatibility mode; the selected local example explicitly disables its IAM deploy role/policy and does not require an OIDC ARN. Host instance-role and SSM security controls remain unchanged.

Fresh local Terraform validation passed with five aws-dev mock runs and two bootstrap mock runs. Assertions cover both deploy modes, missing-OIDC rejection in GitHub mode, no ingress, IMDSv2, disk cleanup, private encrypted/versioned state, transport enforcement, and opt-in OIDC creation. Bootstrap's mock-only apply resolves computed ARNs for the TLS assertion; it does not create AWS resources. Actual account-specific preparation produced a five-create bootstrap bucket-only plan and a 21-create local-backend dev preview. Neither was applied. The final S3-backed dev plan must be generated and reviewed after approved bootstrap.

The largest remaining gap is live execution: fresh verification-only CI, final S3-backed plan approval, actual deployment, 48-check AWS acceptance, and cloud rollback are not established by source/mocks/plans. Hosted Sonar Cloud remains configured but pending. The critic found that describing the fresh temporary CI server as an evaluated new-code gate was inaccurate: it has no baseline. The documentation now distinguishes copied unchanged Sonar Way new-code conditions from the added mandatory overall conditions. Local isolated execution passed at 82.3% overall coverage, and a negative 0% coverage run failed the same 80% gate; fresh GitHub execution remains pending. No provisioning start time or teardown schedule is claimed. Further critic findings and fresh CI evidence must be recorded as they occur.


### Backend runtime image vulnerability repair

The predeployment local amd64 image scan rejected the old `node:22.22.0-alpine` runtime with 59 High/Critical findings across Alpine libraries and bundled package-manager modules. The failed report is retained separately. The builder verified the current official Node 22 Alpine image through Docker's registry and pinned both stages to `22.23.4-alpine3.24` with immutable index digest `sha256:fe4f6d74e20370acb04ad889077d14d0f64a9c8ea6a42bc60cddf1e844699914`. Unused npm, Corepack, and Yarn files/symlinks are removed only from the final runtime; application dependencies and direct non-root Node execution remain.

A fresh linux/amd64 archive built successfully and passed Trivy 0.76.1 with **zero High/Critical findings**, using the same fail-on-High/Critical flags and `--ignore-unfixed=false`. No exclusions, applicability waivers, or weaker gates were added. The exact loaded image ran as UID 1000 under Node v22.23.4, loaded NestJS/PostgreSQL/Kafka/JWT/Zod dependencies, retained compiled code/migrations/seeds, and completed a scrypt probe. See [the image-security evidence summary](evidence/backend-runtime-image-security.json) for hashes, exact commands, and verification limits. Independent review and a fresh complete CI/business-journey run remain separate gates; no image was published to AWS during this repair.

The first final preparation CI run [39973393337](https://github.com/robertovalencia/linked-in-node-and-aws/actions/runs/39973393337) caught two attribute-alignment errors in the new local-mode Terraform test. The repair changes formatting only; the exact recursive formatting check passes and all assertions remain. Fresh exact-source CI is required after the correction.

## 2026-10-26: Independent AWS/Terraform curriculum review

The independent critic read all 24 new lessons (20–43), their real Terraform/workflow/script sources and the isolated built-in-provider lab. The source is **approved for documentation publication and local learning scope**. Independent checks verified 51 pinned source ranges, 40 adjacent source fences, and all 27 local Terraform CLI invocations with their expected exit codes, including three configuration test runs, replacement/move identity assertions and empty-state cleanup. The builder's separately recorded AWS-provider mock output passed two bootstrap and five aws-dev runs; it is not described as an independent duplicate execution or a cloud test.

The largest teaching gap was a rollback excerpt that showed only a success message. Lesson 41 now exposes the actual failure/restore branch and release-pointer update. Review also repaired S3 lock-object permissions/dependency-lock distinctions and prose spacing. The [full critic review](nodejs-aws-study-path/evidence/critic-review.md) records evidence and limits. The largest remaining delivery check at this source-review point is study-app import/runtime validation, especially rewriting nested lab links to the newly published immutable GitHub revision. No AWS provisioning, integration success or teardown schedule is claimed.


## Independent dependency-security review, 2026-10-26

The critic approved the minimal compatible dependency repair: exactly two resolved package entries changed, NestJS 12.2.0 remains, and all existing application/test source is unchanged. The critic independently checked the installed tree and reran the 64 backend tests, then inspected actual zero-audit and 48-check runtime evidence plus the preserved fail-closed gates. [Detailed review](evidence/ci-security-repair/critic.md). The largest remaining gap is hosted SonarCloud owner configuration; a fresh published-commit Verify outcome must be observed separately rather than inferred from local passes.


## 2026-10-27: Cost-first phased AWS redesign review

Prepared an independent cost/architecture packet for the existing zero-ingress EC2/SSM design versus proposed hardening, ALB/TLS, private ECS/RDS with explicit Kafka and DNS dependencies, NAT/endpoints per AZ and optional MSK. Renewed authorized AWS login and performed read-only checks: FREE/ACTIVE/$100; no project resources found in queried scopes; MSK/OIDC explicit SCP denials; Ohio Logs read succeeded. No secret values, account upgrades, paid-service enablement, Terraform source changes or AWS mutations.

Separate architecture and regional-price builders supplied drafts; a fresh critic independently inspected the real source and executed a Decimal audit. Material repairs: retained Kafka cost in ECS alternatives, full replicated higher-use MSK storage, correct charged cross-AZ SKU, private DNS/Cloud Map costs, and complete endpoint/account caveats. All 42 platform and six streaming cases, itemized totals, artifact links and both private saved plan hashes passed. See [review record](aws-cost-review-2026-10-27/critic.md) and [reproducible audit](aws-cost-review-2026-10-27/critic_audit.py).

Fresh local-only saved plans bind unchanged source 8b2c3e0: bootstrap five creates; dev local-backend preview 21 creates, zero ingress, Ohio, no OIDC. Plans/state remain ignored under work/aws-cost-review-2026-10-27; only sanitized summaries are published. A scratch backend override syntax error was corrected; provider schema inspection required normal local permissions. Neither preparation issue changed infrastructure source. No inherited test evidence is claimed as new cloud execution.

The critic recommends proposed phase A at $3.21 expected/24h plus about $0.11 restore rehearsal, with an approximately $4 planning allowance rather than a hard cap. Biggest remaining gap: owner-selected cost scope, hardened implementation and a fresh final S3-backed plan, followed by real cloud security/recovery/48-check evidence and teardown. Cost/design review readiness does not authorize provisioning. The study-path directory and learning/import tools were not edited.

## 2026-10-27: Selected ECS/RDS/NAT preparation review

Separate runtime and Terraform builders implemented the selected scope, with a fresh critic independently inspecting current source, running software and executable evidence. Initial independent checks reproduced 88 backend tests, 29 PostgreSQL TLS/ownership/replay checks, nine Kafka checks and the initial eight Terraform runs. The final review reran the expanded 30 PostgreSQL checks, 10 ECS plus two certificate mocks, 21 publisher contracts and five real nginx DNS/configuration checks. Cost ledgers were independently recomputed against the dated tariffs.

Repairs included password-bearing failed SQL suppression in PostgreSQL server logs, safe no-hostname staging, separate optional certificate request, the isolated ECS state key in publisher contracts, and a DNS fixture with an explicit disposable subnet and proof of a changed IP. The critic reproduced an unsafe inline public SSH rule being accepted by the first offline auditor. That auditor now rejects inline/legacy SG rules, checks ports independently of unknown SG IDs, compares saved source/lock bytes and actual binary-derived JSON, and fails under Python optimization; repeatable negative controls retain the regression. A stale pre-repair plan was regenerated from the final Terraform source.

The [final independent critic](evidence/ecs-preparation/critic.md) approves preparation review only. Hosted CI status is tracked separately in publication evidence; configuration/local passes alone do not establish them. The largest remaining gap is live cloud execution after an owned hostname/issued certificate, final S3-backed plan/cost approval and exact-source verified images. No AWS mutation, credential upload, domain purchase, upgrade or public listener was performed. The learning chat’s study-path/import files remain untouched.

### Hosted Linux fixture correction

The first new hosted Verify run [40586119114](https://github.com/robertovalencia/linked-in-node-and-aws/actions/runs/40586119114) passed source and Terraform jobs but failed PostgreSQL fixture startup. [Original failure log](evidence/ecs-preparation/ci-linux-fixture-before-repair.txt). The release-verification run40586117577 hit the same fixture. Linux preserves a host temporary directory’s 0700 ownership; after dropping to PostgreSQL’s UID the HBA file still under that mount was unreadable. The fixture now copies HBA alongside TLS files into a PostgreSQL-owned container path and keeps HBA/key permissions0600, with shell fail-fast. The full30localchecks pass unchanged. Hosted results for the successor revision must be observed separately; the failure is retained rather than relabeled as success. Application/Terraform behavior did not change for this correction.

### Final KMS request accounting correction

Final official-price recheck found that the otherwise zero customer-managed-key scope did not account for billable AWS-managed-key API use. The current ledger adds a separate symmetric-request meter using the already retrieved Ohio rate $0.000003/call, one call per modeled Secrets read plus100storage/lifecyclecalls per24h as an explicit unmeasured allowance. It deducts no shared free allowance. No key-month charge or infrastructure change is introduced. This raises expected staging to$6.71/24h/$187.40per720h and future activation to$8.32/24h/$235.68per720h. The original critic numbers remain historical in its initial section; its final appendix reviews this correction.

## 2026-10-27: Free hostname for the existing ALB design

Prepared a dynv6 free-zone path for the temporary HTTPS ALB test, preserving the selected topology and AWS estimate. Primary provider documentation supports free hostnames, CNAME/CAA and underscore labels; primary AWS documentation defines validation/issuance gates. Independent public and authoritative DNS checks returned NXDOMAIN for the candidate and no parent CAA answer. Neither proves zone availability/control or ACM issuance.

The [independent critic](evidence/free-hostname/critic.md) approves documentation/preparation scope. The guide keeps the app CNAME below the zone apex, checks the exact final owner/target instead of assuming provider form parsing, requires ACM ISSUED before paid infrastructure, preserves approved CIDR restrictions and removes dangling DNS on teardown. The owner must create/confirm their provider account and reserve an actual zone; no credential was requested. Provider record writes, certificate request, ALB creation and HTTPS testing have not occurred. The largest remaining gap is registered zone control followed by actual certificate validation.

## 2026-10-27: Registered free zone and concrete certificate request review

The owner’s signed-in dynv6 zone list/status verifies `linked-in-node-rv.dynv6.net`; public DNS and provider-authoritative SOA now resolve. An initially stale new-zone form was left open after reservation. A duplicate submission was rejected as taken; inspection of My Zones found the existing owner reservation. No provider record was changed. Personal contact/address values were omitted from repository evidence.

Prepared an ignored local-backend certificate-only plan for `app.linked-in-node-rv.dynv6.net`: exactly one create, DNS-validated nonexportable public ACM certificate/RSA2048 in Ohio. Saved-source/provider-lock bytes and binary-derived JSON agree. The two existing mock safeguards pass. [Sanitized review receipt](evidence/certificate-request/plan-review.json). Actual AWS identity was checked before planning; apply must recheck account772641336063 because the root does not encode an allowed-account constraint. No AWS mutation occurred. The [fresh independent critic](evidence/certificate-request/critic.md) approves user-review readiness only and confirms the real binary/source/JSON/count/domain/export/region/hash checks. Apply requires the same effective credentials for STS and Terraform, not a mismatched CLI-only profile override. The largest remaining gap is approval/request, the actual provider CNAME and ACM ISSUED; infrastructure remains unprovisioned.

## 2026-10-27: Approved certificate request and actual DNS issuance

The human approved requesting and DNS-validating the concrete one-certificate plan. Root verified the original saved-plan SHA256/source/provider lock, no existing same-name certificate, and STS account `772641336063` in the exact same credential environment inherited by Terraform. The approved apply added one certificate, changed zero resources and destroyed zero resources in Ohio. The actual ACM CNAME was saved in the owner's existing dynv6 zone; no guessed token or private provider credential was used. Live ACM reports ISSUED, DNS SUCCESS and export disabled. Three DNS resolvers match the exact record; post-issuance Terraform planning returns no changes. [Execution evidence](evidence/certificate-request/issuance.json).

The [fresh operational critic](evidence/certificate-request/issuance-critic.md) independently checks the live resource/DNS, isolated one-resource state and scope. The certificate is unused (InUseBy empty) and renewal currently INELIGIBLE; this is not ALB/app/automatic-renewal readiness. Request-phase state may still show pending, so authoritative live ACM status is retained separately. Preserve the private local state until migration/destroy; it is not disposable work output. No application resources or public application endpoint were created. Largest remaining gap: approved client CIDRs, state bootstrap/fresh final infrastructure plan/current costs, followed by actual deployment and cloud security/recovery/48-check proof.

## 2026-10-28: HTTPS/CIDR and state-bootstrap plan preparation

The user approved one client /32 for plan preparation only and renewed temporary login for read-only checks. The issued certificate remains valid; Free/ACTIVE/$100 and no app infrastructure were observed in queried scopes. State bucket is absent. Actual saved plans propose five bootstrap creates and 111 HTTPS infrastructure creates, with zero updates/destroys and no app tasks. The local preview is not a final S3-backed apply plan. No Terraform/app definitions, old evidence or learning-owned files were changed.

A separate price builder refreshed all 31 selected Ohio prices/units and documented TLS probe consumption plus a shared-meter S3 state carveout. A fresh critic independently decoded both binaries/source snapshots, recomputed all 12 ledgers and reproduced three checker bypasses. The actual source/plan was safe; the checker now binds SG owner/peer IDs, unknown flags, references/for_each maps and ALB/listener/host-rule/frontend routing. It also rejects nonprivate plan inputs; files/directories were repaired to 0600/0700. Both suites first accept the valid actual plan, then pass 23 HTTPS / 11 legacy negative controls including the original bypasses. [Evidence](evidence/aws-https-plan-2026-10-28/README.md). The operator policy draft remains unattached with 12 wildcard warnings.

The largest remaining gap is approved state bootstrap followed by the actual locked S3 backend and freshly reviewed final infrastructure plan/current costs. Image publication/bootstrap/app activation, actual cloud health/security/restore/rollback/48-check smoke and teardown are still unverified. Scope/cost review is not authorization to provision.

The [final independent HTTPS-plan critic](evidence/aws-https-plan-2026-10-28/critic.md) approves preparation review only. It confirms 23 HTTPS/11 legacy controls, original bypass rejection, six additional graph mutations, exact binary/source/rate privacy checks and all 12 cost ledgers. Next action requires separate approval of the five-create state-bootstrap saved plan.


## R12 complete professional AWS/Terraform learning core ·2026-10-28

A separate critic compared the original44-lesson pack with the expanded84-lesson pack and selected the expansion. The path now includes64cloud guides and321mapped concept entries, including important services absent from the pinned EC2 source. The biggest content gaps found were ALB examples with wrong project paths, Terraform file/template attribution and stale deployment status; these were repaired against actual contract/source and owner evidence. See `docs/nodejs-aws-study-path/evidence/full-curriculum-critic.md`.

Actual evidence:3credential-free labs independently passed;19AWSlesson example checks passed (publicDNS/TLS exercise explicitly unrun);48isolated reader/import tests passed after rerunning2sandbox-blocked socket tests with approved loopback access. Validator passes84lessons/64cloud/321concepts/547relative links/190pinned source ranges/31exact historical excerpts. Importer independently passes7shape/link regressions and3realGit integrity tests. Final actualreader/import preservation verification follows publication.

The remaining gap is liveAWS operating evidence: IAM/connectivity, availability, managed recovery and billable teardown are not proved by local simulations. These belong to the deployment owner. The owner's0f24d6d report establishes reviewed costs/private plans and earlier certificate issuance; bootstrap/application plans were not applied. No cloud changes were made by this curriculum change.


Final R12 release gate completed: the independent critic verified85guides,85internal destinations,8scoped searches,166protected files unchanged and114safe archive members matching source. Actual54Python/11JavaScript reader/import/isolation checks passed. The expansion wins; liveAWS operational evidence remains outside the learning release. [Final independent audit](evidence/cloud-study-release-2026-10-28/independent-audit.md) records exact source revision and evidence limits.


## R12 setup and process walkthrough · 2026-10-28

The GitHub study path now links eight short companion chapters plus their index. They explain the real local setup, contract-preserving migration, account/cost ownership, Terraform roots/state/private plans, verified DNS/certificate issuance, pending application/security/recovery steps, independent curriculum review and GitHub/Study Desk import. Numbered lesson IDs remain unchanged.

A separate critic reviewed all nine files against actual scripts and published evidence, then independently passed the full validator (84 lessons, 64 cloud, 321 concept entries, 663 local links, 190 pinned ranges, 31 excerpts) and inspected 123 archive members, including all nine walkthrough files, with bytes matching source. The largest gap was a beginner following integrated startup without host backend/frontend dependencies before local checks; chapter2 now includes both explicit npm ci commands. [Independent review](evidence/study-process-walkthrough-2026-10-28.md). No application runtime, infrastructure, real costs or credentials changed. Publication/import and fresh protected-data comparisons are verified separately at release.


## R12 AWS visual learning companion · 2026-10-28

Added nine genuine official AWS console example images and one actual blank email/provider sign-in capture. Each caption states provenance, visible fields, historical/version differences, source/lesson connections and recall questions. The account's read-only identity check returned 772641336063, an assumed AccountFullAccessRole session and no IAM users; the guide distinguishes role access, new-experience email sign-in and IAM console credentials without creating identities. Signed-in project screenshots remain pending authentication. No official example is claimed as this account or deployed infrastructure.

The independent critic inspected all 10 images and exact official source-page image URLs, verified captions against source/current IAM guidance, and approved documentation delivery. The largest gap was broken source links outside the standalone ZIP: 78 visual/walkthrough links plus the index handbook link are now pinned to published source; local study links remain portable. The validator now rejects any local link escaping the managed pack, and a deliberately broken existing-file escape was rejected in an isolated fixture. Visuals are included in the archive, while remote official images are explicitly online-only.

Final local validation passes 84 lessons / 64 cloud / 321 concepts / 627 local links / 230 pinned references / 31 exact excerpts; 128 archive members include 3 visual Markdown files, 1 provenance record and 1 local PNG, with all bytes matching source. [Independent visual review](evidence/aws-visual-study-review-2026-10-28.md). Existing runtime/infra, account permissions and cost models were not modified.


## R12 actual IAM permissions-screen clarification · 2026-10-28

The user's supplied screenshot shows Create user Step 2, not the earlier email sign-in screen. Added the unchanged original PNG and a small-concept guide: empty Copy permissions sources, direct policy attachment, ViewOnlyAccess plus ACM read-only as a broad viewing baseline, the optional boundary's distinct ceiling role, and required Step 1 console-access verification. The biggest gap was overly confident inference of the browser account model from a CLI assumed role; the guide now expressly limits that evidence and does not infer console password support from the wizard.

An independent critic inspected the complete original/copy image and matching SHA-256, checked privacy, captions and current official managed-policy/boundary documentation, and approved the documentation. Full overlay validation passed 84 lessons, 632 local links, 230 pinned ranges and 31 exact excerpts. The ZIP contains 130 matching members including 7 visual assets; both local image hashes match provenance. [Review](evidence/iam-permissions-screen-review-2026-10-28.md). No IAM user, policy attachment, password, MFA device, access key or AWS resource was created or modified by this documentation task.


## R12 signed-in project console captures · 2026-10-28

Added ten genuine read-only project captures: AWS Settings, issued/unused ACM certificate, existing default VPC, ECS clusters, RDS databases, ECR private repositories, S3 general-purpose buckets, CloudWatch log groups, NAT gateways and EC2 load balancers. Each small-concept caption states actual scope, visible observations, source/lesson connections and recall questions. Google sign-in and user-completed TOTP registration were observed separately; no personal security-page screenshot, recovery email, device/IP history, MFA QR/seed/code or authentication workflow handle is published. Registration is not claimed as an independently tested sign-in challenge.

The largest interpretive gap was confusing an existing default VPC with the unapplied application network: the actual default VPC is 172.31.0.0/16; planned ECS source is 10.85.0.0/16. Captions also preserve the explicit S3 All AWS Regions/general-purpose-tab exception and clipped map/table limits. An empty scoped list never becomes an account-wide absence or completed-deployment claim.

A separate critic inspected every new PNG and recomputed all 10 hashes, checked captions/source/current identity guidance, independently ran the validator (84 lessons / 664 local links / 237 pinned ranges / 31 exact excerpts) and inspected 141 archive members, 18 visual members, 12 local image hashes, nine remote examples and all visual links. [Independent review](evidence/aws-live-console-review-2026-10-28.md). No resource, account permission or authentication setting was changed by this documentation agent. Cost, provisioning and application verification remain with the deployment owner.


## R12 executable Terraform command workbooks · 2026-10-28

Added two linked companion chapters: a credential-free Terraform command workbook and the actual project's owner-operated AWS command reference. Numbered lessons remain unchanged. All nine local Bash blocks (the fast path plus eight manual blocks) actually passed using Terraform1.17.0, with create/update/destroy, no-change checks, three configuration tests and empty final state. The independent critic separately executed the eight manual blocks with inherited credential/CLI-argument canaries and confirmed their isolation.

The biggest gap was a bare shell test that did not stop subsequent commands after a failed guard or plan. Cloud templates now use fail-fast subshells, require private root/input/run paths, refuse existing binary and JSON review artifacts, protect directory/file modes, and compare approved hashes plus fresh account identity before reaching apply. Ten independent shell-only failure/success probes passed after reproducing the original four-call guard bypass. All ten AWS template blocks pass Bash syntax checking. Stubbed success is not evidence of AWS execution.

The [independent critic](evidence/terraform-command-study-review-2026-10-28.md) selects the repaired guides. The study pack includes the actual local transcript and machine-readable verification scope. No AWS authentication, AWS provider initialization/plan/apply/destroy or GitHub workflow dispatch was run. The deploy=true workflow remains the older EC2/SSM delivery path; ECS activation, current costs and exact saved-plan approval remain owned by the deployment chat. Full publication/import integrity is checked separately at release.

Publication gate: the committed guides reached GitHub and the live Study Desk API returned both revision-pinned workbook links. The importer reports zero stale files; all171 protected study files are unchanged, and145 archive members exactly match source. The transcript metadata uses its packaged filename. This verifies documentation delivery only.


## State bootstrap post-apply critic —29 October 2026

Independent critic inspected actual Terraform log/state and separately queried expected account/owner/region and all bucket controls: PASS for approved five-create bootstrap execution. [Evidence](evidence/aws-state-bootstrap-2026-10-29/critic.md). Largest remaining gap is application infrastructure/runtime deployment; protected state and retained versions still need deliberate retention/cleanup decisions.


## Actual S3-backed plan preparation — 29 October 2026

A separate fresh-context critic inspected actual saved binary/backend/source, account-scoped absence, private controls and current official tariffs. The reviewer accepts the real S3 fixture and rejects 54 unsafe variants; legacy HTTPS 23 and hostname-free 11 pass. Eight additional independent backend/parser probes reject unsafe payloads. The critic required current results ahead of historical checkpoints and readable prose/count corrections; those were repaired. [Full evidence](evidence/aws-s3-plan-2026-10-29/README.md). Preparation review is distinct from application apply/runtime approval. Biggest gap: no cloud application/recovery/rollback evidence, and the actual 24-hour teardown deadline/scheduler/retention remain unresolved.


## R12 actual AWS execution study journal · 2026-10-29

The new eleventh companion chapter records actual login renewal, effective-account verification, the human-approved five-resource bootstrap and independent read-back, actual S3 backend preparation and local saved-plan review. It links published execution evidence, shows copyable inspection commands and explicitly records that desktop iTerm control was denied; no UI automation or alternate control was attempted. Command output remained visible through the agent shell.

The biggest gap found by the fresh independent critic was the distinction between the earlier successful direct offline reviewer and the current expected rejection of the original saved artifact after the deployment owner edited retention source. The journal now labels both observations, forbids forcing the historical plan through source checks, and requires a newly reviewed plan. Bash syntax, all seven pinned targets, full-overlay local links and fail-fast/private-artifact boundaries pass. [Independent review](evidence/aws-execution-journal-review-2026-10-29.md).

The human selected a 24-hour demo, demo-data removal and preserved Terraform state. The shutdown mechanism and exact refreshed artifact are still unresolved; no application apply, task activation or runtime success is claimed. This learning review made no cloud mutation. The archive/import are verified independently of the deployment owner's pending operational work.


## Visible operator and discard-policy preparation — 29 October 2026

Independent review reproduced 12 mocked Terraform tests and 28 helper failure-path tests and inspected the actual stopped preflight. Config-file/optimization environment handling was tightened; the reviewer correctly rejects optimization, and an initial hypothetical bypass concern was withdrawn after actual refusal proof. Source-safe default retention remains intact; explicit discard transitions need successful apply before destruction. Largest unresolved gap: intended client range and credible chosen shutdown mechanism, followed by a fresh plan and exact apply approval. [Evidence](evidence/aws-operator-preparation-2026-10-29/README.md).


## Final matching application-plan preparation — 29 October 2026

A new fresh-context critic independently reviewed exact 2fd776...b56 against current Terraform/provider-lock/template and real saved S3 backend, checked actual approved-client preflight/journal, re-summed all 12 ledgers and rejected 54 controls plus 8 additional mutants. Preparation PASS only. [Final critic](evidence/aws-application-plan-2026-10-29/critic.md). It required explicit historical/current wording in the runbook; those inaccuracies were repaired. Biggest remaining gap is unprovisioned runtime and unproved cloud teardown. Operator-assisted return/renewal/approval is selected; no unattended enforcement exists. Actual T0/T0+24h remain unset until provisioning; exact saved-plan apply still needs human approval.


## Actual initial apply failure and repair review — 30 October 2026

The independent live critic rejected infrastructure completion: RDS retention was refused by the Free plan, direct Route53 writes were refused for a Cloud Map-owned zone, and ALB logging validation failed, leaving a tainted physical ALB. The exact approved initial artifact was consumed; paid resources and the original clock remained. [Actual failed execution and critic](evidence/aws-infrastructure-apply-2026-10-29/README.md).

Builders corrected those source paths. Fresh planning then exposed unintended broker replacement through latest-AMI drift, ineffective empty custom-health blocks and stale volume expiry metadata. The first two repair previews were rejected and preserved. Current source pins the deployed AMI, explicitly sets custom-health threshold 1 for five empty definitions and sets the configured root-volume deadline tag. Eighteen isolated mocks pass. A separate critic verified broker/EBS preservation, all 35 trust paths and 372 cost item products across 12 ledgers. The computed volume tags_all mirror remains historical until actual apply/read-back; this is disclosed and narrowly bound, not claimed fixed. [Exact plan/cost packet](aws-repair-review-2026-10-30.md).

Final strict mixed-action review, all 56 negative controls and eight additional critic controls pass on the exact cd87e0 artifact. The fresh critic independently reran 28 operator tests and inspected the 18 mock-run receipt. The largest remaining gap is live repair and recovery verification; no one-day account compatibility, ALB log delivery, HTTPS behavior, application activation or teardown success is inferred from source or planning. The deadline remains today at 5:51 PM EDT with operator-assisted cleanup.

[Final independent repair critic](evidence/aws-repair-plan-2026-10-30/critic.md). Preparation accepted; no changed-plan apply approved or performed.


## R12 AWS/Terraform questionnaire · November 2, 2026

Added a supplementary 30-question/12-incident companion to the existing 84-lesson path and both README navigation entries. Every stable card maps to existing lessons, priority, a literal project source setting/excerpt, an evidence scope and primary guidance. Four absent-feature examples are explicit. Dated October 30 completion/cleanup/rejected-destroy records and October 31 temporary stop/retained-resource/RDS-restart facts are reconciled without claiming present-day AWS status. Original numbered lessons, personal progress, runtime and infrastructure are unchanged.

The independent critic's largest content gap was mismatched broad references: repaired Terraform/account/ARN, PostgreSQL ownership and outbox guidance, added the missing custom-NACL worked example and a beginner glossary. A real link-check failure from a copied Markdown excerpt was repaired by quoting the actual moved-block lab operation; no link check was disabled. [Independent review](evidence/aws-questionnaire-review-2026-11-02.md).

Actual local verification: full study checker passes 84 lessons/64 cloud/321 concepts, 895 local links, 279 pinned source ranges and 31 historical exact excerpts; companion checks pass all42 cards, 60 mapped lessons and four absent-feature examples. All20 offline regression tests pass. The managed ZIP changes147→150 members: only its existing README changes, exactly questionnaire/map/context are added, no prior member is removed and every member matches source. All85 original lesson/personal files retain their hashes. [Executed checks and failed-then-repaired evidence](evidence/aws-questionnaire-validation-2026-11-02.json).

Verification scope is documentation and study tooling: npm application check/test/build/HTTP acceptance were not rerun because application behavior did not change. Local HEAD was inspected; a remote HEAD read failed DNS and is not claimed verified. No cloud operation, secret-value read, GitHub push/PR/CI dispatch or live reader publication occurred. This addition is local-only.


### R12 questionnaire publication preparation · November 2, 2026

The user subsequently requested Git add/commit/push. The configured remote main was actually read and matched local base7e778a0. A clean source candidate is built from that base plus only learning changes; existing uncommitted deployment changes stay outside the commit. The largest publication gap was that five cards referenced two dated source reports absent from Git. Exact sanitized copies are now packaged under `evidence/questionnaire-records/`, checked by full inspected SHA-256 plus symbol/excerpt and compared with the original whenever present. Current implementation cards still require actual source. Missing/corrupt/conflicting archive controls prevent treating unavailable evidence as a pass.

The clean candidate passes the full checker (84 lessons,64 cloud,321 concepts,902 local links,279 pinned ranges,31 historical excerpts) and26 offline regression tests. Its152-member ZIP includes both archived reports and matches source byte-for-byte; all original lessons/personal progress are preserved. [Executed publication-preparation evidence](evidence/aws-questionnaire-publication-validation-2026-11-02.json) and [independent publication review](evidence/aws-questionnaire-publication-review-2026-11-02.md). These checks prepare the Git publication; only an actual successful push/read-back establishes remote delivery. The earlier local-only review above remains a historical checkpoint. No AWS or live reader operation is performed.
