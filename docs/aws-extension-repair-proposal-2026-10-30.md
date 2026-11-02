> Historical proposal: approved by the human and executed once; partial RDS-size failure. The operative deadline is now 9:51 PM EDT. See the current execution result and micro completion packet.

# Combined four-hour extension and infrastructure repair proposal

Prepared 2026-10-30T20:32:59.323912+00:00. **PROPOSAL ONLY — awaiting one combined human approval.** No resource apply, extension, app activation, account upgrade or cleanup has occurred in this chat. Current operative deadline remains **today, October 30, 2026, 5:51:25 PM EDT** until approval.

Approve the existing clock's deadline moving four hours, from **October 30 at 5:51:25 PM EDT** to **October 30 at 9:51:25 PM EDT**, together with the exact saved repair below. Original start remains October 29 at 5:51:25 PM EDT; this is T0+28 hours, not a restarted clock. Exact proposed UTC deadline: `2026-10-31T01:51:25.219221Z`. Terraform tags conservatively round down to `2026-10-31T01:51:25Z`.

## Exact artifact and scope

Private plan: `/Users/robertovalencia/Documents/Business/linked-in-node-and-aws/work/aws-repair-extension-proposal-2026-10-30-v2/repair.tfplan`

SHA256: `754e2d2deb23e7ed0117ee805d48e4df34c79a93cc68c611a6cd242d58d0f907`

Account `772641336063`, Ohio `us-east-2`; Terraform 1.17.0 and provider 6.70.0. The encrypted, locked S3 backend and isolated application state key are unchanged. All actual states, separate state-bootstrap/certificate roots, and the original `cd87e0…` repair artifact are preserved.

Terraform proposes **18 adds, 82 updates, 6 destroys**: 12 missing creates plus six replacements (one tainted ALB and five freshly verified empty Cloud Map app definitions). The 82 updates are the already reviewed operations bucket policy and deadline metadata. Broker/AMI/root EBS identities and protections remain unchanged. All Terraform source/configuration is identical to the completed review. Every managed resource change and refresh-drift entry is identical after normalizing only the fixed deadline value; the private /32 is unchanged.

Repair includes private RDS with **one-day automated backup retention**, retaining the seven-day source default. This shorter recovery history is a deliberate demo override. Free-plan acceptance of one day is still unproven; stop on rejection, without an account upgrade or disabling backups. ALB logging stays enabled with the reviewed policy correction. Zero ECS tasks/services/task definitions, secret versions, image publication or public DNS record changes are in this plan. A successful apply will still require actual read-back, especially live EBS expiry, private encrypted RDS/retention/protection, ALB logging/TLS/host denial and empty-target response, Cloud Map broker registration and seven alarms. Empty-target 503 does not mean the marketplace is ready.

## Incremental four-hour quote

| Scenario | Idle | Expected | Higher usage |
|---|---:|---:|---:|
| Repaired infrastructure, zero app tasks | $0.91 | **$1.06** | $3.44 |
| Future five app tasks, comparison only | $1.15 | **$1.30** | $3.69 |

Existing partial infrastructure fixed-only envelope: about **$0.74** for four hours, plus unmeasured usage. The separate bounded replacement reserve remains **$0.0325**. These are gross incremental estimates before credits, taxes, usage variation, billing increments and deletion tails; they are not spending caps. The already incurred October private-zone fee is excluded. The proposal does not cross the local calendar month. Rates are the 31 unchanged selections verified today at 14:39 UTC; no new price model or commitment is introduced. See [deterministic extension estimate](evidence/aws-extension-repair-2026-10-30/estimate.json) for Decimal calculations and ledger hash. Official tariff references: [VPC](https://aws.amazon.com/vpc/pricing/), [load balancing](https://aws.amazon.com/elasticloadbalancing/pricing/).

The future five-task comparison does **not** approve app activation. Necessary image/build preparation can proceed separately, but activation still needs its concrete artifacts and approval.

## Verification actually completed

- Refreshed authenticated account, default workspace, pinned tools, actual remote state and all five empty discovery-service receipts. State equals the frozen baseline after sorting only check-result ordering: serial 4, 100 managed resources, same lineage and identities.
- Fresh Terraform fmt 0, validate 0, plan **2 (changes)**, show 0. No apply command executed.
- Reused completed independent critic, 18 Terraform mocks, 56 negative controls, eight prior critic controls and 28 operator tests; no reviewer fan-out or broad repeat testing.
- Ran all strict mixed-action/source/backend/security/cost checks on this exact binary using a separate proposal-bound reviewer instance with the single fixed proposed deadline. Original reviewer file and its original deadline guard remain unchanged. Preparation also enforces the still-operative original deadline. Eight focused controls reject clock reset, later deadline, extra hours, false approval/activation and nonmetadata broker change. This is preparation validation, not new independent critic approval.
- Confirmed Verify run 41077354229 failed in the disposable Kafka drill because a generated cluster ID began with a hyphen and was parsed as an option. Fixed the local generator to reject that encoding; two deterministic regressions pass and the real disposable Kafka TLS/SCRAM/ACL drill now passes **9/9**. Terraform/userdata unchanged. Added the regression to the existing Verify source job.
- Hosted SonarCloud run 41077354419 failed for missing organization/project key/token. It remains blocked; no credential was invented and no gate disabled. Local CI fix is uncommitted/unpushed; hosted Verify has not been rerun and is not claimed green. Application release/activation must not bypass those gates.

## Execution after combined approval

Recheck exact binary hash, embedded/current source and provider lock/template, authenticated account/region, actual S3 backend/workspace/state and five empty definitions immediately before applying. Reject material drift. Record the actual human approval bound to this hash and four-hour deadline before running the saved plan; its apply command has no interactive approval prompt.

Working directory: `/Users/robertovalencia/Documents/Business/linked-in-node-and-aws/infra/aws-ecs-dev`. These are **reference commands only; apply has not run**. Use the cleaned profile environment from the existing operator helper; never print private inputs/state/decoded plans.

```bash
shasum -a 256 /Users/robertovalencia/Documents/Business/linked-in-node-and-aws/work/aws-repair-extension-proposal-2026-10-30-v2/repair.tfplan
AWS_PROFILE=marketplace-dev AWS_REGION=us-east-2 AWS_DEFAULT_REGION=us-east-2 aws sts get-caller-identity
# Only after the exact combined human approval and all immediate guards:
terraform apply -input=false -lock-timeout=60s /Users/robertovalencia/Documents/Business/linked-in-node-and-aws/work/aws-repair-extension-proposal-2026-10-30-v2/repair.tfplan
```

Preserve actual state and diagnostics on any failure. Do not retry consumed/rejected artifacts, untaint, import, target or rewrite state. Stop rather than upgrade the Free account. Verify real repairs before proceeding to later deployment stages.

If approved, begin operator-assisted cleanup preparation by **7:51 PM EDT**, for the **9:51 PM EDT** deadline. There is no automatic cleanup or reminder. Current transition/destroy artifacts and their own exact approval remain necessary; synthetic data is to be discarded through that reviewed cleanup while preserving state and the existing certificate. If extension is declined or no approval arrives, the **5:51 PM EDT** deadline remains and cleanup preparation takes priority.

## One combined approval

Reply: **“Approve the four-hour extension to 9:51 PM EDT and repair plan 754e2d2deb23.”** This authorizes only the fixed deadline extension and this exact infrastructure repair. It does not authorize application activation, account upgrade, changed exposure or teardown.

The explicit approval is required both by the human handoff and `AGENTS.md`: “Cloud provisioning requires approval of the concrete saved plan and current cost estimate; preparation is authorized.”
