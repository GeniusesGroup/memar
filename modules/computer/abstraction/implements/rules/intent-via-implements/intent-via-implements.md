---
Title: "Implements Rule — Intent via Abstraction_Implements"
Labels: Draft
Start Date: 2026-11-14
---
# Implements Rule — Intent via Abstraction_Implements
Rules for [Implements](../../implements.md) live one rule per folder under [`rules/`](../README.md). This rule is the checkable condition for how a type declares the abstractions it intends to implement. The protocol is [`protocol/implements.kh`](../../protocol/implements.kh). Owner corrections of 2026-11-14 are recorded on task `20261114-T094324Z-22560`.

## The rule
- **Do not put a target abstraction's name in a capsule body to claim that the capsule implements it.** A bare line such as `Type_LifeCycle` inside `cp { … }` is not an intent declaration.
- **Do not compose `Abstraction_Implements` into a capsule body.** Intent is not declared by embedding that abstraction. A capsule satisfies `Abstraction_Implements` structurally by implementing `DeclaredAbstractions` with a matching signature ([Khayyam Abstraction → Satisfying an Abstraction](../../../../khayyam/abstraction/abstraction.md#satisfying-an-abstraction)).
- **`DeclaredAbstractions` fills its influenced `Abstractions` by `Push`.** [`Abstractions`](../../../protocol/abstractions.kh) composes [`Container_Push`](../../../../adt/container/protocol/push.kh). Each claimed target is `abstractions.Push(Target)(...)`. Do not invent a parallel add API, do not route through `Container_Add`, and do not introduce a realizing capsule in every caller only to call `Make` then `Add`.
- **An abstraction may carry owner-authorized intent metadata in a companion `<base>.implements.kh`.** The companion's DeclaredAbstractions names that abstraction as its receiver and lists intended targets by Push. For a service-specific request or response observer, the general observer is listed here; the specific observer declares GetRequest or GetResponse with its own service value type instead of composing that generic target. This companion is tooling metadata, not a default implementation of the abstraction's runtime behavior. Declared intent remains separate from structural conformance and establishes no general return-variance rule.
- **Opt-in and tooling-facing.** Implement `DeclaredAbstractions` only when a discoverable pre-completion signal is wanted. It is not a runtime seal and not a substitute for structural satisfaction of the claimed targets.
- **One method names every claimed target.** Domain-specific empty markers (for example `ImplError`) are not needed for disambiguation once `DeclaredAbstractions` returns the set; migrate such markers when those modules are next changed.

## Why
Structural satisfaction cannot signal intent before a capsule is complete. Composing the target — or composing `Abstraction_Implements` itself — into the capsule body was read as that signal and is the wrong construct. `Push` appends to the end with a minimal signature; `Add` chooses location by container logic and returns a count, which this intent list does not need ([Type → Implementation intent](../../../../type/type.md#implementation-intent)).

## Keep it or drop it
An organization may omit pre-completion intent signals and rely only on structural satisfaction; it then accepts that incomplete capsules are invisible to scaffolding tools.

## What this rule does not claim
- It does not change how structural satisfaction of the *claimed* targets is judged.
- It does not settle how the influenced `abstractions` value is constructed before `Push`, nor whether compile-time-only method bodies need the same Error discipline as run-time ones (Khayyam task `20261114-T120330Z-22560`).
- It is enforced by no check this repository runs today; a linter or codegen service may adopt it later.
