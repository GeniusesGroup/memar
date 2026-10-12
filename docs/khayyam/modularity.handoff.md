# Modularity in Khayyam Handoff
Open work for `modularity.md`. Entries are mutable current state — revised as each item moves, removed when it resolves or is dropped. See [documentation-handoff.md](../documentation-handoff.md) for what a handoff is.

## Open Questions

### Naming Without Package Context
1. Is a whole-file inclusion form beyond `in` genuinely needed? Earlier design material mentioned a hypothetical `im` keyword (`tp {name} im {address}`) for including an entire file under one local name, such as `jsonEncode.Encoder`; it was exploratory, not a commitment to a second import mechanism. Whether `in` alone can cover both inclusion of a named entity and any future whole-file inclusion need remains unresolved.

### Cyclic Module Dependencies
Khayyam has not settled whether and how its grammar or tooling restrict cycles among module inclusions. Go forbids cyclic package imports outright, and the ban behaves like a compilation-speed measure rather than a modeling truth: developers satisfy it by dropping type information across package boundaries (for example, passing an account identifier as a plain string where a real identifier Type exists), losing exactly the nominal distinction the type model is for. The conceptual layer has already ruled that mutual conceptual dependence between Modules is not, by itself, a defect and that language cycle restrictions must not be forced onto the model ([Modularity → Conceptual Relationships Are Not Runtime Coupling](../modularity.md#conceptual-relationships-are-not-runtime-coupling)); the language layer still owes the positive decision — no restriction, a restriction with an escape hatch, or an out-of-band tooling rule — and its rationale.

## Anticipated Work
- Both anticipated items below were overtaken on 2026-09-30: the dedicated document exists ([dependency management](../modules/computer/module-dependency.md)), and the manifest is not a language subject. What remains for the language is the one question its own section names — whether the grammar is ever affected by an answer on the dependency side — and nothing is currently pending on it. (From the Manifest-as-Module-Contract topic's retired Future possibilities, and the document-level retired Future possibilities.)
