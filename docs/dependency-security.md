# Dependency security: repair the graph without changing the architecture

The production audit began reporting four high-severity findings: two underlying vulnerable packages and their propagated NestJS dependency paths. These were newly published advisories, not four independent defects in the marketplace code. The baseline audit is preserved in [audit-before.json](evidence/ci-security-repair/audit-before.json).

## What changed and why

Express 5.3.0 accepts body-parser through a compatible `^2.3.0` range. Updating the lockfile resolves body-parser 2.4.0 without a package override. [The upstream body-parser advisory](https://github.com/advisories/GHSA-27r3-jxmh-p828) identifies the compressed-request process-crash risk and the fixed release.

The current NestJS Express adapter 12.2.0 pins Multer exactly to 2.4.0. The patched Multer release is 2.5.0; [the upstream advisory](https://github.com/advisories/GHSA-q7qp-rjg7-q26m) describes the asynchronous upload-filter teardown issue. The marketplace has no upload endpoint, but retaining an installed vulnerable dependency is unnecessary and still fails the required audit.

A temporary npm override targets only this adapter's Multer dependency:

```json
"@nestjs/platform-express": {
  "multer": "2.5.0"
}
```

The existing js-yaml override remains. NestJS stays at 12.2.0. The lockfile changes exactly the body-parser and Multer package entries. No runtime business source, route, database migration or cloud configuration changes. An automatic `npm audit fix --force` would propose unrelated framework downgrades; it was not used.

## How to assess the evidence

The candidate was installed with `npm ci`, checked with `npm ls` for invalid dependencies/peers, and audited using the production dependency graph. See [resolved tree](evidence/ci-security-repair/resolved-tree.txt) and [audit after](evidence/ci-security-repair/audit-after.json). A passing audit means the registry reported no matching production advisories at that time; it is not proof of universal security or a substitute for behavior tests.

Existing backend lint/types/format checks, all 64 backend tests and the build passed in the isolated candidate. The critic independently ran the unchanged backend suite and checked that application/test source remained identical. Full local runtime and hosted verification results are recorded in [results](results.md); do not infer a passing deployment from the dependency graph alone.

## Maintenance decision

Keep the override until an upstream compatible NestJS adapter release includes a patched Multer constraint. At that time inspect upstream release notes, remove the scoped override, update the lockfile, reinstall from scratch, check every resolved copy, and repeat audit and behavior verification. Do not delete the lockfile or suppress the audit to make CI green. A failed advisory gate is useful evidence that maintenance is needed.

The repository's isolated release SonarQube and the separately configured hosted SonarCloud workflow are distinct. Missing hosted organization/project/token settings require owner setup; this patch does not skip that workflow or label missing analysis as success. See [the exact owner setup](sonarqube-cloud.md).

## Interview rehearsal

“I traced the audit to two transitive packages, checked patched upstream releases and the parent's constraints, and chose the smallest compatible dependency change. I preserved the framework version and application contracts, verified the installed graph and tests, then inspected the running application and hosted checks. The override has an explicit removal condition; passing an audit is one security signal, not a complete security claim.”

## References

- [body-parser 2.4.0 release](https://github.com/expressjs/body-parser/releases/tag/v2.4.0)
- [Multer 2.5.0 release](https://github.com/expressjs/multer/releases/tag/v2.5.0)
