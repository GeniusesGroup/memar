# Time Changelog

## Changelog

### Initial draft — the separation position
- Time: 2026-09-06T00:00:00Z
- Type: Added
- Contributors:
  - [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) — claimed, argued
  - [Super Z](../../../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — reviewed, rewrote

#### What changed
- Initial Draft created, recording the interface-shaped position: time's framework presence is a small ordering/comparison contract plus three separable satellite concerns; mutability ruled out; the definitional question kept genuinely open (Omid Hekayati).
- The position was shaped into the four-concern separation with the minimal-commitment contract (ordering and comparison only), so the unresolved definitional question does not block API rules (Super Z).
- The richer semantics (causality, monotonicity) were distributed to the documents that own them (Super Z).
- The Draft was kept deliberately small (Super Z).

#### Deliberation
- The topic was opened from the project's conceptual discussions (Omid Hekayati).
- The definition of time is unsettled and a framework must not hard-code a metaphysics (Omid Hekayati).
- The ecosystem's bundled "standard time library" mixes four separable concerns (instant, duration, civil conversion, formatting) whose coupling leaks into APIs needing only one (Omid Hekayati).
- The pointer-mediated mutable time values observed in a mainstream library were a cost-and-clarity failure consistent with the framework's value-semantics positions (Omid Hekayati).
- The Draft was to open the topic rather than settle it, and was kept deliberately small accordingly (Omid Hekayati — the instruction; Super Z — applied).

---

### Documentation-method migration: rejected alternatives and anticipated work relocated
- Time: 2026-09-06T00:00:00Z
- Type: refactor
- Propagates to:
  - time.handoff.md: Done - anticipated work recorded there under `Anticipated Work`.
- Contributors:
  - [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) - claimed, decided
  - [Super Z](../../../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) - moved

#### What changed
- The body's `Discussion` wrappers dissolved entirely, per the finalized documentation method (documentation-explanation.changelog.md, same date) (Omid Hekayati - decided; Super Z - applied).
- The topic-level `Discussion`'s evidence paragraph (the ecosystem's separation direction: monotonic clocks, timestamp/calendar splits, physical-clock versus event-ordering literature) folded into its topic as inline evidence (Super Z).
- The document-level `Drawbacks` removed from the body; its content preserved below without loss (Super Z).
- Rejected-alternative reasoning moved from the body's `Rationale and alternatives` sections into this entry's `Considered and not done`, without loss (Super Z).
- Anticipated work moved from the body's `Future possibilities` into the paired handoff's `Anticipated Work` (Super Z).

#### Considered and not done
- **Adopt the ecosystem's bundled time type as the framework default (rejected)**: the coupling argument; also contradicts the framework's posture that a concept's abstractions are sized to the responsibilities actually exercised. (Omid Hekayati)
- **Defer the entire topic until Khayyam's type system settles (rejected)**: the separation rule binds API design now - every API accepting a bundled time type today is a future migration; recording the rule early is cheaper. (Omid Hekayati)

#### Considered and not done (from the removed document-level Drawbacks section)
- **Separation has a real ergonomic cost: the common case ("give me now, compare it to later") now names two abstractions where the ecosystem names one** — accepted deliberately, because the bundling cost is paid by every API forever while the ergonomic cost is paid by every call site once — and tooling mitigates the latter, nothing mitigates the former. (Omid Hekayati)

---

### A contract states a duration, not a unit; two duration and timer questions carried here
- Time: 2026-09-29T10:40:00Z
- Type: Changed
- Cited:
  - [Documentation → Content Rule](../../documentation.md#content-rule-no-fabricated-or-redundant-provenance) - Premise: content lives in one authoritative home and is linked, not restated.
- Contributors:
  - [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) - decided: code under `modules/` introduces itself, and a code folder carries only a README
  - Auto (model not recorded) via [Cursor](../../../CONTRIBUTORS.md#cursor) - applied

#### What changed
- `time.md → A contract states a duration, not a unit`: a new section carrying the owner's statement that defining a timer does not force a dependency on a unit of time, and the rule that every contract over a span states a Duration and leaves the unit to the implementation. It came from the module document `modules/time/time.md`, which was deleted under the owner's decision above.
- `time.handoff.md`: two questions from the deleted module handoff `modules/time/time.handoff.md` — whether a common concept over the duration units exists, and whether a contract needs a timer that also reports the instant it fires at. The civil-conversion question now records that `modules/time/utc/` and `modules/time/earth/` already hold civil-calendar declarations.

#### Considered and not done
- Carrying the module handoff's question whether `duration/` and `timer/` each want a main document: the owner's decision that a code folder carries only a README answers it.
- Carrying the module document's statement that civil conversion and formatting are not held in the module: the calendar declarations under `modules/time/` contradict it.
- Moving the module document's duration table and its section on how a capsule satisfies an abstraction: the table describes code, and the section restates Abstraction in Khayyam and Encapsulation in Khayyam.

---

### Realization membership and README symlink
- Time: 2026-09-29T11:17:00Z
- Type: Changed
- Contributors:
  - Auto (model not recorded) via [Cursor](../../../CONTRIBUTORS.md#cursor) - applied

#### What changed
- `time.md`: realization membership for `modules/time/`.
- `time.handoff.md`: numeric counterpart link repointed to `math.handoff.md`.
- `modules/time/README.md`: replaced with a symbolic link to `../../docs/protocols/time/time.md`.

---

### Civil conversion's framework-level placement settled by the membership rule
- Time: 2026-10-04T20:52:36Z
- Type: Changed
- Propagates to:
  - time.handoff.md: Done — the placement question removed; the base document's realization-membership rule is its answer's home.
- Contributors:
  - [Space Bunny Alpha](../../../CONTRIBUTORS.md#space-bunny-alpha) (space-bunny via [OpenCode](../../../CONTRIBUTORS.md#opencode)) — argued, applied

#### What changed
- `time.handoff.md`: "Is civil conversion a framework-level concern at all?" removed — [Realization membership](time.md#realization-membership) places a declaration whose subject is "a calendar that reckons instants into human or astronomical units" under `modules/time/`, and [The four separable concerns](time.md#the-four-separable-concerns) already states civil conversion's contract as inherently political and historical.
- The 2026-09-29 entry's `Considered and not done` above already rejected carrying the retired module document's contrary statement that civil conversion and formatting are not held in the module, on the ground that the calendar declarations under `modules/time/` contradict it; the handoff entry is the last place that question was still tracked as open.

#### Considered and not done
- Retaining the question pending the GUI and scheduling components' actual needs: their pushback bears on which components depend on civil conversion, not on whether the framework states the concern itself, and the separation rule already settles that.

---

### Duration-resolution concept refused; entry narrowed to `NanoInSecond`
- Time: 2026-10-05T09:47:47Z
- Type: Changed
- Propagates to:
  - time.handoff.md: Done — the entry now states that no resolution concept is admitted and asks only about `NanoInSecond`.
- Contributors:
  - [Space Bunny Alpha](../../../CONTRIBUTORS.md#space-bunny-alpha) (space-bunny via [OpenCode](../../../CONTRIBUTORS.md#opencode)) — argued, drafted, applied

#### What changed
- The paired handoff's Open Questions entry "Is there a common concept over the duration units?" narrowed to its residue.
- Recorded as settled: no such concept is admitted. A concept is an abstraction; a concrete instance is a capsule (`docs/khayyam/abstraction.md#a-concept-is-an-abstraction-a-concrete-instance-is-a-capsule`) states that a contract's unit or width "is the implementation's to choose, finer-grained, and never a floor the contract must meet", and [A contract states a duration, not a unit](time.md#a-contract-states-a-duration-not-a-unit) states the same for this protocol — the contract keeps the magnitude asked for and gives up only the measure it is expressed in. A resolution concept would be exactly the floor both passages rule out.
- The entry's one-directional-conversion objection is therefore answered by refusing the question rather than by designing a narrower abstraction, and the `Blocks continuation` line is kept with its answer: nothing waits on it, and nothing is to be built.
- Residue recorded: `NanoInSecond` is already held as an instance of `Duration` under `modules/time/duration/` although what it names is a component of a decomposed instant rather than a span on its own, which the ruling that made it an instance did not argue.
- The entry's cross-reference to [Math Handoff → Is there a common abstraction over all numeric kinds?](../math/math.handoff.md#is-there-a-common-abstraction-over-all-numeric-kinds) went with it, the residue no longer turning on a common abstraction over numeric kinds. The base document's body is unchanged; the other five entries under Open Questions are untouched.

---

### The no-metaphysics rule stated per term
- Time: 2026-10-05T17:18:32Z
- Type: Changed
- Cited:
  - [Time Changelog](./time.changelog.md) - Premise: the owner's own deliberated formulation this rule answers to, recorded in that file's earlier entry.
- Contributors:
  - [Space Bunny Alpha](../../../CONTRIBUTORS.md#space-bunny-alpha) (space-bunny via [OpenCode](../../../CONTRIBUTORS.md#opencode)) — argued, drafted, applied

#### What changed
- `time.md` → [The definitional question, kept open](./time.md#the-definitional-question-kept-open): the requirement as it now stands is that a time contract's terms are ordering and comparison alone, the minimal commitments any of the candidate definitions support.
- The check that now decides it is per term: read a term of an Instant or Duration contract, and a term naming causality, simultaneity across distributed components, or a monotonicity guarantee is not a term this contract carries — that question is owned by networking and process.
- The replaced wording, that Memar's abstractions must not hard-code a metaphysics, named no term and no procedure; the section's next sentence already carried the decidable content, so the rule is now stated as that content and the unsettled definition stays where the document keeps it.

---

### Review of the uncommitted changes of 2026-10-12
- Time: 2026-10-12T09:45:50Z
- Type: Reviewed
- Contributors:
  - [Claude](../../../CONTRIBUTORS.md#claude) (Sonnet-5.5) — reviewed

#### What changed
- Reviewed; no change needed. Two added handoff entries: the unix realization (`modules/time/unix/` holds five `.kh` files with no `tp`, `cp` or `vr` line; `time.kh` lines 9, 15, 19, 22 match the cited declarations) and the timer constants (`modules/time/timer/const.kh` lines 12-20 match). Both anchors in `time.md` exist. The questions are left to the owner.

---

### Module pilot: open questions triaged, Tentative decisions recorded, two entries corrected, the contract question asked
- Time: 2026-10-15T08:30:00Z
- Type: Changed
- Cited:
  - [Documentation — Handoff Practice → Questions Found During a Task](../../documentation-handoff.practice.md#questions-found-during-a-task) - Premise: each question is settled from owning material and recorded Tentative, made smaller by a queued session, or written for the owner.
  - Abstraction in Khayyam → A concept is an abstraction; a concrete instance is a capsule (`docs/khayyam/abstraction.md#a-concept-is-an-abstraction-a-concrete-instance-is-a-capsule`) - Premise: a contract's unit or width is the implementation's.
- Contributors:
  - [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) - decided: documents and moves are held until session 12672 settles placement; protocol declarations may be drafted in Khayyam
  - [Claude](../../../CONTRIBUTORS.md#claude) (Opus-5.5) - argued, drafted, applied

#### What changed
- `time.handoff.md`: a Decisions section, each from cited owning material and without a second opinion yet: the Instant contract carries no representation term (Tentative); `NanoInSecond` is an instance of `Duration` (Tentative); `Timer.When` stays (Tentative); causality and cross-component ordering are not this module's question (Tentative); a fuller concept document (Deferred, on 12672); `maxWhen`, `verifyTimers` and `heapAry` belong to the timing heap's realization (Tentative). Each answered entry keeps its place and points at its decision until the owner rules.
- `time.handoff.md`: a new entry "Does the time contract become ordering, comparison and a clock?", asking the owner to adopt a drafted replacement of `Time` and `Duration` and a new `Clock`, kept in session 20261014T124124Z-3000-0.
- `time.handoff.md` → "Does any contract need a timer that also reports the instant it fires at?": corrected. Its statement that the timer contract reports status only was inaccurate; `modules/time/timer/protocol/timer.kh` declares `When`.
- `time.handoff.md` → "The unix realization declares nothing...": corrected. Its statement that `modules/time/monotonic/` and `modules/time/epoch/` declare what `unix/` lacks was inaccurate; no folder realizes `Time`. The question now waits on session 28224 for which of unix and utc is a lib candidate.
- `time.handoff.md` → "What protects a time-limited value from a clock that moves?": queued session 20261015-T080417Z-23696 to make it smaller, with `Deadline` in `modules/process/operation/protocol/deadline.kh` named as a live consumer.

#### Considered and not done
- Removing the entries the Decisions answer, and moving "Distributed ordering versus the Instant contract" to GP's and sRPC's handoffs: removal waits for the owner ([Recording Is Not Gated; Removal Is](../../documentation.md#recording-is-not-gated-removal-is)).
- Editing `modules/time/protocol/time.kh` and `modules/time/duration/protocol/duration.kh`: they are definitions other modules consume, so the replacement is asked, not applied.
