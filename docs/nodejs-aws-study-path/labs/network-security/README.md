# Local network-security reasoning lab

Run from the repository root with Python 3. No dependencies, AWS credentials or cloud account are required:

```sh
python3 docs/nodejs-aws-study-path/labs/network-security/run.py
```

Predict the named flows first. The runner checks 14 positive/negative outcomes and confirms its JSON source is unchanged. `203.0.113.0/24` and `198.51.100.0/24` are documentation addresses, never targets contacted by the program.

Read `rules.json`, then follow `NetworkModel.connect`: explicit path flags → destination ingress → source egress → established flow. `reply` illustrates matching reverse traffic for a previously accepted flow. The copied negative variants demonstrate missing egress and no-ingress behavior.

This is a new illustrative teaching model, not the current project's Terraform. It deliberately omits many AWS details: ENIs/actual group attachments, route discovery, NACL rule ordering and ephemeral ranges, connection-tracking limits, all protocols, middleboxes, listener/target health, TLS, IAM and application authentication/ownership. Route and NACL flags are supplied assumptions, not simulation results. A live AWS design still needs real permitted/forbidden reachability tests and its own cost-first review in the deployment chat.

For practice, modify a copy of a group rule and predict which flow changes. Never apply this teaching input to AWS. Read [lesson 81](../../generated/81-network-security-local-lab.md) for the reasoning and evidence boundary.
