# Method in Khayyam Changelog

## Changelog

### Initial creation, merging Function as Capsule and Composition Depth
- Time: 2026-07-28T00:00:00Z
- Type: Added
- Cited:
  - [Khayyam - Programming Language](./khayyam.md) — Reference: the canonical specification defines the `mt` subtype and the method signature grammar this document elaborates and motivates.
  - [Encapsulation in Khayyam](./encapsulation.md) — Depends_on: Method Structure relies on the capsule model — Capsule Structure and Privacy, Sovereign Encapsulation — defined there, for its common-case examples and for the state-protection guarantee described under Pass-by-Reference and State Protection. Encapsulation in Khayyam references this document back for the method-signature mechanics.
  - [Logic in Khayyam](./control_flow.md) — Reference: Logic in Khayyam's IF/ELSE model relies on the same pass-by-reference, explicit-influenced-variable mechanic specified here under Method Structure — no chaining, in either document, is a consequence of that mechanic.
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — claimed
  - [Super Z](../../CONTRIBUTORS.md#super-z) (GLM 5.2, medium effort) — rewrote
  - [Claude](../../CONTRIBUTORS.md#claude) (claude-sonnet-5, high effort) — rewrote

#### What changed
- The standalone "Function as Capsule (No fn/func Keyword)" and "Composition Depth as a Decomposition Signal (No Expression Chaining)" documents were synthesized into one Explanation-facet document (Claude — merged).
- A Method Structure topic was newly specified — signature grammar, pass-by-reference, static-vs-instance invocation, body-less methods for FFI/contracts (Claude — specified).
- Method dispatch was elaborated at reference level — static-vs-instance invocation, body-less methods for FFI/contracts (Super Z — rewrote).
- Method parameters were reframed away from an input/output model toward owner / influencing variable / influenced variables in place of the conventional "arguments"/"return values" naming, with a dedicated Explanation topic for the reasoning that a pass-by-reference model where types carry their own mutating methods makes the input/output framing actively misleading, not merely old-fashioned (Omid — the reframing; Claude — written with the dedicated topic).
- The "No Dedicated fn/func Keyword" section was written, leading with the argument that a seemingly type-independent behavior (e.g. `Sum`) almost always turns out to belong to a specific type once examined, with the wrapper-capsule-plus-`Do` pattern presented as the fallback rather than the default (Claude — wrote).
- The open dual-role-variable question — a variable that is both influencing and influenced in the same call — was identified (Omid — identified).

#### Deliberation
- The absence of a `fn`/`func` keyword, the rejection of expression chaining, and the method signature grammar in the canonical Khayyam specification were claimed as original design decisions (Omid Hekayati — claimed).

---

### Migration to the current documentation methodology
- Time: 2026-08-17T00:00:00Z
- Type: refactor
- Cited:
  - [System](../system.md) — Reference: the new "When Is a Responsibility Coherent?" section is cited from Composition Depth as a Decomposition Signal, since that topic's decomposition test is a Khayyam-specific, syntactically-enforced application of the general one stated there.
  - [Modularity](../modularity.md) — Reference: cited alongside System for the same reason, at the architectural rather than conceptual level.
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — requested
  - [Claude](../../CONTRIBUTORS.md#claude) — reviewed, rewrote

#### What changed
- Front-matter `Citations` and `Contributors` were moved into this changelog and the stale `Applied to: []` field was removed.
- The body-level `## Change Rationale` section was removed; its two items are preserved above and in the Initial creation entry.
- A cross-reference was added from Composition Depth as a Decomposition Signal to `system.md`'s new "When Is a Responsibility Coherent?" section and to `modularity.md`, since that topic's decomposition-signal argument is a Khayyam-specific instance of the same independent-responsibility test and had no cross-reference to either despite predating both; no definitional content changed apart from this addition.
- "owner" as used in Method Structure (the type a method is attached to — a capsule, an abstraction, or another method) was checked against Agency's Principal/Agent/delegation model and found unrelated despite the shared word; the corresponding speculative Unresolved question in `khayyam-agency.md` was corrected to record this finding rather than left open.

#### Deliberation
- The owner requested that this document's method-ownership content be checked in light of the Agency/Khayyam discussion happening in the same review effort, and — regardless of whether that check produced any content change — that the document be brought fully up to the current documentation methodology, since it still carried old-style front-matter `Citations`/`Contributors`/`Applied to` and a body-level `## Change Rationale` section despite already having been restructured into `Abstract`/`Introduction`/`Explanation`/`Results`/`Discussion` at some earlier point (Omid Hekayati — requested).

#### Considered and not done
- **Adding a connection between Method's owner/influencing/influenced reframing and Agency (rejected)**: considered on the theory that "owner" is shared vocabulary between the two documents; rejected on inspection — Method's owner is about which type a callable behavior is structurally attached to, not about who is responsible for or delegates an action; the two documents use the same word for genuinely different concepts, and forcing a connection between them would be exactly the kind of unforced, decorative cross-referencing this project's review has been trying to avoid, not the kind that resolves real duplication or drift.

---

### Correct static/instance dispatch enforcement and clarify influencing/influenced code smell
- Time: 2026-08-27T00:00:00Z
- Type: Fixed
- Cited:
  - [Khayyam — Programming Language](./khayyam.md) — Depends_on: the new Separation of Syntax and Governance principle that classifies “which entity a call targets” as syntax
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — requested
  - [Super Z](../../CONTRIBUTORS.md#super-z) — rewrote

#### What changed
- `Method Invocation Rules` corrected from “enforced strictly at the tooling/linter layer” / “flagged as an error” to “enforced by the compiler” / “is a compile-time error” — dispatch determines which entity a call targets (`what exists`), so it belongs to syntax under the Separation principle; the linter may add additional diagnostics.
- The future linter rule for flagging an influencing variable that receives a mutating call is kept, and an influencing→influenced transition in one call is treated as an organizational code-smell to be flagged and refactored (e.g., return an error and let the caller `Close()` the `net.Conn`), not as a language-level error.

#### Deliberation
- The owner clarified that `CF.Return` mid-method is not automatically a smell, and that an influencing→influenced transition is a code-smell nudge rather than a language error (Omid Hekayati — requested).

---

### Second migration wave: `## Discussion` retired per the finalized method
- Time: 2026-09-08T00:00:00Z
- Type: refactor
- Propagates to:
  - khayyam-method.handoff.md: Created - open questions and anticipated work moved there.
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) - requested
  - [OpenCode](../../CONTRIBUTORS.md#opencode) (qwen3.8-flash) - moved

#### What changed
- The body now carries only the fixed top-level sections Abstract, Introduction, Explanation, Results: the document-level `## Discussion` section was removed, and the four topic-level `#### Discussion` wrappers — under Method Structure, Influencing and Influenced Variables, No Dedicated fn/func Keyword, and Composition Depth as a Decomposition Signal — were dissolved, every block relocated or verified already carried by the body, none lost.
- Rejected alternatives and drawback records from those wrappers and from the document-level Drawbacks and Rationale and alternatives sections were relocated to this entry's Considered and not done below; the comparative prior-art surveys from the four topic Prior art wrappers and the document-level Prior art section were relocated to this entry's Related work below.
- The dual-role open question and its compiler/linter-detectability companion moved to the paired handoff's Open Questions; the anticipated linter rule — the only content any Future possibilities wrapper carried, stated under the Influencing and Influenced Variables topic and restated at document level — moved to the paired handoff's Anticipated Work.
- The dedicated `fn`/`func`-keyword-plus-access-modifiers rejection was dropped as already carried by the body: the No Dedicated fn/func Keyword topic itself states the rejection with the same "unnecessary second category of declaration syntax on top of a model that already covers this case" reason; the document-level Future possibilities line was likewise dropped as a strict restatement of the topic-level one, whose fuller wording is the handoff entry.
- No premise evidence required an inline fold: the pass-by-pointer C struct behavior the input/output critique depends on was already stated inline in the Influencing and Influenced Variables topic, and the typical `err Error` influenced-variable pattern was already stated inline in Method Structure's Key Rules and examples.
- The body's plain-text pointer "see Unresolved questions" in the dual-role hypothesis was repointed as a live hyperlink into the paired handoff's Open Questions.

#### Considered and not done
- **Unified parameter list without parenthetical separation (rejected; migrated from the Method Structure topic's retired Rationale and alternatives)**: would make it harder to distinguish at a glance which variables are influencing variables and which are influenced variables, especially for methods with many parameters.
- **Separate keyword for functions vs. methods (rejected; migrated from the Method Structure topic's retired Rationale and alternatives)**: a method is fundamentally its own type category, attachable to any owner type; introducing a separate keyword for the receiver-less case would create an artificial distinction where none exists at the semantic level.
- **Keep "arguments" and "return values" (the conventional framing; rejected; migrated from the Influencing-and-Influenced-Variables topic's retired Rationale and alternatives)**: accurately describes languages where the callee cannot reach back into the caller's variables, but is actively misleading in Khayyam, where every non-owner variable is passed by reference and can, in principle, be mutated through its own exposed methods regardless of which parenthesized group it sits in; keeping the conventional names would quietly promise a read/write guarantee the language does not make.
- **"Input"/"output" (a common relabeling; rejected; migrated from the same topic)**: still a positional framing (which side of the call is it "on"), not a role framing (what does it actually do in this call); it inherits the same misleading guarantee as "arguments"/"return values."
- **Free functions with no owner as the default (rejected; migrated from the No-Dedicated-fn/func-Keyword topic's retired Rationale and alternatives)**: makes it too easy to stop at the first "this doesn't need a type" impression, which the `Sum` example shows is usually wrong on inspection; defaulting to a method on an owning type forces that inspection to happen at declaration time rather than being skipped.
- **Expression-level chaining (rejected; migrated from the Composition-Depth topic's retired Rationale and alternatives)**: allowing chaining, as virtually all modern languages do, was rejected because it removes the friction that currently makes over-large method/widget bodies visible and uncomfortable — without that friction, the language would have no organic pressure toward decomposition, relying entirely on developer discipline or external linting to catch the same problem after the fact.
- **The single underlying choice behind the two syntax rejections (migrated from the removed document-level Rationale and alternatives)**: both the `fn`/`func`-keyword and the expression-chaining rejections trace back to the same underlying choice — Khayyam consistently declines to add a second, shortcut syntax alongside an already-sufficient general mechanism (the method model, attached to whichever type actually owns the behavior; named, pre-declared variables for a method's influenced variables), even where the shortcut is common practice elsewhere and would reduce ceremony in the common case; the influencing/influenced reframing follows a related but distinct logic: not "add no new mechanism" but "name the existing mechanism by what it does, not by an inherited framing (input/output) that doesn't hold once methods are pass-by-reference and types carry their own mutating behavior."
- **Empty parenthetical groups as syntactic ceremony (drawback record; migrated from the Method Structure topic's retired Drawbacks)**: the strict separation of owner, influencing variables, and influenced variables with `()` adds ceremony for methods that need neither; in practice this case is rarer than it first appears — most methods that look parameter-less still have at least one influenced variable, typically an `Error` (e.g. `tp Close mt (self Reader) () (err Error) {}`, not `() ()`, since closing a reader can fail) — but a method that genuinely has nothing to declare on either side, e.g. a `tp Reset mt (self Counter) () () {}` defined to always succeed, still carries two empty parenthetical groups that convey no information, purely for the sake of consistency with every other method's shape.
- **Reframed vocabulary cost and residual incompleteness (drawback record; migrated from the Influencing-and-Influenced-Variables topic's retired Drawbacks)**: owner/influencing/influenced is one more piece of vocabulary a newcomer has to learn instead of reaching for the already-familiar "input"/"output" mental model every other language uses; and the dual-role case shows the three-way split is not yet a complete model — a real, common pattern (a resource handle that is read from and then closed in the same call) does not fit cleanly into exactly one of the two non-owner groups. The dual-role case itself remains stated as current state in the body's The Open Question: A Variable That Is Both section.
- **Thinking cost and wrapper ceremony (drawback record; migrated from the No-Dedicated-fn/func-Keyword topic's retired Drawbacks)**: the reframing adds a real thinking cost before writing anything — instead of just typing a free function, a developer has to first ask which type the behavior actually belongs to (for `Sum`, that means noticing the overflow/coercion questions and picking a numeric type before writing a line of logic); and for the genuinely rare case where no existing type fits, expressing the behavior still requires a named method, typically wrapped in a small capsule to give it a name and a home, rather than a single top-level function declaration — more ceremony than virtually every other language needs for this case.
- **Named temporaries for single-purpose sequences (drawback record; migrated from the Composition-Depth topic's retired Drawbacks)**: even a simple, genuinely single-purpose sequence (e.g. a three-step pure math calculation) requires multiple named temporary variables, which can read as noisier than an equivalent one-line chained expression in other languages, especially for short-lived, never-reused intermediate values.
- **Aggregate verbosity against mainstream code (drawback record; migrated from the removed document-level Drawbacks)**: together, these decisions mean Khayyam code contains more named methods and more named intermediate variables than equivalent code in most mainstream languages: every seemingly type-independent utility requires first identifying which type actually owns the behavior (or, failing that, a purpose-built capsule-plus-method pair); every multi-step computation becomes a sequence of named variables rather than a chained expression; both costs are treated as deliberate, load-bearing friction rather than incidental ceremony to be minimized; and separately, the owner/influencing/influenced reframing of method parameters trades a familiar (if inaccurate) input/output mental model for a more accurate but less familiar one, without yet a settled answer for variables that play both roles in the same call.
- **Misapplication to single-responsibility pipelines (resolved; migrated from the Composition-Depth topic's retired Unresolved questions)**: the earlier concern whether the no-chaining rule could be misapplied to pipelines that only *look* like several operations was resolved — the rule applies uniformly, since each pipeline stage genuinely is a distinct concern with its own failure mode — and the body's Composition Depth as a Decomposition Signal topic states that uniform application directly.
- **The remaining "None at this time"/"None recorded yet" lines from the Method Structure, fn/func, and Composition Depth wrappers carried no claim and are not reproduced.**

#### Related work
- Go's method syntax with an explicit receiver is syntactically similar; Rust's `fn` with `&self`/`&mut self` is semantically similar but introduces reference annotations that Khayyam eliminates; Smalltalk's message-passing model is the closest conceptual match. (Migrated from the Method Structure topic's retired Prior art)
- C's pass-by-pointer struct parameters are the direct prior art for the problem the Influencing and Influenced Variables topic solves — the same "argument that is also mutated internally" pattern that section describes; Go and Rust's pointer/reference parameters share the same structural ambiguity; Rust's borrow checker is the closest prior art for actually *enforcing* a distinction between read-only and mutable access at the language level (via `&` vs `&mut`), which Khayyam's current model does not attempt — the influencing/influenced split is a naming and modeling clarification, not an enforcement mechanism. (Migrated from the Influencing-and-Influenced-Variables topic's retired Prior art)
- Most languages (C, Go, Java, Rust, Python) provide a dedicated function-declaration keyword distinct from their type/class declaration syntax and treat `Sum(a, b)`-style free functions as entirely ordinary; Smalltalk and other strictly message-passing-oriented languages, where even "free functions" are ultimately methods on some object, are closer in spirit to Khayyam's approach; domain-modeling-heavy codebases in many languages (e.g. `Money.add()` over a free `add(a, b)`) already arrive at the same "behavior belongs to a type" conclusion as a best practice, without the language forcing it. (Migrated from the No-Dedicated-fn/func-Keyword topic's retired Prior art)
- Go and Rust both support method chaining freely; this is treated as the default in modern language design, which makes Khayyam's rejection here a deliberate, atypical choice rather than an oversight. (Migrated from the Composition-Depth topic's retired Prior art)
- Taken together, Smalltalk's message-passing model (no free functions, no operator overloading magic) is the closest overall precedent for this document's general stance: prefer an already-general mechanism, explicitly used, over a second, more convenient but less legible one. (Migrated from the removed document-level Prior art, whose per-decision pointer — prior art documented under each topic — is now served by the topic-attributed entries above.)

---

### Type-level arguments for `sc` and `mt`
- Time: 2026-09-15T09:00:00Z
- Type: Changed
- Cited:
  - [Linter](../protocols/linter.md) — Consumed contract: the check is governance; this document owns the grammar.
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — decided (rule home is the subject's document)
  - [Grok](../../CONTRIBUTORS.md#grok) (Grok 4.6 via Cursor) — applied

#### What changed
- Method Invocation Rules now state that an argument position may be a `vr` or, for `sc`/`mt`, the type itself; a bare type where a capsule/abstraction value is expected is a linter-flaggable smell, not a syntax error. Relocated from the retired Khayyam-shelf linter document.

