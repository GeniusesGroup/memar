---
Title: "Type Rule — Explicit Behavior Ownership"
Labels: Draft
Start Date: 2026-11-09
---
# Type Rule — Explicit Behavior Ownership
A rule of this repository, held for [Type](../../type.md), for the operational checks of [Explicit Behavior Ownership](../../type.md#explicit-behavior-ownership). It applies when designing, implementing, or reviewing methods on Types.

## The rule
- **Every method has exactly one visible owner.** Before touching shared behavior, answer from source alone: Where was this behavior defined? Why is it available on this component? Who owns it? If any answer needs an inheritance walk, a mental macro expansion, or documentation beyond the source, visibility has already failed.
- **Never default-implement.** If many components share logic, generate their explicit methods from the single source of truth — generated members must be visible and auditable.
- **Delegate visibly:** the delegating component's source names the target, so what, where, and why are readable in place. Navigating to the target's internals is for depth, not discovery.
- **Multiple delegation targets are fine** when each relationship is explicit in source.
- **No runtime injection:** dynamic proxies or reflection-added methods violate ownership — the source must reflect the full method set.
- **Generation and macro boundary:** if expanded behavior is not readable and navigable without special tooling, reject it or make it transparent.
- **Abstractions stay pure:** no default method bodies on an Abstraction; every implementing Capsule owns each required method explicitly.

## Why it exists
Absorbed from the former Type Practice companion; the Explanation states the principle, and this rule states the checks a reviewer runs.

## Keep it or drop it
An organization may keep implicit behavior transfer and remain outside this rule; it then accepts ownership ambiguity as a standing cost.

## What this rule does not claim
- It does not forbid Abstraction extension that transfers requirements without bodies.
- It is enforced by no check this repository runs today.
