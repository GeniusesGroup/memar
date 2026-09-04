# abstraction_p.Implements Changelog

## Changelog

### Initial draft
- Time: unknown (historical import — drafted 2026-07-08 per the document's Start Date; this changelog was created at migration time, so the entry is reconstructed from the former front matter)
- Type: Added
- Cited:
  - [Control Flow in Khayyam](../khayyam-control_flow.md) — Depends_on: this document builds on the precedent set by that document of keeping behavioral policies as ordinary library-driven mechanisms rather than new syntax.
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — claimed: attribution was recorded in the former front matter without a stated contribution description.
  - [Super Z](../../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash, effort: Medium — extended thinking enabled) — drafted: drafted after an earlier, related proposal (RFC 495390) was rejected for solving the wrong problem; reframed around codegen-scaffolding motivation instead of accidental-satisfaction prevention. Revised after RFC 495414 (a proposed Go-specific 'sealed interface' hardening) was itself rejected: embedding a shared marker struct and independently writing the same empty method are equally easy to do deliberately, so no realization of this pattern, in any backend, provides a stronger guarantee than any other — the surviving reason for a domain-specific name (e.g. Error's ImplError) is disambiguation, not safety.

#### Summary
Defined `abstraction_p.Implements` — a single body-less `Implements()` method any Khayyam abstraction MAY opt into composing — as a tooling-facing signal letting codegen tools discover an incomplete capsule's implementation intent before it structurally satisfies its target abstraction. Established its semantics: strictly opt-in per abstraction, purely a build/dev-time signal with no runtime guarantee, realizable under a domain-specific name for disambiguation (Error's `ImplementsError`/`ImplError()` as the first example), with the incomplete state otherwise ordinary. The former front matter carried an empty `Applied to` field — no propagation was recorded at draft time.

---

### Relocated to `docs/protocols/`
- Time: 2026-09-03T00:00:00Z
- Type: refactor
- Propagates to:
  - khayyam-metaprogramming.md: Done — both `abstraction-implements.md` links repointed to `./protocols/abstraction-implements.md`.
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — directed, decided: documents defining a Memar framework-level abstraction or contract get their own subdirectory under `docs/`, so that base documents referencing the abstraction layer do so deliberately rather than by accident.
  - [Super Z](../../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — moved: relocated this document to the new subdirectory and adjusted its relative links for the added depth.

#### Summary
This document moved from `docs/` into the framework-contracts subdirectory (`docs/abstractions/`, since renamed `docs/protocols/`) — a subdirectory whose membership criterion (recorded in its README) is: documents specifying Memar's own framework-level contracts. The file was untracked in version control at move time, so the relocation is recorded by git history only through this entry and the file's new path; no content change accompanied the move itself.

---

### Migration to the Explanation-facet template
- Time: 2026-09-03T00:00:00Z
- Type: refactor
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — requested: review the documents touched by the protocols-directory change for conformance with the current documentation method, applying the progressive-migration rule.
  - [Super Z](../../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — rewrote.

#### Summary
The document previously followed the legacy RFC body structure (`Summary / Motivation / Guide-level explanation / Reference-level explanation / Drawbacks / Rationale and alternatives / Prior art / Unresolved questions / Future possibilities`) with `Applied to`, `Citations`, and `Contributor(s)` front matter. Migration mapping, with every load-bearing claim preserved without summarizing: Summary became the Abstract; Motivation kept its role under Introduction; Guide-level explanation became the Explanation topic *Declaring and discovering intent*; Reference-level explanation became the topic *Semantics and constraints*; Drawbacks, Rationale and alternatives, Prior art, Unresolved questions, and Future possibilities moved to the document-wide Discussion. Plain-text references were converted to real hyperlinks per the Internal Cross-References convention (the Contract-First Approach mention now links [khayyam.md](../khayyam.md); the Prior-art precedent mention now links [khayyam-control_flow.md](../khayyam-control_flow.md)). The former `Applied to`, `Citations`, and `Contributor(s)` front-matter fields moved into this file (entries above); the base document retains only identity front matter. No position changed.
