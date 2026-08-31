# Encapsulation in Khayyam Changelog

## Changelog

### Created
- Time: 2026-07-15T00:00:00Z (approximated from Start Date)
- Type: Added
- Cited:
  - [Khayyam - Programming Language](./khayyam.md) — Reference: The canonical specification defines capsule, method, and abstraction syntax that this document elaborates and motivates.
  - [Khayyam Design Philosophy](./khayyam-design_philosophy.md) — Reference: The philosophy document recorded the recurring principles (behavior over type identity, domain modeling, syntactic atomicity) underpinning the encapsulation design decisions recorded here. *(That document has since been fully retired and deleted; its content was absorbed into khayyam.md and khayyam-abstraction.md — see khayyam.changelog.md. This citation is preserved as historical provenance only.)*
  - [Abstraction in Khayyam](./khayyam-abstraction.md) — Reference: The abstraction mechanism is specified separately. This document records the encapsulation guarantees (capsules hide all internal state, all interaction occurs through methods) that make the abstraction model possible.
  - [Polymorphism in Khayyam](./khayyam-polymorphism.md) — Reference: Polymorphism classification and dispatch strategy are specified separately. This document defines the capsule-level boundaries that constrain polymorphic behavior.
  - [Method in Khayyam](./khayyam-method.md) — Reference: Method as Callable Capsule — the mechanical spec of the method signature itself (pass-by-reference, parenthesized separation, static-vs-instance invocation, body-less methods) — previously lived in this document's Explanation section and has moved there, since a capsule is an abstraction over `vr`/`mt`, not the other way around. This document now depends on that spec rather than restating it.
  - [Control Flow in Khayyam](./khayyam-control_flow.md) — Reference: The Code Scope (`sc`) topic previously lived in this document's Explanation section and has moved there, since code scopes are structurally the mechanism control-flow libraries (IF/ELSE/LOOP) are built on, not a capsule-level concern.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — claimed: Original design decisions, Sovereign Encapsulation concept, defined the capsule structure, method model, and the elimination of consumer-side mutability keywords in the canonical Khayyam specification
  - [ChatGPT](../CONTRIBUTORS.md#chatgpt) (GPT-5.5, medium effort) — reviewed: critical review
  - [Super Z](../CONTRIBUTORS.md#super-z) (GLM 5.2, medium effort) — rewrote: Restructuring into document template, content consolidation and enrichment; restructured scattered encapsulation-related content into the canonical document template; consolidated content from staging and specification files; added reference-level elaborations on capsule structure, method dispatch, abstraction design, and primitive capsule specification
  - [Claude](../CONTRIBUTORS.md#claude) (claude-sonnet-5, medium effort) — rewrote: Migrated document structure to the current Explanation-facet specification; merged the standalone Absence of Closures and Anonymous Functions document into the Explanation section as a topic following Method as Callable Capsule; extracted Method as Callable Capsule to khayyam-method.md and Code Scope to khayyam-control_flow.md, since capsule is an abstraction over `vr`/`mt` rather than the reverse; reframed Absence of Closures and Anonymous Functions from a negative ("we don't support X") framing to a positive one (closures as an implicit-capsule syntax we chose not to admit, and why)

#### Summary
Initial creation as the authoritative document for Khayyam's encapsulation model.

### Positive reframing of closures
- Time: 2026-07-15T00:00:00Z (approximated; original time not recorded — relative order derived by reversing the base document's newest-first `Change Rationale` listing)
- Type: Changed
- Contributors: not recorded per-change in the source section

#### Summary
"Absence of Closures and Anonymous Functions" renamed to "Closures as Implicit Capsule Syntax" and its opening reframed: rather than starting from "Khayyam does not support closures," it now starts from the structural observation that a closure already *is* an implicit, unnamed capsule, and that Sovereign Encapsulation's existing requirement (state must be named and explicit) is sufficient on its own to explain why this syntax was not admitted — no separate prohibitive rule is needed. The Discussion subsections (Drawbacks, Rationale and alternatives, Prior art) were left unchanged, since the case they make does not depend on which framing introduces the topic. Cross-reference links elsewhere in this document were updated to the new heading.

### Extraction of non-capsule content
- Time: 2026-07-15T00:00:00Z (approximated; original time not recorded)
- Type: refactor
- Contributors: not recorded per-change in the source section

#### Summary
A capsule is an abstraction layered over `vr` and `mt`, not an independent primitive — so content specific to those underlying concepts should be defined in their own documents and only referenced here. Accordingly: "Method as Callable Capsule" (including its Method Invocation Rules and Body-less Methods subsections) moved to [Method in Khayyam](./khayyam-method.md); "Code Scope" moved to [Control Flow in Khayyam](./khayyam-control_flow.md), since `sc` is structurally the mechanism control-flow libraries are built on rather than a capsule-level concern. The Abstract and front-matter Citations were updated to reference both documents instead of restating their content.

### Closures merge
- Time: 2026-07-15T00:00:00Z (approximated; original time not recorded)
- Type: Added
- Contributors: not recorded per-change in the source section

#### Summary
Merged the standalone "Absence of Closures and Anonymous Functions" document into `Explanation` as a new topic, placed immediately after "Method as Callable Capsule," on the grounds that it is a direct corollary of Sovereign Encapsulation rather than an independent rule. All original content (summary, motivation, guide- and reference-level explanation, and the full Discussion bundle) was preserved; only the internal headings were removed as part of folding it into the topic-plus-Discussion shape. The document-wide `Discussion > Drawbacks` and `Rationale and alternatives` were extended with one clause each to reflect the newly merged topic. The standalone file has been retired.

### Structural migration
- Time: 2026-07-15T00:00:00Z (approximated; original time not recorded)
- Type: refactor
- Contributors: not recorded per-change in the source section

#### Summary
Brought the document in line with the current Explanation-facet specification (`documentation-explanation.md`): `Summary` renamed to `Abstract`; `Motivation` moved under a new `Introduction` wrapper alongside an (empty) `Methodology`; the former `Guide-level explanation` promoted to a named, first-listed `Explanation` topic ("Capsules and Methods at a Glance") and linked from the Abstract as "Guide"; the `Reference-level explanation` heading removed, its topics now sitting directly under `Explanation`; added an empty `Results` section per the fixed body-section order.

### Absorbed variable-mutability content
- Time: 2026-07-31T00:00:00Z (date recorded in the source listing; time approximated)
- Type: Added
- Contributors: not recorded per-change in the source section

#### Summary
The "Mutability Is a Type Concern, Not a Variable Concern" section was removed from `khayyam-variable.md` (2026-07-31 review) because it was framed entirely as negation and because the underlying rule is not variable-specific — a capsule's own fields need the identical rule. Its substance was folded into [Sovereign Encapsulation](./khayyam-encapsulation.md#sovereign-encapsulation) as a generalization from capsule-level to reference-level (variables and fields alike): the "ill-posed question" framing, the conflation-of-concerns rationale, and the Rust `let`/`mut` prior-art detail were merged into the existing paragraphs rather than kept as a separate topic. One gap the removed text also left open was surfaced explicitly as a new unresolved question: whether a reference itself (not the instance it points to) can be rebound after initial assignment.

### Resolved field-rebinding question; clarified primitive-capsule inlining; documented rejected closure alternative
- Time: 2026-08-01T00:00:00Z (date recorded in the source listing; time approximated)
- Type: Changed
- Contributors: not recorded per-change in the source section

#### Summary
Three points raised in review (2026-08-01): (1) the reference-rebinding unresolved question was split — resolved for capsule fields (field rebinding is definitionally the same event as field mutation, gated by the same method-only-access rule; obtaining the new instance still requires a constructor or an explicit copy/clone abstraction per `khayyam-variable.md`'s Domain-Driven Arithmetic) and scoped out to `khayyam-variable.md` for bare local variables; (2) the Primitive Capsule Specification topic was clarified to state explicitly that inlining is a backend optimization orthogonal to "all interaction occurs through methods," that the listed behavioral guarantees are illustrative rather than mandatory, and that the cost/safety tradeoff for a given primitive capsule (e.g. `W32`) is local to that capsule's own design rather than a language default — resolving an apparent tension between the "zero-cost" framing and the guarantees discussion; (3) the Closures rationale gained a documented-and-rejected alternative (a lighter explicitly-captured inline syntax short of a full capsule declaration), added for completeness though the underlying design decision was not reopened.

### Fully resolved reference-rebinding; named representation exposure as a permanent, unclosable limitation
- Time: 2026-08-01T00:00:00Z (date recorded in the source listing; time approximated)
- Type: Changed
- Contributors: not recorded per-change in the source section

#### Summary
Further review (2026-08-01) closed the reference-rebinding question at both levels rather than leaving the local-variable half deferred: since Khayyam has no primitive types, obtaining any new instance — for a variable or a field — always goes through that type's own constructor or copy/clone contract, and local-variable rebinding touches no capsule's private state to begin with, so no invariant was ever at risk. Separately, the storage-aliasing unresolved question was split into two distinct cases: genuine low-level memory aliasing (still deferred to future memory-management documents, where an ownership/borrow-tracking policy could plausibly help) versus "representation exposure" — a capsule's own method surface returning a reference to a sub-capsule (or exposing an `unsafe` accessor) that itself has a wider mutation surface than intended, letting a caller bypass the outer capsule's control entirely through the sub-capsule's own legitimate, honestly-declared contract. This second case is documented as permanently unclosable by any compiler or linter policy — it is not a type-soundness gap but an architectural discipline question resting entirely on each capsule author's choice of how narrow a return type to expose, analogous to "representation exposure" / defensive-copying discussions in other OOP languages.

### Completed migration to the Explanation-facet specification
- Time: 2026-08-26T00:00:00Z
- Type: refactor
- Cited:
  - [Documentation](./documentation.md) — Reference: facet meta-layer defining Explanation/Practice/Changelog.
  - [Documentation — Explanation](./documentation-explanation.md) — Depends_on: governing structure the base document was brought fully in line with.
  - [Documentation — Changelog](./documentation-changelog.md) — Depends_on: entry structure used for this companion file.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — requested: full migration to the latest documentation method without any summarizing
  - [Super Z](../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — migrated: structural completion and provenance relocation per the Explanation-facet specification

#### Summary
Completed the migration an earlier pass had started (this document already followed most of the current structure). Remaining steps done here: relocated all remaining provenance out of the base document — front-matter `Applied to`, `Citations`, and `Contributors` moved into this file's entries above (the citation to the retired `khayyam-design_philosophy.md` is preserved with a retirement annotation); the body's former `## Change Rationale` section became the dated entries above, ordered oldest-first by reversing its newest-first listing; the empty `### Methodology` heading was removed per the specification ("unused items are simply omitted, not left as empty headers"); and the empty `Results` section received the standard placeholder sentence used across sibling documents. No prose was summarized or shortened anywhere in the base document — all topics, examples, and Discussion bundles are verbatim. No design decision changed.
