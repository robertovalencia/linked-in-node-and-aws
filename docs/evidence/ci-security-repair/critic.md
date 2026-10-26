# Independent critic — NodeJS/AWS CI repair

Reviewed repository working agreement, README, API contract, requirements and architecture on 2026-10-26. Source repository: `/Users/robertovalencia/Documents/Business/linked-in-node-and-aws`. This review writes no source repository files.

## Baseline findings

1. **Largest gap: production dependency audit fails, despite application checks passing.** GitHub Verify run `40405809089` at `76c237a0e09e3b5d746ec964bdf03b230934f8ac` reports high-severity body-parser `2.0.0–2.3.0` (GHSA-27r3-jxmh-p828) and multer `2.0.0–2.4.0` (GHSA-q7qp-rjg7-q26m). Lock baseline has body-parser 2.3.0, Express 5.3.0, multer 2.4.0 and Nest packages 12.2.0. Express accepts compatible body-parser updates; Nest platform-express pins multer exactly. Preserve the high/critical audit gate and avoid audit-force's proposed major downgrade to Nest 11.1.1.
2. **Hosted SonarCloud is genuinely unconfigured.** Independent configured-name/status inspection found only `SONAR_HOST_URL` variable and no repository secret names. Run `40417867539` at `31bd614d32a2e82dcdb39166d27eb098c48bc916` explicitly fails `Require configured server`: organization, project key and token are empty. No hosted scan or hosted quality pass can be claimed. Keep fail-closed behavior and do not invent project identities.
3. **Documentation mismatch.** `docs/sonarqube-cloud.md` says AWS release also waits on the hosted Cloud gate, while the actual `deploy-dev.yml` verifies with the isolated CI Sonar server. Clarify the document to match actual gates and preserve the separate pending hosted result.

## Candidate acceptance bar

- Minimal compatible dependency repair with reproducible lockfile; no unintended direct dependency churn or major framework change.
- Production audits of all three package scopes return zero vulnerabilities; inspect dependency tree for invalid peers or retained vulnerable copies.
- All existing 64 backend tests and the complete frontend suite remain present and pass, along with strict types/lint/format and builds.
- Existing real API acceptance returns exactly 48 passes and zero failures; browser and Terraform CI gates remain intact.
- Actual hosted Verify run for the published commit succeeds. Describe SonarCloud as pending/failed until real owner onboarding and successful hosted analysis.

Candidate review and evidence pending builder readiness.

## Candidate dependency review

Candidate staged at `work/node-ci-repair/backend` inspected independently. Local verdict: **accept dependency repair; hosted verification still required**.

- Package change is one parent-scoped `@nestjs/platform-express` override for multer `2.5.0`; Nest remains on aligned `12.2.0` packages. Lock changes exactly two package entries: body-parser `2.3.0 → 2.4.0` and multer `2.4.0 → 2.5.0`. No framework downgrade, broad dependency churn or audit suppression.
- Independently hashed all 18 source and 4 test files against the source repository: identical. Existing application contracts, security guards and failure-path tests remain intact.
- Independently executed `npm ls --omit=dev`: successful, no invalid peers. Lock contains one body-parser and one multer entry at patched versions.
- Independently executed existing Jest coverage suite: 4 suites and 64 tests passed, 95.44% line coverage. No test deletion or expectation weakening.
- Reviewed actual builder evidence: reproducible npm ci, strict types/lint/format, backend build and audit JSON all succeeded. Audit changed from four high findings to zero total production findings.
- No actionable new security/contract/failure-path finding in the minimal dependency candidate. Scoped override is an acceptable temporary compatibility choice while upstream Nest pins the older multer version; future Nest updates should remove the override when upstream carries a patched compatible version.

Remaining review items: corrected hosted-Sonar documentation and successful GitHub Verify run for the final published commit, including 48/0 real API, browser and Terraform gates. Hosted SonarCloud remains independently confirmed unconfigured and must retain an explicit pending/failed status until owner onboarding and a real analysis.

## Final source and local runtime evidence review

Final Business repository diff matches the accepted staged dependency candidate. Reviewed updated README, R11 acceptance addendum and traceability, new dependency-security guide and corrected SonarCloud setup document. The stale claim that AWS release waits on the hosted Cloud workflow is repaired; isolated release analysis and hosted Cloud configuration are described separately. No workflow gate is weakened or skipped. The guide documents upstream advisories, scope, audit limitations and override removal criteria.

Reviewed actual `docs/evidence/ci-security-repair/acceptance.json`: exactly 48 completed passes, zero failures, including authentication, cross-owner/cross-role access denial, profile update readback, durable inquiry creation, idempotency conflict/concurrency, acceptance/decline, Kafka notification delivery and read ownership/durability. Builder reports all 28 frontend tests, full checks/builds and all production audits passing. The additional local malformed-compressed-request smoke checks are scoped appropriately and do not assert universal CVE exploit coverage.

**Pre-publish verdict: accept.** Largest gap was the production dependency advisory failure; the minimal compatible graph repair closes that local gap without changing application source or weakening checks. Final hosted Verify result remains to be independently confirmed for the published commit. Hosted SonarCloud remains owner-blocked and must not be represented as a passed scan.
