---
Title: "Type Rule — Categories Are Roles, Not a Hierarchy"
Labels: Draft
Start Date: 2026-11-09
---
# Type Rule — Categories Are Roles, Not a Hierarchy
A rule of this repository, held for [Type](../../type.md), for the operational checks of [Type Categories Are Not a Hierarchy](../../type.md#type-categories-are-not-a-hierarchy). It applies when classifying a Type or relating Capsule, Method, Abstraction, and Scope.

## The rule
- **The four categories are semantic roles, not an inheritance tree.** Capsule, Method, Abstraction, and Scope are not subtypes of one another.
- **Relate them by named connections** (satisfies, attaches to, extends) — not by parent–child classification.
- **Do not invent a fifth category** unless the candidate role is irreducible to specialization, composition, or usage of these four. A language keyword (`struct`, `trait`, `namespace`, …) does not by itself justify a new category.
- **Abstractions stay pure specifications:** no method bodies and no default implementations on an Abstraction ([Explicit Behavior Ownership](../explicit-behavior-ownership/explicit-behavior-ownership.md)).

## Why it exists
Keeps agents from importing OOP taxonomic habits when applying Memar's Type model.

## Keep it or drop it
An organization may keep a keyword-driven taxonomy and remain outside this rule; it then accepts diluted categories.

## What this rule does not claim
- It does not forbid a future fifth category after irreducibility is shown.
- It is enforced by no check this repository runs today.
