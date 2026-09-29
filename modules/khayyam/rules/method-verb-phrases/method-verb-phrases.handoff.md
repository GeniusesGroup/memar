# Khayyam Rule — Method Verb Phrases Handoff
Open state for [method-verb-phrases.md](./method-verb-phrases.md). See the repository's [documentation-handoff.md](../../../../docs/documentation-handoff.md) for what a handoff is.

## Status
Active — rule document added 2026-09-29 from [Method Verb Phrases Research 001](./method-verb-phrases.research.001.md); not yet applied as an automated gate on the corpus.

## Decisions
- **A method name is a verb phrase** — Decided (2026-09-29, owner). A bare noun (`Scheme`, `Time`) does not state what the method does; domain verbs (`Elapsed`) are effective in many places, but no single form is preferred yet.
- **Generic `Read` on `Field_X` is not recommended** — Decided (2026-09-29, owner). Composed owners with several field abstractions would collide on `Read`; `Read` homonyms stream I/O read (Deißenböck & Pizka 2005, IWPC).
- **How is a query on an observer abstraction named?** — Decided for Observer/Mutator families (2026-09-29, owner). `Get` + full concept in natural English order; see [observer and mutator rule](../../../computer/adt/rules/observer-mutator/observer-mutator.md). The Get/Set question below stays open **outside** those families.

## Open Questions
- **Whether `Get…` / `Set…` prefixes are discouraged in this repository** (outside Observer/Mutator families). Commit `40c13e36` (2026-07-18) introduced the restriction under the owner's account in `RFCs/khayyam-encapsulation.md`; it was moved unchanged to [Encapsulation in Khayyam → Naming Conventions](../../../../docs/khayyam/encapsulation.md#naming-conventions). The owner states he never decided that restriction; it is an open question here, not a settled rule. Rejected as a rule claim until the owner rules: treating the encapsulation wording as binding governance.

## Related Artifacts
| Artifact | Relation | Action |
| --- | --- | --- |
| [method-verb-phrases.md](./method-verb-phrases.md) | Base — the rule | Keep in sync |
| [observer-mutator.md](../../../computer/adt/rules/observer-mutator/observer-mutator.md) | ADT rule — Observer/Mutator accessor naming decided here | Keep in sync |
| [receiver-method-names.md](../receiver-method-names/receiver-method-names.md) | Sibling — bare name when receiver supplies context | Keep in sync |
| [Encapsulation in Khayyam → Naming Conventions](../../../../docs/khayyam/encapsulation.md#naming-conventions) | Depends_on — non-binding language suggestions | None (read) |
| [method-verb-phrases.research.001.md](./method-verb-phrases.research.001.md) | Evidence — literature, implicit rules, accessor options | Keep in sync |
