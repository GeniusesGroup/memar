---
Title: "The Error"
Status: Proposed
Start Date: 2026-07-08
ID: 495440
---

# The Error

## Abstract
`Error` is the framework's abstraction for a distinct, identifiable fault condition returned by a fallible operation. This document defines what `Error` is composed of, how its identity and equality work, what crosses a process/network boundary and what does not, how tooling can discover a capsule's intent to implement it, and how an error's vocabulary must be translated whenever it crosses from a diagnostic layer into an actionable one. It absorbs — without summarizing — the boundary-discipline rule previously tracked as a separate document ("Error vs. Log") so that the full Error lifecycle, from composition through cross-boundary behavior, lives in one place. It assumes, and does not re-argue, the principle established in [Type](../type.md) that a static concept (no per-instance dynamic data) must be its own distinct type: every concrete error (`ErrServiceNotFound`, `ErrTransactionUnavailable`, …) is generated as its own type, never instantiated from a shared generic `Error` capsule via an `Init` method.

## Introduction

### Motivation
An error-handling model needs a precise answer to several questions that are easy to leave implicit until they cause inconsistency:

1. What, exactly, must a capsule implement to count as an `Error`?
2. What determines whether two errors are "the same"?
3. What may an error carry across a network or process boundary, and what must stay local — or be redirected to a Log Event — before the error is returned?
4. How does generic infrastructure (retry middleware, alerting, an HTTP gateway) reason about a *class* of errors without enumerating every concrete type?
5. How does tooling (a code generator scaffolding a large capsule) know a capsule intends to become an `Error` before it structurally qualifies as one?
6. How does the system prevent low-level operational detail from leaking into a high-level, business-facing vocabulary while still preserving that operational detail for the operator who needs it?

This document answers each of these directly, recording the reasoning and the alternatives rejected along the way. The first five questions are inherent to any error abstraction; the sixth — the boundary-translation question — was previously tracked in its own document because the broader software ecosystem routinely conflates Error and Log, and the framework needed a single, named rule for translating across layer boundaries rather than the implicit, afterthought logging that prevails elsewhere. Both concerns are unified here: an `Error` that crosses a layer where it is *diagnostic* into a layer where it is only *actionable* is itself a boundary-crossing question, and the rule that governs it is the natural completion of the rule that governs what an `Error` may carry across a process or network boundary in the first place.

### Methodology
This document is the consolidation of two documents previously maintained in parallel: the *Error Abstraction* document (composition, identity, tooling-facing declaration, optional capability interfaces) and the *Error vs. Log* document (the Capture → Persist → Re-express translation discipline). The two were merged because they answer two halves of the same question — what an `Error` is, and what an `Error` is allowed to do when it leaves its origin layer — and forcing a reader to load two documents to assemble a single mental model produced the same scattering problem this project's documentation specification was written to eliminate.

The content was arrived at through: sustained design discussion across multiple working sessions, with each proposed change argued for and against rather than accepted on first suggestion; rejection of an earlier `Equivalence[Error]` method on the grounds that it duplicated the `DataTypeID()` comparison; rejection of a sealed-interface marker pattern after evidence accumulated that it bought no real guarantee beyond a plain exported method; correction of a host-language-specific realization detail that had been incorrectly generalized into the abstraction's canonical composition (the `ADT` family narrowing); and direct testing of the boundary-translation rule against a concrete worked example (the financial-transaction service used in the [Boundary translation](#boundary-translation) topic below) to confirm the three-step Capture → Persist → Re-express pattern actually resolves the two failure modes the rule was written to prevent.

## Explanation

### Composition

```khayyam
tp Error ab {
    DataType
    Field_MediaType
    ADT
    ImplementsError
}
```

A concrete error composes `Error` — the exact mechanics of how a concrete capsule obtains `Error`'s method implementations from a shared parent capsule are intentionally NOT shown here. In the Khayyam realization, placing one capsule inside another via composition is containment only, and the containing capsule must explicitly implement and forward each method itself. That question — the realization's capsule composition and reuse model in general, not specific to `Error` — is tracked as its own future document (see this document's [handoff](./error.handoff.md)); this document does not assume an answer to it.

In a realization that makes forwarding explicit, each concrete error's forwarding methods are written explicitly. That model keeps behavior visible: no implicit resolution chain needs tracing, no complex inheritance relationship forms behind a developer's back, and a capsule's actual behavior is directly readable in its own file. Code generation and other tooling can supply the repetitive work while preserving that visibility.

#### The four composed abstractions
Each embedded abstraction contributes a specific, non-overlapping responsibility to `Error`'s contract:

- **`DataType`** supplies the type-level identity machinery — `Field_ID` (whose value is what `DataTypeID()` returns), `Field_LifeCycle` (recording whether a type is `Experimental`, `Stable`, `Deprecated`, or `EndOfLife`), the `Detail` and `Quiddity` text bundles, and the optional `ExpireInFavorOf` pointer discussed under [Identity and equality](#identity-and-equality). Without `DataType`, `Error` would have no canonical identifier to compare across processes.
- **`Field_MediaType`** supplies the serialization envelope label used when an error's `DataTypeID` (and nothing else) is transmitted across a network boundary. It is what allows a remote receiver to dispatch on the *kind* of error without needing the full concrete type's method set in scope.
- **`ADT`** supplies the null-state family (`IsNil` / `IsNull` / `IsEmpty`). The canonical `Error` contract supplies all three; the question of what `IsNull`/`IsEmpty` should mean for a value whose entire purpose is identity (rather than data) is left to a dedicated ADT session and tracked in this document's [handoff](./error.handoff.md).
- **`ImplementsError`** is the tooling-facing declaration described in its own topic below — a single plain method that lets a code generator discover intent before a capsule structurally qualifies as an `Error`.

### Optional capability interfaces
A concrete error MAY additionally implement any of a small set of independent, orthogonal capability contracts. Generic infrastructure can recognize those capabilities through the realization's type system; the capability set remains separate from `Error`'s mandatory contract. The Khayyam source below is one realization example:

```khayyam
tp ErrStorageUnavailable cp {
    Error
    Internal    // caused by this process's own logic, not the caller's input
    Temporary   // retrying later may succeed
}
```

`Internal`, `Temporary`, and `Timeout` are independent dimensions — an error may be any combination of them, or none. This lets a circuit breaker, retry policy, or alerting system reason about a *class* of errors ("is this retryable?") without needing to enumerate every concrete `DataTypeID`, while keeping this reasoning entirely opt-in per concrete error rather than a mandatory field every error must populate.

A capability is an independent contract. A realization may express composition and inspection with its own type-system features; generic infrastructure then recognizes the capability on a received `Error` value. The following Khayyam source shows that realization pattern:

```khayyam
tp IsTemporary ab

tp IsTemporary mt (self IsTemporary) () (yes Boolean)

tp Retry mt (self SomeService) (req Request) (result Result) (err Error) {
    vr temporaryErr IsTemporary
    err.As(temporaryErr)()
    temporaryErr.IsTemporary()(yes)
    yes.OnTrue(WaitAndRetry)
    yes.OnFalse(ReturnErr)
}
```

The point is that the dispatch is by *type*, not by string comparison or an enum field, and that a concrete error remains free to declare *none* of these capabilities when none apply.

### Multi-cause returns
A method that can fail in more than one way returns the `Error` abstraction; a method with exactly one possible failure cause returns that concrete type directly (a covariant-return consequence of the underlying [Type](../type.md) identity principle):

```khayyam
tp Authorize mt (self Service) (token Token) (result AuthResult) (err ErrPermissionDenied)
tp Find mt (self Service) (id ID) (result Result) (err Error)
```

`Authorize` can fail in exactly one way (the token does not authorize), so its error type is the concrete `ErrPermissionDenied` — the caller can dispatch on the type directly and the realization's covariant-return support gives this no runtime cost. `Find`, by contrast, can fail for several distinct reasons (not found, storage unavailable, timeout, permission denied) and so returns the abstraction; the caller uses the realization's type inspection to recover the specific cause.

### Identity and equality

Identity is `DataTypeID()` alone (via `datatype_p.Field_ID`, part of `DataType`). `Error` does not declare an `Equivalence` method. A realization may provide a convenience comparison helper, such as an implementation-package-level `IsEqual`, where an explicit comparison is useful; the helper does not add a second identity source.

Whether `ExpireInFavorOf` itself is still needed at all is tracked in this document's [handoff](./error.handoff.md) — it may be fully redundant, since `Field_LifeCycle` already records a type's lifecycle stage (including an `EndOfLife` state), but `ExpireInFavorOf` answers a different question (*which type replaces this one*) that `LifeCycle` alone does not.

### Boundary discipline
Two distinct boundary disciplines apply to `Error`, and they are easy to conflate. The first governs what an `Error` value may *carry* across a process or network boundary. The second governs what an `Error` value may *be* (which vocabulary it may speak) when it crosses from a diagnostic layer to an actionable one inside a single process. Both must be respected.

#### What may cross a process or network boundary
Only `DataTypeID` crosses a network or process boundary. A concrete error's own fields, if it has any, are either (a) purely local — consumed before a call ever reaches a boundary (for example, SDK-side field validation, never serialized), or (b) routed to a Log Event through the Capture → Persist → Re-express discipline described below — never transmitted as part of the `Error` value itself.

What arrives on the other side of that boundary is, concretely, a numeric identifier — not a human-language message. A single-locale text string is the wrong currency for a contract crossing machines and organizations: it cannot be compared or dispatched on reliably, it forces every receiver into string matching, and it binds the wire format to one rendering of one audience's vocabulary. An integer identifier is stable, locale-independent, cheap to compare, and lets each receiving side resolve the identifier into its own local text bundle (the `Detail` fields above) for whichever audience it faces. The text an error carries belongs at the ends of the wire, resolved per audience; the identifier is what travels.

Dynamic, per-call data that a caller genuinely needs (for example, a retry-after duration) does not belong inside `Error` at all; it belongs in a separate, not-yet-designed sibling output returned alongside `Error` (tracked in this document's [handoff](./error.handoff.md), out of this document's scope). The discipline is strict: if a piece of data must travel with an error to a remote receiver, it must be encoded in a *new* `DataTypeID` (i.e. a new concrete error type), not appended as a field on an existing one.

#### Immutability: an Error is a fixed contract member, not an accumulating envelope
An `Error` value is immutable by construction: identity is the `DataTypeID`, there are no per-instance fields that participate in the contract, and nothing about a concrete error changes after it is created. This is not an incidental property but a consequence of the identity model — and it puts this protocol deliberately at odds with the wrap-and-enrich convention that dominates the broader ecosystem (Go's `%w` wrapping, exception chaining with attached context, middleware decorating errors as they bubble up). In that convention, each layer appends its own context to the error as it passes through, so the error an upper layer finally receives is an accretion of every intermediate layer's annotations.

That convention is rejected here as a category confusion: it uses the error contract — whose job is to tell the immediate caller what happened and what to do next — as a vehicle for diagnostic bookkeeping, which is Log's job. Each layer's "enrichment" is precisely the diagnostic detail that the [Boundary translation](#boundary-translation) discipline says belongs in a log event persisted at the boundary, not in the contract the next layer must interpret. The alternative is not loss of information: the Capture → Persist → Re-express steps preserve every layer's diagnostic contribution in the log stream, correlated, while the re-expressed error stays exactly as wide as the receiving layer's vocabulary. The ecosystem's contrary experience — "if you don't enrich at each layer you lose the trace" — is real, but it is evidence about ecosystems that lack the separation of concerns this protocol draws, not evidence that the error contract must absorb the log's role. Where the ecosystem practice persists despite this, the failure modes of [Boundary discipline](#boundary-discipline) follow: callers receive errors too detailed for their vocabulary, and diagnostic data arrives scattered across the contract instead of correlated in the log.

The same immutability discipline answers a recurring design question: an error must never be created dynamically to carry per-request particulars (a failing filename, a request id). If those particulars matter to the caller's decision, the *operation's design* is wrong — a well-shaped method returns a fixed, named error type, and whatever identification the caller needs is available through inputs the caller already holds or through the sibling output channel tracked in the unresolved questions. Creating a distinct error instance per request is a signature of diagnostic data being smuggled into the contract.

#### What vocabulary an Error may speak across a layer boundary
This is the *Error vs. Log* discipline. **Error** and **Log** are distinct concerns that the broader software ecosystem routinely conflates. `Error` is a contract addressed to the immediate caller, meant to let that caller decide what to do next. `Log` is a forensic record addressed to an operator or monitoring system. Whenever an error crosses from a layer where it is diagnostic (full of internal detail) into a layer where it is only actionable (meaningful to a business-level caller, free of internal detail), it must be **translated** — captured with context, persisted via a dedicated logging capsule, and re-expressed as a new, layer-appropriate error — not merely forwarded.

Conflating `Error` and `Log` produces two distinct and serious failures:

1. **Low-level system detail leaking to high-level consumers.** A user-facing layer (GUI, public API) ends up displaying or receiving information that is meaningless or actively harmful to expose — connection strings, internal service names, stack-level failure causes, retry counts, or infrastructure identifiers. The consumer at that layer has no use for this detail and no way to act on it.
2. **Loss of the operational context needed to actually investigate the failure.** By the time a low-level failure has been propagated (often unwrapped, often stripped of context) up several layers, the information an operator would need to diagnose it — which server instance, which connection, which upstream dependency, at what time, under what load — has usually already been discarded or scattered across intermediate log statements that are not correlated with the originating error.

Both failures stem from the same root cause: treating "error propagation" and "operational observability" as the same concern, when they are not.

##### The two audiences, stated directly
- **`Error`** is a *contract*. It is part of a method's public behavior, addressed to the *immediate caller*, and its sole purpose is to let that caller make a correct decision about what to do next. An error that crosses a layer boundary must be meaningful and actionable *at that specific layer*. A caller should never need to understand the internal implementation details of the callee to react correctly to its error.
- **`Log`** is an *event* — a functional occurrence within the system that something happened which is operationally significant. A log event may be handled in multiple ways depending on severity and context: stored for later forensic investigation, streamed in real time to another system, or used to trigger an immediate notification (for example alerting an on-call engineer). The key distinction is that a log event records something the *system itself* did or experienced — infrastructure behavior, internal state transitions, resource failures — not something a *user* did or experienced.

This distinction has a direct corollary: **user-domain outcomes must not be modeled as log events.** A `403 Forbidden` response, for example, is not a system event — it is a normal outcome in the user-request domain ("this user is not authorized to perform this action"). Logging it as a system event conflates two separate concerns, pollutes the operational event stream with business-domain data, and obscures both. The correct place to track user request outcomes is within the request-handling domain itself, where the full context of the request is available and the tracking is meaningful to the business, not to an operator monitoring system health.

A third entity completes the picture, and conflating it with either of the two above is the root of most error-handling confusion in the broader ecosystem: the **Bug**. A bug is a defect in human reasoning — an erroneous expectation, design, or implementation held by the people who built the system. It is a property of the development process, not a runtime entity. An `Error`, by contrast, is an informational entity the system itself holds and reports: a named, expected member of a method's contract. Because the two live in different worlds — one human and historical, one informational and runtime — they are *found* by different means: a bug is discovered by human investigation (using Log as forensic evidence among other inputs), while an `Error` is known to the system the moment it exists. Treating an `Error` as if it were a bug to be hunted through log output, or a bug as if it were an `Error` to be modeled in a contract, misplaces both. This distinction is why the Capture → Persist → Re-express discipline below refuses to mix forensic log records into the error contract: the log is the bug's evidence trail; the error is the caller's decision input.

These two concerns have different audiences, different lifetimes, and different content requirements. Conflating them — by letting a low-level error capsule propagate unchanged through every intermediate layer, with logging treated as an afterthought sprinkled wherever convenient — produces errors that are too detailed for their consumer and logs that are too scattered to be useful.

#### Boundary translation

##### The rule: translate at every meaningful boundary
Whenever an error crosses from a layer where it is *diagnostic* (meaningful to an operator, full of internal detail) into a layer where it is *only actionable* (meaningful to a business-level caller, free of internal detail), it MUST be translated, not merely forwarded.

Translation means three steps executed at the boundary, in order:

1. **Capture.** The low-level error is handed to a dedicated logging capsule, which enriches it with contextual metadata relevant to diagnosis — for example `ServerInstanceID`, `ConnectionID`, `TimeStamp`, `UpstreamServiceID`, retry/attempt counters, or any other data meaningful for forensic investigation. This enrichment happens once, at the point where the most context is available — never after the fact, never reconstructed from a bare message string.
2. **Persist.** The enriched record is stored or emitted through the logging capsule's own channel (structured log sink, telemetry pipeline, and so on), entirely separate from the method's return path.
3. **Re-express.** A *new* error, appropriate to the calling layer's vocabulary and concerns, is returned to the caller. This new error carries only what that caller needs to make a decision (for example "transaction could not be completed, retry later" rather than "TCP connection to storage node 10.0.4.12:5432 reset by peer after 3 attempts").

This translation is not optional cleanup — it is the mechanism by which a system maintains a coherent, layer-appropriate vocabulary of failure at every boundary, while still preserving full diagnostic fidelity for operators.

##### Worked example
Consider a financial transaction service that depends on a storage service. The storage layer fails with a low-level connectivity error.

**Without boundary translation (the common, wrong pattern):**
The storage error (`StorageConnectionError: tcp reset by peer, node 10.0.4.12:5432, attempt 3/3`) propagates verbatim through the transaction service and arrives at the GUI. The GUI has no way to present this to a user meaningfully, and the operator has no enriched, correlated log record to investigate from.

**With boundary translation (the Memar pattern):**

```khayyam
tp Logger in "memar/process/log/logger.kh"

tp Err_TransactionTemporarilyUnavailable in "org/finance/errors/transaction_unavailable.kh"
tp LE_TransactionFailure in "org/finance/log-events/transaction_failure-log_event.kh"
tp StorageError in "org/storage/errors/storage-error.kh"

tp RecordTransaction mt (self TransactionService) (req TransactionRequest) (err Error) {
  vr storageErr StorageError
  storage.Save(req.TransactionRecord)(storageErr)

  storageErr.OnAbsent(TransactionSaved)
  tp TransactionSaved sc {
      // storage succeeded — nothing further needed on this path
  }

  storageErr.OnPresent(TransactionStorageFailed)
  tp TransactionStorageFailed sc {
      // 1. Capture: enrich the low-level error with all available context
      vr logEntry LE_TransactionFailure
      logEntry.From(storageErr)()
      logEntry.AttachContext(self.ServerInstanceID, self.ConnectionID, req.TransactionID)()

      // 2. Persist: emit to the logging sink, decoupled from the return path
      //    (if the log sink itself fails, that is a separate, lower-priority concern)
      Logger.DispatchEvent(logEntry)()

      // 3. Re-express: return a new error appropriate to the caller (e.g. a GUI or upstream service)
      //    The caller never learns the cause was a storage connectivity failure
      err.Clone(Err_TransactionTemporarilyUnavailable)()
  }
}
```

The caller of `RecordTransaction` — typically a GUI or an upstream business service — only ever sees `ErrTransactionTemporarilyUnavailable`. It never sees that the underlying cause was a storage connectivity issue, a serialization failure, or a timeout; those distinctions are irrelevant to what the GUI needs to do, which is usually "tell the user and perhaps allow retry." The full diagnostic detail, meanwhile, is fully preserved in the log record, correlated with `TransactionID`, ready for an operator to investigate. The boundary-translation discipline has been validated against the financial-transaction worked example in this section; it has not yet been exercised at scale across a real production codebase.

##### When translation is — and is not — required

Translation at a meaningful boundary consists of the three steps above (Capture → Persist → Re-express), executed in that order, at the first layer where the incoming error's vocabulary no longer matches the outgoing layer's domain.

The following clarifications apply to the rule's scope:

- **Most errors do not need translation.** A purely expected, recoverable condition (for example "this username is already taken", "this record was not found") is a normal part of a method's contract. It is returned as an `Error` and handled by the immediate caller, because it is information the caller can act on directly. No log entry is needed, and no translation is needed — the error is already expressed in the right vocabulary for its caller.
- **Translation is required when vocabularies diverge.** The signal is: "does the caller need to understand anything about how this capsule is implemented to react correctly to this error?" If yes, the error is in the wrong vocabulary and must be translated before crossing the boundary.
- **The logging capsule is not prescribed.** The specific shape of `TransactionFailureLog`, the log sink type, and the telemetry pipeline are framework/library concerns left to the Memar recommended logging capsules or to organization-specific replacements. This document specifies the *discipline* (the decision to enrich and persist at the boundary), not the mechanism.

A companion document specifying the concrete API of the recommended Memar logging capsule (the shape of `TransactionFailureLog`, the `Logger` interface, and standard context-attachment methods) is the natural next step once this boundary-translation discipline itself is finalized — tracked in this document's [handoff](./error.handoff.md).

### Detail and Quiddity fields — two audiences, not one

`Error` inherits, via `DataType`, a bundle of locale-resolved text fields (`Summary`, `Overview`, `UserActionNote`, `DevActionNote`, `TAGS`, `Domain`, from `Detail`; `Name`, `Abbreviation`, `Aliases`, from `Quiddity`). These serve two distinct audiences and must not be conflated:

- **Type documentation** (`Summary`, `Overview`, `Domain`, `TAGS`): describes the concept in general, read independently of any specific occurrence — for example a manager reviewing what a service can fail with. `Domain`, specifically, is a locale-translated, display-oriented grouping label for humans; it is NOT a stable, programmatically-safe classification signal (that role belongs to the optional capability interfaces above, which are type-safe and locale-independent).
- **Occurrence guidance** (`UserActionNote`, `DevActionNote`): addressed to whoever is facing a live occurrence of this error, describing what to do next — `UserActionNote` for the end user, `DevActionNote` for the developer/integrator. These names were chosen over the shorter `UserNote`/`DevNote` specifically to make the "what to do" framing explicit.

`Aliases` and `Abbreviation` are human-lookup conveniences only, never unique and never usable for dispatch or equality — `DataTypeID` is the only identifier with that guarantee. A concrete, confirmed use case for `Aliases` on `Error` specifically: a support agent searching for an error by a user's vaguely-remembered wording over the phone.

### ADT composition — the full `ADT` family at the canonical level

`Error`'s canonical composition embeds the full `ADT` family (`IsNil`/`IsNull`/`IsEmpty`), not just `Nil`. Each realization supplies that family; the host language determines how absence is represented without changing the canonical contract.

What genuinely remains open, and is **not** resolved by this correction, is the deeper semantic question: what `IsNull`/`IsEmpty` actually *mean* for a value whose entire purpose is identity, not data. That question belongs to the `ADT` capsule family's own dedicated document, tracked separately (see this document's [handoff](./error.handoff.md)), and this document does not attempt to answer it — only to state that the canonical `Error` contract requires all three methods.

### `ImplementsError` — a tooling-facing declaration, not a safety mechanism

`Error` embeds `ImplementsError`, requiring a single, plain implementation-intent declaration (for example, a method named `ImplError()` in a realization). This is `Error`'s own domain-specific realization of the general, tooling-facing `abstraction_p.Implements` pattern: it lets a code generator discover a capsule's intent to become an `Error` before the capsule structurally qualifies (i.e. before every other method is written), which the full method-set alone cannot do for an incomplete capsule. The domain-specific name (rather than the fully generic `Implements()`) exists so a capsule declaring intent for more than one abstraction at once can indicate *which* declaration is for which abstraction.

```khayyam
tp ImplementsError ab

tp ImplError mt (self ImplementsError) () ()

tp ErrServiceNotFound cp {
    ImplementsError
    // ... other Error methods, possibly generated ...
}

tp ImplError mt (self ErrServiceNotFound) () () {
    // Body-less or trivial — the method's existence is the signal,
    // its body carries no runtime meaning.
}
```

This method provides **no safety or "sealed interface" guarantee**. `abstraction_p.Implements` and its domain-specific realizations exist purely to help tooling, not to guard against misuse.

### Enforcement of the "each Error is its own type" rule
Per the [Type](../type.md) identity principle, every concrete error is its own distinct type, generated (not hand-authored, in the common case) by a code generator that reads `ImplementsError`-declared, incomplete capsules and scaffolds the remaining `Error` methods. The suggested (non-binding) naming convention for this family is the `Err` prefix with the remainder in PascalCase (`ErrServiceNotFound`, `ErrTransactionUnavailable`); this document is that convention's home. Its status — a topic's explicitly non-binding convention, enforced if at all by per-organization linter configuration — is the kind defined in [documentation-explanation.md → Conventions](../documentation-explanation.md#conventions).

This rule is the load-bearing one that everything else in this document depends on. Without it:

- `ImplementsError`'s tooling-facing declaration would have nothing to *generate*.
- The covariant-return benefit described under [Multi-cause returns](#multi-cause-returns) would collapse, because every error would be the same generic type and a method's error return would have no narrower type to be covariant *to*.
- The optional capability-interface pattern would collapse too, because there would be no distinct concrete types to compose capabilities onto.
- Identity-by-`DataTypeID` would degenerate to "all errors share one `DataTypeID`", making the equality discussion meaningless.

A reader who finds the "every error is its own type" claim surprising, or who wants the full argument for it, should read [Type](../type.md) directly; this document does not re-argue it.
