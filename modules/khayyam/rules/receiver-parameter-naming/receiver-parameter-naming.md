---
Title: "Khayyam Rule — Receiver Parameter Naming"
Status: Draft
Start Date: 2026-09-29
ID: 510446
---

# Khayyam Rule — Receiver Parameter Naming
Khayyam's rules live one rule per folder under [`modules/khayyam/rules/`](../README.md), and this is the rule for the name of the owner parameter in a method signature. It is a governance rule of this repository: [Khayyam → Type → Method](../../../../docs/khayyam/khayyam.md#method) and [Method in Khayyam → Method Structure](./method.md#method-structure) state that any name is allowed in the owner group; this rule states what this repository suggests.

## The rule
The owner parameter in `(self {owner})` may use any identifier the grammar accepts. This repository suggests `self` as the name, so method bodies reference the receiver consistently and readers recognize the owner parameter at a glance.

## Why it exists
The owner group is required for readability ([Method in Khayyam → Method Structure](./method.md#method-structure)); the grammar does not fix its spelling. A single conventional name reduces friction when moving between files and when tooling generates method bodies.

## Keep it or drop it
An organization may require `self`, forbid it, or use another convention (`this`, `receiver`, a domain-specific name). The grammar is unchanged either way.

## What this rule does not claim
- It does not claim the grammar requires `self` or any particular owner name.
- It does not govern method names on the receiver; those are the [method verb phrases rule](../method-verb-phrases/method-verb-phrases.md) and [receiver method names rule](../receiver-method-names/receiver-method-names.md).

## Open questions
This rule's own open state lives in its [handoff](./receiver-parameter-naming.handoff.md).
