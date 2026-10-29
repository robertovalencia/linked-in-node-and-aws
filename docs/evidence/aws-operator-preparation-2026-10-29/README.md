# Operator preparation and fail-closed preflight — 29 October 2026

Historical first-attempt packet. The human later explicitly approved the lookup/private /32, and a NEW saved plan was prepared successfully. See [current application-plan evidence](../aws-application-plan-2026-10-29/README.md). Statements about stopped execution/no fresh plan below describe this earlier checkpoint only.

This packet records new local source/tests and actual authenticated read-only preflight, not application provisioning. The first run stopped at client-range mismatch before Terraform plan. No new saved application plan, apply, timer, DNS routing or AWS-native controller exists.

- [Current status and remaining decisions](status.json)
- [Sanitized step-by-step journal](journal.md)
- [Actual visible preflight transcript](preflight-transcript.txt), [structured executed steps](preflight-steps.json)
- [Twelve mocked Terraform tests](teardown-mocks.json), [actual cleanup-transition source and official references](teardown-transition.json)
- [Twenty-eight fake-CLI helper tests](operator-tests.json)
- [Dated deterministic shutdown cost comparison](shutdown-cost-comparison.json)
- [Independent interim critic](critic.md), [parent repairs and remaining review limits](review-repairs.md), [current local verification](root-verification.json)

The separately approved five-resource state bootstrap and certificate remain. Raw plans/state, contexts, credentials and secret payloads remain private/ignored. The old 8cf application plan cannot be applied against changed source; refusing it is correct evidence. The human selected operator-assisted shutdown, requiring return/login renewal and exact teardown approval. No controller or reminder is requested/created; the AWS-native alternative is not selected. The user's earlier snapshot-retention option is superseded by deleting demo data and preserving state.
