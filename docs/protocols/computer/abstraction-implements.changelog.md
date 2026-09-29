# abstraction_p.Implements Changelog

## Changelog

### Initial draft
- Time: unknown (historical import — drafted 2026-07-08 per the document's Start Date; this changelog was created at migration time, so the entry is reconstructed from the former front matter; [Omid Hekayati]'s `claimed` attribution was recorded there without a stated contribution description)
- Type: Added
- Cited:
  - [Control Flow in Khayyam](../khayyam/control_flow.md) — Depends_on: this document builds on the precedent set by that document of keeping behavioral policies as ordinary library-driven mechanisms rather than new syntax.
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — claimed
  - [Super Z](../../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash, effort: Medium — extended thinking enabled) — drafted

#### What changed
- Defined `abstraction_p.Implements` — a single body-less `Implements()` method any Khayyam abstraction MAY opt into composing — as a tooling-facing signal letting codegen tools discover an incomplete capsule's implementation intent before it structurally satisfies its target abstraction.
- Established its semantics: strictly opt-in per abstraction, purely a build/dev-time signal with no runtime guarantee, realizable under a domain-specific name for disambiguation (Error's `ImplementsError`/`ImplError()` as the first example), with the incomplete state otherwise ordinary.
- The former front matter carried an empty `Applied to` field — no propagation was recorded at draft time.

#### Deliberation
- The draft was authored after an earlier, related proposal (RFC 495390) was rejected, and reframed around codegen-scaffolding motivation (Super Z — drafted).
- It was revised after RFC 495414 (a proposed Go-specific 'sealed interface' hardening) was itself rejected (Super Z — drafted).

#### Considered and not done
- **RFC 495390's accidental-satisfaction-prevention framing (rejected)**: solved the wrong problem.
- **RFC 495414 — a Go-specific 'sealed interface' hardening (rejected)**: embedding a shared marker struct and independently writing the same empty method are equally easy to do deliberately, so no realization of this pattern, in any backend, provides a stronger guarantee than any other; the surviving reason for a domain-specific name (e.g. Error's `ImplError`) is disambiguation, not safety.

---

### Relocated to `docs/protocols/`
- Time: 2026-09-03T00:00:00Z
- Type: refactor
- Propagates to:
  - khayyam-metaprogramming.md: Done — both `abstraction-implements.md` links repointed to `./protocols/abstraction-implements.md`.
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — directed, decided
  - [Super Z](../../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — moved

#### What changed
- This document moved from `docs/` into the framework-contracts subdirectory (`docs/abstractions/`, since renamed `docs/protocols/`) — a subdirectory whose membership criterion (recorded in its README) is: documents specifying Memar's own framework-level contracts.
- The file was untracked in version control at move time, so the relocation is recorded by git history only through this entry and the file's new path; no content change accompanied the move itself.
- Its relative links were adjusted for the added depth.

#### Deliberation
- Documents defining a Memar framework-level abstraction or contract get their own subdirectory under `docs/`, so that base documents referencing the abstraction layer do so deliberately rather than by accident (Omid Hekayati — decided).

---

### Migration to the Explanation-facet template
- Time: 2026-09-03T00:00:00Z
- Type: refactor
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — requested
  - [Super Z](../../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — rewrote

#### What changed
- The document previously followed the legacy RFC body structure (`Summary / Motivation / Guide-level explanation / Reference-level explanation / Drawbacks / Rationale and alternatives / Prior art / Unresolved questions / Future possibilities`) with `Applied to`, `Citations`, and `Contributor(s)` front matter.
- Migration mapping, with every load-bearing claim preserved without summarizing: Summary became the Abstract; Motivation kept its role under Introduction; Guide-level explanation became the Explanation topic *Declaring and discovering intent*; Reference-level explanation became the topic *Semantics and constraints*; Drawbacks, Rationale and alternatives, Prior art, Unresolved questions, and Future possibilities moved to the document-wide Discussion.
- Plain-text references were converted to real hyperlinks per the Internal Cross-References convention (the Contract-First Approach mention now links [khayyam.md](../khayyam/khayyam.md); the Prior-art precedent mention now links [khayyam-control_flow.md](../khayyam/control_flow.md)).
- The former `Applied to`, `Citations`, and `Contributor(s)` front-matter fields moved into this file (entries above); the base document retains only identity front matter.
- No position changed.

#### Deliberation
- Review the documents touched by the protocols-directory change for conformance with the current documentation method, applying the progressive-migration rule (Omid Hekayati — requested).

---

### Second migration wave: Discussion retired; routed to changelog and handoff
- Time: 2026-09-11T08:29:10Z
- Type: Changed
- Cited:
  - [Documentation — Explanation](../documentation-explanation.md) — Depends_on: the three-section skeleton and the Relevance-discipline routing this migration applies are defined by the Explanation facet's governing specification.
  - [Documentation — Handoff](../documentation-handoff.md) — Depends_on: any open work created by this migration follows the Handoff facet's specification.
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) - directed
  - [Super Z](../../CONTRIBUTORS.md#super-z) (GLM 5.3) - applied

#### What changed
- The document-wide `## Discussion` section was retired; the body now carries only the three-section skeleton (Abstract / Introduction / Explanation), with nothing new folded inline — every Discussion block routed to this entry or to the handoff.
- The Discussion's Drawbacks record and Prior-art survey are preserved in this entry below; its Rationale-and-alternatives items are recorded under Considered and not done. The one hyperlink in the migrated content (the Prior-art paragraph's [Control Flow](./control-flow.md) reference) needed no retargeting — this file shares the base document's directory.
- The Unresolved questions' open item (no formal criterion for "complex enough to warrant this" beyond abstraction-author judgment) moved to the newly created paired handoff ([abstraction-implements.handoff.md](./abstraction-implements.handoff.md)) as an Open Question, and the Future possibilities item (extension with parameters or a return value) became that handoff's Anticipated Work.
- The Unresolved questions' Resolved item (Error adopting the pattern via its own domain-specific realization) was dropped rather than migrated: it restates the resolution already graduated into the body's Semantics and constraints — the domain-specific-name MAY, the disambiguation reason, and Error's `ImplementsError`/`ImplError()` example.

#### Considered and not done (migrated from the retired Rationale and alternatives)
- **No declaration at all, detect purely via post-completion structural matching (rejected):** does not address the motivating use case — scaffolding an *incomplete* capsule — since an incomplete capsule does not yet structurally satisfy anything.
- **Domain-specific-only declarations, no shared generic base (considered, not chosen as the sole approach):** every abstraction defining its own uniquely-named `Implements`-analog (as `Error`'s `ImplError` does) loses the ability for a single, generic codegen/linter pass to discover "which capsules across the whole codebase declare some implementation intent" without already knowing which specific abstraction to look for. This document does not preclude a specific abstraction from *additionally* defining its own distinctly-named realization (as `Error` does) for disambiguation when multiple abstractions might be claimed at once — the two are complementary, not mutually exclusive, and neither is "stronger" than the other in terms of guarantee.

#### Related work (from the retired Prior art)
Conceptually closest to Rust's explicit `impl Trait for Type` announcing intent ahead of the compiler's completeness check, but expressed as an ordinary composed method rather than new syntax, consistent with the [Control Flow](./control-flow.md) protocol's precedent of keeping such capabilities library-driven rather than syntax-driven.

#### Drawbacks (from the retired body Discussion)
- Adds one extra, functionally-inert method to every abstraction and capsule that opts in.
- Provides no runtime guarantee of any kind — purely informational. A capsule can declare `Implements` intent and never complete it, or complete it and later forget to keep the declaration, with no language-level consequence either way; tooling correctness depends on this declaration being kept honest, which is a discipline/process concern, not something this document enforces.

---

### Contract-First Approach reference retargeted to abstraction.md
- Time: 2026-09-23T05:38:39Z
- Type: Fixed
- Cited:
  - [Abstraction in Khayyam](../khayyam/abstraction.md) — Reference: implicit structural satisfaction is specified there; this document now points at it instead of a heading khayyam.md no longer carries.
  - [Protocol](../protocol.md) — Depends_on: Protocol vs Contract.
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — decided
  - [Mimo](../../CONTRIBUTORS.md#mimo) (mimo-v2.6-flash via OpenCode) — applied

#### What changed
- The structural-satisfaction sentence now cites abstraction.md's implicit structural satisfaction rather than khayyam.md's "Contract-First Approach" — that named heading no longer exists in khayyam.md, so the old link was dangling.
