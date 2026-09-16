# Domain-Driven Design Handoff

Open work for `protocols/ddd.md`. Entries are mutable current state — revised as each item moves, removed when it resolves or is dropped. See [documentation-handoff.md](../documentation-handoff.md) for what a handoff is.

## Open Questions

### Bounded context in live Memar prose
1. `type.md` (and possibly other files) uses "bounded context" in load-bearing sentences while no Memar document defines it. Define it, replace it with a Memar term, or leave it under [Terminology → The Default Meaning of an Unreferenced Term](../terminology.md#the-default-meaning-of-an-unreferenced-term)? Once defined or refused more sharply, prior-art mentions may point at [What Is Problematic under the Canopy](./ddd.md#what-is-problematic-under-the-canopy). *(Blocking: no for this protocol.)*

### Whether the umbrella's member list grows past four
1. The membership criterion — a commitment belongs when it constrains which force determines the design — may admit further Modeling topics (e.g. Models Must Survive Implementation Changes, Behavior and Structure Are Discovered Together). Examine and either admit them or record why they constrain something else. *(Blocking: no.)*

### Practice companion
1. Deferred. [modeling.practice.md](../modeling.practice.md) owns model discovery; [tdd.practice.md](./tdd.practice.md) owns the expectation-and-check step. The one procedural element here is the label-substitution obligation in [Memar's Stance on the Name](./ddd.md#memars-stance-on-the-name). Extract a companion if that substitution outgrows a paragraph, or if the competing-driver check becomes a repeated review step with failure modes of its own. Until then, inventing a pipeline to fill the slot would commit the mechanism-catalog error this document refuses.

### Protocols folder membership criterion
1. [`protocols/README.md`](./README.md) currently names two kinds. This document argues placement as rules for development conducted under a circulated design name. Widen the README criterion, or restated membership under an existing clause? *(This is a `protocols/` folder question, not a documentation-method question. Blocking: no — the document stands on its conformance topic either way.)*

## Anticipated Work

- When convenient, retarget body prior-art in `modeling.md` that attributes model-first commitments upward to Evans so the body reads as Memar's position (changelog keeps the provenance) — not because naming Domain-Driven Design is forbidden, but because prior art must not read as authority.
- If the multiple-models critique needs more than a bullet — e.g. a stated re-derivation-path obligation — that content belongs to Modeling, not here; this document would then cite it.
- If bounded context is defined or replaced, retarget the absence row and live prose.
