# HTTPS plan preparation evidence — 28 October 2026

The user approved one client /32 for preparing a plan, not provisioning. Raw private plans/context/state are excluded from Git.

- [Account/certificate/inventory preflight](account-preflight.json): renewed temporary login; Free/ACTIVE/$100; existing certificate issued; no app infrastructure in queried scopes.
- [Bootstrap saved-plan summary](bootstrap.json): five creates, private/versioned/encrypted state bucket, TLS-only policy, no OIDC. Approval required.
- [HTTPS local-backend preview](https-preview.json): 111 creates, one HTTPS listener + host rule + approved /32, zero application task definitions/services. The exact CIDR is private. This is not the final S3-backed apply artifact.
- [23 HTTPS negative controls](https-negative-controls.json) and [11 legacy controls](legacy-negative-controls.json), each preceded by a positive valid-plan check. The only stubs replace local terraform-show for unsafe JSON controls; source ZIP checks stay real.
- [Refreshed Ohio prices](rates.json), [retrieval receipt](price-refresh.json), [consumption and S3 state assumptions](cost-assumptions.json). All 31 selected rates/units unchanged; old omitted tier metadata is labeled honestly.
- [Generated IAM draft warnings](iam-draft-warnings.json): three policies, 12 wildcard warnings; unapplied/unattached. This is not an approved operator policy.

The [independent critic](critic.md) verified actual binaries, source binding, privacy, security graph and all 12 cost ledgers. Published source/plan receipts are evidence, not permission to apply. [Next-step review guide](../../aws-https-plan-review-2026-10-28.md).
