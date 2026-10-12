# The Error Handoff
Open work for `modules/process/error.md`. Entries are mutable current state — revised as each item moves, removed when it resolves or is dropped. See [documentation-handoff.md](../../documentation-handoff.md) for what a handoff is. Questions from topics untouched in the 2026-09 session migrate here progressively, per the documentation method's progressive-migration rule.

## Open Questions

### Companion naming convention for propagation safety
- State: whether a naming convention (a prefix or suffix distinguishing errors "safe to propagate as-is" from errors that "must be translated before crossing a boundary") should be introduced is undecided; if introduced, it becomes a follow-up document referencing error.md.
- Next: evaluate against real error families once the framework's first services exist.

### A realization's `IsEqual` and `MediaType()` comparison
- State: a realization's convenience comparison helper may compare both `GetTypeID()` and `MediaType()`. If `MediaType` is a fixed, type-level property (every instance of a given `Type_ID` always reports the same `MediaType`), this check is redundant and should be dropped. If `MediaType` can genuinely vary per-instance for the same `Type_ID`, this reopens the "identity is `GetTypeID()` alone" principle stated under error.md's [Identity and equality](error.md#identity-and-equality) and needs to be resolved explicitly.
- Next: resolve explicitly against the `Type` model's media-type rules.

### `ExpireInFavorOf`
- State: the reasoning that originally justified analyzing it alongside `Equivalence` no longer applies, but whether the underlying capability (declaring "this type is replaced by that one") is still wanted for `Error`, in some form, has not been given a final yes/no. Blocked on `Type_Details` (the file defining it, `modules/computer/type/protocol/type.kh`) being shared for review.
- Next: review `Type_Details`, then decide keep/drop.

### `ADT`'s `IsNull`/`IsEmpty` semantics for a value like `Error`
- State: the canonical `Error` contract supplies all three `ADT` methods (see error.md's [ADT composition](error.md#adt-composition--the-full-adt-family-at-the-canonical-level)); what `IsNull`/`IsEmpty` should actually mean for `Error` remains open, tracked in a dedicated ADT session and its own document.
- Next: joint session with the `ADT` capsule family's dedicated document.

### A realization's capsule composition and method-reuse model, in general (not specific to `Error`)
- State: `Error` is the concrete motivating case that surfaced this. What the language settles: satisfaction is not something the language intervenes in, and a capsule that wants its satisfaction of an abstraction to read as deliberate composes an intent abstraction and explicitly delegates the methods that abstraction requires to a capsule that owns the behavior ([Abstraction → Deliberate Satisfaction Is Composed, Not Declared](../../khayyam/abstraction.md#deliberate-satisfaction-is-composed-not-declared)); reducing the delegation boilerplate is already an organizational Rule rather than a language question ([abstraction scaffolding](../../../bundles/khayyam/rules/abstraction-scaffolding/abstraction-scaffolding.md)). A language-level reuse mechanism is therefore refused rather than open, and the realization's composition example and that section no longer disagree. What remains is the authoring side: how a concrete error is written, and what role code generation plays in writing it.
- Next: dedicated document in the Khayyam set, for the authoring and code-generation residue only.

### The not-yet-designed retry/cache-policy sibling abstraction
- State: the intended home for dynamic, per-call data like a retry-after duration, returned alongside `Error` — out of error.md's scope, tracked separately.
- Next: design once the first service needs retry-after data.

### Does Memar need a Trace concern beside Error and Log?
- State: this document draws the Error/Log line and rejects the other convention — enriching the error at each layer until the story can be reconstructed — as a category confusion, on the ground that reconstructing the operational context is the forensic record's job ([Immutability: an Error is a fixed contract member, not an accumulating envelope](error.md#immutability-an-error-is-a-fixed-contract-member-not-an-accumulating-envelope)). The owner's own working position, recovered 2026-09-30 from an audit of Omid Hekayati's Go-community Telegram-group messages, agrees with the placement rather than adding a third entity: tracing is a logging concern, not error handling — the timing, dependency, and call-path data a trace carries belongs beside the log record, not inside the contract returned to a caller. No document in `docs/` carries a Trace concept, a span, or a correlation identity; [Protocol](../../protocol.md) gives "all API responses must include a correlation ID" as an example of a Policy rather than a concept, and [Chapar](../net/chapar.md#misbehavior-traceability) uses traceability for link-layer fault localization, which is a different subject.
- Question for the owner: does a Trace concern earn a place in the Error protocol's boundary model at all, and if it does, is it a third entity beside Error and Log or a discipline inside Log with only the correlation identity named separately?
- Next: decide together with the logging-capsule API companion document below, which is where a correlation-carrying context would have to be specified. The sources state no span model, sampling policy, or retention rule, so what is undecided is the concept's existence and its boundary, not its shape; nothing else in the sources depends on the answer.

### Whether a structured Memar logging capsule API should be specified
- State: a companion document specifying the concrete API of the recommended Memar logging capsule (the shape of `TransactionFailureLog`, the `Logger` interface, and standard context-attachment methods) is the natural next step once the boundary-translation discipline is finalized; also the natural home for the `Error` family's code-generator input format (how a `.kh`/DSL definition of an error's metadata maps to the generated concrete type).
- Next: draft once the boundary-translation discipline is finalized and the broader `abstraction_p.Implements` pattern settles.

### What makes an error actionable at a layer
- State: the boundary-translation rule obliges an error to be "meaningful and actionable at that specific layer" ([Boundary translation](error.md#boundary-translation)), and it triggers where the incoming vocabulary "no longer matches the outgoing layer's domain". Neither half has a declared referent: no artifact states what a given layer's decision vocabulary is, so no party can determine which errors are already in the right vocabulary and which are owed translation, and the rule's own trigger cannot be evaluated against anything.
- Next: decide whether a layer's decision vocabulary is declared anywhere, and if so by which artifact — the error type it owns, the layer's own protocol, or the abstraction the layer serves. No conformance check exists for the rule until it is, since what cannot be named cannot be compared.

### `TAGS` is listed as a `Detail` member and is declared nowhere
- State: [Detail and Quiddity fields](error.md#detail-and-quiddity-fields--two-audiences-not-one) at `:211` lists six fields inherited via `Type` — `Summary`, `Overview`, `UserActionNote`, `DevActionNote`, `TAGS`, `Domain` — and no `.kh` file declares `TAGS`: `modules/computer/type/protocol/detail.kh:61` archives it inside the Go residue, and the archive at `:19-41` carries the other five, so this document's list of six matches neither archive. The claim is stated here and the subject it would change is this protocol's own bundle, which is why this module owns the defect and not [Type](../../type.md), whose `Detail` abstraction is where a declaration would be written: the question "is `TAGS` a member of this protocol's `Detail`?" is one only this protocol answers.
- Note on the citation: the source record cites this document at `:208,210`, which lands on the paragraph before the section and on its heading; the list itself is at `:211` and `:213`.
- Blocks continuation: nothing in the toolchain — nothing resolves `TAGS` today. It does block a conformance judgment: a party deciding whether a realization satisfies this protocol's `Detail` has nothing to check `TAGS` against, and the five fields that are declared do not settle what the sixth one is.
- Next: owner ruling on whether `TAGS` is a `Detail` member at all — a field name this protocol chose, or the residue of Go's — and then either the declaration written beside the other five or the sixth name struck from the list here.
- Carried from: [Go Target Research 001 → Live problems the two archives jointly expose](../../../bundles/khayyam/targets/go/target.research.001.md#live-problems-the-two-archives-jointly-expose--defects-in-the-sources-and-where-each-one-was-routed), verified 2026-10-02 and routed here 2026-10-08.

## Anticipated Work
- The companion logging-capsule API document (shape of `TransactionFailureLog`, the `Logger` interface, standard context-attachment methods), once the boundary-translation discipline is finalized.
- A dedicated document for the `Error` family's code generator input format, specifying how a `.kh`/DSL definition of an error's metadata maps to the generated concrete type, once the broader `abstraction_p.Implements` pattern is finalized.
- Once the ADT session concludes, revisit error.md's composition if `Nil` alone proves insufficient.
