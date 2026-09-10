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

## Anticipated Work

- A dedicated **Target Platform Implications** document: defining the hosted-mode specification, enumerating the OS abstractions required for productive development outside a unikernel, and specifying the boundary between unikernel-native and hosted-mode behavior. (From the *Execution Semantics Philosophy* topic's retired Future possibilities; the document-level Future possibilities recorded none, so it migrated nothing.)
