# Control Flow Changelog

## Changelog

### Initial draft
- Time: unknown (historical import — drafted 2026-06-30 per the document's Start Date; this changelog was created at migration time, so the entry is reconstructed from the former front matter)
- Type: Added
- Cited:
  - [Control Flow in Khayyam](../khayyam/control_flow.md) — Depends_on: this document builds on the precedent set by that document of keeping behavioral policies as ordinary library-driven mechanisms rather than new syntax.
  - [The Error](./error.md) — Depends_on: cited by title in the former front matter as "Error Handling: Library-Driven and Syntax-Free", without a resolvable URI; the reference now targets the canonical Error document. The former front matter's `Extends` and `Conflicts with` fields were empty.
- Contributors: none recorded — the former front matter carried `Author(s): []`; no attribution was reconstructed beyond what the source recorded.

#### What changed
Opened two still-open design questions about library-driven conditional methods: the general naming convention for domain-specific conditional pairs (preferring two etymologically distinct roots over base-plus-negation, against the readability risk of `X`/`NotX` pairs), and the specific naming and placement of the standard library's success/failure branching pair, with four candidate directions explored and none finalized. The former front matter carried an empty `Applied to` field — no propagation was recorded at draft time. The former front matter also contained a malformed duplicate `Citations` key (two separate blocks under the same field name); its content is consolidated into the Cited entries above.

---

### Relocated to `docs/protocols/`
- Time: 2026-09-03T00:00:00Z
- Type: refactor
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — directed, decided
  - [Super Z](../../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — moved

#### What changed
This document moved from `docs/` into the framework-contracts subdirectory (`docs/abstractions/`, since renamed `docs/protocols/` — see the entry below). No content change accompanied the move itself; relative links to khayyam-control_flow.md, khayyam-memory_model.md, and khayyam-polymorphism.md were adjusted for the added depth. The link to the Error document required no path change — both documents now share the directory.

#### Deliberation
- Documents defining a Memar framework-level abstraction or contract get their own subdirectory under `docs/`, so that base documents referencing the abstraction layer do so deliberately rather than by accident; the folder's criterion is implementation-independent *decisions*, not the absence of Khayyam examples, so this Khayyam-flavored document belongs (Omid Hekayati — directed, decided).

---

### Migration to the Explanation-facet template
- Time: 2026-09-03T00:00:00Z
- Type: refactor
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — requested
  - [Super Z](../../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — rewrote

#### What changed
The document previously followed the legacy RFC body structure (`Summary / Motivation / Guide-level explanation / Reference-level explanation / Drawbacks / Rationale and alternatives / Prior art / Unresolved questions / Future possibilities`) with `Applied to`, duplicated `Citations`, and `Author(s)` front matter. Migration mapping, with every load-bearing claim preserved without summarizing: Summary became the Abstract; Motivation kept its role under Introduction; Guide-level explanation split into the two Explanation topics *Two etymologically distinct roots, not base-plus-negation* and *Candidates for the success/failure branching pair* (the candidates, with their rejection reasons, are the second topic's content); the one-line Reference-level explanation ("Not yet finalized — pending resolution") folded into the second topic's lead, since document-wide Unresolved questions carry the same pending state; Drawbacks, Prior art, Unresolved questions, and Future possibilities moved to the document-wide Discussion. The former `Rationale and alternatives` section was a pointer back to the guide-level alternatives, which now live in the candidates topic — nothing was lost by folding it, and no document-wide Rationale entry was added because the document-wide Discussion had no additional rationale content. The former `Applied to`, duplicate `Citations`, and `Author(s)` front-matter fields moved into this file (entries above). No position changed.

#### Deliberation
- Review of the documents touched by the abstractions-directory change for conformance with the current documentation method, applying the progressive-migration rule, was requested (Omid Hekayati — requested).

---

### Retitled to "Control Flow" and widened from a naming convention to the framework-level control-flow protocol
- Time: 2026-09-03T00:00:00Z
- Type: revised
- Cited:
  - [Control Flow in Khayyam](../khayyam/control_flow.md) — Extends_by: that document's Unresolved questions carried the note that the naming-convention discussion was "not yet a separate document"; its library-driven-conditional rationale is the language-level layer beneath this document's protocol layer.
- Propagates to:
  - khayyam-control_flow.md: Done — its Unresolved questions note referencing the "(not yet a separate document)" discussion updated to reference this document by name.
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — decided
  - [Super Z](../../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — rewrote

#### What changed
The document was retitled from "Conditional Method Naming Convention (Presence/Absence Pattern)" to "Control Flow" (ID unchanged — a title change that widens scope at Draft status, not a new document). The Abstract was rewritten to state the widened scope: the framework-level home for Memar's control-flow protocol, with Khayyam's control-flow document as the language-level rationale layer beneath it. The two existing topics (naming convention, branching-pair candidates) survive unchanged in position; a new topic, *Topics to be developed here*, registers the planned growth areas — the conditional-pair protocol as an abstraction contract, iteration/loop-shaped control flow, and halting semantics — without pre-deciding their content. The filename changed from `conditional_naming_convention.md` to `control-flow.md`; this changelog file follows (`control-flow.changelog.md`) and was retitled accordingly.

#### Deliberation
- A document scoped to a naming convention was too narrow for the directory it lives in and for the subject itself (Omid Hekayati — decided).
- The framework-level control-flow protocol — of which naming is one rule — is the real subject, and this document should grow into it the way the other protocol documents are expected to (records today's open questions, develops the topics as they are actually designed) (Omid Hekayati — decided).
- Khayyam's document explains *why* the language has none of these mechanisms; this one owns *what rules* the framework sets (Omid Hekayati — decided).

---

### Absorption of Control Flow in Khayyam
- Time: 2026-09-10T00:00:00Z
- Type: merged
- Cited:
  - [Control Flow in Khayyam] — Depends_on: this entry absorbs that document's design content into this document's body and relocates its negative reasoning into this changelog; the document, its paired changelog, and its handoff are retired and deleted in the same session.
- Propagates to:
  - khayyam/khayyam.md: Done — the grammar-level facts (no flow keywords or logical operators; the inert `sc` primitive) remain there with the Scope pointer retargeted to this document; the principle section's negative-illustration paragraph migrated into this entry.
  - khayyam/compiler.md: Done — the three pointers into the retired document retargeted (language-side reasoning to Khayyam's *The Grammar Refuses Protocol Semantics*; the goto-draft retirement and the design-cost reasoning to this entry; the intrinsics/event contract question already owned by the compiler handoff).
  - khayyam/encapsulation.md, khayyam/metaprogramming.md, khayyam/README.md, protocols/abstraction-implements.md, protocols/README.md: Done — pointers retargeted to this document.
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — decided the merge, the negatives-to-changelog doctrine, and the content destinations
  - [Super Z](../../CONTRIBUTORS.md#super-z) — analyzed, migrated

#### What changed
- The positive design content of the retired document now lives in this document's body: **Library-Defined Control Flow** (the premise, the generic `IF`/`ELSE` form, the preferred domain-specific form with the `OnPresent`/`OnAbsent` worked example, the mechanism summary), **Structured and Unstructured Flow as Libraries** (both paradigms as equal library constructs on the same primitives, substrate-independence), and **Error Propagation** (the framing, the explicit-output declaration, and the No-Hidden-Control-Flow / No-Core-Level-Panics / Linter-Over-Syntax positions). The propagation-mechanisms survey (exceptions, `Result<T,E>`, Go's pair, panic/recover) joined Prior art; the standard-library `GOTO` package and the richer domain-conditional library joined Future possibilities.
- The retired document's handoff lost nothing: the versioned intrinsics/event contract was already owned by the compiler handoff's open question and anticipated work; the conditional-vocabulary naming question and the two further unresolved questions are owned by this document's newly created paired handoff; the error-path naming-and-layering pointer is owned by [The Error](./error.md).
- The error-typing recommendation (single-cause concrete output, multi-cause abstract output) is subsumed by The Error's Multi-cause returns section, which already owns it; no separate statement is kept.
- In the same session the body completed its migration to the three-section skeleton: the content-free Results placeholder was dropped, and the Discussion section retired — the Drawbacks record and the Prior-art surveys are preserved in this entry (below), and the Unresolved questions and Future possibilities moved to the newly created paired handoff ([control-flow.handoff.md](./control-flow.handoff.md)).

#### Migrated reasoning (negative content, recorded here per the negatives-to-changelog doctrine — bodies carry current positive state only)

**The call-site cost of library-defined flow** (from the retired document's Mechanism Summary topic):

Every conditional, even a trivial one, needs an explicit import and a named scope rather than a single keyword and a brace block — more characters at the call site than a keyword-based language, and that much is a plain, honest fact. What it is not is a hidden cost other languages avoid: a built-in `if` looks free at the call site precisely because its design cost was paid once, permanently, inside the compiler, while the convention around it — how it interacts with error handling, whether a check reads as a naked boolean or a named domain condition — is left to diverge silently, unpaid for, between call sites and teams. In Khayyam, once `IF`/`ELSE` or a domain-named pair like `OnPresent`/`OnAbsent` exists in a codebase, every subsequent call site imports that same reference implementation rather than re-deciding the same shape; the up-front verbosity buys one inspectable, swappable answer to "how do we branch here," instead of a keyword whose actual behavior around errors, logging, or domain meaning still gets reinvented ad hoc at every call site anyway.

**The per-file import cost** (from the retired document's Code Scope topic):

Even a basic construct like `if` or `for` requires an explicit import rather than a keyword the compiler already knows — a real, honest one-time cost per file (the `in` statement), and unfamiliar at first for developers used to keyword syntax. What this should not be read to imply is that keyword-based languages avoid an equivalent cost: they pay it once, permanently, inside the compiler's own source, where it cannot be inspected, customized, or upgraded without forking the language itself. Khayyam's version of that same design cost is visible in application code and, once paid by a library author, becomes a stable, shared reference every caller in the codebase imports rather than reinvents.

**The structured-programming debate and built-in keyword instability** (from the retired document's Structured vs Unstructured Programming topic; the first paragraph's historical survey is provenance, not design):

[Structured programming](https://en.wikipedia.org/wiki/Structured_programming) emerged as a reaction to unrestricted [`goto`](https://en.wikipedia.org/wiki/Goto)-based control flow. Dijkstra's influential critique argued that arbitrary jumps make a subroutine's execution path impossible to reason about locally, and proposed replacing them with three composable constructs — sequence, selection (`if`/`else`), and iteration (`for`/`while`) — that keep control flow representable as nested, well-scoped blocks. [Unstructured programming](https://en.wikipedia.org/wiki/Unstructured_programming), built on unrestricted jumps, is closer to the underlying hardware execution model and predates it; it is still how most compiled code looks once structured constructs are lowered to machine instructions.

Most languages designed since resolved this debate once, permanently, in the compiler: structured constructs became reserved keywords, and `goto` was either removed entirely or kept as a discouraged, restricted escape hatch. Khayyam treats this as the wrong place to resolve it. The argument for preferring structured constructs in most application code is not in dispute here — it is an argument about what most programs should look like, not about what a compiler is capable of expressing. Baking that preference into the grammar as privileged keywords does not make unstructured control flow disappear from the domains that genuinely rely on it — state machines, coroutine schedulers, generated code, interpreter dispatch loops — it just forces those domains to route around the language, or wrap `goto` in a permanent warning label, forever.

Built-in syntax is not immune to instability either: Go's `for`-loop variable-capture semantics changed in Go 1.22, silently altering the behavior of existing code that relied on the previous per-loop (rather than per-iteration) scoping — a reminder that a compiler-owned keyword can still change meaning out from under a codebase whenever its authors decide to revisit it. A library-owned control-flow method's behavior, by contrast, only changes when the codebase's own dependency version does, under that codebase's own control.

The drawback of this model is narrower than it first looks, but not a fake one. It is not that Khayyam creates more room for developers to diverge in style than a language with a built-in `if` does — every language has exactly as much room for that (guard clauses vs. nested `if`, early return vs. exception-driven flow, and so on); it is just invisible at the call site, because the keyword itself never changes no matter how differently it is used. What Khayyam's model changes is *where* that divergence becomes visible: a newcomer has to identify which control-flow library a file is importing before they can read it fluently, rather than recognizing `if` on sight regardless of house style. That is real onboarding friction, and it is exactly why an organization is expected to standardize on one control-flow library per project via its Linter — the same way it already standardizes on one logging library or one HTTP client, rather than leaving that choice to sit in the language.

**The Linter-dependence drawback** (from the retired document's Error Propagation topic):

Without compiler-enforced syntax (like Rust's `?` or Go's required `if err != nil` pattern that at least makes ignoring an error visually obvious), the actual discipline of "every error gets handled" depends entirely on Linter configuration and developer diligence — see [Memory Model](../khayyam/memory_model.md) for the equivalent trade-off in memory safety. A team running a weak or disabled Linter could silently drop errors with no language-level safety net at all.

**Covariant Error Returns** (from the same topic; subsumed by The Error's Multi-cause returns, which already owns the single-cause-concrete / multi-cause-abstract rule — recorded here so the position is not lost):

COVARIANT (subsumed by error.md Multi-cause returns): - **Covariant Error Returns:** a method may declare its error output as the generic `Error` abstraction, or as a specific concrete error capsule type directly (e.g. `(err ErrServiceNotFound)` instead of `(err Error)`), as long as that concrete type itself implements the `Error` abstraction. This is not considered a violation of the abstraction's contract, and gives callers static, compile-time knowledge of exactly which error type to expect without any runtime type-narrowing/reflection mechanism being required in the language for that single-error case. For methods with *multiple* possible error types, the output must be the generic `Error` abstraction; callers then branch via explicit methods on the error (e.g., `err.IsServiceNotFound()(isNotFound)` or domain-specific `OnPresent`/`OnAbsent` checks), not via type-switch/reflection. This distinction — single-error covariant vs. multi-error abstract — was missing in an earlier draft.

#### Carried audit record (from the retired document's changelog)

The retired document's changelog stays recoverable in git history; its final-state audit records are carried here verbatim so nothing is lost. The two body cross-references inside them are retargeted to this document's sections.

#### Considered and not done
- **Structured-only, the mainstream default (rejected as a language-level mandate; migrated from the `Structured vs Unstructured Programming` topic's retired Rationale and alternatives)**: removing `goto`-equivalents from the grammar entirely, as most modern languages do, was rejected because it permanently forecloses the domains that legitimately need unrestricted jumps, forcing them to simulate `goto` with labeled loops, exception-based jumps, or other awkward workarounds.
- **Unstructured-only / goto-first (rejected; migrated from the same topic)**: no serious contemporary language proposes this, and Khayyam does not either; it is listed only to make clear that Khayyam is not reviving unstructured programming as a preferred style, merely refusing to forbid it at the language level.
- **Structured by convention, not by keyword (chosen; migrated from the same topic as the recorded decision)**: neither model is privileged in the grammar; an organization's Linter is expected to enforce whichever convention that organization prefers, exactly as it would enforce any other house style.
- **Domain-named conditional methods as the actual default reach, not a stylistic footnote (chosen alongside `IF`/`ELSE`; migrated from the same topic)**: not a third position in the structured-vs-unstructured debate so much as a demonstration that the debate's own vocabulary (`if`, `goto`) is too narrow to describe the best available option once a domain is stable enough to name its own conditions — a check like `saveErr.OnAbsent(...)` is neither a generic `if` nor a `goto`, and reads better than either; see [Domain-Specific Conditional Methods](#the-preferred-form-domain-specific-conditional-methods) in the body.
- **Built-in control-flow keywords, the conventional approach (rejected; migrated from the `Code Scope` topic's retired Rationale and alternatives)**: would embed specific control-flow semantics into the language, preventing frameworks and organizations from defining their own control-flow policies (e.g., mandatory error checking on each iteration, or logging on each branch).
- **Code scope as a library-only feature without language support (considered, not chosen; migrated from the same topic)**: without the `sc` type, libraries would need to use capsules for control flow, losing the semantic distinction between "a data capsule" and "a control-flow scope."
- **A larger compiler-provided intrinsic set, closer to a mini standard library (considered, not chosen; migrated from the `Execution Primitives: The Compiler's Role` topic's retired Rationale and alternatives)**: would shrink the bootstrapping gap for common cases, but reintroduces the core problem this document exists to avoid — the compiler quietly acquiring opinions about which control-flow shapes are "common" or "standard," permanently, for every program that will ever run on it.
- **No intrinsics at all, everything reconstructed from raw hardware jumps by each library (rejected; migrated from the same topic)**: would make every control-flow library reimplement the same low-level, error-prone plumbing, with no consistency guarantee across libraries.
- **Keeping `if`/`else`/`for` as compiler keywords, the universal default in other languages (rejected; migrated from the `Library-Defined Control Flow` topic's retired Rationale and alternatives)**: rejected not because it is free — it is not, the same design decisions still have to be made, just once, by the language's original authors, and then frozen for every program that will ever run on it — but because it permanently couples one specific control-flow paradigm to the compiler, leaving no path for an organization to govern, extend, or replace it without forking the language.
- **`try-catch`/exception model (rejected; migrated from the `Error Propagation` topic's retired Rationale and alternatives)**: rejected for hiding control flow in implicit stack unwinding.
- **Rust's `?` operator (rejected; migrated from the same topic)**: rejected for binding the compiler to one specific result type and for hiding an early return behind an operator.
- **Go's mandatory verbose boilerplate (rejected; migrated from the same topic)**: rejected as unnecessary ceremony once a strict Linter can enforce the same discipline without forcing every call site to spell it out manually.
- **Built-in, compiler-special-cased control-flow syntax as a category (rejected; migrated from the retired document-level Rationale and alternatives)**: every mechanism in this document traces to this same rejected alternative — keywords for branching/looping/jumping, an exception or `?`-operator mechanism for error propagation — all rejected for the same structural reason: such syntax permanently couples one paradigm to the compiler, leaving no way for an organization to govern, extend, or replace it without forking the language. That coupling is not merely theoretical — built-in syntax can still change meaning out from under a codebase whenever a language's own authors revisit it (see the Go `for`-loop variable-capture change under [Structured vs Unstructured Programming](#structured-and-unstructured-flow-as-libraries)); the difference is that such a change sits entirely outside the codebase's control, whereas a library's behavior only changes when the codebase's own dependency version does. Library-provided methods, by contrast, can be swapped, extended, linted, or restricted entirely at the organizational level — including by choosing to reintroduce something that looks and behaves like a keyword-based `if`, if that is what a team prefers, as long as it is still built from `sc` and the compiler's execution primitives rather than added to the grammar.
- **Document-level drawback record (migrated from the retired document-level Drawbacks section)**: together, the rules mean that every branch, every loop, every jump, and every error-propagation path in Khayyam is an explicit, named, importable method call rather than built-in syntax — more characters to type than virtually any mainstream language for the simplest possible program logic, and that much is a plain fact rather than a trade-off in disguise. What should not be read into it is that the equivalent design cost doesn't exist in languages with built-in keywords: it does, it is simply paid once by the language's own authors, hidden inside the compiler, and frozen for the language's entire lifetime rather than owned by the codebase using it. Khayyam's version of the cost is paid once too — by whoever writes the `IF`/`ELSE` or domain-named library a project settles on — and after that, every call site imports the same answer rather than re-deciding it. This is accepted as the price of keeping that design cost visible, inspectable, and owned by the codebase, rather than owned once, invisibly, and permanently, by the compiler.

#### Related work
- **`Structured vs Unstructured Programming`:** Dijkstra's "Go To Statement Considered Harmful" is the canonical argument for structured programming; Knuth's "Structured Programming with go to Statements" is the canonical rebuttal, arguing that disciplined, restricted use of `goto` is sometimes clearer than the structured alternative. Most mainstream languages since have sided fully with the structured camp at the grammar level; Khayyam's position is closer to Knuth's — that the discipline matters more than the mechanism — but pushes it further by refusing to encode either side into the compiler. (Migrated from the topic's retired Prior art; the block's Go 1.22 loop-variable-capture example was folded into the body as premise evidence — see What changed.)
- **`Code Scope`:** Lisp's macro-based control flow and Forth's immediate words are distant precedents for library-defined control flow. No mainstream language provides `sc`-style scope abstractions as a first-class type. (Migrated from the topic's retired Prior art)
- **`Execution Primitives: The Compiler's Role`:** This mirrors how most compiled languages already treat their own backends: `if`/`while`/`for` all lower to the same small set of conditional-jump instructions at the machine-code level. Khayyam is unusual only in exposing that lowering boundary to library authors directly, rather than hiding it entirely behind compiler-owned keywords. (Migrated from the topic's retired Prior art; the lowering parallel is also stated as premise in the body's first paragraph of that topic)
- **`Library-Defined Control Flow`:** No mainstream general-purpose language fully removes conditional/loop keywords from its grammar; Forth-family languages and some Lisp dialects come closest by treating control flow as ordinary words/forms rather than special syntax. (Migrated from the topic's retired Prior art)
- **Document-level:** No mainstream general-purpose language fully removes both control-flow keywords and an exception/result-based error mechanism from its grammar. Forth-family languages and some Lisp dialects come closest for control flow itself, treating conditionals and loops as ordinary words/forms rather than special syntax; Go's explicit `(value, error)` returns are the closest mainstream precedent for treating error propagation as an ordinary value rather than a dedicated keyword or operator. Khayyam is unusual in making library-defined abstractions the *only* available path for both, rather than a convention layered on top of keywords and operators that still exist underneath. (Migrated from the retired document-level Prior art)


#### Drawbacks (from the retired body Discussion)

Any chosen pair adds two more standard method names developers must learn and use correctly across the entire `Error`-adjacent surface of the standard library; getting the abstraction placement wrong (see [Unresolved questions](#unresolved-questions)) risks duplicate, slightly-divergent implementations across many capsules.

#### Related work (from the retired body Discussion)

Other languages answer that same question — how does execution continue after failure? — with different mechanisms, each a different point in the same trade-off space between visibility, verbosity, and compiler involvement: exceptions unwind the call stack via `throw`/`catch` (Java, Python, JS); Rust's `Result<T, E>` makes failure an ordinary return value inspected via pattern matching, with `?` as sugar for propagating it upward; Go returns an explicit `(value, error)` pair checked with `if err != nil`; and a panic/recover pair combines an abrupt halt with an opt-in unwinding mechanism (Go, and Khayyam's own `PANIC()`). Khayyam has no `try-catch`, `panic`/`recover`, or `?`-operator syntax of its own. Errors are always ordinary, explicit output values (capsules implementing the `Error` abstraction), and abrupt halts are an ordinary standard-library method call (e.g. `PANIC()`), not a compiler directive — closest in spirit to Go's explicit returns, but with the "did you check it" discipline shifted from mandatory boilerplate to the Linter.

This problem closely parallels `Result`/`Option` combinator naming in Rust (`.is_ok()`, `.map_err()`, `.unwrap_or_else()`) and JavaScript Promise's `.then()`/`.catch()` pairing, both of which were considered as background context but not adopted directly, since Khayyam has neither a generic `Result<T, E>` type ([Khayyam polymorphism](../khayyam/polymorphism.md)) nor Promise-style chaining ([Composition Depth as a Decomposition Signal](../khayyam/method.md#composition-depth-as-a-decomposition-signal-no-expression-chaining) rejects expression chaining).

---

### Candidate rejections restated language-neutrally; closures parallel demoted to instance
- Time: 2026-09-23T07:07:01Z
- Type: Fixed
- Cited:
  - [Khayyam](../khayyam/khayyam.md) — Reference: instance of the missing-package-qualification gap, and source of the type-level (`tp.Create()`) resolution form named in the candidate.
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — decided
  - [Mimo](../../CONTRIBUTORS.md#mimo) (mimo-v2.6-flash via OpenCode) — applied

#### What changed
- The `IfFailed`/`IfSucceeded` rejection now leads with the language-neutral reason: a global function name carries no inherent domain context without an explicit receiver. Khayyam's lack of a package/namespace concept follows afterward as that language's instance of the gap, and the replacement direction — type-level (static) invocation, a method defined without `self` invoked on the type identifier — is recorded as where the global-function question closed. Naming the pair itself stays open.
- The `ELSE` paragraph now states the hidden-state-binding principle at protocol level: a construct must carry its dependencies in its own arguments rather than reach for state implied by position or surrounding text. Khayyam's rejection of closures is kept as an instance of that rule, explicitly not its authority.

#### Deliberation
- A protocol-level rule must not take a Khayyam-specific fact as its reason; an instance link after a language-neutral reason is legitimate (Omid Hekayati — decided).
- The global-function-without-receiver topic is closed — rejected — with type-level invocation as its recorded resolution (Omid Hekayati — decided).
