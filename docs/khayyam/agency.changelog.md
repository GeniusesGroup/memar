# Agency in Khayyam Changelog

## Changelog

### Initial draft, as khayyam-concurrency.md
- Time: 2026-06-30T00:00:00Z
- Type: Added
- Cited:
  - [Control Flow in Khayyam](../modules/process/control-flow.md) — Depends_on: this document builds on the precedent set by that document of keeping behavioral policies as ordinary library-driven mechanisms rather than new syntax.
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
  - [Qwen](../../CONTRIBUTORS.md#qwen) (qwen3.8-flash via [OpenCode](../../CONTRIBUTORS.md#opencode)) - moved

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
  - [Mimo](../../CONTRIBUTORS.md#mimo) (mimo-v2.6-flash via [OpenCode](../../CONTRIBUTORS.md#opencode)) — applied

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
  - [Grok](../../CONTRIBUTORS.md#grok) (Grok 4.7 via [Cursor](../../CONTRIBUTORS.md#cursor)) — reviewed, applied
  - [Gemini](../../CONTRIBUTORS.md#gemini) (Gemini 3.8 flash via [Cursor](../../CONTRIBUTORS.md#cursor)) — reviewed

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

---

### Execution-model and linter prescriptions removed from the agency document
- Time: 2026-10-03T11:16:28Z
- Type: Changed
- Propagates to:
  - [Computer — Runtime → Concurrency is hosted, not defined, here](../modules/computer/runtime.md#concurrency-is-hosted-not-defined-here): Pending - the green-thread scheduling account removed here is the runtime's and Concurrency protocol's to state; this document now points at both.
  - [asynchrony rule](../../bundles/khayyam/rules/README.md): Pending - the linter verification of an asynchrony tag, and the reconstruction of blocking-call guarantees by linter rules, are governance rules; the catalog does not carry them.
- Contributors:
  - [Space Bunny Alpha](../../CONTRIBUTORS.md#space-bunny-alpha) (space-bunny via [OpenCode](../../CONTRIBUTORS.md#opencode)) — applied

#### What changed
- [Abstract](./agency.md): the execution claim became a boundary statement — "execution is scheduled in user-space by framework-level schedulers, aligned with Unikernel/Exokernel architecture" became a statement that scheduling belongs to the framework and runtime above the language, cited to [Runtime](../modules/computer/runtime.md). The closing parenthetical "(avoiding the function-coloring problem, keeping the compiler minimal)" became "(avoiding the function-coloring problem)".
- [Definition-Site Over Call-Site](./agency.md#definition-site-over-call-site): the implementation example was removed — "What the tag changes is how the owning library and its scheduler realize the method underneath (for example, suspending a green thread rather than blocking a kernel thread)" became "What the tag changes is what the owning library does with the method underneath it".
- [User-Space Scheduling (Unikernel Synergy)](./agency.md#user-space-scheduling-unikernel-synergy): the topic no longer states a scheduling substrate — "Underlying execution runs on user-space (green) threads managed by library-level schedulers (e.g. the Memar framework's scheduler) — the language syntax itself remains entirely unaware of OS kernel threads. The default architectural stance favors green threads managed by library-level schedulers, for zero-overhead context switching". It now states that the grammar says nothing about how execution is scheduled or what substrate it runs on, and points at the runtime and concurrency contracts.
- [Avoiding Function Coloring](./agency.md#avoiding-function-coloring): the linter attribution and the AST claim were removed — "Because asynchronous behavior is a Linter-verified abstraction (`ab`) rather than a compiler keyword, the function-coloring problem that plagues `async`/`await` languages does not arise, keeping the core AST clean and orthogonal." became "Asynchronous behavior is declared as an abstraction the method composes, not as a keyword, so the function-coloring problem that plagues `async`/`await` languages does not arise: nothing in the source distinguishes a call that may suspend from one that may not, because no declaration makes that distinction at a call site."
- The same topic's cost paragraph no longer says the guarantees "must instead be reconstructed entirely by Linter rules"; it now says they must be reconstructed elsewhere — "by a rule or a tool's check rather than by the grammar".
- [Concurrency Decisions as Agency, Not Syntax](./agency.md#concurrency-decisions-as-agency-not-syntax): "built the same way `IF`/`ELSE` and `PANIC()` are — as an ordinary, named, importable abstraction operating on the compiler's minimal execution primitives" became "as an ordinary, named, importable abstraction", and a library decision a project can "govern via its Linter" became one it can "govern by rule".

---

### Methodology no longer names user-space scheduling among the decisions documented below
- Time: 2026-10-03T00:00:00Z
- Type: Fixed
- Contributors:
  - [Space Bunny Alpha](../../CONTRIBUTORS.md#space-bunny-alpha) (space-bunny via [OpenCode](../../CONTRIBUTORS.md#opencode)) — reviewed, repaired

#### What changed
- [Methodology](./agency.md#methodology): the list of decisions this document says were made independently before Agency existed read "definition-site tagging, user-space scheduling, no baked-in keyword". The entry of 2026-10-03 removed the scheduling substrate this document claimed; the topic now says the grammar states nothing about scheduling and points at the runtime. The list now names "the placement of scheduling above the language", which is what the topic still carries.

---

### The intentional-satisfaction entry withdrawn as another document's own question
- Time: 2026-10-04T21:13:00Z
- Type: Fixed
- Propagates to:
  - [Abstraction in Khayyam Handoff](./abstraction.handoff.md): Done — the entry there carries the question and its three candidate resolutions; this handoff keeps no duplicate.
- Contributors:
  - [Space Bunny Alpha](../../CONTRIBUTORS.md#space-bunny-alpha) (space-bunny via [OpenCode](../../CONTRIBUTORS.md#opencode)) — argued, applied

#### What changed
- The entry "Whether an intentional-satisfaction mechanism should be adopted" is removed from [Agency in Khayyam Handoff](./agency.handoff.md). Its own text assigned the question to [Abstraction in Khayyam](./abstraction.md)'s three candidate options and recorded that [Agency Beyond Concurrency](./agency.md#agency-beyond-concurrency-intentional-vs-accidental-abstraction-satisfaction) states what Agency's vocabulary adds without resolving it; at the time of this entry the question was carried by [Abstraction in Khayyam Handoff](./abstraction.handoff.md), and the position that has since answered it is stated in [Abstraction in Khayyam → Deliberate Satisfaction Is Composed, Not Declared](./abstraction.md#deliberate-satisfaction-is-composed-not-declared).
- No base `.md` body changed, and no `## Anticipated Work` line scheduled this entry.

---

### The Agency Beyond Concurrency section states the settled position and names its own remaining question
- Time: 2026-10-05T09:24:47Z
- Type: Changed
- Cited:
  - [Abstraction in Khayyam → Deliberate Satisfaction Is Composed, Not Declared](./abstraction.md#deliberate-satisfaction-is-composed-not-declared) — Depends_on: the settled position this section now states — the language does not intervene in satisfaction, and a capsule composes an intent abstraction and explicitly delegates the required methods — instead of the open question it previously narrated.
  - [Abstraction in Khayyam → Sharing Behavior Across Implementations](./abstraction.md#sharing-behavior-across-implementations) — Premise: delegation is the ordinary route by which an implementing capsule discharges a required method to a capsule that owns the behavior.
  - [abstraction_p.Implements → Declaring and discovering intent](../modules/computer/abstraction-implements.md#declaring-and-discovering-intent) — Premise: an intent to implement an abstraction is itself an abstraction a capsule composes, the protocol-level precedent for the composed undertaking the section now describes.
  - [Agency → The `agent_for` Relationship](../agency.md#the-agent_for-relationship) — Premise: an Agent relationship is constituted by an undertaking of responsibility, not by two parties having compatible shapes.
  - [Agency → Delegation](../agency.md#delegation) — Premise: responsibility is placed with the Agent that acts, which is why a declaration recognized by the compiler is a different kind of thing from an undertaking written in the capsule's own source.
- Propagates to:
  - [Abstraction in Khayyam Changelog → Deliberate satisfaction is composed and delegated; the language does not intervene](./abstraction.changelog.md#deliberate-satisfaction-is-composed-and-delegated-the-language-does-not-intervene): Done — the `Not done` line that entry recorded for `agency.md` is discharged. The section no longer presents the question as `abstraction.md`'s own unresolved one and no longer takes no position on it: it now states that the composed, delegated undertaking is the settled answer, that Agency's vocabulary is why that form is the right one (an undertaking is the Agent's own act, so nothing needs to be added to the grammar), and that the intent abstraction is judged by the ordinary structural rule with no exemption and no check of its own.
  - [Agency in Khayyam Handoff](./agency.handoff.md): Done — the section's own remaining question has no entry there: whether the receiving side of an abstraction-typed position needs anything — a rule or a tool's check — to surface which satisfiers undertook and which merely resemble. Open questions belong to the handoff, and that file was outside this session's ownership. (Marked `Done` in the entry "The receiving-side question left the section's body for the handoff", which added that entry to the handoff.)
- Contributors:
  - [Space Bunny Alpha](../../CONTRIBUTORS.md#space-bunny-alpha) (space-bunny via [OpenCode](../../CONTRIBUTORS.md#opencode)) — argued, drafted, applied

#### What changed
- [Agency Beyond Concurrency](./agency.md#agency-beyond-concurrency-intentional-vs-accidental-abstraction-satisfaction): the section's second and third paragraphs, which introduced the question as `abstraction.md`'s own unresolved one and then declined to take a position on its three options, are replaced by four paragraphs holding the position. The first states what is settled and links the section that settles it. The second says what Agency adds — resemblance establishes nothing and only a written undertaking does, the undertaking is the capsule's own act placed by [Delegation](../agency.md#delegation) in the capsule's own source beside the delegations, and a language-level marker would make the relationship exist by the compiler's recognition rather than by the capsule's undertaking. The third says why the answer needs no exemption and no separate verification: the intent abstraction is judged by the ordinary structural rule, the delegations are ordinary source under [Type → Explicit Behavior Ownership](../type.md#explicit-behavior-ownership) and [Method → A method implements an abstraction by methods of its own](./method.md#a-method-implements-an-abstraction-by-methods-of-its-own), and tooling finds a deliberate declaration by the means it already uses. The fourth states this document's own remaining question: the settled position governs what the satisfier may write and says nothing about what the receiving party can see, so at a position declared `Reader` an undertaking capsule and a merely resembling one are one value under one rule, and whether the receiving side needs a rule or a tool's check to tell them apart is open — a governance and tooling question, not a grammar one.
- [Abstract](./agency.md#abstract): the second instance is no longer described as more tentative and resting on an open question about whether a capsule should declare intent before it counts as satisfying an abstraction, and no longer says Agency's vocabulary offers a sharper way to state that question without resolving it. It states what `abstraction.md` settles — an intent abstraction composed into the capsule's own definition with the required methods explicitly delegated, and no language intervention in satisfaction — and that Agency's vocabulary says what that answer is about and what it leaves open on the other side of the relationship.
- The heading is unchanged, so the inbound anchors in [Abstraction in Khayyam → Satisfying an Abstraction](./abstraction.md#satisfying-an-abstraction) and in [Agency in Khayyam Handoff](./agency.handoff.md#whether-further-agency-instances-belong-in-the-document) still resolve to this section.

#### Considered and not done
- **Restating `abstraction.md`'s own settled section here (rejected)**: that section owns the position and its evidence; this document states only what Agency's vocabulary adds to it and links the rest, so the two do not drift apart.
- **Naming the mechanism that would answer the receiving-side question (rejected)**: the question is what a rule or a tool's check would need to establish, not what any particular one would be, and this document has no basis to weigh boilerplate, discoverability, and governance cost against each other — the same reason its options paragraph once deferred the satisfier-side question.
- **Closing the receiving-side question as `abstraction.md`'s business (rejected)**: nothing in the language will ever see a delegation at a position declared `ab`, so the question is not about how satisfaction is judged; it is about what the Principal side of the relationship can observe, which no other Khayyam document owns.

---

### The receiving-side question left the section's body for the handoff
- Time: 2026-10-05T18:02:49Z
- Type: Changed
- Propagates to:
  - [Agency in Khayyam Handoff → Whether the receiving side needs anything to tell an undertaking from a resemblance](./agency.handoff.md#whether-the-receiving-side-needs-anything-to-tell-an-undertaking-from-a-resemblance): Done — the entry exists there, carrying the question, the indistinguishability that produces it, and its `Next:`; the `Pending` this changelog recorded for that handoff is discharged.
- Contributors:
  - [Space Bunny Alpha](../../CONTRIBUTORS.md#space-bunny-alpha) (space-bunny via [OpenCode](../../CONTRIBUTORS.md#opencode)) — argued, applied

#### What changed
- [Agency Beyond Concurrency](./agency.md#agency-beyond-concurrency-intentional-vs-accidental-abstraction-satisfaction) → fourth paragraph: the open question it posed is gone, and the position that survives it is now stated as the paragraph's content. Satisfaction is declared, so on the satisfier's side nothing further is needed; what remains unprovided is on the receiving side, where a declared satisfier and a merely resembling one are one value under one rule and the Agent and Principal endpoints are indistinguishable, the language being uninvolved by settled design. The paragraph names the receiving side's question as a governance and tooling question the document does not cross — the place where a rule or a tool's diagnostic would have to live — without asking it.
- [Agency in Khayyam Handoff](./agency.handoff.md) → `## Open Questions`: one entry added, "Whether the receiving side needs anything to tell an undertaking from a resemblance", read off what the paragraph said. No other entry in that file changed.
- The `Pending` propagation this changelog recorded against that handoff, in the entry "The Agency Beyond Concurrency section states the settled position and names its own remaining question", is marked `Done` in place and disclosed here: that entry is from this same uncommitted working thread, and a `Pending` left in place would keep reporting an obligation the work has discharged. Its own text stands, including the description of the question as one this document raised.

#### Considered and not done
- **Answering the receiving-side question (not done)**: the question is what the receiving side can observe and what would have to establish the difference, and this section has no basis on which to weigh a rule against a tool's diagnostic — nothing in the language sees a delegation at a position declared `ab`, so no evidence about satisfaction distinguishes the two cases from here. It belongs to the receiving side: what stands on the other end of an `agent_for` relationship is a governance and tooling question, not a grammar one, and no Khayyam document owns that side. It therefore moves to the handoff unresolved, as the Explanation facet's Relevance discipline requires of an open question.

---

### Review of the uncommitted changes of 2026-10-12
- Time: 2026-10-12T09:50:00Z
- Type: Changed
- Contributors:
  - [Claude](../../CONTRIBUTORS.md#claude) (Sonnet-5.5) — reviewed, revised

#### What changed
- Restored the entry "Reverted: compiler/runtime-boundary content does not belong in this document" (2026-08-17T00:00:00Z) to its original place, verbatim from HEAD. The uncommitted change had removed it with no record and no reason; a changelog is history, and the entry records a decision by Omid Hekayati that later entries and the document still rest on.
- Reviewed the rest of the uncommitted change in [agency.md](./agency.md), [agency.handoff.md](./agency.handoff.md) and this file, and found no further change needed: the `protocols/` links repointed to `modules/` resolve; the execution-model and linter prescriptions removed from the Abstract, Definition-Site Over Call-Site, User-Space Scheduling, Avoiding Function Coloring and Methodology are recorded by the entries of 2026-10-03; the withdrawn handoff entry on an intentional-satisfaction mechanism is recorded by the entry of 2026-10-04 and the answer is placed in [Abstraction in Khayyam](./abstraction.md#deliberate-satisfaction-is-composed-not-declared), which owns it; the new receiving-side handoff entry matches the closing paragraph of Agency Beyond Concurrency and is recorded by the entry of 2026-10-05T18:02:49Z. `memar content check` on the three files reports no problem.

#### Considered and not done
- **Reordering the entry of 2026-10-03T00:00:00Z, which follows one of 2026-10-03T11:16:28Z (not done)**: the order is an existing quirk of recorded history and no information is lost by it.
