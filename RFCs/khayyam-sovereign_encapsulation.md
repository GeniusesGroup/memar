---
RFC Number: 0000
Title: "Sovereign Encapsulation: No Consumer-Side Mutability Keywords"
Status: Proposed
Start Date: 2026-06-30
Applied to: []
Supersedes: null
Superseded by: null
Related:
  Depends_on: ["000001"]
  Extends: []
  Conflicts with: []
Author(s): []
---

## Summary
Khayyam eliminates all consumer-side control keywords and modifiers — there is no `mut`, `const`, `readonly`, `final`, or pointer annotation. All internal data fields of a capsule are strictly private; mutability and lifecycle behavior are intrinsic properties of the capsule's own definition, never something a caller can grant or deny at the call site.

## Motivation
Languages like Rust, C++, and TypeScript split the burden of managing mutability and lifecycle safety between the definition site and the consumer site, via keywords such as `mut`/`const`. This forces the consumer to explicitly dictate how they intend to treat an instance, and lets a caller override boundaries that should fundamentally belong to the domain model — a form of syntactic band-aid for weak encapsulation, and a source of constant call-site cognitive load (deciding whether to append `mut`/`const` on every declaration).

## Guide-level explanation
In Khayyam, a capsule's public methods are its entire contract. If a capsule exposes no mutating methods, it is inherently immutable — the consumer needs no keyword to "promise" not to mutate it, because there is no mechanical way to do so. If a consumer needs a differently-behaving variant of a data structure (e.g. a mutable wrapper around an otherwise immutable value), that is treated as a new business domain requirement: a new capsule with a distinct identity (e.g. `TransactionAmount` wrapping a fixed `Decimal_64_64`), not a local syntax trick like declaring `const`.

## Reference-level explanation
- **Sovereign Encapsulation:** all internal fields are strictly private; there is no public-field syntax; interaction only occurs via method invocation (message passing).
- **Inherent Immutability / Mutability:** derived purely from whether mutating methods exist on the capsule — never from a caller-side annotation.
- **Domain Integrity over Syntactic Configuration:** any required behavioral variant of a data structure is modeled as a new capsule with a new identity, not a modifier.
- **Eradication of Call-Site Cognitive Load:** variables (`vr`) are clean references with no decoration; capabilities are entirely discovered through the referenced capsule's public interface.

## Drawbacks
Every behavioral variant of a value (e.g. a frequently-needed mutable view of an otherwise-immutable type) requires defining and naming a new capsule, rather than a one-character keyword at the call site. This is intentional friction (see RFC 0004), but it does mean more named types exist in a codebase than in languages with consumer-side modifiers.

## Rationale and alternatives
The alternative (consumer-side `mut`/`const`) was rejected because it allows behavior overrides at the call site that bypass the domain model's own invariants, and because it adds a constant low-grade decision burden to every variable declaration.

## Prior art
Rust's `mut`, C++'s `const`, TypeScript's `readonly` all place this responsibility at the consumer site. Smalltalk-style strict message-passing encapsulation (no public fields at all) is closer to Khayyam's model.

## Unresolved questions
None at this time.

## Future possibilities
None recorded yet.
