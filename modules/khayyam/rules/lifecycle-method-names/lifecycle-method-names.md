---
Title: "Khayyam Rule — Lifecycle Method Names"
Status: Draft
Start Date: 2026-09-29
ID: 510447
---

# Khayyam Rule — Lifecycle Method Names
Khayyam's rules live one rule per folder under [`modules/khayyam/rules/`](../README.md), and this is the rule for conventional method names that express teardown and absence on a type's contract. It is a governance rule of this repository: [Khayyam → How Khayyam realizes Memory](../../../../docs/khayyam/khayyam.md#how-khayyam-realizes-memory) and [Memory](../protocols/memory/memory.md) state that absence and teardown are expressed through methods, not keywords; this rule names the spellings this repository uses.

## The rule
When a capsule acquires resources that need explicit release, this repository uses `Deinit()` or `Free()` as the conventional teardown method names. When a type can represent absence, this repository uses `IsNull()` as the conventional absence query name. Path-complete invocation of teardown methods is governance-checked by the [Linter](../../../../docs/protocols/computer/linter.md) under [Memory → Safety enforcement is governance](../../../../docs/protocols/memory/memory.md#safety-enforcement-is-governance).

These names are library convention for this repository, not grammar keywords.

## Why it exists
The grammar has no `nil` keyword and no destructor syntax; lifecycle behavior must be visible on the type's contract. Shared conventional names let tooling, linters, and readers recognize teardown and absence without baking one protocol's spelling into the language.

## Keep it or drop it
An organization may use different conventional names (`Close`, `Dispose`, `IsEmpty`), or leave naming entirely to each capsule author. The language does not require these spellings.

## What this rule does not claim
- It does not claim the grammar reserves `Deinit`, `Free`, or `IsNull`.
- It does not claim every type must implement these methods.
- It does not claim automated teardown insertion; that is [Memory → Teardown is explicit, and automation writes source](../../../../docs/protocols/memory/memory.md#teardown-is-explicit-and-automation-writes-source).

## Open questions
This rule's own open state lives in its [handoff](./lifecycle-method-names.handoff.md).
