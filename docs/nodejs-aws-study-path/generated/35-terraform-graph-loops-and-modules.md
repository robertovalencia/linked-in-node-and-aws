---
title: "Terraform: dependency graphs, loops and module boundaries"
topic: "Terraform: dependency graphs, loops and module boundaries"
last_researched: 2026-10-26
source_labels: Project code; Terraform mechanics; Credential-free practice extension
---

# Terraform: dependency graphs, loops and module boundaries

Prerequisite: trace inputs, locals and outputs. Terraform configuration describes relationships. The next step is predicting the graph those relationships create and how repeated resources receive stable addresses. This is the basis for safe scaling and refactoring.

## A dependency graph, not line-by-line execution

A graph has objects and directional relationships. If a subnet refers to a VPC ID, Terraform knows the VPC must exist before that subnet can use its identity. Independent objects can proceed concurrently. Resource order in a file does not establish this relationship. References usually give Terraform the dependency information it needs while also passing the needed value.

The [project subnet](https://github.com/robertovalencia/linked-in-node-and-aws/blob/9bb88515f14067feb23611c6851c03ca8fbc89b6/infra/aws-dev/main.tf#L13-L17) references the VPC. Its [route association](https://github.com/robertovalencia/linked-in-node-and-aws/blob/9bb88515f14067feb23611c6851c03ca8fbc89b6/infra/aws-dev/main.tf#L26-L29) references both subnet and route table. Its [instance](https://github.com/robertovalencia/linked-in-node-and-aws/blob/9bb88515f14067feb23611c6851c03ca8fbc89b6/infra/aws-dev/main.tf#L99-L106) refers to subnet, security group and instance profile, and also declares `depends_on` for route association and host policies. That extra dependency expresses a readiness relationship that is not fully carried by the instance's argument values.

This does not guarantee application health. Completion of an IAM attachment or route association is not evidence that Node.js has started successfully, that a database migration finished, or that an SSM tunnel works. Infrastructure ordering and application readiness are separate checks.

## for_each produces named instances

[The exact ECR loop](https://github.com/robertovalencia/linked-in-node-and-aws/blob/9bb88515f14067feb23611c6851c03ca8fbc89b6/infra/aws-dev/main.tf#L46-L58) starts with:

```hcl
resource "aws_ecr_repository" "app" {
  for_each             = toset(["backend", "frontend"])
  name                 = "${local.name}/${each.key}"
  image_tag_mutability = "IMMUTABLE"
  force_delete         = true
  image_scanning_configuration { scan_on_push = true }
  encryption_configuration { encryption_type = "AES256" }
}
```

`toset` turns the two names into unique collection members. Each member creates an instance, addressed as `aws_ecr_repository.app["backend"]` or `aws_ecr_repository.app["frontend"]`. The lifecycle policy resource then uses `for_each = aws_ecr_repository.app`, chaining one policy to each repository. This is a relationship between collections, not two hand-maintained lists that must happen to remain aligned.

Stable keys matter. Renaming `backend` to `api` changes an instance address, even if the intended real repository is the same. Review a migration rather than assuming a label is cosmetic. For ordered lists, removing an early index from `count` can shift later identities; named keys often describe long-lived conceptual identities more clearly.

## count and dynamic solve different problems

The [optional deploy role](https://github.com/robertovalencia/linked-in-node-and-aws/blob/9bb88515f14067feb23611c6851c03ca8fbc89b6/infra/aws-dev/main.tf#L127-L135) uses `count = var.enable_github_deployment ? 1 : 0`. A true input creates one instance at index `[0]`; false creates none. The matching policy uses the same switch. The selected local-login configuration disables both while retaining the host role and SSM attachment.

The [CPU-credit declaration](https://github.com/robertovalencia/linked-in-node-and-aws/blob/9bb88515f14067feb23611c6851c03ca8fbc89b6/infra/aws-dev/main.tf#L117-L122) uses a `dynamic "credit_specification"` block. It emits a nested block only for T-family instance types. A dynamic block repeats nested configuration within one resource; it does not create separately addressed resources like `for_each` on an ECR repository. The non-T default omits the field because sending a T-specific API option to another family is invalid.

## Understand what modules exist here

A module is a collection of Terraform files in one directory. A root module is the configuration Terraform is invoked against. A child module is called by a `module` block. This project has two separate root configurations, `infra/bootstrap` and `infra/aws-dev`. They are not demonstrated reusable child modules. The bootstrap owns the state bucket and optional account OIDC provider; aws-dev owns application infrastructure and uses a different state boundary.

A future production extension might extract networking, compute or release storage into child modules. That is a design proposal, not existing implementation. A child module can enforce an interface and reduce repetition; it also adds versioning, address migrations and abstraction costs. Do not introduce a module for every resource merely to increase the module count.

## Practice: predict addresses without AWS

Draw the VPC, subnet, route table, association and instance dependencies from the linked source. Predict which two ECR addresses exist and which two deploy-role-related collections are empty with the selected local-login file. Then inspect the runner's moved-block phase: its renamed local resource retains identity because the address migration is declared explicitly.

Expected result: ECR has backend and frontend keys. The optional deploy role and inline deploy policy each have zero instances in local-login mode; the host role remains. Independent ECR and VPC creation need not follow their source-file ordering. No cloud execution is required to check these conclusions against the tests.

## Checkpoint and answer

### Recall: Can `dynamic "credit_specification"` give each CPU-credit block an independently managed Terraform address?

**Answer:** No. It generates nested blocks inside the instance resource. Top-level `count` or `for_each` creates separately addressed resource instances; dynamic blocks configure one resource's schema.

## Interview tradeoff and pitfalls

Prefer references that communicate real relationships. Excessive `depends_on` makes the graph more conservative and can propagate unknown values, while missing a true readiness relationship can start a dependent action too early. Choose keys for identity, not just convenient display text. Avoid cycles, dependencies added solely to force arbitrary file ordering, and claims that this demo already implements a reusable production module platform.

## References

Official sources checked on 2026-10-26.

- [for_each](https://developer.hashicorp.com/terraform/language/meta-arguments/for_each)
- [count](https://developer.hashicorp.com/terraform/language/meta-arguments/count)
- [dynamic blocks](https://developer.hashicorp.com/terraform/language/expressions/dynamic-blocks)
- [HashiCorp value references](https://developer.hashicorp.com/terraform/language/expressions/references)
- [Module refactoring](https://developer.hashicorp.com/terraform/language/modules/develop/refactoring)


[Previous lesson](./34-terraform-inputs-locals-and-outputs.md) · [Next lesson](./36-terraform-state-locking-and-bootstrap.md)
