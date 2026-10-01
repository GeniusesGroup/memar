---
Title: "Khayyam Rule — Domain Capsule Naming"
Status: Draft
Start Date: 2026-09-29
ID: "497405"
---

# Khayyam Rule — Domain Capsule Naming
Khayyam's rules live one rule per folder under [`modules/khayyam/rules/`](../README.md), and this is the rule for capsule names that organize behavior by domain rather than by utility category. It is a governance rule of this repository.

## The rule
Responsibilities belong in domain-meaningful capsules (`UserRegistry`, `ConnectionIndex`, `ServiceCatalog`), not in utility dumping-ground capsules. This repository discourages capsule names and module groupings whose primary label is a utility category: `Helpers`, `Utils`, `Common`, `Shared`, `Base`, and similar generic containers.

The [file layout rule](../file-layout/file-layout.md) and import model reinforce organizing behavior around domain concepts rather than utility categories.

## Why it exists
Utility-oriented capsules become architectural dumping grounds in mature codebases. Khayyam's modeling style already pushes domain-specific types; a naming rule makes the organizational expectation explicit where the grammar cannot forbid a capsule name.

## Keep it or drop it
An organization may keep utility capsules for transitional code, generated ports, or internal tooling layers. This repository discourages them in authored domain code.

## What this rule does not claim
- It does not claim the grammar rejects `Utils` or `Helpers` as identifiers.
- It does not claim every shared helper must become a domain capsule immediately during porting.
- It does not govern abstraction or method naming; see sibling rules.

## Open questions
This rule's own open state lives in its [handoff](./domain-capsule-naming.handoff.md).
