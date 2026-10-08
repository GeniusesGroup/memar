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

## Anticipated Work
- The Instant representation design.
- The distributed-ordering treatment alongside the networking protocols.
- The definitional discussion's own record, if the project chooses to publish it.
