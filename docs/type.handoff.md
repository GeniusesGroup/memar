# Type Handoff
Open work for `type.md`. Entries are mutable current state — revised as each item moves, removed when it resolves or is dropped. See [documentation-handoff.md](./documentation-handoff.md) for what a handoff is.

## Open Questions

### Rules checking
- State: what happens when rules from different Types conflict? Can business rules be configured without changing the Type's identity? What is the relationship between rule hierarchies and type realization?
- Next: decide with the first rule-bearing realization.

## Anticipated Work
- **Refinement types for invariants**: an SMT solver could check simple invariants at compile time.
- **A dedicated Relation document**: addressing whether and how Relations gain independent status, endpoint ownership, directionality, and arity, as a modeling-layer concern built on top of — not inside — the Type definition, informed by prior art such as Chen's Entity-Relationship model, RDF/OWL, property graph databases, and Alloy.
- **Formal verification of the behavior graph**: with no hidden edges, verification scope equals source scope.
- **Beyond software**: responsibility-clarity applications in organizational design.
