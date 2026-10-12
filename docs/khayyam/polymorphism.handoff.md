# Polymorphism in Khayyam Handoff

## Topic & Purpose
Open questions and anticipated work for the Polymorphism in Khayyam document (`polymorphism.md`), relocated there when the documentation method retired the document's Discussion wrapper from base documents' bodies.

## Status
Active

Open work for `polymorphism.md`. Entries are mutable current state — revised as each item moves, removed when it resolves or is dropped. See [documentation-handoff.md](../documentation-handoff.md) for what a handoff is.

## Open Questions

### Should Abstraction Extension Support Multiple Inclusion Without Conflict Resolution?
- State: moved 2026-09-11 from the document's retired Discussion wrapper. When an abstraction `C` includes both `A` and `B`, and `A` and `B` both define a method with the same name and compatible signatures, the outcome is unsettled: (a) the method is required once (signature unification), (b) the capsule must implement the method separately for each abstraction's "view," or (c) it is a compile-time error and the developer must restructure the abstraction hierarchy. This is the classic diamond problem from multiple inheritance; Khayyam avoids the worst case (behavior transfer), but the name collision issue remains.
- Next: decide among the three options when a real multi-inclusion case demands it — the answer affects how abstraction extension can be used in practice.

### Should There Be a Mechanism for "Sealed" Abstractions?
- State: moved 2026-09-11 from the document's retired Discussion wrapper. A sealed abstraction — satisfiable only by capsules defined within the same module or package — would model closed type hierarchies (e.g., `Result` with exactly two variants: `Ok` and `Err`); without sealing, any external capsule could satisfy the abstraction, which may be undesirable for abstractions that represent a closed set of behaviors. The candidate expression is a Linter rule (enforcing that only certain files can contain capsules satisfying a specific abstraction) rather than a language feature, consistent with Khayyam's governance philosophy.
- Next: decide between the linter-rule expression and a language feature.
- Related need, moved here 2026-10-10 from [Type Practice → Mapping concepts onto realizations](../type.practice.md#mapping-concepts-onto-realizations) step 4: exhaustiveness checking over an open abstraction used as a multi-outcome type is real and unresolved, and is assigned to linter or compiler tooling, not to signature syntax; until that tooling exists, callers rely on manual completeness discipline. Candidate mechanisms: code-generator metadata, whole-program analysis, and closed or sealed hierarchies (Kotlin `sealed class`, Swift protocol-conformance-closed types), which reach exhaustiveness over compiler-known closed sets of Types without runtime tags. The stance is the review maxim "polymorphism is about code reuse, not about teaching the compiler how to do its job."

### Scaffolded Container Capsules: Version Control or Build-Time Generation?
- State: moved 2026-09-11 from the document's retired Discussion wrapper. Whether scaffolded concrete container capsules (e.g. a generated `connection_list.kh`) are intended to be committed to version control or generated fresh on every build is not yet settled; this affects IDE/autocomplete behavior before a build has run. A tooling-level, not language-design, question — but it directly impacts the developer experience of working with domain-specific containers, the primary mechanism through which Khayyam achieves polymorphic container behavior without generic syntax.
- Next: settle in the scaffolding tooling design.

## Anticipated Work

### Polymorphic Data Structures Without Generics
- State: from the document's retired Discussion (Future possibilities). Khayyam's standard library could include polymorphic data structures (List, Map, Set, Queue) implemented purely through abstraction conformance and domain-specific capsules. The design questions around this (scaffolding strategy, generated vs. hand-written capsules) are the [Scaffolded Container Capsules: Version Control or Build-Time Generation?](#scaffolded-container-capsules-version-control-or-build-time-generation) Open Question above; the core question — whether polymorphic containers are viable without generic syntax — is settled affirmatively by the domain-specific capsule pattern documented in [polymorphism.md](./polymorphism.md).
- Next: once the scaffolded-capsules Open Question above settles.

### Cross-Language Polymorphism Mapping
- State: from the document's retired Discussion (Future possibilities). A future document or engineering note could document the exact mapping from Khayyam's polymorphism to each target language: Go target — Khayyam abstraction → Go interface, Smart Compilation monomorphization → Go generic function instantiation; Rust target — Khayyam abstraction → Rust trait, implicit satisfaction → generated `impl` blocks; C target — Khayyam abstraction → C header with function pointers (VTable struct), monomorphization → static inline functions.
- Next: depends on the cross-language compilation (Go, Rust, C target) work.

### Compile-Time Polymorphism Assertions
- State: from the document's retired Discussion (Future possibilities). A future extension could allow developers to write compile-time assertions about polymorphic behavior, expressed as Linter rules rather than language syntax — for example: "All capsules satisfying `Serializer` must also satisfy `Clone`" — enforced at the organizational level, not at the language level.
- Next: depends on the Linter's mechanism for organizational-level rules.
### Where compile-time facts are stated, if anywhere
- State: [polymorphism.md](./polymorphism.md) closes its Matrix analysis by saying compile-time facts (dimensions, layout constraints, optimization hints) are not type identity and that whether the language states them at all, and through what construct, is open, belonging to "whichever document owns the question"; no such document is named and no owner is assigned. It previously assigned the residue to "a dedicated document on compiler-facing abstractions", which the 2026-10-03 removal of compiler prescriptions retired; this entry carries the successor question so it has a tracked work item.
- Next: decide whether the language states compile-time facts at all; if it does, draft the document that owns the construct when the facts the Matrix section names (dimensions, layout constraints, optimization hints) have their first real consumer, and coordinate with [Compiler](../modules/computer/compiler.md).

### Residual inheritance-wording re-audit
- State: the vr-ab review session closed with an open suggestion to re-audit this document (and `abstraction.md`) for surviving "inheritance" phrasing that conflicts with the extension-not-inheritance terminology established in [Type → Explicit Behavior Ownership](../type.md#explicit-behavior-ownership); the pass was never run.
