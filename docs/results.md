# Results and verification boundary

These results were produced for this Node/React migration on 21 October 2026. The reference repository supplied contracts and the 48-check acceptance suite, but its old test reports were not reused as evidence. Read the linked raw reports to distinguish an executed check from a prepared integration.

| Gate | Executed result | Evidence |
|---|---|---|
| Source checks and builds | TypeScript, ESLint, Prettier and both production builds pass | [source check](evidence/source-check.txt), [build](evidence/build.txt) |
| Backend unit tests | 40/40 Jest tests pass | [backend test log](evidence/backend-tests.txt) |
| Frontend component and hook tests | 28/28 Vitest tests pass; 81.13% frontend line coverage | [frontend test log](evidence/frontend-tests.txt) |
| Reference API behavior | 48/48 adapted executable checks pass against the running local stack | [acceptance report](evidence/local-acceptance.json) |
| Adversarial backend behavior | 8/8 independent probes pass, including concurrent idempotency, changed-payload conflict and ownership denial | [adversarial report](evidence/backend-adversarial.json) and [database invariants](evidence/backend-db-invariants.json) |
| Dependency and application recovery | 9/9 local restart and replay checks pass | [failure drill](evidence/failure-drill.json) |
| Desktop and mobile user journeys | 2/2 real-browser smoke journeys pass on the nginx-served stack, covering discovery, compare, profile, login and durable inquiry | [browser report](evidence/browser-smoke.json) and [screenshots](evidence/browser/desktop-discovery.png) |
| Local SonarQube | Evaluated gate **OK**: new-code coverage 89.3% against 80%, new duplication 0%, new violations 0; no open issues in the scanned project | [gate](evidence/sonar-gate.json), [issues](evidence/sonar-issues.json), [scan log](evidence/sonar-scan.txt) |
| AWS definitions | Both Terraform roots validate; one mocked security plan passes | [Terraform log](evidence/terraform.txt) |
| Remote release control flow | 2/2 fake-CLI success/rollback fixtures pass | [orchestration report](evidence/infra-remote-orchestration.json) |

The SonarQube 89.3% is its **new-code** metric, not coverage of the whole backend. Backend unit-only coverage is much lower in some infrastructure modules; the 48 real HTTP checks and restart drill exercise those modules through the running stack. The backend unit test log shows the exact coverage table. The two browser journeys do not establish full visual or assistive-technology parity.

The first restart drill failed because nginx held stale container IPs after service recreation. The repair and passing rerun are both retained in [failure evidence](evidence/failure-drill-before-edge-repair.json) and [final evidence](evidence/failure-drill.json). The first remote release fixture exposed a relative secret-cleanup trap; its failing and repaired reports are [here](evidence/infra-remote-orchestration-before-repair.json) and [here](evidence/infra-remote-orchestration.json). These are corrections, not inherited success claims.

## External environments

The AWS dev architecture, Terraform, deployment workflow and release scripts are **prepared**. No account-specific `terraform plan`, provisioning, ECR push, SSM execution, live AWS smoke test or live rollback has occurred. The next cloud gate is an actual saved plan for the intended AWS account, reviewed with the [cost estimate](costs.md) before billable provisioning. The refreshed core estimate is approximately **$1.25 for 24 hours** or **$2.49 for 48 hours** in us-east-1, assuming full dev teardown at the deadline and excluding usage-dependent charges. See the [short-run cleanup plan](short-run.md).

GitHub Verify passed on the private repository at [run 39643863786](https://github.com/robertovalencia/linked-in-node-and-aws/actions/runs/39643863786). The hosted SonarQube job [run 39643863707](https://github.com/robertovalencia/linked-in-node-and-aws/actions/runs/39643863707) failed because its account URL/token were absent. `SONAR_HOST_URL` is now set to the Free EU service; Sonar organization/project creation and the token remain. GitHub protected environments, Jira import and AWS deployment remain unverified. The [hosted Sonar guide](sonarqube-cloud.md) gives the exact setup. The evaluated local SonarQube gate is separate from the hosted job. The [independent review record](reviews.md) names each critic's verdict and remaining limits.
