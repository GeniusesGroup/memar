# Control Flow in Khayyam Changelog

## Changelog

### Created by merging the Library-Driven Control Flow and Domain-Driven Arithmetic documents
- Time: 2026-07-29T00:00:00Z (approximated from Start Date)
- Type: Added
- Cited:
  - [Khayyam - Programming Language](./khayyam.md) — Reference: The canonical specification defines the `sc` subtype and the `in` import mechanism that library-provided control-flow methods are built on.
  - [Encapsulation in Khayyam](./khayyam-encapsulation.md) — Depends_on: Library-Defined Control Flow's ELSE-must-reference-its-condition rule is a direct application of that document's Closures as Implicit Capsule Syntax topic (no implicit binding to 'whatever came before').
  - [Method in Khayyam](./khayyam-method.md) — Depends_on: Control flow (IF/ELSE, OnPresent/OnAbsent) is built entirely from ordinary method calls, and inherits that document's pass-by-reference, explicit-output-variable, no-chaining model rather than introducing any dedicated call syntax of its own.
  - [The Error](./error.md) — Depends_on: Error Propagation treats `Error` (and its concrete subtypes) as the value being propagated; what the abstraction itself is, and what contract it must satisfy, is defined there, not here.
- Propagates to:
  - khayyam-encapsulation.md: Done — the Code Scope topic was removed from that document's Explanation section and relocated into this document as part of the same merge (see its changelog).
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — claimed: Original design decisions for library-driven control flow, elimination of logical/arithmetic operators, and the code scope (`sc`) mechanism in the canonical Khayyam specification
  - [ChatGPT](../CONTRIBUTORS.md#chatgpt) (Unspecified custom GPT; exact underlying model not recorded — fill in if known; high effort) — proposed: Extracting Domain-Driven Arithmetic out of this document, reframing Error Handling as Error Propagation (a form of control flow rather than an unrelated concern), separating what the compiler provides (execution primitives) from what libraries build on top of it, and reframing Structured Programming historically rather than as an unquestioned default
  - [Claude](../CONTRIBUTORS.md#claude) (claude-sonnet-5, high effort) — rewrote: Created this document by merging the standalone Library-Driven Control Flow and Domain-Driven Arithmetic documents, together with the Code Scope topic relocated from khayyam-encapsulation.md, into the current Explanation-facet specification. Applied the architectural review agreed between the author and ChatGPT: promoted the compiler-exposes-primitives-only conclusion into the Abstract as a stated outcome, split a new Execution Primitives topic out of Library-Defined Control Flow (renamed Library-Defined Control Flow), expanded Structured Programming into a full Structured vs Unstructured Programming topic with its own Discussion bundle, renamed and reframed Error Handling as Error Propagation, and removed residual Domain-Driven Arithmetic content (comparison-operator examples aside) following its extraction to khayyam-variable.md

#### Summary
Initial creation. Created by merging the standalone "Library-Driven Control Flow" and "Domain-Driven Arithmetic: Operator Elimination and Compile-Time Formula Evaluation" documents into the current Explanation-facet specification, together with the "Code Scope" topic relocated from `khayyam-encapsulation.md` (code scopes are the primitive `IF`/`ELSE`/`LOOP` are built on, not a capsule-level concern). Both standalone document files, and the Code Scope section in `khayyam-encapsulation.md`, have been retired/removed accordingly.

### Architectural rescoping (2026-07-31)
- Time: 2026-07-31T00:00:00Z (date recorded in the source listing; time approximated)
- Type: Changed
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — argued: extracted Domain-Driven Arithmetic out of this document himself, to be treated separately in `khayyam-variable.md`
  - [ChatGPT](../CONTRIBUTORS.md#chatgpt), [Claude](../CONTRIBUTORS.md#claude) — reviewed: dialectical review partners for the rescoping described below

#### Summary
Following dialectical review with ChatGPT and Claude: `Domain-Driven Arithmetic` was extracted out of this document entirely by the author, to be treated separately in `khayyam-variable.md`; the residual comparison/arithmetic-operator references, the `MathEval` compile-time-type-checking Unresolved question, and the corresponding Future-possibilities item were removed here accordingly (see the companion note handed off alongside this revision for what to check against the target document). The document's core conclusion — that the compiler exposes only execution primitives and privileges no control-flow model — was promoted into the Abstract as a stated outcome rather than left implicit or treated as the document's starting motivation. The former `Structured programming` stub was expanded into a full `Structured vs Unstructured Programming` topic with its own Discussion bundle, reframing the historical goto-versus-structured debate as a question of what a compiler should privilege, not what a compiler should permit. A new `Execution Primitives: The Compiler's Role` topic was split out of the former `Library-Driven Control Flow` topic (itself renamed `Library-Defined Control Flow`) to keep "what the compiler provides" separate from "what libraries build on top of it." `Error Handling: Library-Driven and Syntax-Free` was renamed `Error Propagation` and reframed as one instance of control flow rather than an unrelated concern, with a short comparison of propagation strategies used by other languages (exceptions, `Result` types, Go-style returns, panic/recover) added to its opening.

### Drawback-framing correction (2026-07-31)
- Time: 2026-07-31T00:00:00Z (date recorded in the source listing; time approximated)
- Type: Fixed
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — corrected: flagged that several Drawbacks/Rationale passages compared Khayyam's visible design costs against other languages' costs as if the latter were zero
  - [Claude](../CONTRIBUTORS.md#claude) (claude-sonnet-5) — rewrote: applied the correction across every affected passage

#### Summary
The author flagged that several Drawbacks/Rationale passages implicitly compared Khayyam's *visible* design costs (imports, ceremony, more characters at a call site) against other languages' costs as if the latter were zero, when in fact those languages pay an equivalent design cost once, invisibly, inside the compiler — frozen for the language's lifetime rather than owned and adjustable by the codebase using it. The author also noted that `Structured vs Unstructured Programming` implied only two paradigms (structured, unstructured) existed, when `Domain-Specific Conditional Methods` demonstrates a third — one that is frequently the *better* option, not a stylistic fallback. Every Drawbacks/Rationale passage touching this comparison (`Structured vs Unstructured Programming`, `Code Scope`, `Execution Primitives`, `Library-Defined Control Flow`, and the document-wide Discussion) was rewritten to state the honest, narrower residual cost (onboarding-recognition friction, ecosystem-bootstrapping maturity, or plain call-site character count) instead of an implied "other languages don't pay this" framing, and to credit domain-named conditionals as a genuine third option rather than a footnote to `IF`/`ELSE`.

### Openness and scope clarifications (2026-07-31)
- Time: 2026-07-31T00:00:00Z (date recorded in the source listing; time approximated)
- Type: Changed
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — clarified: judged that divergent `IF` libraries across projects is not a realistic failure mode and declined to add the proposed Drawback; requested the paradigm list be made explicitly non-exhaustive
  - [Claude](../CONTRIBUTORS.md#claude) (claude-sonnet-5) — rewrote: applied the clarifications

#### Summary
Per further author feedback: the "structured / unstructured / domain-named" paradigm list was made explicitly non-exhaustive and scoped to today's conventional, classical-hardware execution model — nothing in Khayyam couples a control-flow model to a particular computation substrate, so a fundamentally different future paradigm (e.g. quantum computing's superposition-based branching) can be added as another library without touching the language, and this is now stated directly in both the Abstract and `Structured vs Unstructured Programming`. A proposed Drawback about divergent `IF` libraries across projects was not added, per the author's judgment that this is not a realistic failure mode. The residual bootstrapping-cost Drawback under `Execution Primitives`, and two "open cross-document question" phrasings that implicitly demanded an unwritten companion document, were softened to avoid creating any obligation toward other documents or overstating the difficulty of reaching high productivity. The Abstract now also explicitly acknowledges that method invocation is itself a control-flow event, and states — rather than leaves implicit — that Khayyam deliberately treats Method as a more foundational Type covered elsewhere, not as an oversight in this document's scope.

### Completed migration to the Explanation-facet specification
- Time: 2026-08-26T00:00:00Z
- Type: refactor
- Cited:
  - [Documentation](./documentation.md) — Reference: facet meta-layer defining Explanation/Practice/Changelog.
  - [Documentation — Explanation](./documentation-explanation.md) — Depends_on: governing structure the base document was brought fully in line with.
  - [Documentation — Changelog](./documentation-changelog.md) — Depends_on: entry structure used for this companion file.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — requested: migration of this document to the latest documentation method without summarizing
  - [Super Z](../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — migrated: structural completion and provenance relocation per the Explanation-facet specification

#### Summary
Completed the migration (this document already followed most of the current structure since its creation). Remaining steps done here: relocated all remaining provenance out of the base document — front-matter `Applied to`, `Citations`, and `Contributors` moved into this file's entries above; the body's former `## Change Rationale` section became the dated entries above; the empty `Results` section received the standard placeholder sentence used across sibling documents; and one broken cross-reference was repaired — the Motivation linked `./khayyam-method.md#method-as-callable-capsule`, an anchor that no longer exists in `khayyam-method.md` because the mechanical signature spec now lives under that document's "Method Structure" topic, so the link label and target were updated accordingly. No prose was summarized or shortened anywhere in the base document; no design decision changed.

---

### Correct examples and clarify the compiler-event contract; narrow covariant claim; clarify mid-scope exits
- Time: 2026-08-27T00:00:00Z
- Type: Fixed
- Cited:
  - [Method in Khayyam](./khayyam-method.md) — Depends_on: `sc` entry/exit and the `IF`/`ELSE` exclusivity are learned from `sc` events
  - [The Error](./error.md) — Depends_on: single-error vs. multi-error channel typing
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — requested: clarified that the compiler is an independent app emitting events, that type-as-argument need not be restricted at language level, and that `CF.Return`/`Break` mid-scope is not automatically a smell
  - [Super Z](../CONTRIBUTORS.md#super-z) — rewrote: content below

#### Summary
Four focused fixes, each with the full historical path now preserved here (base document carries only the corrected current state):
1. Replaces the `err = ErrPaymentTemporarilyUnavailable` statement in the payment example (which used `=`, a token that does not exist in Khayyam) with explicit `CopyFrom` calls on a named intermediate error variable.
2. Clarifies `Execution Primitives: The Compiler's Role` to state that the compiler is an independent application emitting `sc` entry/exit and jump events to which DAA/linter subscribe; third-party CF libraries target the `sc`/event contract, not a privileged `IF`. No syntax change is required.
3. Narrows `Covariant Error Returns` to the single-error case; multi-error methods must use the generic `Error` abstraction and branch via explicit methods (e.g., `IsServiceNotFound()`), not reflection.
4. Adds a current-state note to `Code Scope` that a mid-scope `CF.Return()` (like `return` in other languages) is ordinary control flow, not automatically a smell; what matters is not mixing the concept of scope (`sc` names *what* would run) with the concept of driving control flow (*when*).
