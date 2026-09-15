# Variable in Khayyam Handoff

Open work for `variable.md`. Entries are mutable current state — revised as each item moves, removed when it resolves or is dropped. See [documentation-handoff.md](../documentation-handoff.md) for what a handoff is.

## Open Questions

### Does the standard `MathEval` evaluator type-check formula operands at compile time?
- State: Whether the standard `MathEval.FromString()`-style evaluator performs full compile-time type-checking of formula operands (preventing nonsensical cross-type operations like adding incompatible domain quantities), or only validates syntax while deferring type errors to runtime, is not yet settled for the recommended framework implementation. (From the Domain-Driven-Arithmetic topic.)

### Can a file export a variable under an alias?
- State: Whether a file can export a variable under a different name than its declaration name (aliasing) is not currently addressed. (From the Variable-Scope-and-Visibility topic.)

### Where is the boundary between "enforced clarity" and "forced verbosity"?
- State: When does a domain-specific capsule name become unnecessary indirection? (From the Self-Documenting-Code topic, question 1.)

### Should teams be able to adjust the clarity/verbosity boundary?
- State: Should Khayyam provide a linter rule or a compiler directive that allows teams to define their own boundaries for this trade-off? (From the Self-Documenting-Code topic, question 2.)

### Should the linter auto-fix migrated multi-declarations?
- State: Should the linter provide an auto-fix mode that converts multi-declaration syntax (if encountered in migrated code) into separate `vr` declarations? (From the retired document-level Unresolved questions.)

### How does the variable model interact with the Memar framework's governance layer?
- State: Are there framework-specific rules for variable naming, scoping, or lifecycle that extend beyond the language-level rules documented in `variable.md`? (From the retired document-level Unresolved questions.)

## Anticipated Work

- A linter auto-completion mode that proposes the full type annotation as the developer types, reducing the mechanical cost of explicit typing without compromising readability. (From the Explicit-Types topic.)
- A formal specification for compile-time type-checking of `MathEval`-style formula operands, resolving the open question above by defining exactly which cross-type operand errors the standard evaluator is guaranteed to catch before runtime. (From the Domain-Driven-Arithmetic topic.)
- A linter rule that detects capsule names that are unlikely to carry domain meaning (e.g., names that are synonyms for primitive operations like `Counter`, `Index`, `Flag`) and suggests merging them into their parent capsule's domain. (From the Self-Documenting-Code topic.)
- A migration tool that automatically converts variable declarations from other languages into Khayyam's `vr` syntax, handling the separation of declaration and initialization. (From the retired document-level Future possibilities.)
- A linter rule set for variable naming conventions, configurable per organization, that enforces the domain-meaningful naming principle at the project level. (From the retired document-level Future possibilities.)
