# Time Changelog

## Changelog

### Initial draft — the separation position
- Time: 2026-09-06T00:00:00Z
- Type: Added
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — claimed, argued
  - [Super Z](../../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — reviewed, rewrote

#### What changed
- Initial Draft created, recording the interface-shaped position: time's framework presence is a small ordering/comparison contract plus three separable satellite concerns; mutability ruled out; the definitional question kept genuinely open (Omid Hekayati).
- The position was shaped into the four-concern separation with the minimal-commitment contract (ordering and comparison only), so the unresolved definitional question does not block API rules (Super Z).
- The richer semantics (causality, monotonicity) were distributed to the documents that own them (Super Z).
- The Draft was kept deliberately small (Super Z).

#### Deliberation
- The topic was opened from the project's conceptual discussions (Omid Hekayati).
- The definition of time is unsettled and a framework must not hard-code a metaphysics (Omid Hekayati).
- The ecosystem's bundled "standard time library" mixes four separable concerns (instant, duration, civil conversion, formatting) whose coupling leaks into APIs needing only one (Omid Hekayati).
- The pointer-mediated mutable time values observed in a mainstream library were a cost-and-clarity failure consistent with the framework's value-semantics positions (Omid Hekayati).
- The Draft was to open the topic rather than settle it, and was kept deliberately small accordingly (Omid Hekayati — the instruction; Super Z — applied).

---

### Documentation-method migration: rejected alternatives and anticipated work relocated
- Time: 2026-09-06T00:00:00Z
- Type: refactor
- Propagates to:
  - time.handoff.md: Done - anticipated work recorded there under `Anticipated Work`.
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) - claimed, decided
  - [Super Z](../../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) - moved

#### What changed
- The body's `Discussion` wrappers dissolved entirely, per the finalized documentation method (documentation-explanation.changelog.md, same date) (Omid Hekayati - decided; Super Z - applied).
- The topic-level `Discussion`'s evidence paragraph (the ecosystem's separation direction: monotonic clocks, timestamp/calendar splits, physical-clock versus event-ordering literature) folded into its topic as inline evidence (Super Z).
- The document-level `Drawbacks` removed from the body; its content preserved below without loss (Super Z).
- Rejected-alternative reasoning moved from the body's `Rationale and alternatives` sections into this entry's `Considered and not done`, without loss (Super Z).
- Anticipated work moved from the body's `Future possibilities` into the paired handoff's `Anticipated Work` (Super Z).

#### Considered and not done
- **Adopt the ecosystem's bundled time type as the framework default (rejected)**: the coupling argument; also contradicts the framework's posture that a concept's abstractions are sized to the responsibilities actually exercised. (Omid Hekayati)
- **Defer the entire topic until Khayyam's type system settles (rejected)**: the separation rule binds API design now - every API accepting a bundled time type today is a future migration; recording the rule early is cheaper. (Omid Hekayati)

#### Considered and not done (from the removed document-level Drawbacks section)
- **Separation has a real ergonomic cost: the common case ("give me now, compare it to later") now names two abstractions where the ecosystem names one** — accepted deliberately, because the bundling cost is paid by every API forever while the ergonomic cost is paid by every call site once — and tooling mitigates the latter, nothing mitigates the former. (Omid Hekayati)
