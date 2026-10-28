---
title: "Terraform remote state and access control"
topic: "Terraform remote state and access control"
last_researched: 2026-10-27
source_labels: Terraform mechanics; New design exercise; Project code comparison
---

# Terraform remote state and access control

Prerequisite: environment and provider boundaries. State associates Terraform addresses with managed object identities and records metadata needed for future operations. Remote state means storing that information in a backend reached over a service interface. It improves collaboration only when storage permissions, locking, history, encryption and recovery are deliberately configured.

A backend is part of the control plane for infrastructure. Someone who can replace or disclose state can affect more than a configuration file. This lesson studies that authority without contacting a backend. No bucket, account, remote workspace or shared state is created by the advanced local lab.

## Step 1: read the project's state controls

Open the [pinned backend example](https://github.com/robertovalencia/linked-in-node-and-aws/blob/8b2c3e087014d76f9025dc47f5ede7837d73bfe6/infra/aws-dev/backend.hcl.example). It specifies a bucket placeholder, an application state key, a region, encryption and `use_lockfile = true`. An example file is a configuration template; it does not prove that a particular account contains a bucket or that a caller can access it.

The separate [bootstrap root](https://github.com/robertovalencia/linked-in-node-and-aws/blob/8b2c3e087014d76f9025dc47f5ede7837d73bfe6/infra/bootstrap/main.tf) declares versioning, server-side encryption, public-access blocking and a denial of insecure transport for state storage. Read those as complementary controls. Encryption addresses stored content. Transport protection addresses traffic. Versioning supports recovery. Public-access blocking reduces accidental exposure. None of them alone gives an operator least-privilege access or ensures a recovery procedure has been tested.

## Step 2: separate storage and resource authority

A Terraform run can need permission to read state, acquire and release a lock, write a new state version and manage provider resources. Those are different actions with different targets. A plan that refreshes resources can still read sensitive infrastructure metadata even when it cannot create anything. “Read-only plan job” should describe exact permission boundaries rather than imply the job sees no secrets.

For an S3 backend, the configured state object and lock object require distinct operations. Consult the backend's current permission requirements and scope object paths carefully. Lockfile use is optional and must be enabled. The official [S3 backend documentation](https://developer.hashicorp.com/terraform/language/backend/s3) also describes the older DynamoDB locking mechanism as deprecated; do not add a new table just because an old tutorial does. This curriculum does not migrate any existing backend.

Backend authentication settings should not be embedded as secrets in committed configuration or passed casually through persistent backend configuration arguments. Initialization records backend metadata locally, and plans can preserve configuration information. Prefer an appropriate runtime credential mechanism and protect local working directories as well as remote storage. A private bucket cannot prevent disclosure from a publicly uploaded plan artifact.

## Step 3: understand remote outputs and their blast radius

`terraform_remote_state` exposes another state's root outputs as values. It can look like a small API: perhaps the consumer only asks for a subnet ID. However, access to the underlying backend snapshot commonly permits reading the entire state, not just that output. Declaring an output sensitive does not create a per-output storage access boundary. The [remote-state data source reference](https://developer.hashicorp.com/terraform/language/state/remote-state-data) explicitly warns about this distinction.

Imagine a producer state containing both a public endpoint and a database password. Giving another team backend read access so it can retrieve the endpoint can expose the password as well. An alternative design publishes selected nonsecret information through a separate, deliberately permissioned interface. Another option is provider data lookup when a suitable service API exists. Evaluate update ordering, availability and stale-value behavior; eliminating state coupling does not eliminate dependencies.

Root outputs form a compatibility surface. A child output is not automatically exposed to remote consumers unless the root exports it. Rename or remove an exported value only with consumer review. Avoid a dependency cycle where state A needs an output from B while B needs A before either can plan. Split foundational contracts or redesign the ownership relationship so initialization has a clear order.

## Step 4: combine locking, history and encryption

Locking serializes operations that could write the same state when the backend supports it. It prevents two cooperating runs from both acting on an old snapshot. It does not prevent an administrator changing an object outside Terraform, and it does not make a multi-resource apply transactional. Backend encryption protects stored bytes from some forms of disclosure; authorized readers still receive usable content. Both controls need access management and operational discipline.

State history and backups are sensitive copies. Define who may read old versions, how long they remain, and how a restore is authorized. Keep a recoverable snapshot before any exceptional state manipulation. Restoration requires understanding whether real objects have changed since the snapshot; an older file can reintroduce stale ownership and propose unintended work. Lesson 78 develops that recovery reasoning.

Treat a lock error as information. Identify the owning operation and allow it to complete. Never make `-lock=false` a routine retry strategy. A stale lock needs evidence that its owner has stopped; `force-unlock` is an exceptional repair, not a concurrency optimization. The [locking reference](https://developer.hashicorp.com/terraform/language/state/locking) describes why misuse can permit conflicting writers.

## Practice and expected results

On paper, define three proposed roles: producer operator, consumer application planner and recovery operator. List whether each needs full-state read, state write, lock access and resource administration. If the consumer only needs an endpoint, identify a narrower publication interface. Expected result is a permission table whose entries have a specific purpose, including old snapshot access.

Run the advanced local lab for a bounded observation of state mechanics. It pulls a snapshot into its temporary directory, checks serial and lineage, restricts that backup file's permissions, then verifies empty local state after cleanup. It does not test S3 policies, remote locking or account authorization. Keep those evidence boundaries visible in interviews and run records.

### Recall: Does marking an exported output sensitive prevent a backend reader from obtaining it?

**Answer:** No. Sensitivity affects display behavior. A reader of the underlying state may access the stored value. Remote-state access must be evaluated at the snapshot and backend permission boundary.

## References

Official documentation checked on 2026-10-27.

- [Remote-state outputs and access warning](https://developer.hashicorp.com/terraform/language/state/remote-state-data)
- [S3 backend locking and permissions](https://developer.hashicorp.com/terraform/language/backend/s3)
- [State locking](https://developer.hashicorp.com/terraform/language/state/locking)

[Previous lesson](./72-terraform-provider-aliases-and-environments.md) · [Next lesson](./74-terraform-sensitive-and-ephemeral-values.md)
