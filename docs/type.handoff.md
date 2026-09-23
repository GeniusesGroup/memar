# Type Handoff

Open work for `type.md`. Entries are mutable current state — revised as each item moves, removed when it resolves or is dropped. See [documentation-handoff.md](./documentation-handoff.md) for what a handoff is.

## Open Questions

### Type identification framework
- State: whether to rely on intuition without a framework (rejected — the tendency is to over-type or under-type without consistency) and whether to use a strict checklist with binary answers (rejected — domain modeling is not binary; the responsibility criterion reduces the gray zone but does not eliminate it, which is a feature, not a flaw) were both settled in type.md's changelog; the framework's residual gray-zone interpretation risk is stated inline in the document.

### Definition of Type
- State: defining Type structurally was rejected (a structural definition fails to capture the modeling-level distinction — two concepts with the same structure are not necessarily the same concept); defining Type as a formal type-theoretic construct was considered and deferred (Martin-Löf Type Theory defines types through introduction, elimination, and computation rules — rigorous but possibly too formal for the current stage; a future revision could strengthen the definition toward this formalism).
- Next: revisit the MLTT-strengthening option when the model stabilizes toward Proposed.

### Nominal identity's interaction with generics
- State: how does nominal identity interact with generic or parameterized types? If `Registry<T>` is a Type, is `Registry<Person>` the same concept as `Registry<Company>`? In nominal systems, each instantiation is a different type — this seems correct, but the implications for code reuse need exploration.
- Next: explore when the generics-position work (khayyam-polymorphism) matures.

### Method as Type — category or behavior?
- State: does Method fundamentally represent a Type category, or is Method a behavior owned by another Type? The current model treats Method as a Type, supported by the "fundamental semantic building block" and "independent, referenceable existence" arguments — but alternative interpretations remain possible (a Method as a behavioral facet of the Type it is attached to) and the position has not yet been validated through implementation experience. Related: how does "Method as Type" affect compilation and dispatch — does a Method have a runtime representation, or is it purely compile-time?
- Next: validate through the first implementation experience.

### EBO's working answers and open edges
- State: generated-code transparency (generators must emit readable, auditable source files — never opaque binaries or compiler intermediates) is the recorded working answer with tooling specifics open; multiple delegations are allowed (a component may hold and delegate to several other components, each relationship explicit in source); performance overhead is accepted (explicit delegation may cost slightly versus inlined inheritance; clarity is favored, and optimization belongs to compilers and runtimes, not source-level design); dynamic behavior (dynamic proxies and reflection-based method addition) generally violates EBO — runtime-added methods mean source no longer reflects the available set; and the macro boundary (exactly where transparent code generation ends and opaque macro magic begins) remains open — the guiding principle is human cognitive accessibility, and resolution may ultimately be linter configuration rather than language rule.
- Next: settle the macro boundary with the first code-generation tooling.

### Rules checking
- State: are rules checked at compile time or runtime? This is the most consequential implementation decision. What happens when rules from different Types conflict? Can business rules be configured without changing the Type's identity? What is the relationship between rule hierarchies and type realization?
- Next: decide with the first rule-bearing realization.

### Formal semantics of "semantic identity"
- State: proposed direction — nominal declaration + contract specification + contextual scoping. Needs rigorous definition.
- Next: define rigorously before Proposed status.

### Multiple Abstraction satisfaction
- State: can a Capsule satisfy multiple Abstractions? How are method name conflicts resolved?
- Next: decide with the Abstraction document's next revision.

### Gradual typing at boundaries
- State: how does a language enforcing "every type is a semantic entity" interoperate with systems that do not share this philosophy?
- Next: design when the first interop boundary appears.

### Bootstrapping without primitives
- State: without primitives, what are the foundational Capsules, and how are they defined without circularity? An implementation concern that affects the Type model's coherence. Cross-referenced 2026-09-16 from the retired `chats-context -- Error & ADT.md` audit: the concrete motivating case recorded there was the String↔Error circular dependency in the stdlib bootstrap, with the owner's standing rejection of solving it via a hidden primitive type (on principle — see the No primitive types rule under Type Principles Realized in `khayyam/khayyam.md`); the language-side track of the same question is tracked in Khayyam's own handoff entry "Stdlib bootstrap ordering under the no-hidden-primitive rule" (`khayyam/khayyam.handoff.md`).
- Next: settle with Khayyam's foundational-capsule work.

### Accidental satisfaction mitigation
- State: implicit structural satisfaction (no `impl` keyword) risks accidental conformance (Go's well-known problem); whether this warrants a mitigation mechanism is recorded as an open question in the Abstraction document.
- Next: tracked in the Abstraction document; revisit here when it moves.

## Anticipated Work

- **Refinement types for invariants**: an SMT solver could check simple invariants at compile time.
- **Formal specification of the satisfaction mechanism**: once design decisions are made, the Capsule/Abstraction bridge could be specified formally.
- **Gradual typing at boundaries**: a mechanism for converting between semantic Types and structural types at API boundaries.
- **Rule analysis tooling**: static analysis to verify invariants, detect rule conflicts, and identify over-constraining.
- **A dedicated Relation document**: addressing whether and how Relations gain independent status, endpoint ownership, directionality, and arity, as a modeling-layer concern built on top of — not inside — the Type definition, informed by prior art such as Chen's Entity-Relationship model, RDF/OWL, property graph databases, and Alloy.
- **AI-assisted delegation generation**: instant, auditable scaffolding of forwarding methods.
- **Formal verification of the behavior graph**: with no hidden edges, verification scope equals source scope.
- **Ownership-clarity metrics**: IDEs and linters could compute and display an "ownership clarity score" for each component — a measure of how easily a reader can determine the origin of each behavior.
- **Delegation pattern library**: standardized forwarding/adapting/decorating patterns reducing the burden without hiding anything.
- **Beyond software**: responsibility-clarity applications in organizational design.
