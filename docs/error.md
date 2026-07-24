---
Title: "The Error"
Status: Proposed
Start Date: 2026-07-08
ID: 495442
Applied to: []
Citations:
  - Title: "Static Concepts Must Be Types"
    URI: "./type-static_concepts_must_be_types.md"
    Relation: Depends_on
    Reason: "Establishes the principle that every static concept (no per-instance dynamic data) — including every concrete error — must be its own distinct type rather than an instance of a shared generic capsule. Error is the motivating case for that RFC, and this document cannot be understood or implemented without it."
  - Title: "abstraction_p.Implements — A Tooling-Facing Implementation-Intent Declaration"
    URI: ""
    Relation: Depends_on
    Reason: "Defines the general tooling-facing Implements pattern that Error's ImplementsError method is a domain-specific realization of. Naming, semantics, and the rejection of sealed-interface hardening all derive from that pattern's own specification."
  - Title: "Documentation"
    URI: "./documentation.md"
    Relation: Reference
    Reason: "Specifies the canonical document structure this file follows."
  - Title: "Khayyam — Programming Language"
    URI: "./Khayyam.md"
    Relation: Reference
    Reason: "Source of truth for the syntax of every code example in this document (tp/mt/vr/cp/ab/sc keywords, capsule composition, abstraction composition, body-less methods as contracts)."
Contributors:
  - Name: "Omid Hekayati"
    URI: "mailto:omid@genius.group"
    Tasks:
      - Works: ["Authored all core design decisions across an extended multi-session discussion", "Defined Error's method composition and boundary-crossing discipline", "Rejected Equivalence and sealed-interface markers", "Established the ImplementsError naming rationale and the optional capability-interface pattern", "Decided (informed by document#495421, developed in a parallel session) that each Error concept is its own concrete type", "Authored the Error vs. Log boundary-translation discipline that this document absorbs", "Directed the merge of the two source documents into this single canonical document"]
        URI: ""
  - Name: "Gemini"
    URI: "https://gemini.google.com/"
    Model: "3.1 pro"
    Effort: "Extended thinking enabled"
    Tasks:
      - Works: ["Initial draft", "Argued for and against alternatives"]
        URI: ""
  - Name: "Claude"
    URI: "https://claude.ai"
    Model: "claude-sonnet-5"
    Effort: "Medium - extended thinking enabled"
    Tasks:
      - Works: ["Critical review"]
        URI: ""
  - Name: "Super Z"
    URI: "https://z.ai"
    Model: "GLM-5.2"
    Effort: ""
    Tasks:
      - Works: ["Drafted and revised the Error interface across several rounds", "Identified and corrected two Go package-visibility bugs in an intermediate marker-method design", "Argued for and then against a sealed-interface marker pattern as evidence developed", "Consolidated the Error Abstraction and Error vs. Log discussions into this single canonical document", "Verified all Khayyam code examples against Khayyam.md's syntax rules", "Restructured the merged content to follow documentation.md's body-section specification"]
        URI: ""
---

# The Error Abstraction — Composition, Identity, and Boundary Discipline

## Abstract
`Error` is the framework's abstraction for a distinct, identifiable fault condition returned by a fallible operation. This document defines what `Error` is composed of, how its identity and equality work, what crosses a process/network boundary and what does not, how tooling can discover a capsule's intent to implement it, and how an error's vocabulary must be translated whenever it crosses from a diagnostic layer into an actionable one. It absorbs — without summarizing — the boundary-discipline rule previously tracked as a separate document ("Error vs. Log") so that the full Error lifecycle, from composition through cross-boundary behavior, lives in one place. It assumes, and does not re-argue, the principle established in *Static Concepts Must Be Types* that a static concept (no per-instance dynamic data) must be its own distinct type: every concrete error (`ErrServiceNotFound`, `ErrTransactionUnavailable`, …) is generated as its own type, never instantiated from a shared generic `Error` capsule via an `Init` method.

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
This document is the consolidation of two documents previously maintained in parallel: the *Error Abstraction* RFC (composition, identity, tooling-facing declaration, optional capability interfaces) and the *Error vs. Log* RFC (the Capture → Persist → Re-express translation discipline). The two were merged because they answer two halves of the same question — what an `Error` is, and what an `Error` is allowed to do when it leaves its origin layer — and forcing a reader to load two documents to assemble a single mental model produced the same scattering problem this project's documentation specification was written to eliminate.

The content was arrived at through: sustained design discussion across multiple working sessions, with each proposed change argued for and against rather than accepted on first suggestion; rejection of an earlier `Equivalence[Error]` method on the grounds that it duplicated the `DataTypeID()` comparison; rejection of a sealed-interface marker pattern (RFCs 495390, 495393, 495414) after evidence accumulated that it bought no real guarantee beyond a plain exported method; correction of a Go-specific realization detail that had been incorrectly generalized into the abstraction's canonical composition (the `ADT` family narrowing); and direct testing of the boundary-translation rule against a concrete worked example (the financial-transaction service used in the [Boundary translation](#boundary-translation) topic below) to confirm the three-step Capture → Persist → Re-express pattern actually resolves the two failure modes the rule was written to prevent.

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

A concrete error composes `Error` — the exact mechanics of how a concrete capsule obtains `Error`'s method implementations from a shared parent capsule are intentionally NOT shown here. Khayyam has no automatic inheritance or method promotion: placing one capsule inside another via composition is containment only, and the containing capsule must explicitly implement and forward each method itself. That question — Khayyam's capsule composition and reuse model in general, not specific to `Error` — is tracked as its own future RFC (see [Unresolved questions](#unresolved-questions)); this document does not assume an answer to it.

Worth stating plainly: the absence of automatic method promotion means a concrete error's forwarding methods must be written explicitly, one way or another. This is not treated here as a defect requiring mitigation. Explicit forwarding has a real benefit — no implicit resolution chain to trace, no accidental complex inheritance relationships forming behind a developer's back, and a capsule's actual behavior is always visible directly in its own file rather than inherited invisibly from elsewhere. In an era where hand-typing repetitive boilerplate is no longer how most such code actually gets produced — whether by a code generator (the tooling-facing pattern this document depends on) or by AI-assisted development — the traditional cost argument against explicitness carries much less weight than it would have in an earlier era of software development, while the comprehension benefit of explicitness remains fully intact regardless of who or what writes the code.

#### The four composed abstractions
Each embedded abstraction contributes a specific, non-overlapping responsibility to `Error`'s contract:

- **`DataType`** supplies the type-level identity machinery — `Field_ID` (whose value is what `DataTypeID()` returns), `Field_LifeCycle` (recording whether a type is `Experimental`, `Stable`, `Deprecated`, or `EndOfLife`), the `Detail` and `Quiddity` text bundles, and the optional `ExpireInFavorOf` pointer discussed under [Identity and equality](#identity-and-equality). Without `DataType`, `Error` would have no canonical identifier to compare across processes.
- **`Field_MediaType`** supplies the serialization envelope label used when an error's `DataTypeID` (and nothing else) is transmitted across a network boundary. It is what allows a remote receiver to dispatch on the *kind* of error without needing the full concrete type's method set in scope.
- **`ADT`** supplies the null-state family (`IsNil` / `IsNull` / `IsEmpty`). Khayyam's `Error` canonically requires all three; the question of what `IsNull`/`IsEmpty` should mean for a value whose entire purpose is identity (rather than data) is left to a dedicated ADT session and tracked under [Unresolved questions](#unresolved-questions).
- **`ImplementsError`** is the tooling-facing declaration described in its own topic below — a single plain method that lets a code generator discover intent before a capsule structurally qualifies as an `Error`.

### Optional capability interfaces
A concrete error MAY additionally implement any of a small set of independent, orthogonal capability interfaces, checked by generic infrastructure via type-assertion rather than declared on `Error` itself:

```khayyam
tp ErrStorageUnavailable cp {
    Error
    Internal    // caused by this process's own logic, not the caller's input
    Temporary   // retrying later may succeed
}
```

`Internal`, `Temporary`, and `Timeout` are independent dimensions — an error may be any combination of them, or none. This lets a circuit breaker, retry policy, or alerting system reason about a *class* of errors ("is this retryable?") without needing to enumerate every concrete `DataTypeID`, while keeping this reasoning entirely opt-in per concrete error rather than a mandatory field every error must populate.

A capability interface is itself an `ab`, declared in the same vocabulary as `Error` itself. A concrete error declares it by composition in its capsule body (as `ErrStorageUnavailable` does above); generic infrastructure then type-asserts against it on a received `Error` value:

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
A method that can fail in more than one way returns the `Error` abstraction; a method with exactly one possible failure cause returns that concrete type directly (a covariant-return consequence of the underlying *Static Concepts Must Be Types* principle):

```khayyam
tp Authorize mt (self Service) (token Token) (result AuthResult) (err ErrPermissionDenied)
tp Find mt (self Service) (id ID) (result Result) (err Error)
```

`Authorize` can fail in exactly one way (the token does not authorize), so its error type is the concrete `ErrPermissionDenied` — the caller can dispatch on the type directly and the compiler's covariant-return support gives this no runtime cost. `Find`, by contrast, can fail for several distinct reasons (not found, storage unavailable, timeout, permission denied) and so returns the abstraction; the caller type-asserts or branches on `DataTypeID()` to recover the specific cause.

### Identity and equality

Identity is `DataTypeID()` alone (via `datatype_p.Field_ID`, part of `DataType`). `Error` does NOT declare an `Equivalence` method. An earlier draft included one; it was removed because, once it is established that `Error` carries no per-instance dynamic field meaningful to compare beyond "which error occurred" (see [Boundary discipline](#boundary-discipline) below), any equivalence check would only re-derive the `DataTypeID` comparison under a second name. A generic, package-level helper function (`error.IsEqual`, in the implementation package, not a required interface method) is provided for convenience where an explicit comparison is useful.

A related, briefly considered design — using `ExpireInFavorOf() DataType` (from `datatype_p.Details`) as an implicit equivalence relation, so that a deprecated error could be treated as "equal to" its replacement — was rejected as misleading: conflating "this type is being phased out in favor of that one" with "these two values are the same" is a category error. Whether `ExpireInFavorOf` itself is still needed at all, now that this reasoning for keeping it has been rejected, is tracked in [Unresolved questions](#unresolved-questions) — it may be fully redundant, since `Field_LifeCycle` already records a type's lifecycle stage (including an `EndOfLife` state), but `ExpireInFavorOf` answers a different question (*which type replaces this one*) that `LifeCycle` alone does not.

#### Discussion

##### Drawbacks

Equality by `DataTypeID` alone means two structurally identical errors defined in different files (or different organizations) are *not* equal, even if a human would call them the same concept. This is intentional — identity is anchored to the file URI the type was declared in, exactly as Khayyam's import mechanism anchors everything else — but it does mean the framework has no built-in notion of "synonymous errors across organizations." Cross-organization error mapping, when it is needed, is an application concern handled at a translation boundary (see [Boundary translation](#boundary-translation)), not a property of `Error` itself.

##### Rationale and alternatives

- **`Equivalence[Error]` method (rejected):** redundant with `DataTypeID()` comparison once it was established that `Error` carries no comparison-meaningful per-instance data. Maintaining it would have required every concrete error to implement a method whose body always degenerates to the same `DataTypeID` comparison.
- **`ExpireInFavorOf` as implicit equivalence (rejected):** conflates type-lifecycle phasing with value equality. A deprecated type and its replacement are not "the same value" — they are two distinct types, one of which is being phased out in favor of the other.
- **Identity by `Name` or `Aliases` (rejected):** human-readable names are not guaranteed unique across files, are locale-dependent, and may change as a type's vocabulary evolves. `DataTypeID` is stable, programmatically safe, and locale-independent.

##### Unresolved questions

- **`IsEqual`'s `MediaType()` comparison.** The generic `error.IsEqual` helper compares both `DataTypeID()` and `MediaType()`. If `MediaType` is a fixed, type-level property (every instance of a given `DataTypeID` always reports the same `MediaType`), this check is redundant and should be dropped. If `MediaType` can genuinely vary per-instance for the same `DataTypeID`, this reopens the "identity is `DataTypeID` alone" principle stated above and needs to be resolved explicitly. Not yet decided.
- **`ExpireInFavorOf`.** The reasoning that originally justified analyzing it alongside `Equivalence` no longer applies, but whether the underlying capability (declaring "this type is replaced by that one") is still wanted for `Error`, in some form, has not been given a final yes/no. Blocked on `datatype_p.Details` (the file defining it) being shared for review.

### Boundary discipline
Two distinct boundary disciplines apply to `Error`, and they are easy to conflate. The first governs what an `Error` value may *carry* across a process or network boundary. The second governs what an `Error` value may *be* (which vocabulary it may speak) when it crosses from a diagnostic layer to an actionable one inside a single process. Both must be respected.

#### What may cross a process or network boundary
Only `DataTypeID` crosses a network or process boundary. A concrete error's own fields, if it has any, are either (a) purely local — consumed before a call ever reaches a boundary (for example, SDK-side field validation, never serialized), or (b) routed to a Log Event through the Capture → Persist → Re-express discipline described below — never transmitted as part of the `Error` value itself.

Dynamic, per-call data that a caller genuinely needs (for example, a retry-after duration) does not belong inside `Error` at all; it belongs in a separate, not-yet-designed sibling output returned alongside `Error` (tracked in the [Unresolved questions](#unresolved-questions), out of this document's scope). The discipline is strict: if a piece of data must travel with an error to a remote receiver, it must be encoded in a *new* `DataTypeID` (i.e. a new concrete error type), not appended as a field on an existing one.

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

The caller of `RecordTransaction` — typically a GUI or an upstream business service — only ever sees `ErrTransactionTemporarilyUnavailable`. It never sees that the underlying cause was a storage connectivity issue, a serialization failure, or a timeout; those distinctions are irrelevant to what the GUI needs to do, which is usually "tell the user and perhaps allow retry." The full diagnostic detail, meanwhile, is fully preserved in the log record, correlated with `TransactionID`, ready for an operator to investigate.

##### When translation is — and is not — required

Translation at a meaningful boundary consists of the three steps above (Capture → Persist → Re-express), executed in that order, at the first layer where the incoming error's vocabulary no longer matches the outgoing layer's domain.

The following clarifications apply to the rule's scope:

- **Most errors do not need translation.** A purely expected, recoverable condition (for example "this username is already taken", "this record was not found") is a normal part of a method's contract. It is returned as an `Error` and handled by the immediate caller, because it is information the caller can act on directly. No log entry is needed, and no translation is needed — the error is already expressed in the right vocabulary for its caller.
- **Translation is required when vocabularies diverge.** The signal is: "does the caller need to understand anything about how this capsule is implemented to react correctly to this error?" If yes, the error is in the wrong vocabulary and must be translated before crossing the boundary.
- **The logging capsule is not prescribed.** The specific shape of `TransactionFailureLog`, the log sink type, and the telemetry pipeline are framework/library concerns left to the Memar recommended logging capsules or to organization-specific replacements. This document specifies the *discipline* (the decision to enrich and persist at the boundary), not the mechanism.

##### Discussion

###### Drawbacks

This rule cannot be reduced to a structural or syntactic check, unlike most other rules in this RFC set (for example definite assignment, or `Deinit`-path coverage). Determining whether a given error *should* have been translated at a given boundary requires understanding the semantic role of that boundary — a judgment about domain architecture, not about code shape. A structural linter can verify that a logging capsule was called somewhere along a path, or that a return type is `Error`-compatible. It cannot determine whether the *specific* error returned still leaks internal vocabulary inappropriate to its caller, or whether a low-level error was forwarded unchanged when it should have been re-expressed.

This class of review is better suited to AI-assisted static analysis trained on the distinction described here, operating as a complementary check alongside (not a replacement for) the structural linter rules defined elsewhere.

###### Rationale and alternatives

The alternative — letting errors propagate verbatim through every layer, with logging treated as an afterthought — was rejected as the direct cause of both failure modes described in [Boundary discipline](#boundary-discipline). It is the prevailing pattern in most codebases precisely because no language or framework makes translation the path of least resistance; this document makes it explicit that the Memar framework does.

###### Prior art

This pattern echoes the general "fault boundary translation" practice recommended in Domain-Driven Design and clean-architecture literature (translating infrastructure exceptions into domain exceptions at a repository boundary), but is stated here as an explicit, named, framework-wide rule rather than an implicit convention. The specific enrichment-before-logging step (attaching `ServerInstanceID`, `ConnectionID`, correlated IDs to the log record at the point of maximum available context) draws on observability engineering practices — structured logging, distributed tracing correlation — that exist in the ecosystem as best practices but are rarely enforced architecturally.

###### Unresolved questions

Whether a companion naming convention (for example a type-naming prefix or suffix distinguishing errors that are "safe to propagate as-is" from errors that "must be translated before crossing a boundary") should be introduced is not yet decided. If introduced, this would become a follow-up document referencing this one.

###### Future possibilities

A companion document specifying the concrete API of the recommended Memar logging capsule (the shape of `TransactionFailureLog`, the `LogSink` interface, and standard context-attachment methods) is the natural next step once this boundary-translation discipline itself is finalized.

### Detail and Quiddity fields — two audiences, not one

`Error` inherits, via `DataType`, a bundle of locale-resolved text fields (`Summary`, `Overview`, `UserActionNote`, `DevActionNote`, `TAGS`, `Domain`, from `Detail`; `Name`, `Abbreviation`, `Aliases`, from `Quiddity`). These serve two distinct audiences and must not be conflated:

- **Type documentation** (`Summary`, `Overview`, `Domain`, `TAGS`): describes the concept in general, read independently of any specific occurrence — for example a manager reviewing what a service can fail with. `Domain`, specifically, is a locale-translated, display-oriented grouping label for humans; it is NOT a stable, programmatically-safe classification signal (that role belongs to the optional capability interfaces above, which are type-safe and locale-independent).
- **Occurrence guidance** (`UserActionNote`, `DevActionNote`): addressed to whoever is facing a live occurrence of this error, describing what to do next — `UserActionNote` for the end user, `DevActionNote` for the developer/integrator. These names were chosen over the shorter `UserNote`/`DevNote` specifically to make the "what to do" framing explicit.

`Aliases` and `Abbreviation` are human-lookup conveniences only, never unique and never usable for dispatch or equality — `DataTypeID` is the only identifier with that guarantee. A concrete, confirmed use case for `Aliases` on `Error` specifically: a support agent searching for an error by a user's vaguely-remembered wording over the phone.

#### Discussion

##### Rationale and alternatives

- **A single free-text `Description` field (rejected):** collapses two genuinely different jobs (describing the type in general versus advising the occurrence-facing reader on what to do) into one blob of text, with no machine-readable signal of which audience a given sentence serves.
- **Locale-independent `Domain` as a classification signal (rejected):** would couple a business-domain taxonomy to `Error`'s dispatch model, freezing a particular taxonomy into the type system when capability interfaces already provide a more flexible, type-safe alternative.

##### Prior art

The Detail/Quiddity split (type documentation vs. occurrence guidance) has no direct precedent identified in mainstream error-handling literature; it was arrived at independently during this discussion. Most prior art (Go's `error`, Rust's `Error` trait, Java's `Throwable`) carries a single free-text message or a context-display string with no built-in audience distinction.

### ADT composition — the full `ADT` family at the canonical/Khayyam level

`Error`'s canonical composition embeds the full `ADT` family (`IsNil`/`IsNull`/`IsEmpty`), not just `Nil`. An earlier draft of this document narrowed this to `Nil` alone; that was a mistake, made by generalizing a Go-specific realization detail into the abstraction's canonical definition. The narrowing to `Nil` is legitimate only as Go's own realization, motivated by a Go-specific fact: Khayyam variables are always true references (never nullable pointers), so "nil" in Khayyam does not carry the same meaning it does in Go, and the concept of absence Khayyam needs is not reducible to a simple pointer-nil check the way Go's `err == nil` is. Go's memar-go realization may therefore continue to use only `adt_p.Nil`, as a backend-specific divergence (the same kind of divergence already established for `ImplementsError`'s naming), but this must not be read back into the Memar-level definition of `Error` itself.

What genuinely remains open, and is **not** resolved by this correction, is the deeper semantic question: what `IsNull`/`IsEmpty` actually *mean* for a value whose entire purpose is identity, not data. That question belongs to the `ADT` capsule family's own dedicated RFC, tracked separately (see [Unresolved questions](#unresolved-questions)), and this document does not attempt to answer it — only to correctly state that Khayyam's `Error` requires all three methods, whatever their eventual semantics turn out to be.

#### Discussion

##### Drawbacks

Requiring three methods whose semantics are not yet settled is an uncomfortable position: implementers writing concrete errors today are being asked to provide `IsNull`/`IsEmpty` implementations whose contracts are not yet fully defined. The mitigation is that a concrete error can return a fixed, conservative answer (`false` for both, since an `Error` value that exists is by definition not null) until the dedicated ADT RFC resolves the deeper question.

##### Rationale and alternatives

- **Narrow to `Nil` alone at the canonical level (an earlier draft; rejected):** generalized a Go-specific realization fact into the abstraction. Khayyam's reference semantics are different enough from Go's pointer semantics that the same narrowing does not necessarily make sense in other backends.
- **Drop `ADT` from `Error`'s composition entirely (rejected):** would remove the only contract-level way to ask "is there actually an error here at all" without a separate side-channel boolean. The `OnPresent`/`OnAbsent` dispatch used in the worked example under [Boundary translation](#boundary-translation) depends on this.

##### Unresolved questions

- **`ADT`'s `IsNull`/`IsEmpty` semantics for a value like `Error`.** Khayyam's `Error` canonically requires all three `ADT` methods (see above); Go's realization narrows to `Nil` alone for Go-specific reasons and is not a template for other backends. What `IsNull`/`IsEmpty` should actually mean for `Error` remains open, tracked in a dedicated ADT/Khayyam session and its own RFC.

### `ImplementsError` — a tooling-facing declaration, not a safety mechanism

`Error` embeds `ImplementsError`, requiring a single, plain, exported method (`ImplError()` in the Go realization). This is `Error`'s own domain-specific realization of the general, tooling-facing `abstraction_p.Implements` pattern: it lets a code generator discover a capsule's intent to become an `Error` before the capsule structurally qualifies (i.e. before every other method is written), which the full method-set alone cannot do for an incomplete capsule. The domain-specific name (rather than the fully generic `Implements()`) exists so a capsule declaring intent for more than one abstraction at once can indicate *which* declaration is for which abstraction.

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

This method provides **no safety or "sealed interface" guarantee** — an earlier design (now Rejected) attempted to harden the Go realization into a compiler-enforced sealed interface using an unexported method and a required embedded marker struct. On review, this was found to add real ceremony (the marker had to live in a specific package, one extra embedded field per concrete type) without buying a real guarantee: deliberately embedding a shared marker struct and deliberately writing the same plain method independently are equally trivial for anyone acting in bad faith, so neither realization is actually harder to fake than the other. Accidental (non-deliberate) collision was separately judged implausible on its own, given `Error`'s real, fully-expanded method count (~15-20 methods once `DataType` is expanded). `abstraction_p.Implements` and its domain-specific realizations exist purely to help tooling, not to guard against misuse.

#### Discussion

##### Rationale and alternatives

- **Sealed-interface marker method (RFCs 495390, 495393, 495414 — all rejected):** examined in detail and found to provide no guarantee beyond a plain exported method. The marker added ceremony (one extra embedded struct per concrete type, in a specific package) without adding any real protection — a determined bad actor can embed the marker just as trivially as they can write the plain method.
- **The fully generic `Implements()` name, with no domain suffix (rejected):** a capsule declaring intent for more than one abstraction at once would have no way to indicate *which* declaration was for which abstraction. The `ImplError` name resolves that ambiguity at zero cost.
- **No tooling-facing declaration at all (rejected):** a code generator scaffolding a large capsule from a `.kh` definition would have no signal that an incomplete capsule is *meant* to become an `Error`, and would be forced to wait until every required method is hand-written before it could recognize the capsule as conforming. The declaration shifts intent-discovery to the earliest possible moment.

##### Future possibilities

A dedicated RFC for the `Error` family's code generator input format (referenced by *Static Concepts Must Be Types*' own Future possibilities as a general follow-up), specifying how a `.kh`/DSL definition of an error's metadata maps to the generated concrete type, is the natural next step once the broader `abstraction_p.Implements` pattern is itself finalized.

### Enforcement of the "each Error is its own type" rule

Per *Static Concepts Must Be Types*, every concrete error is its own distinct type, generated (not hand-authored, in the common case) by a code generator that reads `ImplementsError`-declared, incomplete capsules and scaffolds the remaining `Error` methods. The suggested (non-binding) naming convention for this family is the `Err` prefix (`ErrServiceNotFound`, `ErrTransactionUnavailable`), as already recorded in that document.

This rule is the load-bearing one that everything else in this document depends on. Without it:

- `ImplementsError`'s tooling-facing declaration would have nothing to *generate*.
- The covariant-return benefit described under [Multi-cause returns](#multi-cause-returns) would collapse, because every error would be the same generic type and a method's error return would have no narrower type to be covariant *to*.
- The optional capability-interface pattern would collapse too, because there would be no distinct concrete types to compose capabilities onto.
- Identity-by-`DataTypeID` would degenerate to "all errors share one `DataTypeID`", making the equality discussion meaningless.

A reader who finds the "every error is its own type" claim surprising, or who wants the full argument for it, should read *Static Concepts Must Be Types* directly; this document does not re-argue it.

## Results

Insufficient time has passed since this consolidated document was adopted to report real, observed outcomes from its use across multiple concrete errors. The boundary-translation discipline, in particular, has been validated against the financial-transaction worked example used in [Boundary translation](#boundary-translation) but has not yet been exercised at scale across a real production codebase. This section will be filled in once there is such experience to draw on.

## Discussion

### Drawbacks

1. **Type proliferation**, inherited directly from *Static Concepts Must Be Types*' own Drawback 1 — a system with many distinct error concepts will contain many distinct type definitions. Mitigated by code generation (the `abstraction_p.Implements` pattern); the framework's position is that this is an intended, correct consequence, not a flaw.
2. **Two design threads remain genuinely open** (see [Unresolved questions](#unresolved-questions)) — this document should not be read as completely closing the `Error` abstraction's design, only as the current, consolidated, best understanding.
3. **`ADT`'s `IsNull`/`IsEmpty` semantics for `Error` are not yet defined** — the methods are required (canonically, in Khayyam), but what they should actually return for a value like `Error` is deferred to the dedicated ADT session. Go's realization sidesteps this by using only `Nil`, which is a legitimate, narrower backend-specific choice, not a resolution of the underlying question.
4. **Boundary translation cannot be linted structurally** — see the topic-level Discussion under [Boundary translation](#boundary-translation). This shifts the burden of verifying the rule onto semantic review or AI-assisted static analysis, neither of which is yet built.

### Rationale and alternatives

- **Single generic `Error` capsule with an `Init` method (rejected):** this is *Static Concepts Must Be Types*' central rejected alternative, applied here to `Error` specifically — the concept motivating case for that document in the first place. Demotes identity from the type system to runtime data; incompatible with covariant returns and with the optional capability-interface pattern (both depend on distinct concrete types).
- **`Equivalence[Error]` method (rejected):** redundant with `DataTypeID()` comparison once it was established that `Error` carries no comparison-meaningful per-instance data.
- **Sealed-interface marker method (RFCs 495390, 495393, 495414 — all rejected):** examined in detail and found to provide no guarantee beyond a plain exported method; see the [ImplementsError topic](#implementserror--a-tooling-facing-declaration-not-a-safety-mechanism) above.
- **A single `Category()` enum for classification (rejected in favor of optional capability interfaces):** a closed enum forces every error into one bucket along one axis; `Internal`/`Temporary`/`Timeout` capture genuinely orthogonal dimensions (an error can be any combination) more accurately than a single tag could, and remain fully optional per concrete error rather than mandatory.
- **Keeping the Error composition rules and the boundary-translation rules in separate documents (rejected):** the two are halves of the same question — what an `Error` *is* and what an `Error` is *allowed to do* when it leaves its origin layer. Forcing a reader to load two documents to assemble a single mental model produced the same scattering problem this project's documentation specification was written to eliminate.

### Prior art

Go's `error` interface (single method, value-oriented, identity via `errors.Is`/`errors.As` chain-walking) and Rust's `Error` trait with enum-based error families are both discussed in depth in *Static Concepts Must Be Types* and its companion *Static Concepts Must Be Types — vs Go Philosophy*, which this document defers to rather than repeating.

The Detail/Quiddity split (type documentation vs. occurrence guidance) has no direct precedent identified in mainstream error-handling literature; it was arrived at independently during this discussion.

The boundary-translation pattern echoes the general "fault boundary translation" practice recommended in DDD and clean-architecture literature (translating infrastructure exceptions into domain exceptions at a repository boundary), but is stated here as an explicit, named, framework-wide rule rather than an implicit convention. The specific enrichment-before-logging step (attaching `ServerInstanceID`, `ConnectionID`, correlated IDs to the log record at the point of maximum available context) draws on observability engineering practices (structured logging, distributed tracing correlation) that exist in the ecosystem as best practices but are rarely enforced architecturally.

### Unresolved questions

- **`IsEqual`'s `MediaType()` comparison.** The generic `error.IsEqual` helper compares both `DataTypeID()` and `MediaType()`. If `MediaType` is a fixed, type-level property (every instance of a given `DataTypeID` always reports the same `MediaType`), this check is redundant and should be dropped. If `MediaType` can genuinely vary per-instance for the same `DataTypeID`, this reopens the "identity is `DataTypeID` alone" principle stated under [Identity and equality](#identity-and-equality) and needs to be resolved explicitly. Not yet decided.
- **`ExpireInFavorOf`.** The reasoning that originally justified analyzing it alongside `Equivalence` no longer applies (see [Identity and equality](#identity-and-equality) above), but whether the underlying capability (declaring "this type is replaced by that one") is still wanted for `Error`, in some form, has not been given a final yes/no. Blocked on `datatype_p.Details` (the file defining it) being shared for review.
- **`ADT`'s `IsNull`/`IsEmpty` semantics for a value like `Error`.** Khayyam's `Error` canonically requires all three `ADT` methods (see the [ADT composition topic](#adt-composition--the-full-adt-family-at-the-canonicallykhayyam-level) above); Go's realization narrows to `Nil` alone for Go-specific reasons and is not a template for other backends. What `IsNull`/`IsEmpty` should actually mean for `Error` remains open, tracked in a dedicated ADT/Khayyam session and its own RFC.
- **Khayyam's capsule composition and method-reuse model, in general (not specific to `Error`).** An earlier draft of this document's composition example incorrectly implied that composing `Error` into a concrete capsule automatically promotes its methods, the way Go's struct embedding does. Khayyam has no such automatic inheritance: composition is containment only, and a containing capsule must explicitly implement and forward each method itself. The full implications of this (how concrete errors are actually meant to be authored, what role code generation plays versus a possible future language-level reuse mechanism) needs its own dedicated RFC, since the relevant information is currently scattered across `Khayyam.md`'s capsule and abstraction-composition sections rather than settled in one place. Not specific to `Error`, but `Error` is the concrete motivating case that surfaced it.
- **Whether the optional capability-interface set (`Internal`, `Temporary`, `Timeout`) is complete**, or whether additional orthogonal dimensions will be needed as more of the framework is built out. No process for adding new ones has been defined yet (presumably: propose a new capability interface the same way these three were introduced, but this has not been stated as a rule anywhere).
- **The not-yet-designed retry/cache-policy sibling abstraction**, referenced above as the intended home for dynamic, per-call data like a retry-after duration — out of this document's scope, tracked separately.
- **Whether a companion naming convention is needed** to distinguish errors that are "safe to propagate as-is" from errors that "must be translated before crossing a boundary" (carried forward from the original *Error vs. Log* document). Not yet decided.
- **Whether a structured Memar logging capsule API should be specified** as a follow-up document (carried forward from the original *Error vs. Log* document).

### Future possibilities

- A dedicated RFC for the `Error` family's code generator input format (referenced by *Static Concepts Must Be Types*' own Future possibilities as a general follow-up), specifying how a `.kh`/DSL definition of an error's metadata maps to the generated concrete type.
- Once the ADT session concludes, revisit this document's composition if `Nil` alone proves insufficient.
- A companion document specifying the concrete API of the recommended Memar logging capsule (the shape of `TransactionFailureLog`, the `LogSink` interface, and standard context-attachment methods), as the natural next step once the boundary-translation discipline is finalized.

## Change Rationale

- **Initial draft (RFC 495442, "The Error Abstraction").** Defined `Error`'s composition (`DataType`, `Field_MediaType`, `ADT`, `ImplementsError`), identity by `DataTypeID` alone, the rejection of `Equivalence` and of sealed-interface markers, the optional capability-interface pattern (`Internal`/`Temporary`/`Timeout`), and the multi-cause return signature convention. Tracked `ADT`'s `IsNull`/`IsEmpty` semantics, the `IsEqual`/`MediaType` redundancy question, and the open Khayyam capsule-composition model as Unresolved questions.
- **Boundary-translation rule (originally RFC 000010, "Error vs. Log").** Authored as a separate document in parallel, defining the Capture → Persist → Re-express discipline, the two-audience distinction between `Error` (caller-facing contract) and `Log` (operator-facing forensic event), the corollary that user-domain outcomes must not be modeled as log events, and the worked financial-transaction example showing the rule in action. Noted explicitly that the rule cannot be reduced to a structural or syntactic check, and is better suited to AI-assisted static analysis than to a linter.
- **Consolidation (this revision).** Merged RFC 000010's content into RFC 495442. The merge was prompted by the recognition that the two documents answer two halves of the same question — what an `Error` *is* (composition, identity, tooling-facing declaration) and what an `Error` is *allowed to do* when it leaves its origin layer (the boundary-translation discipline) — and forcing a reader to load two documents to assemble a single mental model produced the same scattering problem this project's documentation specification was written to eliminate. The merge:
  - Reorganized the body to follow the `documentation.md` specification's `Abstract` / `Introduction` (`Motivation`, `Methodology`) / `Explanation` (topic-first, author-named) / `Results` / `Discussion` / `Change Rationale` structure, replacing the source documents' earlier `Summary` / `Guide-level explanation` / `Reference-level explanation` layout. This was a structural migration, not a content rewrite.
  - Preserved every load-bearing claim, alternative rejection, and Unresolved question from both source documents. No content was summarized, compressed, or dropped.
  - Added a single [Composition](#composition) sub-topic enumerating the responsibility of each embedded abstraction (`DataType`, `Field_MediaType`, `ADT`, `ImplementsError`), to give a reader a one-glance overview that neither source document provided in that form.
  - Added a [Boundary discipline](#boundary-discipline) topic that explicitly separates the *two* boundary rules (what an `Error` may carry across a process/network boundary, vs. what vocabulary an `Error` may speak across a layer boundary inside a single process), since the source documents addressed them separately and a reader consolidating the two could otherwise conflate them.
  - Added an [Enforcement](#enforcement-of-the-each-error-is-its-own-type-rule) topic stating explicitly that the "each `Error` is its own type" rule is load-bearing for every other section, and listing what would collapse without it — a dependency that was implicit in the source documents but never stated as such.
  - Verified every Khayyam code example against `Khayyam.md`'s syntax rules (the `tp`/`mt`/`vr`/`cp`/`ab`/`sc` keyword set, the `(self Type) (args) (returns)` method signature shape, the absence of assignment operators, the dot-only invocation rule, the body-less method as contract/FFI declaration, the `OnPresent`/`OnAbsent` dispatch pattern from the source worked example).
  - Carried forward every Unresolved question and Future possibility from both source documents, de-duplicating the two entries that were the same question stated twice (the logging-capsule API follow-up).
