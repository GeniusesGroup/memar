# The Error Changelog

## Changelog

The entries below consolidate the document's former front-matter provenance (`Applied to`, `Citations`, `Contributors`) and its former `## Change Rationale` section. The source records did not carry per-phase timestamps; all three historical phases predate the document's first commit (2026-07-24), so each carries `Time: unknown`. Contributor attribution follows the former `Contributors` field, whose Works lists were not pinned to phases; each contributor is listed under the phase their recorded contribution belongs to.

### Initial draft — the Error Abstraction document (495440)
- Time: unknown (historical import)
- Type: Added
- Cited:
  - [Khayyam](../khayyam.md) — Reference: source of truth for the syntax of every code example in this document (`tp`/`mt`/`vr`/`cp`/`ab`/`sc` keywords, capsule composition, abstraction composition, body-less methods as contracts).
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — claimed, argued: authored all core design decisions across an extended multi-session discussion; defined `Error`'s method composition and boundary-crossing discipline; rejected `Equivalence` and sealed-interface markers; established the `ImplementsError` naming rationale and the optional capability-interface pattern.
  - [Gemini](../../CONTRIBUTORS.md#gemini) (3.1 Pro, extended thinking) — drafted, argued: initial draft.
  - [Super Z](../../CONTRIBUTORS.md#super-z) (GLM-5.2) — drafted, argued: drafted and revised the interface across several rounds; identified and corrected two Go package-visibility bugs in an intermediate marker-method design; argued for, then against, a sealed-interface marker pattern as evidence developed.
  - [Claude](../../CONTRIBUTORS.md#claude) (claude-sonnet-5, extended thinking) — reviewed.

#### Summary
Defined `Error`'s composition (`DataType`, `Field_MediaType`, `ADT`, `ImplementsError`), identity by `DataTypeID()` alone, the rejection of `Equivalence` and of sealed-interface markers, the optional capability interfaces (`Internal`/`Temporary`/`Timeout`), and the multi-cause return convention. Tracked `ADT`'s `IsNull`/`IsEmpty` semantics, the `IsEqual`/`MediaType` redundancy question, and the open Khayyam capsule-composition model.

---

### Boundary-translation rule (originally the separate Error vs. Log document, 000010)
- Time: unknown (historical import)
- Type: Added
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — claimed: authored the boundary-translation discipline that this document absorbs.

#### Summary
Authored in parallel as a standalone document, defining the Capture → Persist → Re-express discipline; the two-audience distinction between `Error` (caller-facing contract) and Log (operator-facing forensic event); the corollary that user-domain outcomes must not be modeled as log events; and the worked financial-transaction example demonstrating the rule. Noted explicitly that the rule cannot be reduced to a structural or syntactic check and is better suited to AI-assisted static analysis than to a linter.

---

### Consolidation of the two documents into one
- Time: unknown (historical import — first committed together on 2026-07-24)
- Type: refactor
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — directed: decided on the merge once both halves were recognized as one question; also decided (informed by document 495420, developed in a parallel session) that each Error concept is its own concrete type.
  - [Super Z](../../CONTRIBUTORS.md#super-z) (GLM-5.2) — rewrote: consolidated the two discussions into this single canonical document; restructured the merged content to follow then-current body-section specification; verified all Khayyam code examples against khayyam.md's syntax rules.

#### Summary
Merged the *Error vs. Log* boundary-translation rules into the *Error Abstraction* document, on the recognition that they answer two halves of one question — what an `Error` *is*, and what it is allowed to do when it leaves its origin layer — and that forcing readers to load two documents produced the same scattering problem the documentation specification was written to eliminate. Every load-bearing claim, alternative rejection, and unresolved question from both sources was preserved without summarizing; a Composition overview topic was added; a Boundary discipline topic now separates the two boundary rules explicitly (process/network crossing vs. diagnostic-to-actionable layer translation); an Enforcement topic states that "each Error is its own type" is load-bearing for everything else.

---

### References repointed to the Type document
- Time: 2026-08-25T00:00:00Z
- Type: refactor
- Propagates to:
  - type.md: Done — the principle this document depends on now lives there as "Stateless Types"; see type.changelog.md for its dissolution record.
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — directed: dissolve pre-facet micro-documents so citations point at Type and Modeling generally.
  - [Super Z](../../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — rewrote.

#### Summary
Error was the motivating case of the dissolved *Static Concepts Must Be Types* document (495421); that document's principle now lives in [Type](../type.md). Nine references were repointed with no content change: the front-matter `Citations` entry, the Abstract's assumption statement, Multi-cause returns, both code-generator Future-possibilities notes, Enforcement (including the `Err` naming-convention pointer, which now targets type.practice.md), Drawback 1, the generic-`Init` rejection rationale, and Prior art (which now names only the memar-go companion analysis directly, since the base document it used to cite alongside that companion is gone).

Recorded for a future pass, so the outstanding work is searchable: this document still carries legacy `Applied to`/`Citations`/`Contributors` front matter and a `## Change Rationale` section from before the Facet split, and is due for its own Explanation-facet migration like the rest of the set.

---

### Migration to the Explanation-facet template
- Time: 2026-08-25T00:00:00Z
- Type: refactor
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — requested: continue the documentation-correction pass onto this document itself.
  - [Super Z](../../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — rewrote.

#### Summary
The body already conformed to `documentation-explanation.md` (Abstract; Introduction with Motivation and Methodology; topic-first Explanation with per-topic Discussion bundles; Results; document-wide Discussion); the remaining work was provenance and identity. The former `Applied to`, `Citations`, and `Contributors` front-matter fields and the trailing Change Rationale section moved into this file (entries above, in phase order). Citation dispositions: the Type dependency is now linked directly in the body (see the repointing entry); the Khayyam syntax-source citation became an ordinary body link at its one reader-needed mention (Unresolved questions, capsule-composition model); the abstraction_p.Implements dependency had never had a resolvable URI and remains tracked through the Implements-pattern follow-up under Unresolved questions; the Documentation structure-compliance citation became obsolete under the facet split. H1 aligned to the Title ("The Error"), dropping the subtitle descriptor the Abstract already carries; this changelog retitled accordingly.

---

### Relocated to `docs/protocols/`
- Time: 2026-09-03T00:00:00Z
- Type: refactor
- Propagates to:
  - khayyam-control_flow.md: Done — both `error.md` links repointed to `./protocols/error.md`.
  - khayyam-control_flow.changelog.md: Done — both historical `error.md` references repointed to the new path, content unchanged.
  - khayyam-metaprogramming.md: Done — both `abstraction-implements.md` links repointed to `./protocols/abstraction-implements.md` (that document's relocation was registered in its own changelog).
  - type.practice.md: Done — the `error.md` link repointed to `./protocols/error.md`.
  - chapar.changelog.md: Done — the historical `error.md` reference repointed to the new path, content unchanged.
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — directed, decided: documents defining a Memar framework-level abstraction or contract get their own subdirectory under `docs/`, so that base documents referencing the abstraction layer do so deliberately rather than by accident; the subdirectory was later renamed `docs/protocols/` when its membership widened to Memar's protocol specifications — see the renaming entry below.
  - [Super Z](../../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — moved, rewrote: relocated this document and its changelog, adjusted internal relative links for the new depth, repointed the inbound references listed above.

#### Summary
This document and its changelog moved from `docs/` into the framework-contracts subdirectory (`docs/abstractions/`, since renamed `docs/protocols/`) — a subdirectory whose membership criterion (recorded in its README) is: documents specifying Memar's own framework-level contracts, as distinct from the conceptual foundation documents at `docs/` root. These documents are the source of truth for their protocols, not executable code; implementations live in the `memar-{language}` repositories. No content change; no new dependency or citation introduced.
