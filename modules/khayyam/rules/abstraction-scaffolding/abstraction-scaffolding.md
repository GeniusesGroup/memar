---
Title: "Khayyam Rule — Abstraction Scaffolding"
Status: Draft
Start Date: 2026-09-29
ID: "497409"
---

# Khayyam Rule — Abstraction Scaffolding
Khayyam's rules live one rule per folder under [`modules/khayyam/rules/`](../README.md), and this is the rule for linter and IDE assistance that reduces explicit-delegation boilerplate without adding grammar. It is a governance rule of this repository: [Abstraction in Khayyam](../../../../docs/khayyam/abstraction.md) states that satisfaction is implicit and delegation must stay explicit in source; this rule states what organizational tooling may generate or verify.

## The rule
The elimination of repetitive delegation boilerplate is offloaded to organizational linter and scaffolding tooling. A linter rule in this repository may:

- Detect when a capsule partially implements an abstraction's method set.
- Auto-generate missing delegation lines (scaffolding) when a developer intends to satisfy an abstraction.
- Verify that a delegation call targets the correct shared capsule.
- Warn when a developer appears to hand-duplicate shared logic instead of delegating.
- Scaffold all missing method signatures with empty bodies when abstraction implementation is intended.
- Issue proactive warnings when a capsule partially implements an abstraction in a context where full satisfaction is clearly expected.

Generated or suggested source remains explicit, linear, and free of compiler magic; tooling writes or proposes lines the author keeps.

Smart remediation when a compilation error occurs because a method exists only on an embedded capsule — suggesting the exact explicit delegation method — is part of the same family of assistance. For example, if `TcpServer` tries to call `.Log()` but only its internal `Logger` has `Log`, the linter suggests adding an explicit delegation method on `TcpServer`.

## Why it exists
Khayyam rejects implicit `impl` keywords and behavior transfer; without scaffolding, explicit delegation is verbose. Tooling that writes or verifies delegation preserves the language guarantee while keeping development ergonomic.

## Keep it or drop it
An organization may disable scaffolding, require hand-written delegation only, or use a different IDE workflow. The language does not require any of these assists.

## What this rule does not claim
- It does not claim the linter must implement every bullet today.
- It does not claim generated delegation changes what a program means without the author accepting the edit.
- It does not claim searchable `impl` blocks exist; discovery is tool-assisted graph traversal.

## Open questions
This rule's own open state lives in its [handoff](./abstraction-scaffolding.handoff.md).
