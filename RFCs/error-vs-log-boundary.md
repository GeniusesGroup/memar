---
RFC Number: 000010
Title: "Error vs. Log: Boundary Translation Discipline"
Status: Draft
Start Date: 2026-06-30
Applied to: []
Supersedes: null
Superseded by: null
Related:
  Depends_on: ["000009"]
  Extends: []
  Conflicts with: []
Author(s): []
---

## Summary
**Error** and **Log** are distinct concerns that the broader software ecosystem routinely conflates. Error is a contract addressed to the immediate caller, meant to let that caller decide what to do next. Log is a forensic record addressed to an operator or monitoring system. Whenever an error crosses from a layer where it is diagnostic (full of internal detail) into a layer where it is only actionable (meaningful to a business-level caller, free of internal detail), it must be **translated** — captured with context, persisted via a dedicated logging capsule, and re-expressed as a new, layer-appropriate error — not merely forwarded.

## Motivation

### The Problem

Across the software development ecosystem, the concepts of Error and Log are routinely conflated. A typical codebase treats "something went wrong" as a single undifferentiated event: it gets wrapped, re-thrown, or propagated upward through every layer of the system until it eventually surfaces — often verbatim — at the topmost consumer, frequently a GUI or an API response shown directly to an end user.

This conflation produces two distinct and serious failures:

1. **Low-level system detail leaking to high-level consumers.** A user-facing layer (GUI, public API) ends up displaying or receiving information that is meaningless or actively harmful to expose — connection strings, internal service names, stack-level failure causes, retry counts, or infrastructure identifiers. The consumer at that layer has no use for this detail and no way to act on it.
2. **Loss of the operational context needed to actually investigate the failure.** By the time a low-level failure has been propagated (often unwrapped, often stripped of context) up several layers, the information an operator would need to diagnose it — which server instance, which connection, which upstream dependency, at what time, under what load — has usually already been discarded or scattered across intermediate log statements that are not correlated with the originating error.

Both failures stem from the same root cause: treating "error propagation" and "operational observability" as the same concern, when they are not.

### The Core Distinction

**Error** is a *contract*. It is part of a method's public behavior, addressed to the *immediate caller*, and its sole purpose is to let that caller make a correct decision about what to do next. An error that crosses a layer boundary must be meaningful and actionable *at that specific layer*. A caller should never need to understand the internal implementation details of the callee to react correctly to its error.

**Log** is a *record*. It is addressed to a human operator or an automated monitoring system, not to a calling capsule. Its purpose is forensic: to preserve enough operational context that a failure can be investigated after the fact, regardless of whether the immediate caller needed (or was able) to do anything about it.

These two concerns have different audiences, different lifetimes, and different content requirements. Conflating them — by letting a low-level error capsule propagate unchanged through every intermediate layer, with logging treated as an afterthought sprinkled wherever convenient — produces errors that are too detailed for their consumer and logs that are too scattered to be useful.

## Guide-level explanation

### The Rule: Translate at Every Meaningful Boundary

Whenever an error crosses from a layer where it is *diagnostic* (meaningful to an operator, full of internal detail) into a layer where it is *only actionable* (meaningful to a business-level caller, free of internal detail), it MUST be translated, not merely forwarded.

Translation means three steps executed at the boundary, in order:

1. **Capture.** The low-level error is handed to a dedicated logging capsule, which enriches it with contextual metadata relevant to diagnosis — for example `ServerInstanceID`, `ConnectionID`, `TimeStamp`, `UpstreamServiceID`, retry/attempt counters, or any other data meaningful for forensic investigation. This enrichment happens once, at the point where the most context is available — never after the fact, never reconstructed from a bare message string.
2. **Persist.** The enriched record is stored or emitted through the logging capsule's own channel (structured log sink, telemetry pipeline, etc.), entirely separate from the method's return path.
3. **Re-express.** A *new* error, appropriate to the calling layer's vocabulary and concerns, is returned to the caller. This new error carries only what that caller needs to make a decision (e.g. "transaction could not be completed, retry later" rather than "TCP connection to storage node 10.0.4.12:5432 reset by peer after 3 attempts").

This translation is not optional cleanup — it is the mechanism by which a system maintains a coherent, layer-appropriate vocabulary of failure at every boundary, while still preserving full diagnostic fidelity for operators.

### Example

Consider a financial transaction service that depends on a storage service. The storage layer fails with a low-level connectivity error.

**Without boundary translation (the common, wrong pattern):**
The storage error (`StorageConnectionError: tcp reset by peer, node 10.0.4.12:5432, attempt 3/3`) propagates verbatim through the transaction service and arrives at the GUI. The GUI has no way to present this to a user meaningfully, and the operator has no enriched, correlated log record to investigate from.

**With boundary translation (the Memar pattern):**

```khayyam
tp ErrTransactionTemporarilyUnavailable in "memar/finance/errors/transaction-unavailable.kh"
tp StorageError in "memar/storage/errors/storage-error.kh"
tp TransactionFailureLog in "memar/finance/logs/transaction-failure-log.kh"

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
      vr logEntry TransactionFailureLog
      logEntry.From(storageErr)(logEntry)
      logEntry.AttachContext(self.ServerInstanceID, self.ConnectionID, req.TransactionID)(logEntry)

      // 2. Persist: emit to the logging sink, decoupled from the return path
      //    (if the log sink itself fails, that is a separate, lower-priority concern)
      self.LogSink.Record(logEntry)()

      // 3. Re-express: return a new error appropriate to the caller (e.g. a GUI or upstream service)
      //    The caller never learns the cause was a storage connectivity failure
      err = ErrTransactionTemporarilyUnavailable
  }
}
```

The caller of `RecordTransaction` — typically a GUI or an upstream business service — only ever sees `ErrTransactionTemporarilyUnavailable`. It never sees that the underlying cause was a storage connectivity issue, a serialization failure, or a timeout; those distinctions are irrelevant to what the GUI needs to do, which is usually "tell the user and perhaps allow retry." The full diagnostic detail, meanwhile, is fully preserved in the log record, correlated with `TransactionID`, ready for an operator to investigate.

## Reference-level explanation

Translation at a meaningful boundary consists of the three steps described in the Guide-level explanation above (Capture → Persist → Re-express), executed in that order, at the first layer where the incoming error's vocabulary no longer matches the outgoing layer's domain.

The following clarifications apply to the rule's scope:

- **Most errors do not need translation.** A purely expected, recoverable condition (e.g. "this username is already taken", "this record was not found") is a normal part of a method's contract. It is returned as an Error and handled by the immediate caller, because it is information the caller can act on directly. No log entry is needed, and no translation is needed — the error is already expressed in the right vocabulary for its caller.
- **Translation is required when vocabularies diverge.** The signal is: "does the caller need to understand anything about how this capsule is implemented to react correctly to this error?" If yes, the error is in the wrong vocabulary and must be translated before crossing the boundary.
- **The logging capsule is not prescribed.** The specific shape of `TransactionFailureLog`, the log sink type, and the telemetry pipeline are framework/library concerns left to the Memar recommended logging capsules or to organization-specific replacements. This RFC specifies the *discipline* (the decision to enrich and persist at the boundary), not the mechanism.

## Drawbacks

This rule cannot be reduced to a structural or syntactic check, unlike most other rules in this RFC set (e.g. definite assignment, `Deinit`-path coverage in RFC 000008). Determining whether a given error *should* have been translated at a given boundary requires understanding the semantic role of that boundary — a judgment about domain architecture, not about code shape. A structural linter can verify that a logging capsule was called somewhere along a path, or that a return type is `Error`-compatible. It cannot determine whether the *specific* error returned still leaks internal vocabulary inappropriate to its caller, or whether a low-level error was forwarded unchanged when it should have been re-expressed.

This class of review is better suited to AI-assisted static analysis trained on the distinction described in this RFC, operating as a complementary check alongside (not a replacement for) the structural linter rules defined elsewhere.

## Rationale and alternatives
The alternative — letting errors propagate verbatim through every layer, with logging treated as an afterthought — was rejected as the direct cause of both failure modes described in the Motivation section. It is the prevailing pattern in most codebases precisely because no language or framework makes translation the path of least resistance; this RFC makes it explicit that Memar does.

## Prior art
This pattern echoes the general "fault boundary translation" practice recommended in DDD and clean-architecture literature (translating infrastructure exceptions into domain exceptions at a repository boundary), but is stated here as an explicit, named, framework-wide rule rather than an implicit convention. The specific enrichment-before-logging step (attaching `ServerInstanceID`, `ConnectionID`, correlated IDs to the log record at the point of maximum available context) draws on observability engineering practices (structured logging, distributed tracing correlation) that exist in the ecosystem as best practices but are rarely enforced architecturally.

## Unresolved questions
This RFC is still under author review and has not yet been finalized for merge into canonical documentation. Whether a companion naming convention (e.g. a type-naming prefix or suffix distinguishing errors that are "safe to propagate as-is" from errors that "must be translated before crossing a boundary") should be introduced is not yet decided. If introduced, this would become a follow-up RFC referencing this one.

## Future possibilities
A companion RFC specifying the concrete API of the recommended Memar logging capsule (the shape of `TransactionFailureLog`, the `LogSink` interface, and standard context-attachment methods) is the natural next step once this boundary-translation discipline itself is finalized.
