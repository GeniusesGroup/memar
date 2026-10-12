# Time Handoff
Open work for `modules/time/time.md`. Entries are mutable current state — revised as each item moves, removed when it resolves or is dropped. See [documentation-handoff.md](../../documentation-handoff.md) for what a handoff is.

## Open Questions

### The Instant representation
- State: width, range, precision, and whether a monotonic source is part of the contract — blocked on the definitional question below and on the runtime substrate questions of [Concurrency Realization](../computer/concurrency.handoff.md).
- Next: settle after the substrate and definitional items move.

### Is there a common concept over the duration units?
- State: settled: no such concept is admitted. [A concept is an abstraction; a concrete instance is a capsule](../../khayyam/abstraction.md#a-concept-is-an-abstraction-a-concrete-instance-is-a-capsule) states that what a contract names is the concept and that "the unit or width it is measured in is the implementation's to choose, finer-grained, and never a floor the contract must meet", and [A contract states a duration, not a unit](time.md#a-contract-states-a-duration-not-a-unit) says the same of this protocol: the contract keeps the magnitude asked for and gives up only the measure it is expressed in. A resolution concept would be exactly the floor both passages rule out, so the one-directional conversion objection is answered by refusing the question rather than by a narrower abstraction. Residue: `NanoInSecond` is already held as an instance of `Duration` under `modules/time/duration/` although what it names is a component of a decomposed instant rather than a span on its own, which the ruling that made it an instance did not argue.
- Blocks continuation: nothing. No contract in the sources states a resolution today, and none is to.
- Next: owner ruling on `NanoInSecond` alone — whether it remains an instance of `Duration`, becomes an instance of `Instant`, or is something else. Every contract names `Duration`.

### Does any contract need a timer that also reports the instant it fires at?
- State: the Go monomorphization `Timer_Time_Timer_Status` was removed from `modules/time/timer/protocol/timer.kh` on 2026-09-26: no contract named it, and the timer's status is already `Timer_Status` in `modules/time/timer/protocol/timer-status.kh`. Whether a contract needs a timer that also reports the instant it fires at was left unasked by that removal.
- Next: owner ruling; until then the timer contract reports status only.

### Distributed ordering versus the Instant contract
- State: how causality and ordering guarantees across components relate to the Instant contract belongs with [GP](../net/giti.md) and [sRPC](../net/sRPC.md); not settled here.
- Next: joint session with the networking protocols.

### Does Time warrant a fuller concept document?
- State: currently the separation rule is the permanent home; whether a dedicated concept document earns its place is undecided.
- Next: revisit when the representation design starts.

### What protects a time-limited value from a clock that moves?
- State: this document keeps monotonicity out of the contract on purpose, listing it among the richer semantics that belong to [networking](../net/networking.md) and [process](../../process.md) rather than being smuggled into the Instant contract, and the representation itself is open above. The owner's position, recovered 2026-09-30 from an audit of Omid Hekayati's Go-community Telegram-group messages (Gommunity), is that this deferral is safe for instants that record *when* something happened and unsafe for a value whose validity is a window: a one-time code, a signed grant, a session bound to a deadline. Measured against an origin outside the system's control — a unix-epoch instant corrected by time synchronization or set by a user — such a window can be extended or ended without any elapsed real time passing, which turns a validity period into a request. The owner's stated instrument is a monotonic source, whose origin is the system's own start.
- Candidate source: the owner's own standing question, recovered 2026-10-04 from a retired session note and unexamined since - a library helper named `relativetime` in [go-zero](https://github.com/zeromicro/go-zero) (`core/timex/relativetime.go`) raises the question in its own shape: is a relative-time computation ever an acceptable source for a deadline, or is a monotonic source the only acceptable one? The file has not been read, so what is registered here is the question and where to examine it, not a finding.
- Question for the owner: is this a rule of this protocol — a contract that bounds validity states which source its deadline is measured against — or a rule each protocol repeats where it issues something expiring? And can the requirement be stated as a constraint on the contract while [The Instant representation](#the-instant-representation) stays open, or does it wait for that answer?
- Next: state it before the first expiring credential is designed; [SDK → The agreement artifact for delegation](../process/service-sdk.handoff.md#the-agreement-artifact-for-delegation) and the revocation question beside it are the first cases that would need it, and a contract written without the answer has no way to say which clock it trusts.

### The unix realization declares nothing, so this module's protocol has no implementer
- State: `modules/time/unix/` holds `now.kh`, `atomic.kh`, `epoch.kh`, `const.kh` and `time.kh` and carries no `tp`, `cp` or `vr` line in any of them, so nothing implements the four declarations of this module's own protocol: `Time` at `modules/time/protocol/time.kh:9`, `SecondElapsed` at `:15`, `NanoInSecondElapsed` at `:19`, and `Time_Stringer` at `:22`. [Realization membership](time.md#realization-membership) puts a declaration under `modules/time/` when its subject is time itself — an instant and the epoch or clock it is read against — so both the contract and the missing realization are this module's rather than a neighbour's, and [Math](../math/math.md) is not the owner merely because a duration is a number.
- Blocks continuation: nothing in the toolchain — nothing resolves the contract today. It does block reading [The Instant representation](#the-instant-representation) against a candidate realization, because there is none to read it against, and the tree already holds two sibling folders — `modules/time/monotonic/` and `modules/time/epoch/` — that declare what this one declares nothing of.
- Next: owner ruling on whether `modules/time/unix/` is written as the unix clock realization of this contract or retired in favour of a sibling; nothing is written before that ruling.
- Carried from: [Go Target Research 001 → Live problems the two archives jointly expose](../../../bundles/khayyam/targets/go/target.research.001.md#live-problems-the-two-archives-jointly-expose--defects-in-the-sources-and-where-each-one-was-routed), verified 2026-10-02 and routed here 2026-10-08.

### `maxWhen`, `verifyTimers` and `heapAry` are archived, and the heap's even-arity invariant has no live home
- State: the three constants exist only inside the archived Go block of `modules/time/timer/const.kh:12-20` — `maxWhen` as the maximum for a timer's `when` field, `verifyTimers` as the switch that adds heap-validity checks, and `heapAry` as the default heap arity, which the same comment requires to be an even number. Nothing live declares them and nothing live reads them, so nothing is broken today; what is lost is the invariant, which survives only as a sentence in residue. A mechanism that waits on an instant or a span is named as this module's own subject by [Realization membership](time.md#realization-membership), so the timer's realization belongs here whatever else the timer grows.
- Blocks continuation: nothing in the toolchain. It does block writing a timer realization against the arity, since the one statement of the requirement is a comment, and [Does any contract need a timer that also reports the instant it fires at?](#does-any-contract-need-a-timer-that-also-reports-the-instant-it-fires-at) is a question about the same contract.
- Next: owner ruling on whether the even-arity rule belongs in a contract or in the timer's own realization, then the three constants written where that ruling puts them. [A contract states a duration, not a unit](time.md#a-contract-states-a-duration-not-a-unit) bears on the same boundary: it keeps a unit out of the contract.
- Carried from: [Go Target Research 001 → Live problems the two archives jointly expose](../../../bundles/khayyam/targets/go/target.research.001.md#live-problems-the-two-archives-jointly-expose--defects-in-the-sources-and-where-each-one-was-routed), verified 2026-10-02 and routed here 2026-10-08.

## Anticipated Work
- The Instant representation design.
- The distributed-ordering treatment alongside the networking protocols.
- The definitional discussion's own record, if the project chooses to publish it.
