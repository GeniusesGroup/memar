# Control Flow in Khayyam Handoff

Open work for `khayyam-control_flow.md`. Entries are mutable current state — revised as each item moves, removed when it resolves or is dropped. See [documentation-handoff.md](./documentation-handoff.md) for what a handoff is.

## Open Questions

### Execution Primitives: The Compiler's Role
The precise, versioned contract for the compiler's control-flow primitives — the `sc`/jump intrinsics *and* the event stream that DAA/linter subscribe to — has not been published as a standalone, versioned specification yet. Until it is, third-party CF libraries cannot target it without depending on compiler internals (see [Anticipated Work](#anticipated-work)).

### Library-Defined Control Flow
The standard, recommended conditional method vocabulary for common cases (especially the naming of the success/failure or presence/absence branching pair on `Error` and similar capsules) is still open.

### Error Propagation
No open question remains for the core propagation mechanism itself; two adjacent questions are owned elsewhere and are recorded here as pointers: [The Error](./protocols/error.md) holds the framework-level question of when a low-level error should be translated/logged rather than propagated verbatim (the question behind the payment example's "naming and layering of this error path" note in the body), and the [Control Flow](./protocols/control-flow.md) protocol document (Draft) holds the standard conditional-method naming question for branching on error/success.

## Anticipated Work

- A standard-library `GOTO`/jump-based control-flow package, alongside the structured `IF`/`LOOP` family, is expected to exist so the unstructured path is not merely theoretical. (From the `Structured vs Unstructured Programming` topic's retired Future possibilities.)
- A formal, versioned specification of the intrinsic + event contract, so third-party control-flow libraries can target it without depending on compiler internals. (From the `Execution Primitives: The Compiler's Role` topic's retired Future possibilities; resolves that topic's open question above.)
- A richer standard library of named, domain-flavored conditional and error-propagation methods is expected to grow over time. (From the `Library-Defined Control Flow` topic's and the retired document-level Future possibilities; the document-level wording subsumes the topic-level one.)
