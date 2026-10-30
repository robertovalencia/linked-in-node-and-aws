# Current repair prices and costs — 30 October 2026

Official rates fetched at 2026-10-30T14:39:51.232268+00:00. All 31 rates, units and tiers are unchanged from 29 October. This was read-only price research and calculation. No AWS resource changes, account upgrade, login, inventory or Terraform operation occurred.

| Scenario | Hours | Profile | Gross USD |
|---|---:|---|---:|
| Infrastructure only, zero app tasks | 24 | idle | 5.95 |
| Infrastructure only, zero app tasks | 24 | expected | 6.84 |
| Infrastructure only, zero app tasks | 24 | higher | 21.14 |
| Infrastructure only, zero app tasks | 720 | idle | 164.39 |
| Infrastructure only, zero app tasks | 720 | expected | 191.32 |
| Infrastructure only, zero app tasks | 720 | higher | 622.29 |
| Future five app tasks (not planned) | 24 | idle | 7.43 |
| Future five app tasks (not planned) | 24 | expected | 8.32 |
| Future five app tasks (not planned) | 24 | higher | 22.62 |
| Future five app tasks (not planned) | 720 | idle | 208.86 |
| Future five app tasks (not planned) | 720 | expected | 235.78 |
| Future five app tasks (not planned) | 720 | higher | 666.76 |

The original deadline remains **today, 30 October at 5:51:25 PM EDT / 21:51:25Z**. At calculation time 2026-10-30T14:41:07.630884+00:00, 7.171552 hours remained. These 24-hour and 720-hour comparison windows do not extend it.

| Same existing deadline, hypothetical immediate repair | Profile | Remaining recurring gross USD |
|---|---|---:|
| Infrastructure only | idle | 1.6274 |
| Infrastructure only | expected | 1.8939 |
| Infrastructure only | higher | 6.1671 |
| Future five app tasks (not planned) | idle | 2.0703 |
| Future five app tasks (not planned) | expected | 2.3368 |
| Future five app tasks (not planned) | higher | 6.6100 |

The partial-state fixed envelope remains **$0.185931/hour**, or **$1.3334** over the remaining interval if unchanged. This excludes the existing nonprorated October private-zone charge, all unmeasured traffic, logs, metrics, API/storage usage and billing increments. It is not an invoice. Root must verify the live inventory independently.

Illustrative separate replacement reserve: **$0.0325**, with one additional billed ALB hour and two IPv4 address-hours under the stated at-most-one-hour assumption. It is excluded from steady-state and remaining recurring totals. Each ALB lifetime and NAT partial hour rounds up; IPv4 seconds have a 60-second minimum. No exact sunk-cost claim is made.

One-day RDS retention reduces the recovery window from seven days; backups remain enabled. Free-plan acceptance remains unproven. The excess-backup storage allowance is unchanged, so no retention-proportional saving is claimed. One registered Cloud Map broker instance is priced in infrastructure; a future five-task application would have six registered resources. No paid health checks, extra zone, MSK, WAF, customer-managed KMS key, paid security service or shutdown controller is added.

All figures are gross USD before credits, taxes and shared allowances. Neither a budget nor credits are hard spending caps. The existing zone charge is included once in 24-hour totals; do not double-count it when combining elapsed and remaining views. The 720-hour comparison crosses October/November and models two nonprorated zone charges. Sources:

- [AWS Cloud Map pricing](https://aws.amazon.com/cloud-map/pricing/)
- [Route 53 pricing and nonprorated zones](https://aws.amazon.com/route53/pricing/)
- [Elastic Load Balancing pricing](https://aws.amazon.com/elasticloadbalancing/pricing/)
- [Public on-demand catalog index](https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/index.json)

Raw exact-SKU API products, official tariff pages, retrieval dates, effective dates, deterministic ledgers and SHA256 manifest are private siblings. Retrieval date is not tariff effective date. Account context in the price receipt is static; root separately verifies identity and eligibility.
