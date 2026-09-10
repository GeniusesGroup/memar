# Method in Khayyam Handoff

Open work for `khayyam-method.md`. Entries are mutable current state — revised as each item moves, removed when it resolves or is dropped. See [documentation-handoff.md](./documentation-handoff.md) for what a handoff is.

## Open Questions

### A variable that is both influencing and influenced in the same call
- Whether a variable playing both the influencing and influenced role in the same call should get explicit notation (a third grouping, a marker, or something else), or whether it should remain disallowed/discouraged — treated as a signal to split the method — is not yet decided. The case, the `sk Socket` example, and the working decomposition hypothesis live in the body at [The Open Question: A Variable That Is Both](./khayyam-method.md#the-open-question-a-variable-that-is-both).

### Detecting a mutated influencing variable
- Whether the compiler or linter should (or even can, without deeper static analysis) detect when a variable declared in the influencing group is, in fact, being mutated inside the method body via one of its own exposed methods — surfacing exactly the dual-role case above as a warning.

## Anticipated Work

- A linter rule that flags an influencing variable receiving a call to one of its own known-mutating methods, prompting the author to either move it to the influenced group or consider splitting the method, once the dual-role question above is resolved. (From the Influencing and Influenced Variables topic's retired Future possibilities; the document-level Discussion restated the same rule.)
