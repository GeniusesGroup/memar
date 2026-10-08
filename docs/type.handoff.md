# Type Handoff
Open work for `type.md`. Entries are mutable current state — revised as each item moves, removed when it resolves or is dropped. See [documentation-handoff.md](./documentation-handoff.md) for what a handoff is.

## Open Questions

### The implementation module is named `datatype`, and the concept is named Type
- State: the concept is **Type** ([`type.md`](./type.md)), and the module realizing it in this repository is [`modules/computer/datatype/`](../modules/computer/datatype/). The name was chosen to dodge Go's `type` keyword, because the folder held an abstraction bridge rather than Khayyam sources. That reason has expired: the units are `.kh` and the language's keyword for the form is `tp` and `vr` ([`bundles/khayyam/core/src/scan.ts`](../bundles/khayyam/core/src/scan.ts)), so nothing in Khayyam reserves `type`. The owner's ruling on 2026-10-05 is that the module takes the concept's own name, `type`. A second folder, [`modules/computer/datatypes/`](../modules/computer/datatypes/), holds three files and is the one [composition-not-duplication](../bundles/khayyam/rules/composition-not-duplication/composition-not-duplication.md) already records as a collision against `datatype`, so the pair must be settled before the rename has a base.
- Next: decide what `datatypes/` is and whether it is kept, then migrate the URI. **This is not a rename but a source-wide migration**: 98 `.kh` units carry `modules/computer/datatype/` in an `in` URI, and the [import address rule](../bundles/khayyam/rules/import-address/import-address.md) owns the spelling. The migration therefore belongs to the rule's owner and not to a session that is placing folders.
- Question for the owner: whether the rename is worth a 98-file URI migration now, and whether `datatypes/` is a duplicate to retire or a distinct subject that survives under its own name.

### Rules checking
- State: are rules checked at compile time or runtime? This is the most consequential implementation decision. What happens when rules from different Types conflict? Can business rules be configured without changing the Type's identity? What is the relationship between rule hierarchies and type realization?
- Next: decide with the first rule-bearing realization.

### Bootstrapping without primitives
- State: without primitives, what are the foundational Capsules, and how are they defined without circularity? An implementation concern that affects the Type model's coherence. Cross-referenced 2026-09-16 from the retired `chats-context -- Error & ADT.md` audit: the concrete motivating case recorded there was the String↔Error circular dependency in the stdlib bootstrap, with the owner's standing rejection of solving it via a hidden primitive type (on principle — see the No primitive types rule under Type Principles Realized in `khayyam/khayyam.md`); the language-side track of the same question is tracked in Khayyam's own handoff entry "Stdlib bootstrap ordering under the no-hidden-primitive rule" (`khayyam/khayyam.handoff.md`).
- Next: settle with Khayyam's foundational-capsule work.

## Anticipated Work
- **Refinement types for invariants**: an SMT solver could check simple invariants at compile time.
- **Formal specification of the satisfaction mechanism**: once design decisions are made, the Capsule/Abstraction bridge could be specified formally.
- **Rule analysis tooling**: static analysis to verify invariants, detect rule conflicts, and identify over-constraining.
- **A dedicated Relation document**: addressing whether and how Relations gain independent status, endpoint ownership, directionality, and arity, as a modeling-layer concern built on top of — not inside — the Type definition, informed by prior art such as Chen's Entity-Relationship model, RDF/OWL, property graph databases, and Alloy.
- **AI-assisted delegation generation**: instant, auditable scaffolding of forwarding methods.
- **Formal verification of the behavior graph**: with no hidden edges, verification scope equals source scope.
- **Ownership-clarity metrics**: IDEs and linters could compute and display an "ownership clarity score" for each component — a measure of how easily a reader can determine the origin of each behavior.
- **Delegation pattern library**: standardized forwarding/adapting/decorating patterns reducing the burden without hiding anything.
- **Beyond software**: responsibility-clarity applications in organizational design.
