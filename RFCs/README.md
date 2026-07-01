# Memar Framework — RFCs
This directory contains the design decisions behind the Memar framework and all its components, including the Khayyam language, the recommended toolchain, and the broader architectural philosophy.

**These RFCs are not limited to any single component.** A given RFC may affect the language, the recommended framework library, linter/compiler behavior, OS-layer assumptions, or several of these at once. The scope of each RFC is stated explicitly in its own content.

**For readers and AI assistants:** you do not need to read every RFC in full to answer a question. Start from the titles and status column below to find what is relevant, then jump directly to the specific section you need inside that file. Every RFC follows the same section structure (Summary → Motivation → Guide-level explanation → Reference-level explanation → Drawbacks → Rationale and alternatives → Prior art → Unresolved questions → Future possibilities), so you can navigate directly to the section that answers your question rather than reading end-to-end.

Template for new RFCs: [`000000-rfc-template.md`](./000000-rfc-template.md)

---

## Index

| Number | Title | Status |
|--------|-------|--------|
| [000001](./000001-framework-language-os-relationship.md) | The Relationship Between Framework, Language, and Operating System | Proposed |
| [000002](./000002-sovereign-encapsulation.md) | Sovereign Encapsulation: No Consumer-Side Mutability Keywords | Proposed |
| [000003](./000003-library-driven-control-flow.md) | Library-Driven Control Flow | Proposed |
| [000004](./000004-composition-depth-as-decomposition-signal.md) | Composition Depth as a Decomposition Signal (No Expression Chaining) | Proposed |
| [000005](./000005-absence-of-closures.md) | Absence of Closures and Anonymous Functions | Proposed |
| [000006](./000006-domain-driven-arithmetic.md) | Domain-Driven Arithmetic: Operator Elimination and Compile-Time Formula Evaluation | Proposed |
| [000007](./000007-containers-without-generics.md) | Containers, Generics Elimination, and Rich Domain Models | Proposed |
| [000008](./000008-memory-model.md) | Memory Model: Sovereignty, No Pointers/Null, No Lifetime Annotations, PGO | Proposed |
| [000009](./000009-error-handling.md) | Error Handling: Library-Driven and Syntax-Free | Proposed |
| [000010](./000010-error-vs-log-boundary.md) | Error vs. Log: Boundary Translation Discipline | **Draft** |
| [000011](./000011-concurrency.md) | Concurrency: Syntax-Free and Definition-Driven | Proposed |
| [000012](./000012-domain-decomposition-over-aggregate-roots.md) | Domain Decomposition over Aggregate-Root Modeling | Proposed |
| [000013](./000013-naming-driven-package-elimination.md) | Naming-Driven Package Elimination | **Draft** |
| [000014](./000014-dependency-resolution.md) | Dependency Resolution via File URI and Companion Manifest | **Draft** |
| [000015](./000015-function-as-capsule.md) | Function as Capsule (No fn/func Keyword) | Proposed |
| [000016](./000016-constants-as-capsule-methods.md) | Constants as Capsule-Returned Values | **Draft** |
| [000017](./000017-rejection-of-default-implementations.md) | Rejection of Default Implementations (No Trait Default Methods) | Proposed |
| [000018](./000018-i18n-sidecar-metadata.md) | Native Localization (I18n) via Sidecar Metadata (`-detail.kh`) | Proposed |
| [000019](./000019-rejection-of-macros.md) | Rejection of Syntactic Macros and Meta-Programming | Proposed |
| [000020](./000020-conditional-naming-convention.md) | Conditional Method Naming Convention (Presence/Absence Pattern) | **Draft** |
| [000021](./000021-decorators-rejection.md) | Decorators Rejection | Proposed |
| [000022](./000022-tuples-rejection.md) | Tuples Rejection | Proposed |
| [000023](./000023-multiple-declarations-rejection.md) | Multiple Declarations Rejection | Proposed |

---

## Status legend

| Status | Meaning |
|--------|---------|
| **Draft** | Direction is not yet settled; real, unresolved questions remain. See each file's "Unresolved questions" section for exactly what is open. |
| **Proposed** | Design discussion reached consensus. Ready for final review before being reflected in canonical documentation. `Applied to` field is currently empty — not yet merged into any target doc. |
| **Final** | Reflected in canonical documentation. `Applied to` lists exactly where. |
| **Superseded** | Replaced by a newer RFC. See `Superseded by` field. |
| **Rejected** | Considered and explicitly not adopted. Kept for the historical record. |

---

## Notes

- None of the RFCs in this initial batch are marked **Final** yet, because none have been applied to canonical documentation — this is a deliberate next step, not an oversight. The `Applied to` field in each RFC's front-matter will be filled in as decisions are reflected in the relevant documents.
- Five RFCs carry **Draft** status: 000010, 000013, 000014, 000016, and 000020. Each carries a named, genuine unresolved question in its "Unresolved questions" section — not a placeholder, but a specific open design decision that needs to be settled before the RFC can move to Proposed.
