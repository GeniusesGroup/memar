# Khayyam - Programming Language Handoff

Open work for `khayyam.md`. Entries are mutable current state — revised as each item moves, removed when it resolves or is dropped. See [documentation-handoff.md](../documentation-handoff.md) for what a handoff is.

## Open Questions

### If a team needs to deploy Khayyam code on a standard Linux server, how much of the language's value proposition is lost?
(From the *Execution Semantics Philosophy* topic's retired Discussion.)

### Should Khayyam define a hosted mode for development and testing?
It would simulate unikernel constraints on a standard OS, similar to how Rust's `#[no_std]` is opt-in rather than the default. (From the *Execution Semantics Philosophy* topic's retired Discussion.)

### What is the minimum set of OS abstractions a hosted mode must provide?
For productive development outside a unikernel. (From the *Execution Semantics Philosophy* topic's retired Discussion.)

### Is the system-modeling language framing the right way to position Khayyam externally?
Or does it create confusion with actual modeling languages (UML, Alloy) that serve a different purpose? (From the *System-Modeling Language Philosophy* topic's retired Discussion.)

### At what project size does the architectural integrity trade-off begin to pay for itself?
(From the *System-Modeling Language Philosophy* topic's retired Discussion.)

### Where is the boundary between "enforced clarity" and "forced verbosity"?
When does a domain-specific capsule name become unnecessary indirection? A capsule called `RetryCounter` adds clarity; a capsule called `LoopIndex` may not. (From the *Self-Documenting Code and Naming* topic's retired Discussion.)

### Should Khayyam provide a linter rule or a compiler directive that allows teams to define their own boundaries for this trade-off?
(From the *Self-Documenting Code and Naming* topic's retired Discussion.)

### What level of syntactic atomicity provides meaningful benefits without introducing excessive verbosity?
Highly regular, atomic syntax can feel verbose to experienced developers who rely on implicit conventions — where is the boundary between clarity and unnecessary ceremony? (From the *Syntactic Atomicity and Semantic Clarity* topic's retired Discussion.)

### How can syntactic atomicity be measured objectively?
(From the *Syntactic Atomicity and Semantic Clarity* topic's retired Discussion.)

### Which forms of ambiguity are most harmful to long-term system maintainability?
(From the *Syntactic Atomicity and Semantic Clarity* topic's retired Discussion.)

### The precise boundary between "what Khayyam specifies" and "what a Khayyam implementation provides" still needs worked examples before it can be considered settled.
See [Khayyam Is Not Its Own Compiler or Runtime](./khayyam.md#khayyam-is-not-its-own-compiler-or-runtime). (Document-level, from the removed `## Discussion`.)

### Is there a size or complexity threshold at which splitting a specific topic back out into its own dedicated document becomes worthwhile?
Now that philosophy and syntax reference live in one document — the way *Behavior Over Type Identity* already points to [Abstraction in Khayyam](./abstraction.md) rather than restating it in this one. (Document-level, from the removed `## Discussion`.)

### Does the "Code scope MUST be used only inside a method body" rule remain a deliberate language-level decision, or should it be relaxed?
[type.md → Scope](../type.md#scope--type-as-semantic-boundary) states that placement is a rule of this layer, not a defining property of Scope — and cites namespace- and module-level boundaries as realizations of the same category that are not nested inside any Method, a shape the current `sc` grammar cannot express. Decide either to keep the rule (consistent with scopes being inert until a library-provided method drives them, per [Control Flow](../protocols/control-flow.md)) or to open the placement to non-method boundaries; the type-level position holds under either outcome. (Left open when the placement-based Scope justification was withdrawn from type.md.)

### Stdlib bootstrap ordering under the no-hidden-primitive rule
- State: recovered 2026-09-16 from an audit of the retired `chats-context -- Error & ADT.md` context note. The Error document's String dependence cannot be resolved by a hidden primitive type — the owner ruled that out on principle (a hidden primitive contradicts the no-primitive-types rule stated in [Type Principles Realized](./khayyam.md#type-principles-realized)), and the Error & ADT session's recorded rejection of solving stdlib bootstrap via a hidden primitive type had not been carried into any tracked document. The general ordering problem — how the first stdlib capsules (String, Error, and their mutual needs) are built when Khayyam has no primitive types at all — is otherwise unrecorded; an earlier promotional migration note (removed 2026-09-23; not a language document) covered ecosystem onboarding, not the language's own first-capsule ordering.
- Next: a dedicated stdlib session, per the source note; the dedicated ADT session also feeds it.

### Whether the compiler/linker must reject mutual `in` inclusion cycles between files, independent of module-level cycles
- State: recovered 2026-09-16 from the same audit. The Error & ADT session identified that the file-inclusion contract ([RFC 000013](../protocols/filesystem.md) era, now stated in [Khayyam → Import Mechanism](./khayyam.md#import-mechanism-in)) does not address mutual `in` inclusion between files, and recorded that this gates the stdlib bootstrap question above. The [Modularity in Khayyam](./modularity.handoff.md#cyclic-module-dependencies) handoff owns the *module-level* cycle decision; the *file-inclusion-level* cycle question has no tracked owner and was never carried into a handoff.
- Next: decide with the Import Mechanism's next revision, or fold into the module-cycle decision whichever layer the ruling actually belongs to.

### Which method returns human-facing text, and on which owner?
[Self-Documenting Code and Naming](./khayyam.md#self-documenting-code-and-naming) states that a description or a human-readable name is a value a method writes into an influenced variable, so another language is another method on the same type. The signature of that method, and whether the owner is the type being described or a companion type, is not worked. Examples in this document set still use `//` lines; those lines are not that method.

### Translating a Go tree before memar-khayyam exists
A file-by-file translation of an existing Go module, ahead of the Khayyam implementation repository, produces sources that have to choose among incompatible sketches. The settled points for a later pass, already stated in the language documents, are: a protocol is an abstraction; a field-shaped value is one type plus one method that names what a code generator implements ([Encapsulation → Capsule Structure and Privacy](./encapsulation.md#capsule-structure-and-privacy)); human-facing text is a method result, as above. Writing a migration map and translating a large module are not the next step. A set of about 179 empty Go files was named as movable into place; they are not in this workspace, so they were not moved.

## Anticipated Work

- A dedicated **Target Platform Implications** document: defining the hosted-mode specification, enumerating the OS abstractions required for productive development outside a unikernel, and specifying the boundary between unikernel-native and hosted-mode behavior. (From the *Execution Semantics Philosophy* topic's retired Future possibilities; the document-level Future possibilities recorded none, so it migrated nothing.)
