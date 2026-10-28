---
title: "Terraform expressions and type system"
topic: "Terraform expressions and type system"
last_researched: 2026-10-27
source_labels: Terraform mechanics; New credential-free practice extension; Project code comparison
---

# Terraform expressions and type system

Prerequisite: lessons 32–39. Read a plan confidently before making an expression clever. This lesson develops a new service-inventory example; it does not describe additional deployed project infrastructure. The objective is to predict the type, availability and resource-identity consequences of an expression before running it.

## Step 1: separate values from instructions

An expression produces a value. Terraform then uses that value as an input to a graph of operations. A `for` expression transforms a collection; it is not a shell loop executing an API call once per iteration. A conditional expression selects a result. The graph and provider determine the eventual operations. This separation explains why a collection can be transformed in `locals` without creating any resource.

Start with `{ catalog = { enabled = true }, preview = { enabled = false } }`. The new lab computes `{ for key, service in var.services : key => service if service.enabled }`. The result is a map with `catalog` as its only key. Braces construct a mapping; square brackets would construct a sequence. The trailing `if` removes elements. It does not set the omitted element to null. That difference matters because feeding the result into `for_each` changes which resource addresses exist.

Write the expected keys before running anything. Next, change an owner's name without changing the map key. The object's contents change but its address remains stable. Finally disable a previously enabled key: Terraform now proposes removal of that instance. The same filter that looks harmless in a console can authorize destruction when it supplies resource identity.

## Step 2: give inputs a deliberate shape

The lab declares a map of objects with a required string owner, optional boolean enabled defaulting to true, and optional string tier defaulting to standard. A type constraint defines an accepted interface. `any` does not mean “all possible types simultaneously”; Terraform still needs a concrete compatible type. Prefer an explicit object when consumers rely on named attributes.

Objects and maps are related but different: object attributes can have distinct types; map elements share an element type. Tuples describe individual positions; lists describe a sequence of one element type. Sets remove duplicates and do not promise positional order. Turning a list into a set therefore changes both information and addressing choices. Type conversions can also discard extra attributes when converting a larger object to a narrower object constraint. An object declaration is a useful contract, but it does not automatically reject every misspelled extra key. Test the behavior you intend instead of describing Terraform objects as universally “strict.” [Type constraints](https://developer.hashicorp.com/terraform/language/expressions/type-constraints) document these conversions.

Do not use implicit conversion as a substitute for a design decision. If an output combines a port number with text, convert it deliberately with `tostring` or a formatting function. In a conditional, keep both branches compatible. Returning an object from one branch and an unrelated string from the other forces Terraform to find a common type or report an error, which can conceal the interface you meant to expose.

## Step 3: distinguish absent, null and unknown

An omitted attribute is absent from the supplied object. A null value represents omission where the receiving argument permits it. An unknown value exists conceptually but cannot yet be calculated. A newly created resource ID is often unknown during planning. Null is therefore not a synonym for “known after apply.” [Types and values](https://developer.hashicorp.com/terraform/language/expressions/types) explain null's role.

In the lab, `optional(string, "standard")` gives a non-null default when tier is omitted or explicitly null. By contrast, `optional(string)` permits a null result. A resource argument set to null can use a provider default, but a required argument can reject it. Decide this at the module boundary; otherwise a missing value travels deeper into a provider diagnostic that the caller cannot easily interpret.

Unknown values propagate through calculations. A plan can show unknown output values while still knowing all instance keys. `for_each` needs its keys during planning. Do not construct those keys from future IDs. Keep identity in configuration and place computed IDs in map values. `try` handles certain evaluation errors; it does not magically reveal an unknown value. `can` tests whether an expression can be evaluated without an error; it is useful in validation, not an excuse to hide every broken reference.

## Step 4: use functions and templates with boundaries

Use `trimspace` to normalize an owner, `contains` to allow a small tier vocabulary, and `alltrue` to validate every object. Normalize once near the input boundary so outputs remain predictable. Avoid timestamps or randomness in identity expressions: values that change each run can force recurring differences.

The project reads a static shell script with `file("${path.module}/user-data.sh")` in [its pinned AWS root](https://github.com/robertovalencia/linked-in-node-and-aws/blob/8b2c3e087014d76f9025dc47f5ede7837d73bfe6/infra/aws-dev/main.tf). That call reads the script without treating its contents as a Terraform template. A separate new illustration, `templatefile("${path.module}/notice.tftpl", { owner = var.owner })`, reads an existing UTF-8 template and substitutes explicitly supplied variables. It does not establish an execution dependency on a file created later. Prefer `jsonencode` for JSON and `yamlencode` for YAML rather than assembling escaped structured text by hand. The [templatefile reference](https://developer.hashicorp.com/terraform/language/functions/templatefile) describes its input boundary.

## Practice and expected results

Run `python3 docs/nodejs-aws-study-path/labs/terraform-advanced/run.py`. Read the child contract and predict two initial keys, catalog's standard tier, and preview's absence. The runner proves those observations, changes catalog's owner, and adds search while preserving existing IDs. Its tests exercise an explicit null default and reject an invalid tier. No AWS provider is involved. An unknown ID in the first plan is expected; an unknown map key would be a design failure.

### Recall: Does a typed object reject every extra caller attribute?

**Answer:** No. Conversion to an object constraint can discard extra attributes. Define useful types, validate semantic rules and test likely caller mistakes rather than promising automatic rejection of all unexpected keys.

### Recall: Why can a filtered map lead to destruction?

**Answer:** When it supplies `for_each`, its keys define instances. Removing an existing key removes that instance from desired configuration, so the plan normally proposes destruction unless a deliberate ownership or migration operation changes that outcome.

## References

Official documentation checked on 2026-10-27; the runnable extension was executed with Terraform 1.17.0.

- [Types and values](https://developer.hashicorp.com/terraform/language/expressions/types)
- [Type constraints and optional attributes](https://developer.hashicorp.com/terraform/language/expressions/type-constraints)
- [Template files](https://developer.hashicorp.com/terraform/language/functions/templatefile)

[Previous lesson](./69-cloud-cost-allocation-and-optimization.md) · [Next lesson](./71-terraform-modules-and-contracts.md)
