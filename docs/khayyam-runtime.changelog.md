# Khayyam Runtime Specification Changelog

## Changelog

### Clarify runtime patching vs. Immutable Infrastructure
- Time: 2026-08-27T00:00:00Z
- Type: Changed
- Cited:
  - [Khayyam Compiler Directives](./Khayyam-compiler.md) — Reference: the same `unsafe` runtime-patching description there
  - [Polymorphism in Khayyam](./khayyam-polymorphism.md) — Reference: the Dynamic Dispatch Reducibility note that expects reducibility under Immutable Infrastructure
- Contributors:
  - [Super Z](../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — rewrote: content below

#### Summary
Appends to `Change logic in runtime` a relation note: the default/safe deployment model is Immutable Infrastructure (no runtime capability addition without recompilation); the described `unsafe` WASM-like module replacement is an explicit, opt-in escape hatch, audited and never used for normal evolution, and therefore does not contradict the principle.

---

### Migrate to the Explanation-facet structure
- Time: 2026-08-30T00:00:00Z
- Type: refactor
- Cited:
  - [Documentation — Explanation](./documentation-explanation.md) — Depends_on: the structure this migration follows — YAML front matter, the `Abstract → Introduction → Explanation → Results → Discussion` body, and the per-topic Discussion pattern — is that specification's, applied to this document for the first time.
  - [Khayyam - Programming Language](./khayyam.md) — Reference: *Khayyam Is Not Its Own Compiler or Runtime* and *Separation of Syntax and Governance*, which supply the framing for the new Abstract, Motivation, and Discussion content.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — requested: migrate this document (and its two sibling tooling documents) to the latest documentation methodology; clarified the framing constraint that governs the new sections — none of the three tooling documents may impose anything on Khayyam itself, since together they are recommendations to each component's developers about how Khayyam's own thinking should find concrete manifestation.
  - [Super Z](../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — rewrote: content below.

#### Summary
This document is now structured per `documentation-explanation.md`: YAML front matter added (Status: Proposed; Start Date and ID assigned retroactively from the file's first commit date, 2026-06-26); Abstract, Motivation, per-topic Discussion sections, Results, and a document-wide Discussion added. The opening note (Khayyam does not dictate a runtime; this is the Memar Framework's reference architecture) is preserved and now does double duty as the anchor of the new framing: this document binds runtime *implementers*, never the language, and is deliberately one-runtime opinionated without elevating the Memar Framework's choices to Khayyam requirements. No rule content was removed: the Concurrency and Execution Model section (User-Space Scheduling, Library-Driven Primitives, the MUST-level Core Affinity & Lock-Free Design commitment) and Change Logic in Runtime with its Immutable Infrastructure relation note are both preserved under Explanation. The new Discussion content is derived from Khayyam's own philosophy documents rather than new design decisions — in particular, the motivation that the runtime is the last layer where hidden magic could quietly return, and the caution against readers mistaking Memar-Framework choices for language requirements. New open questions recorded: the user-space/kernel-boundary interaction for pinned tasks; what the `unsafe` tag gates at the runtime layer; whether any part of this reference architecture should eventually become a conformance floor for *any* Khayyam runtime, versus remaining Memar-specific.

#### Rationale and alternatives
Considered renaming the document (e.g., to "Memar Runtime Reference Architecture") to resolve the Khayyam/Memar naming tension the migration's Discussion now describes. Rejected: renaming is a title/concept decision belonging to Omid's review, not a structural migration step — recorded as an open thread in the Discussion instead. Also considered moving the Immutable Infrastructure relation note into a proper `#### Rationale and alternatives` under the Change Logic topic; kept it as the blockquote the previous entry added, since it is a cross-document relation statement, not this topic's own alternatives record.
