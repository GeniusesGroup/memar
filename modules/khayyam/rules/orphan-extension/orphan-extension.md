---
Title: "Khayyam Rule — Orphan Extension"
Status: Draft
Start Date: 2026-09-29
ID: 510450
---

# Khayyam Rule — Orphan Extension
Khayyam's rules live one rule per folder under [`modules/khayyam/rules/`](../README.md), and this is the rule for attaching methods to a type outside the type's owning directory. It is a governance rule of this repository: [Modularity in Khayyam → Inclusion Is Not Module Definition](../../../../docs/khayyam/modularity.md#inclusion-is-not-module-definition) states the syntax; [Inheritance in Khayyam → Linter Rules](../../../../docs/khayyam/inheritance.md#linter-rules) records the language-level separation; this rule states how this repository's linter treats cross-directory extension.

## The rule
Khayyam relies on the file system for modularity (no `package` keyword). Syntactically, a file may import a type and attach new methods to it in another file.

- **Local directory extension** — permitted: a type included with `in` may have further methods attached in another file of the same local directory (file-splitting without a package keyword).
- **Distant or external extension** — a governance failure (monkey-patching): attaching a method to a type imported from an external library or a different domain directory. The reference [Linter](../../../../docs/protocols/computer/linter.md) configuration warns or errors on that attachment. The repair is composition (wrap the external capsule in a local one), not a grammar restriction.

The local/distant boundary is directory-based by default and is organization-overridable — see the linter handoff.

## Why it exists
Methods that appear on a type without being defined in its original source are hidden behavior acquisition — the same class of problem inheritance rules reject for capsules. Distinguishing local file-splitting from cross-library patching keeps extension predictable.

## Keep it or drop it
An organization may allow orphan extension for adapters, test doubles, or generated glue. This repository's reference linter configuration does not.

## What this rule does not claim
- It does not claim the grammar forbids cross-file method attachment.
- It does not claim which directory counts as "local" beyond the default; that is organization-overridable.
- It does not claim the compiler participates in the check; this is linter governance.

## Open questions
This rule's own open state lives in its [handoff](./orphan-extension.handoff.md).
