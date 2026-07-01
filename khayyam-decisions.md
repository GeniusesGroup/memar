# Khayyam / Memar — Design Decision Log

**Purpose:** This file is the single source of truth for design decisions made in discussion (across multiple chats) that are not yet reflected in the official documentation (`Khayyam.md`, `Khayyam-rationale.md`, `Khayyam-linter.md`, etc.). Upload this file to Project Knowledge and keep it updated after every chat that produces a real decision, so new chats can be given full context instead of relying on memory.

**How to maintain this file:**
- Add a new entry under the relevant section whenever a discussion reaches a real conclusion (not just an open question).
- Each entry should be self-contained enough to be understood without re-reading the original chat.
- When a decision gets formally written into the actual documentation, mark it `[APPLIED]` and note where, but keep the entry (don't delete) so the reasoning trail is preserved.
- Open questions that did NOT reach a conclusion should go in the "Open Questions" section at the bottom, not be presented as decisions.

---

## 1. Core Philosophy Confirmations

### 1.1 Framework precedes language and OS, not the other way around
The traditional assumption that a development framework lives inside a language/OS is rejected. In Memar, the framework decides the assumptions under which language and OS are developed. Unikernel-style thinking (single address space, no general-purpose OS abstraction layer) is meant to be visible throughout the codebase, not confined to an OS layer — e.g. it shows up in how control flow (`IF`/`ELSE`, async) is pushed out of syntax and into user-space library code.

### 1.2 Safety guarantees in the toolchain are opt-in, not mandatory by definition
Static checks like exhaustive `Deinit()`/`Free()` path coverage are explicitly a **default recommended policy**, not an inherent, unbypassable property of the language the way Rust's borrow checker is unbypassable for producing a binary. An organization may replace or relax this tool. This should be stated explicitly and early in `Khayyam-rationale.md` / `Khayyam-linter.md` so readers don't mistake the default tool's guarantees for a language-level guarantee.
**Status: should be written explicitly into the docs — not yet `[APPLIED]`.**

### 1.3 Most of the documentation is *recommendation*, not *mandate*
Many ideas in the Khayyam docs are presented as "this is how it's easier to achieve X in Khayyam," not "this is the only legal way." Any organization can build its own tools/conventions on top of the same syntax. Where this is unclear in the current text, it needs an explicit disclaimer.
**Status: open — author intends to add clarifying language where ambiguous.**

---

## 2. Closures — Final Decision

**Decision:** Closures and anonymous functions remain excluded from the language.

**Reasoning (revised, final form):**
- The argument is **not** about performance/heap-allocation (a named capsule holding the same references has the same memory-lifetime profile as a closure — this earlier justification in the docs is misleading and should be corrected).
- The real argument is **architectural explicitness**: state that drives behavior must surface as a named, discoverable, single-responsibility domain entity, not be hidden inside an unnamed function.
- Real-world evidence for *why this matters in practice*: in ecosystems where both a closure-based and a capsule/struct-based path exist side-by-side for the same need (e.g. Go's `http.HandleFunc` vs `http.Handle`), developers consistently take the lazier closure path, and encapsulation suffers (e.g. `pattern` ends up living outside the handler capsule in both Go variants). Removing the lazy path entirely is a deliberate forcing function, not an oversight.
- Counter-risk acknowledged: a developer could in theory recreate the same laziness with a throwaway, badly-named single-use capsule. This is treated as a **naming-convention / linter concern**, not a reason to reconsider the syntax decision.

**`[APPLIED candidate]`** — replacement text for the closures section of `Khayyam-rationale.md` was drafted and approved in chat (see prior message in the language-design chat for the exact Markdown block: section "Absence of Closures and Anonymous Functions"). Needs to be pasted into the actual repo file.

---

## 3. Generics — Final Decision

**Decision:** No generics in the syntax; codegen/scaffolding tools generate concrete types (e.g. `ConnectionList`) instead.

**Reasoning (final):**
- Generics create an illusion of correctness. In practice, domain-specific logic that *must* live inside the container (e.g. "no duplicate connections" validation inside `ConnectionList.Insert()`) gets pushed **outside** the encapsulated type when using generic containers, because the generic abstraction has no room for it. This directly breaks encapsulation.
- This is the same root issue as the closures decision: a generic shortcut removes the forcing function that would otherwise make the developer model the domain correctly.

**Open tooling question (not a design flaw, just unresolved mechanics):** are scaffolded concrete-type files (like `connection_list.kh`) committed to version control, or generated fresh on every build? This affects IDE/autocomplete behavior before a build runs. **Status: open, tooling-level, does not affect language design.**

---

## 4. Method Calls Are Statements, Not Chainable Expressions

**Decision confirmed (not a flaw, a deliberate trade-off):** Khayyam method calls cannot be chained (`a.Foo().Bar()` is not legal); every intermediate result needs an explicitly declared variable.

**Reasoning (final, see Section 7 below for the deeper principle this connects to):**
- This is **intentional friction**, working together with the "composition depth as decomposition signal" principle (Section 7): a method/widget body growing long because of many chained/sequential steps is meant to be read as a signal that the responsibility should be split into a separate capsule/widget — not as a cost to be optimized away with chaining syntax.
- This applies uniformly, including to things that *feel* like one operation (e.g. a parse → validate → transform → aggregate pipeline). Each stage is a distinct concern with its own failure mode, and Khayyam intentionally provides no shortcut letting them collapse into one undifferentiated block.

**`[APPLIED candidate]`** — proposed addition to `Khayyam-rationale.md`, new subsection "Composition Depth as a Decomposition Signal" under the Library-Driven Control Flow section. Full Markdown text was drafted and approved in chat. Needs to be pasted into the actual repo file.

---

## 5. Aggregation / DDD-style modeling

**Decision:** Rejected the traditional DDD pattern where a domain "owner" entity (e.g. `User`) directly contains sub-concerns like `username`, `email`, `password` as its fields/methods. In Memar's model, `username`, `email`, etc. are independent capsules; any "User" concept is just one possible *aggregator* among several, and aggregators are not fixed, singular, or domain-owned — they typically form at the composition layer (GUI widgets/pages), but are not *limited* to that layer ("usually" does not mean "only").

**Example used to clarify:** Google-login-based identity vs. local-form-based identity shows why a single fixed `User` aggregator model breaks down — different aggregators are needed for different identity-resolution contexts.

**Corollary (Section 7):** when an aggregator/widget body starts doing more than its single named responsibility (e.g. a "register comment" widget also resolving "who is the current user"), that's the decomposition signal — split into a separate widget that returns just an `ActiveUserID`, and push validation/error-handling for that sub-concern down into that separate widget, not the caller.

---

## 6. Error vs. Log — Boundary Translation Discipline

**Decision:** Treated as a **framework-level rule**, not a language-syntax matter. Drafted as a standalone document `error-log.md`, proposed for the root of the `memar` repo (sibling to `Khayyam.md`, not a subsection of it), because:
- It cannot be mechanically enforced by a structural linter — determining whether an error *should* have been translated at a boundary requires semantic/architectural judgment, which is suited to AI-assisted review, not a structural check.

**Core rule:** Low-level diagnostic errors must be *translated* (captured with context → logged via a dedicated logging capsule → re-expressed as a new, layer-appropriate error) whenever they cross from a diagnostic-detail layer into a decision-only layer (e.g. service layer → GUI). Not every error needs this — only ones crossing such a boundary. Expected/recoverable conditions (e.g. "username taken") don't need logging at all, just normal error return.

**`[APPLIED candidate]`** — full draft already produced as a file (`error-log.md`) in the chat. **Author is reviewing it separately before deciding to merge; not yet finalized.**

---

## 7. Conditional Control Flow Naming (IF/ELSE replacement) — STILL OPEN, NOT FINAL

**Confirmed direction:**
- `IF`/`ELSE` as generic, library-provided functions are not meant to be used everywhere. Developers are encouraged to write domain-specific conditional methods whose name expresses the actual behavior being tested (reinforces "no special-casing of control flow in syntax" — same family of decision as the closures and generics calls above).
- An earlier proposal to make `ELSE` implicit (no explicit reference back to the condition, relying on lexical adjacency to "the nearest unpaired conditional before it") was **rejected** — it would reintroduce implicit/hidden state binding, which conflicts with the same principle used to reject closures. `ELSE`, when used, must keep an explicit reference to the same condition value it pairs with.
- A naming pitfall was identified and should become a general convention: avoid antonym pairs built by negation-prefix (`IfErrorOccurred` / `IfErrorNotOccurred`) because the `Not`/no-`Not` difference is visually easy to miss, both for humans skimming a diff and for AI assistants. Prefer **two etymologically distinct roots** instead (e.g. avoid `X`/`NotX`, prefer `Failed`/`Succeeded`-style pairs).

**Still genuinely unresolved (do NOT treat as decided):**
- Whether the actual success/failure pair of methods should live on the `Error` abstraction itself, or on a more general underlying abstraction (the same one that already backs `IsNull()`/"Behavioral Nullability" in the docs) that `Error` merely implements alongside other nullable/container-like capsules (e.g. an `Optional`-style search result).
- Whether asking an `Error` capsule "what to do on success" is semantically backwards (an error represents failure by identity; pairing it with a success-callback may belong one level up, on the shared presence/absence abstraction instead).
- Candidate naming considered but not committed: `OnFailure`/`OnSuccess` (Error-specific, possibly semantically backwards per above) vs. `OnPresent`/`OnAbsent` (neutral, would work for both Error and general optional/container types) — **no final choice made.**
- How to avoid one-implementation-per-capsule duplication without introducing inheritance: leaning toward "Explicit Delegation Verification" (a one-line delegation call to a shared default implementation, checked/scaffolded by the linter) — consistent with the existing "Rejection of Default Implementations" principle in `Khayyam-linter.md` — but this is a direction, not a finalized mechanism.

**Recommended next step:** this whole topic (final abstraction name, its placement, and its exact method signatures) was identified as being better suited to a separate "Memar standard library design" chat rather than continued inside the core language-syntax chat, since it has moved from "does the language lack syntax" to "what should this library API look like."

---

## 8. Documentation Structure / Process Notes

- `error-log.md` → proposed as new standalone file at repo root, sibling to `Khayyam.md`.
- A future `naming-conventions.md` was discussed as a destination for conventions like "use etymologically distinct roots for antonym method pairs," but Section 7 reframed the IF/ELSE topic specifically as a **standard library abstraction**, not just a naming convention — so it may belong partly in `naming-conventions.md` (the general rule about antonym pairs) and partly in a new standard-library design document (the specific `Error`/presence abstraction itself). Not yet split or finalized.
- Documentation proposals must always be in **English**, Markdown format, ready to paste (this file follows that same rule for any quoted blocks).
- Chat replies stay in whatever language the user uses (Persian in this case); only the documentation deliverables are English.
- General working agreement: sustainable, correct development is treated as a multi-generational, time-intensive effort; proposals should not be rushed or shallow just to save time, since correction costs later are much higher.

---

## 9. Suggested Chat-Splitting Going Forward

To keep each chat focused and within context limits, the following split was proposed:
1. **This chat** — core Khayyam syntax tightening (`Khayyam.md` + `Khayyam-rationale.md`).
2. **Separate chat** — `Khayyam-linter.md` deep dive (e.g. the still-open `PANIC`/diverging-function static-analysis question from Section 1.2-adjacent discussion).
3. **Separate chat** — `Khayyam-runtime.md` / `Khayyam-compiler.md` (scheduler, PANIC/runtime interaction, how Unikernel thinking shows up in the execution model).
4. **Separate chat** — Memar standard library design (the Section 7 open question, plus any future abstractions like `error-log.md`'s logging capsule API).
5. **Separate chat** — `Khayyam-migration_guide.md`, if/when relevant.

---

*Last updated from chat content through: the IF/ELSE conditional-naming discussion (Section 7). Update this footer whenever new entries are added.*
