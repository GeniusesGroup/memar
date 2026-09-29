---
Title: "Khayyam Rule — Commented Generic Bindings"
Status: Draft
Start Date: 2026-09-28
ID: 510445
---

# Khayyam Rule — Commented Generic Bindings
Khayyam's rules live one rule per folder under [`modules/khayyam/rules/`](../README.md), and this is the rule for a generic Go interface whose methods the port left in the clue block because their types were type parameters. It rewrites source; it is applied by `abstraction_bridge.py tidy --rule commented-generic-bindings` in [`targets/go/`](../../targets/go/abstraction_bridge.py).

## The rule
A Go interface in a clue block may declare type parameters, each a binding `NAME Constraint`, and methods that use `NAME` as a parameter or result type. When the constraint names one type, the binding fixes it: each such method becomes a Khayyam method on the abstraction that stands for the interface, with `NAME` replaced by the Khayyam name of that type.

- The type is resolved through the block's imports to the module it names, and among that module's abstractions to the one that stands for it under the [qualified names rule](../qualified-names/qualified-names.md). In `modules/time/timer/protocol/timer.kh`, `TIME time_p.Time` resolves to `Time` in `modules/time/protocol/time.kh`, and `ST TimerStatus` to `Timer_Status` in `modules/time/timer/protocol/timer-status.kh`. The `in` lines the new method needs are added.
- The method takes a bare name under the [receiver method names rule](../receiver-method-names/receiver-method-names.md), unless every method already on the abstraction carries the owner's name, in which case it follows them. Its receiver is named as the abstraction's other methods name it. Its parameter names follow the [result parameter names rule](../result-parameter-names/result-parameter-names.md). Its Go comments are carried above it.
- A binding that does not resolve to exactly one abstraction is left as a comment and reported; no type is invented. So is a method that uses a type parameter inside another type (`...ELEMENT`, `Iterator[K, V]`), a binding whose constraint is not a single type (`K Key[K]`), and an interface with no Khayyam abstraction standing for it.
- A type parameter whose constraint is open — `any`, `comparable`, or none — fixes no type and is not a binding. A method that uses only such parameters is left and counted apart; a method that mixes one with a binding is reported.

```khayyam
tp When mt (self Timer) () (t Time)
tp Status mt (self Timer) () (s Timer_Status)
```

## Why it exists
A Go interface parameterized by a type is, in every use the corpus makes of it, a contract whose type is fixed by its constraint: `Timer[TIME time_p.Time, ST TimerStatus]` means a timer whose `When` returns a time and whose `Status` returns a timer status. An abstraction-owned signature names abstractions ([Abstraction → What You Cannot Do](../../../../docs/khayyam/abstraction.md#what-you-cannot-do)), and the constraint is exactly the abstraction the signature names. Leaving those methods in the clue block leaves the contract incomplete for no reason the documents give.

## Keep it or drop it
An organization may write every such method by hand, or keep the generic parameters until Khayyam states a form for them. The rule applies only where the answer is mechanical, and reports the rest.

## What this rule does not claim
- It does not claim Khayyam has or lacks generics. It claims only that a constraint naming one abstraction is that abstraction in a Khayyam signature.
- It does not claim an open type parameter has a Khayyam form.
- It does not claim the resolved type is the one the author would choose; it is the one the constraint names.

## Open questions
This rule's own open state lives in its [handoff](./commented-generic-bindings.handoff.md).
