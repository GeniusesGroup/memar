# The Type Handoff
Open work for `type.md`. Entries are mutable current state — revised as each item moves, removed when it resolves or is dropped. See [documentation-handoff.md](../../documentation-handoff.md) for what a handoff is.

## Open Questions

### What positions may a Type's life cycle hold?
- State: the Type's life cycle is declared with no positions at `modules/computer/type/protocol/life-cycle.kh`. The positions it was meant to take survive only in archived comments in that file, which the owner has ruled are not evidence, while source files across the corpus use undeclared position names (`LifeCycle_*`, `Software_PreAlpha`, `ServiceStatePreAlpha`; counted at thirty-three files on 2026-10-02 and not re-measured). [The Error → Composition](../process/error.md#composition) names four positions — `Experimental`, `Stable`, `Deprecated`, `EndOfLife` — and nothing in this repository declares that list. The subject is this module's: [The Type → Type life cycle](./type.md#type-life-cycle) carries the position, and The Error consumes it rather than owning it.
- A second empty life-cycle abstraction, `SoftwareLifeCycle`, is declared at `protocol/software-life_cycle.kh:4` (`modules/computer/type/protocol/software-life_cycle.kh`) and imported by nothing; whether it is the same subject under a second name is open.
- Blocks continuation: nothing in the toolchain resolves either abstraction today. It blocks any statement of what positions a Type may hold, including the one The Error already makes.
- Next: owner ruling on the position set, and on whether `SoftwareLifeCycle` merges into the Type's life cycle or is retired; then the positions declared in the realization, and The Error's composition checked against them.
- Carried from: Go Target Research 001 → Live problems the two archives jointly expose (`bundles/khayyam/targets/go/target.research.001.md#live-problems-the-two-archives-jointly-expose--defects-in-the-sources-and-where-each-one-was-routed`), verified 2026-10-02, routed to Type's handoff 2026-10-08, and moved here 2026-10-10.

### Are a Type's rules checked when it is defined, or while it runs?
- State: whether a realization checks the rules a Type owns at definition time or at runtime is the most consequential decision a realization makes about them. [Type → Type and Rules](../../type.md#type-and-rules) separates invariants, constraints, behavioral rules, and business rules, and records that Design by Contract checks at runtime by default because checking at definition time is undecidable in general; it does not choose a strategy for this module. Moved here 2026-10-10 from Type's handoff, which keeps the rule questions that do not depend on a realization.
- Blocks continuation: no.
- Next: decide with the first rule-bearing realization.

### In what context is the short identifier unique, and is the universally unique identifier read through the Type?
- State: [The Type → Type identity](./type.md#type-identity) takes the short identifier from the leading 64 bits of the universally unique one, as the realization's own comment at `modules/computer/type/protocol/id.kh` says. No source states in what context that shorter form is guaranteed unique. Separately, the realization composes reading operations for the short identifier and its Base64 form into the Type, while the reading operations for the universally unique identifier are declared at `modules/computer/type/protocol/uuid.observers.kh` and composed into nothing.
- Blocks continuation: no.
- Next: state the short identifier's uniqueness context, and whether a consumer reads the universally unique identifier through the Type.

### Companion artifacts per language, or a method per language?
- State: this module carries a Type's human-facing details in companion artifacts beside its definition, one per human language, as moved here from [Type](../../type.md) and [Type Practice](../../type.practice.md). Khayyam → Self-Documenting Code and Naming (`docs/khayyam/khayyam.md#self-documenting-code-and-naming`) states that human-facing text is a value a method writes, "so another language is another method on that type", and the realization declares the details as methods returning text. Whether a companion artifact is the source those methods read, or a second carrier beside them, is not stated anywhere.
- Blocks continuation: no; it blocks a concrete companion-artifact convention.
- Next: settle together with Khayyam's handoff entry Which method returns human-facing text, and on which owner? (`docs/khayyam/khayyam.handoff.md#which-method-returns-human-facing-text-and-on-which-owner`).

## Anticipated Work
- **A concrete companion-artifact convention**, recorded in `modules/computer/type/README.md` once realized. The example Type Practice carried before 2026-10-10 was `TypeName-detail.en` and `TypeName-detail.fa`.
- **Delegation pattern library**: standardized forwarding, adapting, and decorating patterns that reduce the burden without hiding anything. Moved here 2026-10-10 from Type's handoff as a library realization; no module yet owns delegation patterns, so this home is provisional.
