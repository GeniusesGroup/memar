---
Title: "Type Rule — Type Metadata Carrier"
Labels: Draft
Start Date: 2026-11-09
---
# Type Rule — Type Metadata Carrier
A rule of this repository, held for [Type](../../type.md), for how [Type Metadata](../../type.md#type-metadata) is carried. It applies when adding access, intent, or human-facing data to a Type.

## The rule
- **Access needs are already answered inside the Type:** boundary-level encapsulation plus each method's own invocation level. Never introduce a declared access marker for visibility.
- **Tooling intent signals are ordinary constructs,** and only where automated assistance has real value; keep such signals inert at runtime.
- **Multilingual or human-facing data belongs to the Type and has one source.** Localized names, labels, documentation, and localized failure descriptions are carried apart from the functional definition — never inline in it, never in external lookup maps keyed by string.
- **Every further realization receives that data from the one source;** adding a realization means deriving it again, not re-translating.
- **A wording change by a translator must never touch the functional definition.**
- **A localized description explains the subject enough for its audience to distinguish and use it.** Missing or inadequate source wording is a reason to write or investigate an adequate description, not to emit an empty overview; uncertainty is stated where it matters. Empty action notes are appropriate only when no action is needed.
- **Shared human-facing words have one source.** When several types use the same domain name, their companion methods call the owning type's localized method instead of repeating the literal. Persian companion filenames use `per`, as English uses `eng`.
- **A metadata family not covered above uses the same test:** tools and logic → first-class constructs; humans and volume → companion artifacts — then record the decision in [Type](../../type.md) so the family joins the recorded set. The question is never what new declaration form expresses this.

## Why it exists
Absorbed from the former Type Practice companion so carrier choices sit as a rule beside Type rather than a second document under `docs/`.

## Keep it or drop it
An organization may keep external string maps and remain outside this rule; it then accepts drift between contract and human-facing copy.

## What this rule does not claim
- It does not name every metadata family a Type may grow.
- It is enforced by no check this repository runs today.
