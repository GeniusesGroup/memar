# Control Flow Changelog

## Changelog

### Initial draft
- Time: unknown (historical import — drafted 2026-06-30 per the document's Start Date; this changelog was created at migration time, so the entry is reconstructed from the former front matter)
- Type: Added
- Cited:
  - [Control Flow in Khayyam](../khayyam-control_flow.md) — Depends_on: this document builds on the precedent set by that document of keeping behavioral policies as ordinary library-driven mechanisms rather than new syntax.
  - [The Error](./error.md) — Depends_on: cited by title in the former front matter as "Error Handling: Library-Driven and Syntax-Free", without a resolvable URI; the reference now targets the canonical Error document. The former front matter's `Extends` and `Conflicts with` fields were empty.
- Contributors: none recorded — the former front matter carried `Author(s): []`; no attribution was reconstructed beyond what the source recorded.

#### Summary
Opened two still-open design questions about library-driven conditional methods: the general naming convention for domain-specific conditional pairs (preferring two etymologically distinct roots over base-plus-negation, against the readability risk of `X`/`NotX` pairs), and the specific naming and placement of the standard library's success/failure branching pair, with four candidate directions explored and none finalized. The former front matter carried an empty `Applied to` field — no propagation was recorded at draft time. The former front matter also contained a malformed duplicate `Citations` key (two separate blocks under the same field name); its content is consolidated into the Cited entries above.

---

### Relocated to `docs/protocols/`
- Time: 2026-09-03T00:00:00Z
- Type: refactor
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — directed, decided: documents defining a Memar framework-level abstraction or contract get their own subdirectory under `docs/`, so that base documents referencing the abstraction layer do so deliberately rather than by accident; the folder's criterion is implementation-independent *decisions*, not the absence of Khayyam examples, so this Khayyam-flavored document belongs. The subdirectory was later renamed `docs/protocols/` — see the entry below.
  - [Super Z](../../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — moved: relocated this document to the new subdirectory and adjusted its relative links for the added depth.

#### Summary
This document moved from `docs/` into the framework-contracts subdirectory (`docs/abstractions/`, since renamed `docs/protocols/`). No content change accompanied the move itself; relative links to khayyam-control_flow.md, khayyam-memory_model.md, and khayyam-polymorphism.md were adjusted for the added depth. The link to the Error document required no path change — both documents now share the directory.

---

### Migration to the Explanation-facet template
- Time: 2026-09-03T00:00:00Z
- Type: refactor
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — requested: review the documents touched by the abstractions-directory change for conformance with the current documentation method, applying the progressive-migration rule.
  - [Super Z](../../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — rewrote.

#### Summary
The document previously followed the legacy RFC body structure (`Summary / Motivation / Guide-level explanation / Reference-level explanation / Drawbacks / Rationale and alternatives / Prior art / Unresolved questions / Future possibilities`) with `Applied to`, duplicated `Citations`, and `Author(s)` front matter. Migration mapping, with every load-bearing claim preserved without summarizing: Summary became the Abstract; Motivation kept its role under Introduction; Guide-level explanation split into the two Explanation topics *Two etymologically distinct roots, not base-plus-negation* and *Candidates for the success/failure branching pair* (the candidates, with their rejection reasons, are the second topic's content); the one-line Reference-level explanation ("Not yet finalized — pending resolution") folded into the second topic's lead, since document-wide Unresolved questions carry the same pending state; Drawbacks, Prior art, Unresolved questions, and Future possibilities moved to the document-wide Discussion. The former `Rationale and alternatives` section was a pointer back to the guide-level alternatives, which now live in the candidates topic — nothing was lost by folding it, and no document-wide Rationale entry was added because the document-wide Discussion had no additional rationale content. The former `Applied to`, duplicate `Citations`, and `Author(s)` front-matter fields moved into this file (entries above). No position changed.

---

### Retitled to "Control Flow" and widened from a naming convention to the framework-level control-flow protocol
- Time: 2026-09-03T00:00:00Z
- Type: revised
- Cited:
  - [Control Flow in Khayyam](../khayyam-control_flow.md) — Extends_by: that document's Unresolved questions carried the note that the naming-convention discussion was "not yet a separate document"; its library-driven-conditional rationale is the language-level layer beneath this document's protocol layer.
- Propagates to:
  - khayyam-control_flow.md: Done — its Unresolved questions note referencing the "(not yet a separate document)" discussion updated to reference this document by name.
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — decided: a document scoped to a naming convention was too narrow for the directory it lives in and for the subject itself; the framework-level control-flow protocol — of which naming is one rule — is the real subject, and this document should grow into it the way the other protocol documents are expected to (records today's open questions, develops the topics as they are actually designed). Khayyam's document explains *why* the language has none of these mechanisms; this one owns *what rules* the framework sets.
  - [Super Z](../../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — rewrote.

#### Summary
The document was retitled from "Conditional Method Naming Convention (Presence/Absence Pattern)" to "Control Flow" (ID unchanged — a title change that widens scope at Draft status, not a new document). The Abstract was rewritten to state the widened scope: the framework-level home for Memar's control-flow protocol, with Khayyam's control-flow document as the language-level rationale layer beneath it. The two existing topics (naming convention, branching-pair candidates) survive unchanged in position; a new topic, *Topics to be developed here*, registers the planned growth areas — the conditional-pair protocol as an abstraction contract, iteration/loop-shaped control flow, and halting semantics — without pre-deciding their content. The filename changed from `conditional_naming_convention.md` to `control-flow.md`; this changelog file follows (`control-flow.changelog.md`) and was retitled accordingly.
