# Agency in Khayyam Changelog

## Changelog

### Initial draft, as khayyam-concurrency.md
- Time: 2026-06-30T00:00:00Z
- Type: Added
- Cited:
  - [Control Flow in Khayyam](./control_flow.md) — Depends_on: this document builds on the precedent set by that document of keeping behavioral policies as ordinary library-driven mechanisms rather than new syntax.
  - [Framework](../framework.md) — Depends_on.
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — claimed, argued

#### What changed
- Established that Khayyam embeds no concurrency model into its syntax: no `go`/`async`/`await` keywords.
- A method's synchronous or asynchronous nature is an intrinsic property of its own definition, tagged via an abstraction at the definition site (not the call site), not a choice made by the caller.
- Execution runs on user-space threads managed by framework-level schedulers, aligned with Unikernel/Exokernel architecture.
- Written as a single flat document (`Summary` / `Guide-level explanation` / `Reference-level explanation` / `Drawbacks` / `Rationale and alternatives` / `Prior art` / `Unresolved questions` / `Future possibilities`), ahead of this project's Explanation-facet specification and its documentation-changelog convention — no paired changelog file existed until this one.

#### Considered and not done
- **Syntax-level concurrency primitives (rejected)**: rejected on the function-coloring-avoidance argument.

---

### Renamed to khayyam-agency.md and reframed through the Agency lens
- Time: 2026-08-17T00:00:00Z
- Type: refactor
- Cited:
  - [Agency](../agency.md) — Depends_on: this document's central new claim — that a Worker/Actor-style representation should not be hard-coded into a language's grammar — is stated in Agency's own terms (Execution Agent as a representation, not a primitive) rather than reconstructed independently here.
  - [Process](../process.md) — Depends_on: the Concurrency topic's escalating decision chain (shared state → ... → synchronization → locking) is cited directly as the reasoning a `go`-style keyword would bypass.
- Propagates to:
  - khayyam-control_flow.md: Reference only — this document's citation of Control Flow's own general syntax-minimalism argument was checked against the current file and found accurate; no change needed there.
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — requested, argued
  - [Claude](../../CONTRIBUTORS.md#claude) — reviewed, rewrote, recommended

#### What changed
- `khayyam-concurrency.md` was renamed `khayyam-agency.md` and migrated into the current Explanation-facet template.
- No existing technical content (definition-site tagging, user-space scheduling, function-coloring avoidance) was removed or weakened.
- A new topic, "Concurrency Decisions as Agency, Not Syntax," was added, connecting the original, independently-reasoned design decisions to Agency's and Process's later, independently-developed vocabulary and stating explicitly what was previously only implicit: that rejecting `go`/`async`/`await` as keywords avoids the same modeling error Agency and Process later named independently (treating an execution representation as a primitive rather than as a stand-in for a bounded responsibility), and that this convergence is being recorded now, after the fact — a retrospective connection, not a rewrite of the original motivation.
- Front-matter `Citations` — which had carried a duplicate, YAML-invalid `Citations:` key from the original draft — and `Author(s)` were moved into this changelog; the malformed duplicate `Citations` key is resolved by the same front-matter migration already applied elsewhere in this project.
- The document's placeholder-looking ID (`000011`) was replaced with a computed UTC-hour-count identifier (495210, from the original Start Date), matching the convention `khayyam-control_flow.md` and this project's other documents already use.

#### Deliberation
- In the same conversation as the Agency/Process/Worker Telegram-post discussion, it was raised that `khayyam-concurrency.md` did not need to remain an independent, narrowly-scoped document (Omid Hekayati — requested).
- Two alternatives were proposed: merging it into `khayyam-control_flow.md`, or renaming and broadening it to `khayyam-agency.md` so that Khayyam-specific design decisions could be discussed through the same Agency lens the project had just finished applying to `process.md`; the proposal explicitly floated a broader scope (Omid Hekayati — proposed).
- An independent recommendation was explicitly asked for, rather than agreement (Omid Hekayati — requested).
- `khayyam-control_flow.md` was read in full before recommending (Claude — reviewed).
- Merging into `khayyam-control_flow.md` was recommended against, on the grounds recorded under Considered and not done (Claude — recommended).
- The rename to `khayyam-agency.md` was recommended, scoped for now to the concurrency-specific content that already existed, with an explicit Unresolved question left open about whether the document's scope should later grow to cover other Agency-flavored Khayyam decisions, rather than speculatively writing that broader scope now (Claude — recommended).
- Baking concurrency primitives into the language — as most languages do, under pressure from prior art — was argued to be the same category of naive modeling this project's Agency and Process documents already name: treating Worker/Actor as a primitive rather than as a representation of a bounded execution responsibility; and Khayyam should not add that flawed abstraction merely because other languages do (Omid Hekayati — argued).

#### Considered and not done
- **Merging into `khayyam-control_flow.md` (considered, rejected).** Both documents share a design philosophy — the compiler exposes minimal primitives, named behavior is a library decision — but concurrency and control flow (branching, looping, error propagation) are different subjects a reader would look for separately; `khayyam-control_flow.md` is already substantial, and the shared philosophy is already stated generally enough there to be cited by this document rather than requiring the two to merge. This also matches `process.md`'s own precedent of keeping Concurrency as its own topic rather than folding it into a general control-flow-equivalent topic.
- **Expanding this document's scope immediately to cover every Agency-flavored Khayyam decision (considered, rejected for now).** This pass keeps the document's actual content limited to what already existed (concurrency), and records the broader-scope question as an Unresolved question rather than writing speculative content for design decisions (e.g. method-ownership-by-other-methods) that have not themselves been finalized yet.

---

### Closed the method-ownership speculative question after checking khayyam-method.md directly
- Time: 2026-08-17T00:00:00Z
- Type: Fixed
- Cited:
  - [Method in Khayyam](./method.md) — Reference: checked directly to resolve Unresolved question 3, rather than continuing to speculate about its content secondhand.
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — requested
  - [Claude](../../CONTRIBUTORS.md#claude) — reviewed, rewrote

#### What changed
- The candidate connection between Khayyam's method-ownership model and Agency, raised speculatively in the previous entry, does not hold up on inspection — resolved as a non-connection rather than left open.
- `khayyam-method.md`'s Method Structure topic was read directly and showed that a method's "owner" there is a type-system attachment point (the type a callable behavior is structurally attached to — a capsule, an abstraction, or another method), not a party responsible for or delegating an action; the two documents share the word "owner" but not the underlying concept.
- Unresolved question 3 was updated to record this as a closed sub-question rather than leaving it as an open possibility.

#### Deliberation
- A direct check of `khayyam-method.md` was requested, given this document's own speculative mention of method-ownership as a possible future Agency connection (Omid Hekayati — requested).

---

### Removed premature Worker/Actor naming from Unresolved questions and Future possibilities
- Time: 2026-08-17T00:00:00Z
- Type: Fixed
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — argued
  - [Claude](../../CONTRIBUTORS.md#claude) — rewrote

#### What changed
- The "Worker"/"Actor" naming was removed from Unresolved question 2, Future possibilities, and the closing paragraph of "Concurrency Decisions as Agency, Not Syntax" — the three places where this document had drifted into naming a specific mechanism ("Worker/Actor package") while arguing against exactly that kind of premature naming — each replaced with unnamed language ("a standard-library representation of an execution Agent," "whatever it ends up being called"), leaving the concrete design and vocabulary entirely to a dedicated future runtime/compiler-focused document rather than suggesting a shape here.

#### Deliberation
- It was pointed out that even proposing a specific execution mechanism's name or shape — including as a mere Future-possibility suggestion, not a language feature — risks the same category of error this document argues against, since naming "Worker" or "Actor" in prose can quietly become the assumed answer the same way a keyword would in grammar (Omid Hekayati — argued).
- It was noted that this document's own name had changed from concurrency-specific to Agency-general, and that it should not stay implicitly concurrency-only just because concurrency is the only fully worked-out example so far (Omid Hekayati — argued).

---

### Broadened beyond concurrency: Agency Beyond Concurrency topic added, title changed, compiler/runtime-boundary content migrated in
- Time: 2026-08-17T00:00:00Z
- Type: Changed
- Cited:
  - [Abstraction in Khayyam](./abstraction.md) — Depends_on: the new "Agency Beyond Concurrency" topic is grounded directly in that document's own "Is Khayyam's Structural Satisfaction Model Sufficient..." Unresolved question, checked firsthand before writing.
  - [khayyam-design_philosophy.md] — Depends_on: "Khayyam Is Not Its Own Compiler or Runtime" is migrated from that document's Reference-level explanation, as part of that document's planned retirement.
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — argued, requested
  - [Claude](../../CONTRIBUTORS.md#claude) — rewrote

#### What changed
- This document no longer reads as concurrency-specific: its title, Abstract, and Unresolved questions now reflect two checked instances (concurrency; abstraction satisfaction) rather than one.
- The three places that had drifted into naming a specific mechanism ("Worker/Actor") despite the document's own argument against doing so — Unresolved question 2, Future possibilities, and the closing paragraph of *Concurrency Decisions as Agency, Not Syntax* — are now unnamed, each replaced with unnamed language.
- "Agency Beyond Concurrency: Intentional vs. Accidental Contract Satisfaction" was added, reframing `khayyam-abstraction.md`'s own open question (structural vs. intentional abstraction satisfaction) through Agency's vocabulary (an `agent_for`-style relationship requires a declared, intentional undertaking; Khayyam's current structural model has none in this sense) without taking a position on which of that document's three resolution options is correct.
- The document was retitled from "Agency in Khayyam: Concurrency Without Baked-In Primitives" to "Agency in Khayyam", and the Abstract rewritten to introduce both instances rather than reading as concurrency-only.
- "Khayyam Is Not Its Own Compiler or Runtime" was migrated from the document slated for retirement into Future possibilities, reinforcing that this document does not design an execution-Agent representation itself — that belongs to a separate runtime/compiler document rather than to this one.

#### Deliberation
- Pushback was made on three places where this document, despite arguing against premature mechanism-naming, had itself named "Worker/Actor" as a proposed package, with a request that all three be de-named (Omid Hekayati — argued, requested).
- It was separately requested that this document's scope not stay implicitly concurrency-only now that its title no longer says "concurrency" (Omid Hekayati — requested).
- An offer was made to supply any document needed to check a real connection rather than have one guessed at (Omid Hekayati — offered).
- It was confirmed that `khayyam-design_philosophy.md` is slated for retirement, with the direction that transferable content should move into documents already in scope, including this one (Omid Hekayati — confirmed).
- `khayyam-abstraction.md` and `khayyam-design_philosophy.md` were requested and read before writing anything further, per the standing practice this review has followed since an earlier, incorrect speculative connection (method-ownership) was caught and reverted (Claude — reviewed).

---

### Reverted: compiler/runtime-boundary content does not belong in this document
- Time: 2026-08-17T00:00:00Z
- Type: Fixed
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — argued
  - [Claude](../../CONTRIBUTORS.md#claude) — rewrote

#### What changed
- The compiler/runtime-boundary elaboration ("the language specification defines *what* is guaranteed... a specific compiler or runtime defines *how*...") was removed from Future possibilities, leaving only the original, simpler pointer to Khayyam's compiler/runtime documentation generally — this document no longer carries compiler/runtime-boundary content, and that elaboration belongs with the compiler/runtime documentation itself.
- The underlying content was not migrated into `Khayyam-compiler.md` in this pass — that document has its own, larger migration pending and is being handled as a separate, self-contained task.

#### Deliberation
- It was pointed out that migrating "Khayyam Is Not Its Own Compiler or Runtime" into this document was an odd choice, since Khayyam already has (or needs) a dedicated compiler/runtime document — specifically to tell a future organization building a Khayyam compiler what problems others already ran into, so they aren't reproduced — and that content belongs there, not here (Omid Hekayati — argued).
- `Khayyam-compiler.md` was supplied as the existing document this content should eventually connect to, with the note that he has not yet reviewed that document closely himself (Omid Hekayati — supplied).

---

### Second migration wave: `## Discussion` retired per the finalized method
- Time: 2026-09-08T00:00:00Z
- Type: refactor
- Propagates to:
  - khayyam-agency.handoff.md: Created - open questions and anticipated work moved there.
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) - requested
  - [OpenCode](../../CONTRIBUTORS.md#opencode) (qwen3.8-flash) - moved

#### What changed
- The body's fixed top-level sections are now Abstract, Introduction, Explanation, Results only: the document-level `## Discussion` and the nested `#### Discussion` wrapper under the *Agency Beyond Concurrency* topic are retired.
- The wrapper's four Unresolved questions moved to the new paired handoff's Open Questions; its Future possibilities moved to that handoff's Anticipated Work.
- The drawback of Linter-reconstructed concurrency-safety guarantees stays in the body as a current-state claim, folded inline into *Avoiding Function Coloring* — it states where those guarantees come from in the design as it stands, not how the decision came to be.
- The wrapper's rejected alternatives (built-in `async`/`await` syntax; Go's `go` keyword) moved under this entry's Considered and not done; its Erlang/BEAM and goroutine survey moved under Related work.
- The document-level `## Discussion` carried no content of its own — both of its subsections were pointers to the topic-level wrapper — and was dropped; its pointers named *Concurrency Decisions as Agency, Not Syntax*, while the wrapper they pointed at sat under *Agency Beyond Concurrency*.
- The Abstract's "see Unresolved questions" pointer now links to the paired handoff's Open Questions.
- Final audit pass: the cross-document pointer in *Avoiding Function Coloring* to Control Flow's retired *Rationale and alternatives* was retargeted to that document's changelog (this wave's migration entry, Considered and not done).

#### Considered and not done
- **Built-in `async`/`await` syntax (rejected; migrated from the *Agency Beyond Concurrency* topic's retired Discussion wrapper)**: built-in `async`/`await` syntax (Rust, JS, Python, C#) was rejected specifically because of the function-coloring problem it introduces. Read retrospectively through Agency, the rejection also avoids hard-coding one particular execution-Agent representation into the grammar — an additional, independently-arrived-at reason for the same conclusion, not the original one.
- **Go's `go` keyword (rejected; migrated from the same wrapper)**: rejected as a syntax-level concurrency primitive that, per [Framework](../framework.md)'s framework-first philosophy, should not be hardcoded into the language at all; the Agency reading adds the same independently-arrived-at reason recorded above.

#### Related work
- **Erlang/BEAM (migrated from the *Agency Beyond Concurrency* topic's retired Discussion wrapper)**: BEAM's process model and user-space green-thread scheduling are the closest prior art for definition-driven, syntax-light concurrency at scale; read through Agency, BEAM's own "process" is itself a named execution-Agent representation, not unlike what a future Khayyam Worker/Actor library would provide, except BEAM commits to it at the language level while Khayyam leaves the choice to a library.
- **Go's goroutines (migrated from the same wrapper)**: popularized lightweight user-space threads but still couple their creation to a dedicated keyword (`go`), which Khayyam avoids.

---

### Definition-site tag: caller-observation and library-owned behavior stated
- Time: 2026-09-23T04:38:49Z
- Type: Fixed
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — decided
  - [Mimo](../../CONTRIBUTORS.md#mimo) (mimo-v2.6-flash via OpenCode) — applied

#### What changed
- Definition-Site Over Call-Site now states that the async tag does not change what a caller observes: a call remains a statement whose influenced variables are written when the statement completes (definite assignment and uniform call syntax survive); what changes is how the owning library and its scheduler realize the method — behavior defined by that library, changeable by swapping the library, never by changing Khayyam's syntax.
- The topic closes with each such library specifying its own method's behavior. An intermediate wording that hedged the examples as "illustrative, answering every question" was removed on owner review: a wrong example is fixed, not disclaimed.

#### Deliberation
- The call-site-semantics critique (unanswered in two disposal attempts) was resolved at the rule level by the ruling that sync/async behavior belongs to each method's library, not to the language (Omid Hekayati — decided).
- The illustrative-examples hedge was rejected as the wrong remedy for example gaps (Omid Hekayati — decided).

---

### Abstraction satisfaction no longer worded as contract satisfaction
- Time: 2026-09-23T08:28:49Z
- Type: Fixed
- Cited:
  - [Abstraction in Khayyam](./abstraction.md) — Depends_on: an abstraction names required behavior; it is not a contract.
  - [Protocol](../protocol.md) — Depends_on: Protocol vs Contract.
- Propagates to:
  - abstraction.md: Done — the inbound anchor now names abstraction satisfaction.
  - agency.handoff.md: Done — both inbound anchors retargeted (handoff: no entry of its own).
- Contributors:
  - [Grok](../../CONTRIBUTORS.md#grok) (Grok 4.7 via Cursor) — reviewed, applied
  - [Gemini](../../CONTRIBUTORS.md#gemini) (Gemini 3.8 flash via Cursor) — reviewed

#### What changed
- The Agency Beyond Concurrency heading and its closing question now say satisfying an abstraction, not satisfying a contract. The intentional-undertaking point is unchanged: structural match is still distinguished from a declared commitment, and the document still takes no position on abstraction.md's three options.

#### Deliberation
- One review dissolved the heading as Agency's undertaking vocabulary, not a redefinition of Abstraction (Grok — reviewed). The other treated "satisfying a contract" as the retired abstraction-as-contract collocation on a section whose subject is abstraction satisfaction (Gemini — reviewed). The applied reading keeps the undertaking point and drops the word *contract*, because abstraction.md already defines an abstraction as naming required behavior rather than parties, obligations, or commitments.

#### Considered and not done
- **Leaving the heading and adding only a parenthetical gloss (rejected)**: the heading is the anchor abstraction.md and the handoff follow, so the collision would remain at the link target.

---

### A method shows asynchronous behavior by implementing that abstraction
- Time: 2026-09-23T08:43:30Z
- Type: Fixed
- Propagates to:
  - agency.handoff.md: Done — the declaration-form question is removed (handoff: no entry of its own).
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — decided
  - [Grok](../../CONTRIBUTORS.md#grok) (Grok 4.7 via [Cursor](../../CONTRIBUTORS.md#cursor)) — applied

#### What changed
- Asynchronous behavior is an abstraction the method implements by defining that abstraction's methods on itself. The method may compose an intent abstraction such as `abstraction_p.Implements` so tooling can see the implementation. The open question is removed from the handoff.

#### Considered and not done
- **A tag slot on the method signature, a bare name in an `mt` body, a marker method as the only form, or a convention with no declaration (rejected)**: the method implements the abstraction with methods of its own, and may present that fact through an intent abstraction (Omid Hekayati — decided).
