# Event Changelog

## Changelog

---

### The Event protocol stated
- Time: 2026-10-03T00:00:00Z
- Type: Added
- Propagates to:
  - [Modularity → Event as a Module Capability](../../knowledge/modularity/modularity.md#event-as-a-module-capability): Pending - the capability's name is consumed from there rather than restated, and this document names the contract behind it; no change needed unless the capability's framing there moves.
  - [Process → Events](../process.md#events): Reference - the concept is cited downward and not restated; the protocol says nothing that revises it.
  - qualified names rule (`bundles/khayyam/rules/qualified-names/qualified-names.md`): Pending - `EventTarget` is settled by this document and the bare `Event` beside it is not; the rule's handoff carries the open case.
  - `modules/process/event/`: Done - the sources' abstractions were renamed to the names this protocol states, and the race specialization now declares its three methods without the unjustified `Process_` prefix and in the module that exposes the capability rather than in this one. The two Go clue blocks the live declarations already carried were dropped; the parts they did not carry were kept, per the go-clue-residue rule. `modules/process/race/`: Done - it owns `Race_Event`, `EventListener_Race_Event`, `Race_EventTarget`, and the target capsule, so the specialization and its realization are its own surface.
  - `modules/khayyam/lsp/`: Done - a name nothing in a document answers now publishes a diagnostic over the server's own stdio, so the next hand rename is reported to the author.
- Tasks:
  - [docs/protocols/process/event.md](./event.md): Closed - the protocol is stated; seven questions are carried in [the handoff](./event.handoff.md).
  - [docs/protocols/process/event.handoff.md](./event.handoff.md): Closed
  - Rename of the Event capability across the sources: Closed
  - The editor's diagnostic gap for an unbound type name: Closed
  - A one-command rename of a declaration and its dependents: Partial - the sources rename was done by enumerating consumers; the command that does the enumerating is not built, and what it needs is stated below.
- Contributors:
  - [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) (Space Bunny Alpha via OpenCode) - claimed, requested
  - [Space Bunny Alpha](../../../CONTRIBUTORS.md#space-bunny-alpha) (via OpenCode) - argued, rewrote, tested

#### What changed
The Event protocol is stated at [event.md](./event.md), entering at `Draft`. Its claims:

- An `Event` is an abstraction a Type composes to declare that an occurred fact of that kind exists; it composes identity and time, and it is a runtime occurrence rather than a stored record.
- The capability is named `EventTarget`, matching [Modularity → Event as a Module Capability](../../knowledge/modularity/modularity.md#event-as-a-module-capability), and belongs to the Type or Module that exposes it. A bare `Target` says nothing about events in a body of source where every other event name is qualified.
- `EventListener` has exactly one mandatory member, `EventHandler`.
- The ecosystem's `capture`, `once`, `passive`, synchrony, and abort-signal are not members of either abstraction: each is a property of a registration rather than of a listener, and `capture` additionally names a target tree this protocol does not have.
- A dispatch sees the listener set as it stood when it began, so a handler cannot change what the rest of the dispatch sees.
- A dispatch's `Error` carries the dispatch's own failures and not its handlers', by the [Error versus Log](../error/error.md#boundary-discipline) separation applied at the dispatch rather than at a layer crossing.
- A target accepts only the kind of event it declared, through a specialization that composes narrower event and listener abstractions rather than through a type parameter — the shape Abstraction → Behavior Over Type Identity (`docs/khayyam/abstraction.md#behavior-over-type-identity`) gives a constrained contract in a language with no type-parameter form. The *N*×*M* cost of writing specializations out is stated in the document rather than left to a reader's discovery.

Alongside it:

- `EventTarget` replaced the bare `Target` across the sources, and `Target_Race_Event` became `Race_EventTarget` in a file renamed to `event-target-race-event.kh` to match its declaration. Its three methods lost a `Process_` prefix nothing in the sources justify. The Go residue was carried with the rename so the stale spelling is not read back out of it later.
- The language server now publishes `unbound-type-name` for a name a document uses and nothing in it supplies. The compiler gate refuses the same names, but it walks inclusions first and returns on the first failure, so on this repository as it stands it never reached that question; the editor's answer is the one that would have caught the hand rename.

#### A specialization belongs to the module that exposes it
- State: the first draft placed `Target_Race_Event` in this protocol's own folder, renamed it `EventTarget_Race_Event`, and priced the `N*×M*` cost of writing specializations out as a cost this protocol carries. Both were wrong. The module boundary was wrong first — the race module is built on the Event concept and must not be able to add a declaration to the protocol it is built on. The declaration itself was then found to be unsatisfiable, which is the owner's own objection and stronger than a boundary argument: `docs/khayyam/abstraction.md` holds that a capsule satisfies an abstraction only when each method's influencing-variable types match **exactly**, with the receiver the one thing permitted to differ. `Race_Event` is not `Event`, so `DispatchEvent` narrowed to `Race_Event` satisfies nothing, and the detector composed beside it could never be a `Detector`.
- What is there instead: `modules/process/race/protocol/event.kh` declares `Race_Event` in the race module, `modules/process/race/protocol/detector.kh` composes `EventTarget` directly, and `modules/process/race/race-event-target.kh` is a capsule satisfying it with the capability's own signature and recognizing the occurrence in its dispatch. The cost is a run-time check where a narrowed signature would have had a compile-time one, and that trade is now written where a reader meets it: [How a target narrows to one kind of event](./event.md#how-a-target-narrows-to-one-kind-of-event).
- Consequence for the document: the *N*×*M* paragraph is gone rather than revised, and the protocol's surface is `Event`, `EventListener`, and `EventTarget` with no fourth name in it.
- Rule: `modules/khayyam/rules/composition-not-duplication/composition-not-duplication.md`, which states the standing condition so this need not be re-derived — and which found, on measurement, one further instance in the sources that is reported and not fixed.

#### Files removed, and where each thing went
- Removed, with nothing left to carry them: `modules/process/event/target.kh` (the Go `Target[E]` struct) — its Khayyam realization is `modules/process/race/race-event-target.kh`, the parts the declarations above it did not carry are in that file's own Go clue block, and the initial-capacity constant it seeded its listener list from is still `modules/process/event/const.kh`, pending the owner's decision on where a capacity belongs.
- Removed: `modules/process/event/protocol/target-race-event.kh`, which held `Target_Race_Event` — superseded, per the entry above, by composition.
- Removed: `modules/process/event/tests/target.kh`, which held one Go line asserting `event_p.Target[*Event] = &Target[*Event]{}` — the Go idiom for a satisfaction assertion, which Khayyam has no syntax for. Its obligation is carried by `tests/event-target.kh`, in the form [Test → The Form the Expectation Takes Is the Domain's](../test/test.md#the-form-the-expectation-takes-is-the-domains) gives a domain with no runner.
- Removed: the Go clue block at the foot of `modules/process/event/protocol/event-listener.kh`, and with it the five commented members `Synchronous()`, `Capture()`, `Once()`, `Passive()` and `AbortSignal()`. **These were not dropped.** Each is named and rejected under *Considered and not done* below, with the argument; the question of whether a **registration** is a concept this protocol declares — which is where a kept one of the five would live, and which `AddEventListener`'s bare `EventListener` parameter leaves unstated — is carried in the [handoff](./event.handoff.md). Their prose survives in the committed history at `git show 6f8bf9e:modules/process/event/protocol/event-listener.kh`.
- Removed: `modules/process/race/protocol/event-target-race-event.kh` and `modules/process/race/protocol/event-listener-race-event.kh`, both of which existed only for the length of this change.
- Every one of these was committed at `6f8bf9e`, so none is lost to a reader who knows to look: `git log --diff-filter=D -- <path>` names the commit that removed it and `git show 6f8bf9e:<path>` names the content.

#### Considered and not done
- **Five listener members from the ecosystem's own vocabulary.** Considered carrying `capture`, `once`, `passive`, a synchrony declaration, and an abort signal on `EventListener`, each as an opt-in member a listener could decline to implement. Rejected because the properties do not belong to the listener: a registration states them, one listener may hold several registrations, and a member a listener must carry is a member that is true of one of its uses and false of another. `capture` fails a second test — it names a position in a target tree, and a participant that reacts to an occurrence does not become part of the process that produced it.
- **A `Synchronous` member on the target rather than the listener.** Considered as the way to make blocking explicit, since a listener that blocks the caller is the case the sources' own residue warns about. Rejected because [Process → Events](../process.md#events) assigns synchrony to the dispatch mechanism, and what the protocol can require is the consequence rather than the value: a listener may not assume the caller's state is unchanged, and a caller may not assume its own continuation is unaffected.
- **A type-parameterized `EventTarget[E]`.** Rejected as the protocol's shape because an abstraction's signature may name only abstractions and because the language's stated position asks why a requirement exists before asking how to spell it — where a constraint is the language's own, a written specialization is not evidence the constraint was architectural. The requirement and its price are both stated in the document so the polymorphism discussion meets a concrete case.
- **Naming the abstraction for the capability, leaving the bare name to the capsule.** Considered under the qualified names rule (`bundles/khayyam/rules/qualified-names/qualified-names.md`)'s ruling that between an abstraction and a capsule one module path names alike the abstraction keeps the name — which, read literally, would have left `Target` as the abstraction's name and renamed the capsule instead. Rejected because the name is settled upstream: [Modularity → Event as a Module Capability](../../knowledge/modularity/modularity.md#event-as-a-module-capability) already names the capability `EventTarget`, and a name that says nothing about events fails the rule on collision grounds before taste is reached.
- **Settling `Equivalence` over occurrences here.** Considered answering it from [The Error → Identity and equality](../error/error.md#identity-and-equality), whose argument against a declared `Equivalence` reaches `Event` almost literally. Left open instead, because the case that differs — two occurrences of one kind really are two things — turns on whether Memar asks "have I already seen this occurrence" at all, which is a question about the framework rather than about this protocol.
- **A practice companion.** Not written; the protocol states no followable procedure, and [documentation-practice.practice.md](../../knowledge/documentation/practice/practice.practice.md) holds a practice file back when the procedure is one or two sentences.

#### What the one-command rename still needs
The sources rename was carried out by enumerating every consumer by hand and correcting each. That is the failure the owner's request names: the enumeration is the work, and it does not scale past one abstraction. modules/khayyam/targets/go/renames.py (`bundles/khayyam/targets/go/renames.py`) is the existing precedent — dry by default, plan before write, a frontend check as the safety net — but it is driven by a hand-written name list and it deliberately leaves the Go residue blocks alone, so it renames names someone already knew to be colliding rather than a declaration and its dependents. What a command would need that nothing in the tree has: an occurrence index from a declaration to its use sites, and a workspace enumeration to build it from. Neither exists, and [Language Server Protocol `textDocument/rename`](https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#textDocument_rename) cannot be the answer in the editor yet — every `in` in every file is refused for want of a manifest, so a cross-file rename has no resolver to ask.

---

### Two handoff entries the protocol and the language already answer are removed

- Time: 2026-10-04T21:05:39Z
- Type: Changed
- Cited:
  - [Event → What this protocol does not claim](./event.md#what-this-protocol-does-not-claim) — Evidence: a handler's effect on its own dispatch is bounded by the listener-set rule and by whatever the dispatch mechanism states, which is the ruling the re-entrancy entry was asking the owner for.
  - [Event → How a target narrows to one kind of event](./event.md#how-a-target-narrows-to-one-kind-of-event) — Evidence: the cost that carries is a run-time check rather than a multiplication of declarations, and the protocol's surface is three names with no specialization among them.
  - Polymorphism in Khayyam → Abstract (`docs/khayyam/polymorphism.md`) — Evidence: the language's ruling that it rejects generic type-parameter syntax, which is the half of the specialization entry that belonged to the language rather than to this protocol.
- Propagates to:
  - Polymorphism in Khayyam (`docs/khayyam/polymorphism.md#abstract`): Done — no change needed; the position the entry pointed at is already the language's, for every case rather than this one.
- Contributors:
  - [Space Bunny Alpha](../../../CONTRIBUTORS.md#space-bunny-alpha) (space-bunny via [OpenCode](../../../CONTRIBUTORS.md#opencode)) — argued, applied

#### What changed
- `event.handoff.md`: two entries are removed.
  - *A handler that registers against the target it is being dispatched to deadlocks* — the entry asked whether the protocol owes an explicit statement that a handler must not re-enter its own target, or whether that is the dispatch mechanism's rule to state. The protocol answers it: what a handler may do to the dispatch is bounded by the dispatch's own listener-set rule and by whatever the dispatch mechanism states, and the protocol adds no sandbox claim it could not keep. The copy-then-iterate shape the entry described is therefore a mechanism decision the protocol already declines to own.
  - *What does the specialization cost, and does the language owe a type-parameter form?* — the entry recorded that the cost belongs to the exposing module rather than to this protocol, which `event.md` states, and that the language-level half belongs to the polymorphism discussion. Both halves are answered: the protocol's surface is `Event`, `EventListener`, and `EventTarget` with no specialization among them, a type-parameterized `EventTarget[E]` is rejected as the protocol's shape, and the language rejects generic type-parameter syntax outright. What remains is the run-time-check cost the protocol states, which is not a question.
- No base-document body changed, and no `## Anticipated Work` line was removed: the dispatch-mechanism line still carries the synchrony and visit-order work those other entries hold open, and no line scheduled either removed entry.
- The remaining ten entries are untouched, including the registration-type entry whose premise the paired changelog records as carried forward here.

---

### Four further handoff entries the protocol and one source now answer are removed

- Time: 2026-10-05T09:34:04Z
- Type: Changed
- Cited:
  - [Event → What an Event Is](./event.md#what-an-event-is) — Evidence: `Observer_Time` supplies when the fact occurred, which fixes the composed time to the occurrence rather than to the notification.
  - [Event → Why capture, once, passive, and synchrony are not members](./event.md#why-capture-once-passive-and-synchrony-are-not-members) — Evidence: the corollary naming where the five belong — the dispatch mechanism's parameters and its registration's parameters, on a registration type a system with them states for itself.
  - [Event → What this protocol does not claim](./event.md#what-this-protocol-does-not-claim) — Evidence: the protocol adds no sandbox claim it could not keep, which is the ruling the aggregate blocking-listener question was reaching for.
  - `modules/gui/protocol/event.kh` — Evidence: `Event_Methods` is declared in the GUI's own protocol file beside `GUI_Event_2` and carries one GUI-only member, `PreventDefault`.
- Propagates to:
  - `modules/gui/event.kh:18,56`: Pending — the two `memar:impl` comments still name `memar/process/event/protocol.Event_Methods`, an address under this module's path that no file declares; `Event_Methods` is the GUI's own abstraction, so the comments should name it under the GUI's path. The defect is separately recorded at `modules/README.handoff.md:49`. Not this chat's file.
- Contributors:
  - [Space Bunny Alpha](../../../CONTRIBUTORS.md#space-bunny-alpha) (space-bunny via [OpenCode](../../../CONTRIBUTORS.md#opencode)) — argued, applied

#### What changed
- `event.handoff.md`: four entries are removed.
  - *Should `Event`'s Time be the occurrence's or the dispatch's?* — the entry asked which of the two the composed `Observer_Time` is, and recorded what each choice would cost on redelivery. The protocol states it: the abstraction supplies when the fact occurred. Redelivery therefore preserves the time rather than restamping it, which is the consequence the entry named, and it is now stated rather than open.
  - *Does the protocol owe a registration type, and do any of the five belong on one?* — the entry recorded that the argument for keeping the five out was whole as it stood and said nothing about what happens to them, and set the two branches: either the protocol declares a registration and the questions it must answer become a contract, or the sentence saying the five are the mechanism's goes into [The EventListener contract](./event.md#the-eventlistener-contract). The second branch is what happened: the section now says where the five belong and that a system having them states them in its own dispatch contract and its own registration type. No registration is declared, and none is owed.
  - *Is `Event_Methods` this protocol's `EventHandler` under an older name?* — the entry marked this a fact to be read rather than a judgment to be made. Read: `Event_Methods` is declared in the GUI's own protocol file and its one member is `PreventDefault`, a DOM cancelation call this protocol has no use for, so it is not this protocol's listener-methods abstraction under an older name. What follows is a wrong address in two residue comments, recorded under Propagates to.
  - *Does the protocol owe anything about a handler that blocks or misbehaves?* — the entry separated the individual obligation, which [Process → Events](../process.md#events) already permits, from the aggregate, and left the aggregate open. The protocol now declines the aggregate by name, in the same list where it declines a narrowing of the capability and a representation.
- No base-document body changed, and no `## Anticipated Work` line was removed: the dispatch-mechanism line still carries the synchrony and visit-order work those entries held open, and no line scheduled any of these four.
