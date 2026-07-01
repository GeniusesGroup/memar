# Error vs. Log: Boundary Translation Discipline

## The Problem
Across the software development ecosystem, the concepts of **Error** and **Log** are routinely conflated. A typical codebase treats "something went wrong" as a single undifferentiated event: it gets wrapped, re-thrown, or propagated upward through every layer of the system until it eventually surfaces — often verbatim — at the topmost consumer, frequently a GUI or an API response shown directly to an end user.

This conflation produces two distinct and serious failures:

1. **Low-level system detail leaking to high-level consumers.** A user-facing layer (GUI, public API) ends up displaying or receiving information that is meaningless or actively harmful to expose — connection strings, internal service names, stack-level failure causes, retry counts, or infrastructure identifiers. The consumer at that layer has no use for this detail and no way to act on it.
2. **Loss of the operational context needed to actually investigate the failure.** By the time a low-level failure has been propagated (often unwrapped, often stripped of context) up several layers, the information an operator would need to diagnose it — which server instance, which connection, which upstream dependency, at what time, under what load — has usually already been discarded or scattered across intermediate log statements that are not correlated with the originating error.

Both failures stem from the same root cause: treating "error propagation" and "operational observability" as the same concern, when they are not.

## The Core Distinction
**Error** is a *contract*. It is part of a method's public behavior, addressed to the *immediate caller*, and its sole purpose is to let that caller make a correct decision about what to do next. An error that crosses a layer boundary must be meaningful and actionable *at that specific layer*. A caller should never need to understand the internal implementation details of the callee to react correctly to its error.

**Log** is a *record*. It is addressed to a human operator or an automated monitoring system, not to a calling capsule. Its purpose is forensic: to preserve enough operational context that a failure can be investigated after the fact, regardless of whether the immediate caller needed (or was able) to do anything about it.

These two concerns have different audiences, different lifetimes, and different content requirements. Conflating them — by letting a low-level error capsule propagate unchanged through every intermediate layer, with logging treated as an afterthought sprinkled wherever convenient — produces errors that are too detailed for their consumer and logs that are too scattered to be useful.

## The Rule: Translate at Every Meaningful Boundary
Whenever an error crosses from a layer where it is *diagnostic* (meaningful to an operator, full of internal detail) into a layer where it is *only actionable* (meaningful to a business-level caller, free of internal detail), it MUST be translated, not merely forwarded.

Translation means:
1. **Capture.** The low-level error is handed to a dedicated logging capsule, which enriches it with contextual metadata relevant to diagnosis — for example `ServerInstanceID`, `ConnectionID`, `TimeStamp`, `UpstreamServiceID`, retry/attempt counters, or any other data meaningful for forensic investigation. This enrichment happens once, at the point where the most context is available — never after the fact, never reconstructed from a bare message string.
2. **Persist.** The enriched record is stored or emitted through the logging capsule's own channel (structured log sink, telemetry pipeline, etc.), entirely separate from the method's return path.
3. **Re-express.** A *new* error, appropriate to the calling layer's vocabulary and concerns, is returned to the caller. This new error carries only what that caller needs to make a decision (e.g., "transaction could not be completed, retry later" rather than "TCP connection to storage node 10.0.4.12:5432 reset by peer after 3 attempts").

This translation is not optional cleanup — it is the mechanism by which a system maintains a coherent, layer-appropriate vocabulary of failure at every boundary, while still preserving full diagnostic fidelity for operators.

## Example
Consider a financial transaction service that depends on a storage service. The storage layer fails with a low-level connectivity error:

```khayyam
// Inside the transaction recording capsule, calling the storage layer:
vr storageErr StorageError
storage.Save(transactionRecord)(storageErr)

storageErr.OnAbsent(TransactionSavedSuccessfully) ()
tp TransactionSavedSuccessfully sc { /* ... */ }

storageErr.OnPresent(TransactionSaveFailed) ()
tp TransactionSaveFailed sc {
    // 1. Capture: hand the low-level error to a logging capsule with context
    vr logEntry FailureLog
    logEntry.From(storageErr)(logEntry)
    logEntry.AttachContext(serverInstanceID, connectionID, transactionID)(logEntry)

    // 2. Persist: send it to the logging/telemetry sink, decoupled from the return path
    logSink.Record(logEntry)(/* logging itself can fail; that is a separate, lower-priority concern */)

    // 3. Re-express: return a new, layer-appropriate error to the actual caller (e.g. the GUI)
    err = ErrTransactionTemporarilyUnavailable
}
```

The caller of the transaction service — typically a GUI or an upstream business service — only ever sees `ErrTransactionTemporarilyUnavailable`. It never sees that the underlying cause was a storage connectivity issue, a serialization failure, or a timeout; those distinctions are irrelevant to what the GUI needs to do, which is usually just "tell the user, perhaps allow retry." The full diagnostic detail, meanwhile, is fully preserved in the log record, correlated with `transactionID`, ready for an operator to investigate.

## What This Rule Does Not Mean
- This does **not** mean every error must be translated at every single layer. Many errors are already meaningful and actionable at the immediate caller's level and should simply propagate as-is (this is the common case, and is what most error-propagation examples in this documentation set illustrate). Translation is required specifically when an error crosses from a diagnostic-detail layer into a decision-only layer — not on every function boundary.
- This does **not** mean Log replaces Error, or that every error must be logged. A purely expected, recoverable condition (e.g., "this username is already taken") is a normal part of a method's contract and does not need a Log entry — it needs to be returned as an Error and handled by the caller, because it is information the caller can act on directly, not a forensic event.
- This does **not** prescribe a specific logging capsule, format, or sink. Per Khayyam's general philosophy, the *mechanism* of logging is a framework/library concern, left to the recommended Memar logging capsules or to organization-specific replacements. This document only establishes the *discipline*: that the decision to log and the decision to translate are made deliberately, at the boundary, rather than left to whichever error happens to bubble up first.

## Why This Cannot Be Enforced by the Compiler or a Traditional Linter
Unlike most rules described in `Khayyam-linter.md` (such as definite assignment, Deinit-path coverage, or orphan-rule violations), this rule cannot be reduced to a structural or syntactic check. Determining whether a given error *should* have been translated at a given boundary requires understanding the *semantic role* of that boundary — whether the caller is a diagnostic-detail consumer or a decision-only consumer — which is a judgment about domain architecture, not about code shape.

A structural linter can verify that a `Logger` capsule was called somewhere along a path, or that a return type is `Error`-compatible. It cannot determine whether the *specific* error returned still leaks internal vocabulary inappropriate to its caller, or whether a low-level error was forwarded unchanged when it should have been re-expressed. This class of review is better suited to AI-assisted static analysis trained on this document's distinction, operating as a complementary check alongside (not a replacement for) the structural linter rules defined elsewhere in this RFC set.
