# The Error Handoff

Open work for `protocols/error.md`. Entries are mutable current state — revised as each item moves, removed when it resolves or is dropped. See [documentation-handoff.md](../documentation-handoff.md) for what a handoff is. Questions from topics untouched in the 2026-09 session migrate here progressively, per the documentation method's progressive-migration rule.

## Open Questions

### Companion naming convention for propagation safety
- State: whether a naming convention (a prefix or suffix distinguishing errors "safe to propagate as-is" from errors that "must be translated before crossing a boundary") should be introduced is undecided; if introduced, it becomes a follow-up document referencing error.md.
- Next: evaluate against real error families once the framework's first services exist.

### `IsEqual`'s `MediaType()` comparison
- State: the generic `error.IsEqual` helper compares both `DataTypeID()` and `MediaType()`. If `MediaType` is a fixed, type-level property (every instance of a given `DataTypeID` always reports the same `MediaType`), this check is redundant and should be dropped. If `MediaType` can genuinely vary per-instance for the same `DataTypeID`, this reopens the "identity is `DataTypeID` alone" principle stated under error.md's [Identity and equality](./error.md#identity-and-equality) and needs to be resolved explicitly. Not yet decided.
- Next: resolve explicitly against the `DataType` model's media-type rules.

### `ExpireInFavorOf`
- State: the reasoning that originally justified analyzing it alongside `Equivalence` no longer applies, but whether the underlying capability (declaring "this type is replaced by that one") is still wanted for `Error`, in some form, has not been given a final yes/no. Blocked on `datatype_p.Details` (the file defining it) being shared for review.
- Next: review `datatype_p.Details`, then decide keep/drop.

### `ADT`'s `IsNull`/`IsEmpty` semantics for a value like `Error`
- State: Khayyam's `Error` canonically requires all three `ADT` methods (see error.md's [ADT composition](./error.md#adt-composition--the-full-adt-family-at-the-canonicalkhayyam-level)); Go's realization narrows to `Nil` alone for Go-specific reasons and is not a template for other backends. What `IsNull`/`IsEmpty` should actually mean for `Error` remains open, tracked in a dedicated ADT/Khayyam session and its own document.
- Next: joint session with the `ADT` capsule family's dedicated document.

### Khayyam's capsule composition and method-reuse model, in general (not specific to `Error`)
- State: an earlier draft of error.md's composition example incorrectly implied that composing `Error` into a concrete capsule automatically promotes its methods, the way Go's struct embedding does. Khayyam has no such automatic inheritance: composition is containment only, and a containing capsule must explicitly implement and forward each method itself. The full implications of this (how concrete errors are actually meant to be authored, what role code generation plays versus a possible future language-level reuse mechanism) need their own dedicated document, since the relevant information is currently scattered across [khayyam.md](../khayyam.md)'s capsule and abstraction-composition sections rather than settled in one place. Not specific to `Error`, but `Error` is the concrete motivating case that surfaced it.
- Next: dedicated document in the Khayyam set.

### Whether the optional capability-interface set (`Internal`, `Temporary`, `Timeout`) is complete
- State: additional orthogonal dimensions may be needed as more of the framework is built out; no process for adding new ones has been defined yet (presumably: propose a new capability interface the same way these three were introduced, but this has not been stated as a rule anywhere).
- Next: state the addition rule in error.md when the second real need appears.

### The not-yet-designed retry/cache-policy sibling abstraction
- State: the intended home for dynamic, per-call data like a retry-after duration, returned alongside `Error` — out of error.md's scope, tracked separately.
- Next: design once the first service needs retry-after data.

### Whether a structured Memar logging capsule API should be specified
- State: a companion document specifying the concrete API of the recommended Memar logging capsule (the shape of `TransactionFailureLog`, the `Logger` interface, and standard context-attachment methods) is the natural next step once the boundary-translation discipline is finalized; also the natural home for the `Error` family's code-generator input format (how a `.kh`/DSL definition of an error's metadata maps to the generated concrete type).
- Next: draft once the boundary-translation discipline is finalized and the broader `abstraction_p.Implements` pattern settles.

## Anticipated Work

- The companion logging-capsule API document (shape of `TransactionFailureLog`, the `Logger` interface, standard context-attachment methods), once the boundary-translation discipline is finalized.
- A dedicated document for the `Error` family's code generator input format, specifying how a `.kh`/DSL definition of an error's metadata maps to the generated concrete type, once the broader `abstraction_p.Implements` pattern is finalized.
- Once the ADT session concludes, revisit error.md's composition if `Nil` alone proves insufficient.
