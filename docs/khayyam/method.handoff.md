# Method in Khayyam Handoff

Open work for `method.md`. Entries are mutable current state — revised as each item moves, removed when it resolves or is dropped. See [documentation-handoff.md](../documentation-handoff.md) for what a handoff is.

## Open Questions

### A variable that is both influencing and influenced in the same call
- Whether a variable playing both the influencing and influenced role in the same call should get explicit notation (a third grouping, a marker, or something else), or whether it should remain disallowed/discouraged — treated as a signal to split the method — is not yet decided. The case, the `sk Socket` example, and the working decomposition hypothesis live in the body at [The Open Question: A Variable That Is Both](./method.md#the-open-question-a-variable-that-is-both).
- Owner position (review 2026-09-23): the dual-role need remains a *signal* that something is crooked somewhere — a prompt to find and fix the underlying modeling problem, making the code readable — not a feature to notate. Other languages do not emphasize this signal; Khayyam does, deliberately. A previous counter-class against the split hypothesis (atomic read-modify-write via `Counter.Increment`) is withdrawn: for atomic operations the correct shape is a *dedicated method that owns the atomic operation as its own clear abstraction* — the method encapsulates the read-modify-write; the call site does not need dual-role notation for it. No strong concrete example has been found where a method genuinely needs one variable for both influence and being influenced while remaining correctly modeled; until one is, the signal stands.
- Notation for the dual role (if a real case survives the signal) remains open.

### Detecting a mutated influencing variable
- Whether the compiler or linter should (or even can, without deeper static analysis) detect when a variable declared in the influencing group is, in fact, being mutated inside the method body via one of its own exposed methods — surfacing exactly the dual-role case above as a warning.

## Anticipated Work

- A linter rule that flags an influencing variable receiving a call to one of its own known-mutating methods, prompting the author to either move it to the influenced group or consider splitting the method, once the dual-role question above is resolved. (From the Influencing and Influenced Variables topic's retired Future possibilities; the document-level Discussion restated the same rule.)
