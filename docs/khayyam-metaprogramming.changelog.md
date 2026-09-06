# Metaprogramming in Khayyam Changelog

## Changelog

### Initial draft — synthesis of the standalone Decorators and Macros documents
- Time: unknown (historical import — drafted 2026-07-30 per the document's Start Date; this changelog was created at migration time, so the entry is reconstructed from the document's former `## Change Rationale` section)
- Type: Added
- Contributors: none recorded — the source front matter carried only identity fields, with no contributor attribution; none was reconstructed.

#### Summary
Synthesizes the standalone "Decorators Rejection" and "Rejection of Syntactic Macros and Meta-Programming" documents into this document's Decorators Rejection and Rejection of Syntactic Macros topics. Reflective Programming is newly drafted rather than migrated from an existing document; treat it as more provisional than the rest of this document — several open questions are logged under its own Discussion, and the illustrative `reflect_p.Structural` naming is not a settled proposal.

---

### Migration to the Explanation-facet template
- Time: 2026-09-03T00:00:00Z
- Type: refactor
- Cited:
  - [The Error](./protocols/error.md) — Evidence: the document formerly cited under the title "Error Handling: Library-Driven and Syntax-Free" now exists in this document set under this path, closing the stale open question that recorded it as not yet supplied.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — requested: review the documents touched by the abstractions-directory change for conformance with the current documentation method, applying the progressive-migration rule.
  - [Super Z](../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — rewrote.

#### Summary
The body already conformed to `documentation-explanation.md` (Abstract; Introduction with Motivation and Methodology; topic-first Explanation with per-topic Discussion bundles; Discussion); the migration work was provenance and staleness. The legacy `## Change Rationale` section moved into this file (entry above), per the rule that provenance lives in the paired changelog. The Results section received the standard placeholder. Document-wide Unresolved question 2 — which recorded the Error-handling document as "not yet been supplied to this document set for review" — was removed as stale: that document now exists as [The Error](./protocols/error.md). The body's link to `abstraction-implements.md` had already been repointed to its new `protocols/` location in the relocation pass recorded in that document's changelog. No position changed.
