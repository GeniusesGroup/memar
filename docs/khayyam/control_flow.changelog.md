# Control Flow in Khayyam Changelog

## Changelog

### Created by merging the Library-Driven Control Flow and Domain-Driven Arithmetic documents
- Time: 2026-07-29T00:00:00Z (approximated from Start Date)
- Type: Added
- Cited:
  - [Khayyam - Programming Language](./khayyam.md) — Reference: The canonical specification defines the `sc` subtype and the `in` import mechanism that library-provided control-flow methods are built on.
  - [Encapsulation in Khayyam](./khayyam-encapsulation.md) — Depends_on: Library-Defined Control Flow's ELSE-must-reference-its-condition rule is a direct application of that document's Closures as Implicit Capsule Syntax topic (no implicit binding to 'whatever came before').
  - [Method in Khayyam](./khayyam-method.md) — Depends_on: Control flow (IF/ELSE, OnPresent/OnAbsent) is built entirely from ordinary method calls, and inherits that document's pass-by-reference, explicit-output-variable, no-chaining model rather than introducing any dedicated call syntax of its own.
  - [The Error](./protocols/error.md) — Depends_on: Error Propagation treats `Error` (and its concrete subtypes) as the value being propagated; what the abstraction itself is, and what contract it must satisfy, is defined there, not here.
- Propagates to:
  - khayyam-encapsulation.md: Done — the Code Scope topic was removed from that document's Explanation section and relocated into this document as part of the same merge (see its changelog).
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — claimed
  - [ChatGPT](../CONTRIBUTORS.md#chatgpt) (Unspecified custom GPT; exact underlying model not recorded — fill in if known; high effort) — proposed
  - [Claude](../CONTRIBUTORS.md#claude) (claude-sonnet-5, high effort) — rewrote

#### What changed
- Initial creation: this document was created by merging the standalone "Library-Driven Control Flow" and "Domain-Driven Arithmetic: Operator Elimination and Compile-Time Formula Evaluation" documents, together with the "Code Scope" topic relocated from `khayyam-encapsulation.md`, into the current Explanation-facet specification. Code scopes are the primitive `IF`/`ELSE`/`LOOP` are built on, not a capsule-level concern.
- Both standalone document files, and the Code Scope section in `khayyam-encapsulation.md`, have been retired/removed accordingly.
- The agreed architectural review was applied: the compiler-exposes-primitives-only conclusion was promoted into the Abstract as a stated outcome; a new Execution Primitives topic was split out of Library-Defined Control Flow (renamed Library-Defined Control Flow); Structured Programming was expanded into a full Structured vs Unstructured Programming topic with its own Discussion bundle; Error Handling was renamed and reframed as Error Propagation; and residual Domain-Driven Arithmetic content (comparison-operator examples aside) was removed following its extraction to khayyam-variable.md.

#### Deliberation
- The original design decisions for library-driven control flow, the elimination of logical/arithmetic operators, and the code scope (`sc`) mechanism in the canonical Khayyam specification were claimed (Omid Hekayati — claimed).
- Extracting Domain-Driven Arithmetic out of this document was proposed (ChatGPT — proposed).
- Reframing Error Handling as Error Propagation — a form of control flow rather than an unrelated concern — was proposed (ChatGPT).
- Separating what the compiler provides (execution primitives) from what libraries build on top of it was proposed (ChatGPT).
- Reframing Structured Programming historically rather than as an unquestioned default was proposed (ChatGPT).
- The architectural review was agreed between the author and ChatGPT (Omid Hekayati, ChatGPT).

### Architectural rescoping (2026-07-31)
- Time: 2026-07-31T00:00:00Z (date recorded in the source listing; time approximated)
- Type: Changed
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — argued
  - [ChatGPT](../CONTRIBUTORS.md#chatgpt), [Claude](../CONTRIBUTORS.md#claude) — reviewed

#### What changed
- `Domain-Driven Arithmetic` was extracted out of this document entirely by the author himself, to be treated separately in `khayyam-variable.md` (Omid Hekayati — argued).
- The residual comparison/arithmetic-operator references, the `MathEval` compile-time-type-checking Unresolved question, and the corresponding Future-possibilities item were removed here accordingly (see the companion note handed off alongside this revision for what to check against the target document).
- The document's core conclusion — that the compiler exposes only execution primitives and privileges no control-flow model — was promoted into the Abstract as a stated outcome rather than left implicit or treated as the document's starting motivation.
- The former `Structured programming` stub was expanded into a full `Structured vs Unstructured Programming` topic with its own Discussion bundle, reframing the historical goto-versus-structured debate as a question of what a compiler should privilege, not what a compiler should permit.
- A new `Execution Primitives: The Compiler's Role` topic was split out of the former `Library-Driven Control Flow` topic (itself renamed `Library-Defined Control Flow`) to keep "what the compiler provides" separate from "what libraries build on top of it."
- `Error Handling: Library-Driven and Syntax-Free` was renamed `Error Propagation` and reframed as one instance of control flow rather than an unrelated concern, with a short comparison of propagation strategies used by other languages (exceptions, `Result` types, Go-style returns, panic/recover) added to its opening.

#### Deliberation
- The rescoping was reviewed dialectically with ChatGPT and Claude (ChatGPT, Claude — reviewed).

### Drawback-framing correction (2026-07-31)
- Time: 2026-07-31T00:00:00Z (date recorded in the source listing; time approximated)
- Type: Fixed
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — corrected
  - [Claude](../CONTRIBUTORS.md#claude) (claude-sonnet-5) — rewrote

#### What changed
- Every Drawbacks/Rationale passage touching this comparison (`Structured vs Unstructured Programming`, `Code Scope`, `Execution Primitives`, `Library-Defined Control Flow`, and the document-wide Discussion) was rewritten to state the honest, narrower residual cost (onboarding-recognition friction, ecosystem-bootstrapping maturity, or plain call-site character count) instead of an implied "other languages don't pay this" framing, and to credit domain-named conditionals as a genuine third option rather than a footnote to `IF`/`ELSE`.

#### Deliberation
- Several Drawbacks/Rationale passages were flagged as implicitly comparing Khayyam's *visible* design costs (imports, ceremony, more characters at a call site) against other languages' costs as if the latter were zero, when in fact those languages pay an equivalent design cost once, invisibly, inside the compiler — frozen for the language's lifetime rather than owned and adjustable by the codebase using it (Omid Hekayati — corrected).
- It was also noted that `Structured vs Unstructured Programming` implied only two paradigms (structured, unstructured) existed, when `Domain-Specific Conditional Methods` demonstrates a third — one that is frequently the *better* option, not a stylistic fallback (Omid Hekayati).

### Openness and scope clarifications (2026-07-31)
- Time: 2026-07-31T00:00:00Z (date recorded in the source listing; time approximated)
- Type: Changed
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — clarified
  - [Claude](../CONTRIBUTORS.md#claude) (claude-sonnet-5) — rewrote

#### What changed
- The "structured / unstructured / domain-named" paradigm list was made explicitly non-exhaustive and scoped to today's conventional, classical-hardware execution model — nothing in Khayyam couples a control-flow model to a particular computation substrate, so a fundamentally different future paradigm (e.g. quantum computing's superposition-based branching) can be added as another library without touching the language, and this is now stated directly in both the Abstract and `Structured vs Unstructured Programming`.
- The residual bootstrapping-cost Drawback under `Execution Primitives`, and two "open cross-document question" phrasings that implicitly demanded an unwritten companion document, were softened to avoid creating any obligation toward other documents or overstating the difficulty of reaching high productivity.
- The Abstract now also explicitly acknowledges that method invocation is itself a control-flow event, and states — rather than leaves implicit — that Khayyam deliberately treats Method as a more foundational Type covered elsewhere, not as an oversight in this document's scope.

#### Deliberation
- That the paradigm list be made explicitly non-exhaustive was requested (Omid Hekayati — clarified).
- A Drawback about divergent `IF` libraries across projects was proposed; the author declined to add it (Omid Hekayati — clarified).

#### Considered and not done
- **A Drawback about divergent `IF` libraries across projects (not added)**: per the author's judgment that this is not a realistic failure mode.

### Completed migration to the Explanation-facet specification
- Time: 2026-08-26T00:00:00Z
- Type: refactor
- Cited:
  - [Documentation](./documentation.md) — Reference: facet meta-layer defining Explanation/Practice/Changelog.
  - [Documentation — Explanation](./documentation-explanation.md) — Depends_on: governing structure the base document was brought fully in line with.
  - [Documentation — Changelog](./documentation-changelog.md) — Depends_on: entry structure used for this companion file.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — requested
  - [Super Z](../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — migrated

#### What changed
- The migration to the Explanation-facet specification was completed — structural completion and provenance relocation per that specification (this document already followed most of the current structure since its creation).
- All remaining provenance was relocated out of the base document: front-matter `Applied to`, `Citations`, and `Contributors` moved into this file's entries above; the body's former `## Change Rationale` section became the dated entries above.
- The empty `Results` section received the standard placeholder sentence used across sibling documents.
- One broken cross-reference was repaired — the Motivation linked `./khayyam-method.md#method-as-callable-capsule`, an anchor that no longer exists in `khayyam-method.md` because the mechanical signature spec now lives under that document's "Method Structure" topic, so the link label and target were updated accordingly.
- No prose was summarized or shortened anywhere in the base document; no design decision changed.

#### Deliberation
- The migration of this document to the latest documentation method was requested, without summarizing (Omid Hekayati — requested).

---

### Correct examples and clarify the compiler-event contract; narrow covariant claim; clarify mid-scope exits
- Time: 2026-08-27T00:00:00Z
- Type: Fixed
- Cited:
  - [Method in Khayyam](./khayyam-method.md) — Depends_on: `sc` entry/exit and the `IF`/`ELSE` exclusivity are learned from `sc` events
  - [The Error](./protocols/error.md) — Depends_on: single-error vs. multi-error channel typing
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — requested
  - [Super Z](../CONTRIBUTORS.md#super-z) — rewrote

#### What changed
Four focused fixes, each with the full historical path now preserved here (base document carries only the corrected current state):

1. Replaces the `err = ErrPaymentTemporarilyUnavailable` statement in the payment example (which used `=`, a token that does not exist in Khayyam) with explicit `CopyFrom` calls on a named intermediate error variable.
2. Clarifies `Execution Primitives: The Compiler's Role` to state that the compiler is an independent application emitting `sc` entry/exit and jump events to which DAA/linter subscribe; third-party CF libraries target the `sc`/event contract, not a privileged `IF`. No syntax change is required.
3. Narrows `Covariant Error Returns` to the single-error case; multi-error methods must use the generic `Error` abstraction and branch via explicit methods (e.g., `IsServiceNotFound()`), not reflection.
4. Adds a current-state note to `Code Scope` that a mid-scope `CF.Return()` (like `return` in other languages) is ordinary control flow, not automatically a smell; what matters is not mixing the concept of scope (`sc` names *what* would run) with the concept of driving control flow (*when*).

#### Deliberation
- That the compiler is an independent app emitting events was clarified (Omid Hekayati — requested).
- That type-as-argument need not be restricted at language level was clarified (Omid Hekayati — requested).
- That `CF.Return`/`Break` mid-scope is not automatically a smell was clarified (Omid Hekayati — requested).

---

### Second migration wave: `## Discussion` retired per the finalized method
- Time: 2026-09-08T00:00:00Z
- Type: refactor
- Propagates to:
  - khayyam-control_flow.handoff.md: Created - open questions and anticipated work moved there.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) - requested
  - [OpenCode](../CONTRIBUTORS.md#opencode) (qwen3.8-flash) - moved

#### What changed
- The body retains only the fixed top-level sections `Abstract`, `Introduction`, `Explanation`, `Results`; the document-level `## Discussion` is gone.
- All five topic-level `#### Discussion` wrappers are gone — `Structured vs Unstructured Programming`, `Code Scope`, `Execution Primitives: The Compiler's Role`, `Library-Defined Control Flow`, and `Error Propagation`.
- Drawbacks that are current-state claims about the design's cost are folded inline into their topics: the where-divergence-becomes-visible onboarding friction and the per-project Linter standardization expectation (Structured vs Unstructured Programming); the explicit-import one-time-per-file cost and where keyword languages pay the equivalent cost (Code Scope); the first-control-flow-package bootstrapping cost (Execution Primitives); the call-site verbosity and its once-per-codebase inspectable answer (Library-Defined Control Flow); the full dependence of error-handling discipline on Linter configuration and developer diligence (Error Propagation). The `Code Scope` wrapper's mid-scope `CF.Return()`/`CF.Break()` clarification — a current-state statement of what is and is not a smell — is likewise folded inline.
- The Go 1.22 loop-variable-capture example is folded inline into the `Structured vs Unstructured Programming` topic as premise evidence for the claim that a compiler-owned keyword can change meaning out from under a codebase — a claim the body's folded Execution Primitives drawback cross-references.
- The retired `Unresolved questions` — the unpublished, versioned `sc`/jump-intrinsic and event contract, and the standard conditional-method vocabulary including the presence/absence pair naming on `Error`-like capsules — are now the paired handoff's `Open Questions`, together with the `Error Propagation` pointers to the framework-level error translation/logging question (owned by [The Error](./protocols/error.md)) and the conditional-method naming question (owned by the [Control Flow](./protocols/control-flow.md) protocol document); the retired `Future possibilities` items — the standard-library `GOTO`/jump package, the formal intrinsic + event specification, and the richer domain-flavored conditional/error-propagation library — are its `Anticipated Work`. The "None at this time" and "None recorded yet" placeholders were dropped as content-free.
- The `Error Propagation` topic's retired `Prior art` survey (Rust's `Result`/`?`, Go's explicit `(value, error)` returns, exception-based models; closest in spirit to Go with enforcement moved to tooling) is dropped as graduated: the body's `Error Propagation` topic already states the full comparison in its second paragraph and both the closest-to-Go and the discipline-shift-to-Linter claims in its third.
- The retired `Rationale and alternatives` blocks and the document-level Drawbacks record are preserved below under `Considered and not done`, and the retired per-topic and document-level `Prior art` surveys under `Related work`.
- Dangling references repaired in the body: the payment example's error-path comment and the presence/absence naming note now point to the paired handoff's Open Questions, and the Methodology's pointer to "this document's Discussion sections" now points to this changelog.

#### Considered and not done
- **Structured-only, the mainstream default (rejected as a language-level mandate; migrated from the `Structured vs Unstructured Programming` topic's retired Rationale and alternatives)**: removing `goto`-equivalents from the grammar entirely, as most modern languages do, was rejected because it permanently forecloses the domains that legitimately need unrestricted jumps, forcing them to simulate `goto` with labeled loops, exception-based jumps, or other awkward workarounds.
- **Unstructured-only / goto-first (rejected; migrated from the same topic)**: no serious contemporary language proposes this, and Khayyam does not either; it is listed only to make clear that Khayyam is not reviving unstructured programming as a preferred style, merely refusing to forbid it at the language level.
- **Structured by convention, not by keyword (chosen; migrated from the same topic as the recorded decision)**: neither model is privileged in the grammar; an organization's Linter is expected to enforce whichever convention that organization prefers, exactly as it would enforce any other house style.
- **Domain-named conditional methods as the actual default reach, not a stylistic footnote (chosen alongside `IF`/`ELSE`; migrated from the same topic)**: not a third position in the structured-vs-unstructured debate so much as a demonstration that the debate's own vocabulary (`if`, `goto`) is too narrow to describe the best available option once a domain is stable enough to name its own conditions — a check like `saveErr.OnAbsent(...)` is neither a generic `if` nor a `goto`, and reads better than either; see [Domain-Specific Conditional Methods](./khayyam-control_flow.md#the-preferred-form-domain-specific-conditional-methods) in the body.
- **Built-in control-flow keywords, the conventional approach (rejected; migrated from the `Code Scope` topic's retired Rationale and alternatives)**: would embed specific control-flow semantics into the language, preventing frameworks and organizations from defining their own control-flow policies (e.g., mandatory error checking on each iteration, or logging on each branch).
- **Code scope as a library-only feature without language support (considered, not chosen; migrated from the same topic)**: without the `sc` type, libraries would need to use capsules for control flow, losing the semantic distinction between "a data capsule" and "a control-flow scope."
- **A larger compiler-provided intrinsic set, closer to a mini standard library (considered, not chosen; migrated from the `Execution Primitives: The Compiler's Role` topic's retired Rationale and alternatives)**: would shrink the bootstrapping gap for common cases, but reintroduces the core problem this document exists to avoid — the compiler quietly acquiring opinions about which control-flow shapes are "common" or "standard," permanently, for every program that will ever run on it.
- **No intrinsics at all, everything reconstructed from raw hardware jumps by each library (rejected; migrated from the same topic)**: would make every control-flow library reimplement the same low-level, error-prone plumbing, with no consistency guarantee across libraries.
- **Keeping `if`/`else`/`for` as compiler keywords, the universal default in other languages (rejected; migrated from the `Library-Defined Control Flow` topic's retired Rationale and alternatives)**: rejected not because it is free — it is not, the same design decisions still have to be made, just once, by the language's original authors, and then frozen for every program that will ever run on it — but because it permanently couples one specific control-flow paradigm to the compiler, leaving no path for an organization to govern, extend, or replace it without forking the language.
- **`try-catch`/exception model (rejected; migrated from the `Error Propagation` topic's retired Rationale and alternatives)**: rejected for hiding control flow in implicit stack unwinding.
- **Rust's `?` operator (rejected; migrated from the same topic)**: rejected for binding the compiler to one specific result type and for hiding an early return behind an operator.
- **Go's mandatory verbose boilerplate (rejected; migrated from the same topic)**: rejected as unnecessary ceremony once a strict Linter can enforce the same discipline without forcing every call site to spell it out manually.
- **Built-in, compiler-special-cased control-flow syntax as a category (rejected; migrated from the retired document-level Rationale and alternatives)**: every mechanism in this document traces to this same rejected alternative — keywords for branching/looping/jumping, an exception or `?`-operator mechanism for error propagation — all rejected for the same structural reason: such syntax permanently couples one paradigm to the compiler, leaving no way for an organization to govern, extend, or replace it without forking the language. That coupling is not merely theoretical — built-in syntax can still change meaning out from under a codebase whenever a language's own authors revisit it (see the Go `for`-loop variable-capture change under [Structured vs Unstructured Programming](./khayyam-control_flow.md#structured-vs-unstructured-programming)); the difference is that such a change sits entirely outside the codebase's control, whereas a library's behavior only changes when the codebase's own dependency version does. Library-provided methods, by contrast, can be swapped, extended, linted, or restricted entirely at the organizational level — including by choosing to reintroduce something that looks and behaves like a keyword-based `if`, if that is what a team prefers, as long as it is still built from `sc` and the compiler's execution primitives rather than added to the grammar.
- **Document-level drawback record (migrated from the retired document-level Drawbacks section)**: together, the rules mean that every branch, every loop, every jump, and every error-propagation path in Khayyam is an explicit, named, importable method call rather than built-in syntax — more characters to type than virtually any mainstream language for the simplest possible program logic, and that much is a plain fact rather than a trade-off in disguise. What should not be read into it is that the equivalent design cost doesn't exist in languages with built-in keywords: it does, it is simply paid once by the language's own authors, hidden inside the compiler, and frozen for the language's entire lifetime rather than owned by the codebase using it. Khayyam's version of the cost is paid once too — by whoever writes the `IF`/`ELSE` or domain-named library a project settles on — and after that, every call site imports the same answer rather than re-deciding it. This is accepted as the price of keeping that design cost visible, inspectable, and owned by the codebase, rather than owned once, invisibly, and permanently, by the compiler.

#### Related work
- **`Structured vs Unstructured Programming`:** Dijkstra's "Go To Statement Considered Harmful" is the canonical argument for structured programming; Knuth's "Structured Programming with go to Statements" is the canonical rebuttal, arguing that disciplined, restricted use of `goto` is sometimes clearer than the structured alternative. Most mainstream languages since have sided fully with the structured camp at the grammar level; Khayyam's position is closer to Knuth's — that the discipline matters more than the mechanism — but pushes it further by refusing to encode either side into the compiler. (Migrated from the topic's retired Prior art; the block's Go 1.22 loop-variable-capture example was folded into the body as premise evidence — see What changed.)
- **`Code Scope`:** Lisp's macro-based control flow and Forth's immediate words are distant precedents for library-defined control flow. No mainstream language provides `sc`-style scope abstractions as a first-class type. (Migrated from the topic's retired Prior art)
- **`Execution Primitives: The Compiler's Role`:** This mirrors how most compiled languages already treat their own backends: `if`/`while`/`for` all lower to the same small set of conditional-jump instructions at the machine-code level. Khayyam is unusual only in exposing that lowering boundary to library authors directly, rather than hiding it entirely behind compiler-owned keywords. (Migrated from the topic's retired Prior art; the lowering parallel is also stated as premise in the body's first paragraph of that topic)
- **`Library-Defined Control Flow`:** No mainstream general-purpose language fully removes conditional/loop keywords from its grammar; Forth-family languages and some Lisp dialects come closest by treating control flow as ordinary words/forms rather than special syntax. (Migrated from the topic's retired Prior art)
- **Document-level:** No mainstream general-purpose language fully removes both control-flow keywords and an exception/result-based error mechanism from its grammar. Forth-family languages and some Lisp dialects come closest for control flow itself, treating conditionals and loops as ordinary words/forms rather than special syntax; Go's explicit `(value, error)` returns are the closest mainstream precedent for treating error propagation as an ordinary value rather than a dedicated keyword or operator. Khayyam is unusual in making library-defined abstractions the *only* available path for both, rather than a convention layered on top of keywords and operators that still exist underneath. (Migrated from the retired document-level Prior art)
