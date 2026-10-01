---
Title: "Khayyam Rule — Type as Argument"
Status: Draft
Start Date: 2026-09-29
ID: "497406"
---

# Khayyam Rule — Type as Argument
Khayyam's rules live one rule per folder under [`modules/khayyam/rules/`](../README.md), and this is the rule for passing a bare type or a method value where a capsule or abstraction instance is expected. It is a governance rule of this repository: [Method in Khayyam → Type-level arguments for `sc` and `mt`](../../../../docs/khayyam/method.md#type-level-arguments-for-sc-and-mt) states what the compiler accepts; this rule states what this repository discourages.

## The rule
- **Bare type where a value is expected**: passing a bare type name where the signature expects a capsule or abstraction instance is a governance smell; the [Linter](../../../../docs/protocols/computer/linter.md) may flag it.
- **Closure-style `mt` pass**: passing an `mt` in closure style — capturing state as an implicit capsule — is discouraged; express the behavior as a named capsule implementing the relevant abstraction ([Encapsulation in Khayyam → Closures as Implicit Capsule Syntax](../../../../docs/khayyam/encapsulation.md#closures-as-implicit-capsule-syntax)).

Type-level arguments for `sc` and `mt` positions that the signature explicitly allows remain valid.

## Why it exists
The grammar permits type-level arguments for control-flow libraries; using that mechanism to smuggle implicit state or to pass types where values belong obscures ownership and works against sovereign encapsulation.

## Keep it or drop it
An organization may allow closure-style method values or bare-type calls in generated or FFI glue code. This repository flags them in authored domain code.

## What this rule does not claim
- It does not claim the grammar forbids type-level `sc` or `mt` arguments where the signature requires them.
- It does not claim every bare-type pass is wrong — only that it is a smell worth reporting.
- It does not replace the closures-as-implicit-capsule language decision; it reinforces it at the linter layer.

## Open questions
This rule's own open state lives in its [handoff](./type-as-argument.handoff.md).
