# Time Handoff

Open work for `protocols/time/time.md`. Entries are mutable current state — revised as each item moves, removed when it resolves or is dropped. See [documentation-handoff.md](../documentation-handoff.md) for what a handoff is.

## Open Questions

### The Instant representation
- State: width, range, precision, and whether a monotonic source is part of the contract — blocked on the definitional question below and on the runtime substrate questions of [Concurrency Realization](../computer/concurrency.handoff.md).
- Next: settle after the substrate and definitional items move.

### Is civil conversion a framework-level concern at all?
- State: the political-churn argument (zone rules change by legislation) suggests it belongs to application-layer libraries, but GUI and scheduling components push back.
- State: the implementation tree already holds civil-calendar declarations — weekday names with per-language locales under `modules/time/utc/`, and calendar spans such as a month and a year under `modules/time/earth/` — so the question is live for existing code, not only for future design.
- Next: decide against the GUI and scheduling components' actual needs.

### Is there a common concept over the duration units?
- State: the counterpart of the numeric question in [Math Handoff → Is there a common abstraction over all numeric kinds?](../math/math.handoff.md#is-there-a-common-abstraction-over-all-numeric-kinds), at duration resolution rather than numeric width. `Duration` is the concept the unit instances share (`Second`, `NanoSecond`, and `NanoInSecond` under `modules/time/duration/`), and it is what every contract names today, so nothing is blocked by the absence of a narrower one; what is missing is a way for a contract to state a *resolution* — "a duration no coarser than a microsecond", or "the remainder of a second" — without naming an instance.
- The question: does such a concept exist, and what does it require? Two things any answer meets: units convert in one direction only ([A contract states a duration, not a unit](../time/time.md#a-contract-states-a-duration-not-a-unit)), so a contract asking for a resolution states a floor, which is the one direction the conversion does not guarantee; and `NanoInSecond` is already held as an instance of `Duration` although what it names is a component of a decomposed instant rather than a span on its own, which the ruling that made it an instance did not argue.
- Blocks continuation: nothing. No contract in the corpus states a resolution today, so nothing waits on the answer.
- Next: owner ruling, then a concept beside the units under `modules/time/duration/`. Until then the units stand as instances of `Duration` and every contract names `Duration`.

### Does any contract need a timer that also reports the instant it fires at?
- State: the Go monomorphization `Timer_Time_Timer_Status` was removed from `modules/time/timer/protocol/timer.kh` on 2026-09-26: no contract named it, and the timer's status is already `Timer_Status` in `modules/time/timer/protocol/timer-status.kh`. Whether a contract needs a timer that also reports the instant it fires at was left unasked by that removal.
- Next: owner ruling; until then the timer contract reports status only.

### Distributed ordering versus the Instant contract
- State: how causality and ordering guarantees across components relate to the Instant contract belongs with [GP](../net/giti.md) and [sRPC](../net/sRPC.md); not settled here.
- Next: joint session with the networking protocols.

### Does Time warrant a fuller concept document?
- State: currently the separation rule is the permanent home; whether a dedicated concept document earns its place is undecided.
- Next: revisit when the representation design starts.

## Anticipated Work

- The Instant representation design.
- The distributed-ordering treatment alongside the networking protocols.
- The definitional discussion's own record, if the project chooses to publish it.
