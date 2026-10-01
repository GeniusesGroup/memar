---
Title: "Khayyam Rule — Unbound Type Name"
Status: Draft
Start Date: 2026-09-26
ID: "497335"
---

# Khayyam Rule — Unbound Type Name
Khayyam's rules live one rule per folder under [`modules/khayyam/rules/`](../README.md), and this is the fourth of the four import-resolution rules. It is a compiler-gate rule of this toolchain, not a statement of the language: the language states that a signature names a type, and whether a name in a signature is bound by anything the file declares or includes is a tool's condition over its own semantic representation.

## The rule
A type name used in a signature, a capsule field, or an abstraction composition that no declaration in the unit and no inclusion supplies refuses the unit, with the implementation label `unbound-type-name`. [core/src/frontend.ts](../../core/src/frontend.ts) builds the visible set from the unit's own declarations plus what its `in` declarations bring in, and refuses any unqualified reference outside it. A qualified reference — one containing `.`, of the form `pkg.Type` — is skipped and carries no check today.

## Why it exists
Khayyam has no implicit types and no primitives: every name in a signature is a modeled concept, and a name that resolves to nothing is a claim about a concept that no source in the program supplies. Refusing it at the unit boundary is what lets the semantic representation be the single carrier of what the unit declares — a representation holding an unresolved name would be a representation whose meaning depends on a file the toolchain has not read.

## Keep it or drop it
An organization may keep this rule or drop it, and the way to drop it is to make every name resolvable by construction: a manifest that declares a unit's closure, a generated preamble, or a build step that rewrites each unit's names to qualified ones. A tool that simply stopped checking would be accepting signatures whose types are unknown, which is the position that makes a semantic representation a guess.

## What this rule does not claim
- It does not claim the language refuses an unbound name, nor that the language defines name resolution at all; the toolchain's resolver is a reading, and this document is where the reading is on record.
- It does not claim what a qualified reference means. `pkg.Type` is accepted without a binding check, and its resolution semantics are undecided — they are one of the open questions the [toolchain handoff](../../execution.handoff.md) carries.
- It does not claim a diagnostic message, a code, or a recovery behavior; the diagnostics contract is deferred and the label is an implementation label.

## Open questions
This rule's own open state lives in its [handoff](./unbound-type-name.handoff.md).
