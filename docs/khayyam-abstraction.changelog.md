# Abstraction in Khayyam Changelog

## Changelog

### Initial consolidation, superseding two prior drafts
- Time: 2026-07-11T00:00:00Z
- Type: Added
- Cited:
  - [Control Flow in Khayyam](./khayyam-control_flow.md) — Depends_on: this document builds on the precedent set by that document of keeping behavioral policies as ordinary library-driven mechanisms rather than new syntax.
- Propagates to:
  - khayyam.md: Reference — this document elaborates and motivates `khayyam.md#Abstraction`.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — claimed: defined the core abstraction model and authored the pure-contract philosophy.
  - [Gemini](../CONTRIBUTORS.md#gemini) (3.1 pro, extended thinking) — drafted: initial draft text.
  - [Claude](../CONTRIBUTORS.md#claude) (claude-sonnet-5, medium effort with extended thinking) — reviewed, rewrote: identified the structural-vs-nominal tension, drafted the intentional-satisfaction problem statement, argued for and against alternatives, consolidated multiple prior drafts into this unified document.
  - [Super Z](../CONTRIBUTORS.md#super-z) (GLM, medium effort) — rewrote: merged the prior drafts' content into this document.

#### Summary
Consolidated all design decisions, resolved policies, and open questions related to the `ab` (abstraction) type in Khayyam into a single authoritative document, superseding two prior drafts ("Intentional Abstraction Satisfaction" and "Rejection of Default Implementations") and merging them with existing DX Scaffolding content. Established: abstractions carry no type parameters and no default method bodies; satisfaction is purely structural (no `implements`-equivalent); shared behavior across implementations requires explicit delegation, not inheritance-like defaults; the central open question is whether structural ("accidental") satisfaction is sufficient or whether Khayyam needs an intentional-satisfaction mechanism, with three candidate resolutions identified and none chosen.

---

### Migration to the current documentation methodology, and Behavior Over Type Identity merged in from khayyam-design_philosophy.md
- Time: 2026-08-17T00:00:00Z
- Type: refactor
- Cited:
  - [khayyam-design_philosophy.md] — Depends_on: "Behavior Over Type Identity" and "Reassessment of Parametric Polymorphism" are migrated from that document's Reference-level explanation into this document's Explanation, as part of that document's planned retirement. No stable link is given because that document is slated for removal once its remaining content is redistributed; see this entry's Rationale and alternatives.
- Propagates to:
  - khayyam-agency.md: Done — a related migration ("Khayyam Is Not Its Own Compiler or Runtime") was carried out there in the same review effort; see khayyam-agency.changelog.md.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — requested: asked for this document to be checked for an Agency connection (see khayyam-agency.md's "Agency Beyond Concurrency" topic, added in the same pass), and, while reviewing it, for it to be brought fully up to the current documentation methodology regardless of whether the Agency check changed anything; separately confirmed that `khayyam-design_philosophy.md` is slated for full retirement and asked that any of its content transferable to documents already in scope for this review be transferred now rather than lost.
  - [Claude](../CONTRIBUTORS.md#claude) — reviewed, rewrote: restructured this document from `Summary/Motivation/Guide-level explanation/Reference-level explanation/Drawbacks/Rationale and alternatives/Prior art/Unresolved questions/Future possibilities` (each a top-level section, with "Unresolved questions" items 4 and 5 themselves containing full nested Drawbacks/Rationale/Prior art/Unresolved-questions blocks — the same kind of structural artifact found and fixed in `modularity.md` earlier in this review) into the current template (`Abstract → Introduction → Explanation → Results → Discussion`); moved former "Unresolved questions" items 4 ("Abstraction Design and Over-Abstraction Risk") and 5 ("Abstraction Stability and Versioning") into the document-level Discussion's own Unresolved questions, since their substantive prose was genuine Explanation-level content, not merely restatements of an open question; moved front-matter `Citations`, `Contributor(s)`, and `Applied to` into this changelog; replaced every occurrence of "RFC" referring to Memar's own documents with "document," linking to [Polymorphism in Khayyam](./khayyam-polymorphism.md) and [Control Flow in Khayyam](./khayyam-control_flow.md) where those documents actually exist, and describing the two now-superseded, absorbed drafts ("Intentional Abstraction Satisfaction," "Rejection of Default Implementations") in plain text without a link, since they no longer exist as separate documents; added "Behavior Over Type Identity" and "A Note on Parametric Polymorphism," migrated from `khayyam-design_philosophy.md`, connecting the already-present "Pure Contract Philosophy" to the more general principle behind it and to why Khayyam needs fewer of the classic parametric-polymorphism patterns (`identity<T>()`, `swap<T>()`, `Option<T>`, `Result<T,E>`) than languages that motivated them by constraints Khayyam does not have.

#### Summary
This document is now structured per `documentation-explanation.md`. A structural artifact — two "Unresolved questions" items that were actually full sub-topics with their own nested Discussion blocks — is resolved by moving their substantive content into Explanation and their actual open questions into this document's own Discussion. "Behavior Over Type Identity" and "A Note on Parametric Polymorphism" are added, migrated from `khayyam-design_philosophy.md`, which is being retired; this document keeps only the abstraction-satisfaction-relevant portion of that content, since the more general vision-level material in the source document belongs elsewhere.

#### Rationale and alternatives
Considered migrating "Reassessment of Parametric Polymorphism" to `khayyam-polymorphism.md` instead of here, since it is arguably more about polymorphism mechanics than about abstraction satisfaction specifically, and `khayyam-design_philosophy.md`'s own text names a "dedicated document" for the compilation mechanism this content leads into. Deferred: `khayyam-polymorphism.md` was not supplied for this review, and guessing at its existing content and structure risks duplicating or contradicting something already stated there — the same mistake this review has corrected elsewhere (`modularity.md`'s Protocol paraphrase, this document's own now-corrected structural artifact). Placed here instead, next to the closely related "Pure Contract Philosophy" it elaborates, with a note that `khayyam-polymorphism.md` may be the better long-term home once it can be checked directly.

---

### Corrected: restored full original prose that the previous migration had compressed
- Time: 2026-08-17T00:00:00Z
- Type: Fixed
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — argued: pointed out that the previous entry's migration had summarized and shortened substantial parts of this document — including replacing "Abstraction Validation and DX Scaffolding" with a meta-note instead of its actual content, condensing four full-paragraph Drawbacks into one-line summaries, and condensing six full-paragraph Prior art entries (Go, Rust, Java, TypeScript, Zig, Haskell) into one-line summaries — and that shortening a foundational document like this produces future ambiguity rather than clarity.
  - [Claude](../CONTRIBUTORS.md#claude) — rewrote, corrected: re-read the entire original document in full before rewriting, rather than working from section headings and partial excerpts as the previous pass had. Restored "Abstraction Validation and DX Scaffolding"'s actual Scaffolding/Proactive Warnings content; restored all four Drawbacks to their full original paragraphs, including the `FileLogger`/`Stringer` example; restored all six Prior art entries to their full original paragraphs; restored the `Reader`/`FileReader`, `PresenceHelper`/`Cache`, and `DefaultValidator`/`UserRecord` code examples and the surrounding explanatory text that had been dropped; restored the full "Tooling support for boilerplate reduction" subsection and its four bullets. No content beyond the original document's own text was removed in this correction — only front matter (already migrated in the previous entry) and the mechanical RFC-to-document conversions remain different from the source.

#### Summary
The previous migration entry, despite its own description, had in practice summarized several sections rather than reorganizing them intact — the most serious instance being "Abstraction Validation and DX Scaffolding," which was replaced with a placeholder note rather than the section's real content. This entry corrects that: the document now carries the full original prose, code examples, and paragraph-level reasoning throughout, reorganized into the current template but not condensed.

#### Rationale and alternatives
Considered treating the previous entry's version as good enough, since the current template's own conventions do not forbid concise writing. Rejected: conciseness introduced here was not a stylistic choice, it was an accidental loss of substance during migration — several sections lost their only citable reasoning (e.g., why `FileLogger`/`Stringer` is a real accidental-satisfaction case, not a hypothetical one) and their only worked examples. A foundational, heavily-cross-referenced document like this one is exactly the case where under-specification compounds into future ambiguity, which is the concrete harm this correction addresses.

---

### Correct the receiver-type rule in Abstraction Realization
- Time: 2026-08-27T00:00:00Z
- Type: Fixed
- Cited:
  - [Polymorphism in Khayyam](./khayyam-polymorphism.md) — Reference: examples there use `tp Read mt (self FileReader)…` vs. `self Reader`, exposing the drift
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — requested: noted that examples and the “identical signatures” rule contradicted
  - [Super Z](../CONTRIBUTORS.md#super-z) — rewrote: corrected the rule to exclude the receiver; added covariant-return reference

#### Summary
Corrects the rule in `Abstraction Realization (Implicit Satisfaction)`. The previous wording required “receiver type, parameter types, and return types all match” identically, yet every normative example declared `tp Read mt (self Reader)…` on the abstraction and `tp Read mt (self FileReader)…` on the capsule with a different receiver. The rule now states that for each method the influencing-variable types must match exactly, the influenced-variable types must match exactly or via covariant return, and the receiver is definitionally the implementing capsule itself.

#### Rationale and alternatives
Alternatives: (a) keep the identical-receiver wording and change examples to use the abstraction as receiver (rejected — capsule would not own its method); (b) add an explicit `as Reader` annotation (rejected — reintroduces `impl` ceremony). The chosen wording preserves structural satisfaction while making receiver ownership explicit.
