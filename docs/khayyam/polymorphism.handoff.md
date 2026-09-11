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

### Can the Smart Compilation Strategy Be Extended to Devirtualization?
- State: moved 2026-09-11 from the document's retired Discussion wrapper. Whether Khayyam's compiler supports devirtualization — converting a runtime dispatch (VTable) call to a direct call when the compiler can prove the concrete type at a specific call site, common in JVM and .NET runtimes — is unsettled. If supported, the monomorphization/dynamic-dispatch decision would not need to be made at compile time; it could be deferred and optimized incrementally, increasing the optimization potential for plugin architectures and dynamically loaded code.
- Next: test the deferred-optimization idea against the plugin and dynamically-loaded-code scenarios the dispatch strategy already names.

### Should There Be a Mechanism for "Sealed" Abstractions?
- State: moved 2026-09-11 from the document's retired Discussion wrapper. A sealed abstraction — satisfiable only by capsules defined within the same module or package — would model closed type hierarchies (e.g., `Result` with exactly two variants: `Ok` and `Err`); without sealing, any external capsule could satisfy the abstraction, which may be undesirable for abstractions that represent a closed set of behaviors. The candidate expression is a Linter rule (enforcing that only certain files can contain capsules satisfying a specific abstraction) rather than a language feature, consistent with Khayyam's governance philosophy.
- Next: decide between the linter-rule expression and a language feature.

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
