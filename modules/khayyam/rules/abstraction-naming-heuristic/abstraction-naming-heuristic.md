---
Title: "Khayyam Rule — Abstraction Naming Heuristic"
Status: Draft
Start Date: 2026-09-29
ID: 510444
---

# Khayyam Rule — Abstraction Naming Heuristic
Khayyam's rules live one rule per folder under [`modules/khayyam/rules/`](../README.md), and this is the rule for how an abstraction name should frame a domain concept rather than a technical capability. It is a governance rule of this repository, companion to the [identifier naming rule](../identifier-naming/identifier-naming.md).

## The rule
An abstraction name uses PascalCase and domain-concept framing — what the abstraction *is* in the domain (`Reader`, `Writer`, `Repository`). Names that frame a technical capability or adjective (`Readable`, `Writable`, `Filterable`) are discouraged in this repository: they often signal over-abstraction risk and obscure which domain concept owns the behavior.

## Why it exists
Abstractions are pure behavioral specifications ([Abstraction in Khayyam](../../../../docs/khayyam/abstraction.md)); their names are what the rest of the corpus must write. A capability suffix invites interfaces that describe what code *can do* rather than what domain role it plays, which is the same trajectory that produces `Filterable` beside `User` instead of a named domain abstraction.

## Keep it or drop it
An organization may require capability-style abstraction names, forbid them outright, or apply this only in public API surfaces. This repository applies the heuristic repository-wide as convention, not as a compiler gate.

## What this rule does not claim
- It does not claim the grammar rejects capability-framed abstraction names.
- It does not claim every `Filterable`-shaped name is wrong — only that this repository discourages the pattern by default.
- It does not govern capsule names, method names, or variable names; those live under sibling rules.

## Open questions
This rule's own open state lives in its [handoff](./abstraction-naming-heuristic.handoff.md).
