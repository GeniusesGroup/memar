---
Title: "Type Rule — Identity at Definition Time"
Labels: Draft
Start Date: 2026-11-09
---
# Type Rule — Identity at Definition Time
A rule of this repository, held for [Type](../../type.md), for the operational checks of [Stateless Types](../../type.md#stateless-types) and Type identity. It applies when mapping concepts onto realizations and when reviewing identity carried as data.

## The rule
- **Which concept this is is answered by the Type alone, at definition time** — never by inspecting runtime data.
- **Three roles stay separate:** identity lives in the type system; behavior in Methods on the Type; data in instance fields. Do not simulate one role with another.
- **A concept with no per-instance state is still a Type** when domain participants name and reason about it on its own terms, and each such Type MUST be its own named entity ([Map Concepts onto Realizations](../map-concepts-onto-realizations/map-concepts-onto-realizations.md)).
- **Refuse identity as a name field, tag, string constant, or enum value inside one shared container filled at runtime.** That demotes identity checks to runtime comparison outside the type system's guarantees.
- **Instance variation within one Type is fields on that Type's realization**, not new Types. Structural similarity or difference between realizations neither creates nor dissolves Type identity.

## Why it exists
Absorbed from the Type Explanation so agents receive the MUST through get-rules-for-subject. Mapping steps that apply it sit in [Map Concepts onto Realizations](../map-concepts-onto-realizations/map-concepts-onto-realizations.md).

## Keep it or drop it
An organization may keep sentinel strings as concept identity and remain outside this rule; it then accepts identity checks outside the type system.

## What this rule does not claim
- It does not decide whether a candidate is a concept; that is Modeling's.
- It is enforced by no check this repository runs today.
