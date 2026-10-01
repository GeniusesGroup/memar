---
Title: "Khayyam Rule — Unresolved Import"
Status: Draft
Start Date: 2026-09-26
ID: "497332"
---

# Khayyam Rule — Unresolved Import
Khayyam's rules live one rule per folder under [`modules/khayyam/rules/`](../README.md), and this is the first of the four import-resolution rules. It is a compiler-gate rule of this toolchain, not a statement of the language: [Khayyam → Import Mechanism (`in`)](../../../../docs/khayyam/khayyam.md#import-mechanism-in) states that the value is a URI, and what a tool does when the URI it names resolves to nothing is the tool's own condition.

## The rule
An `in` declaration whose URI resolves to nothing refuses the unit, with the implementation label `unresolved-import`. [core/src/frontend.ts](../../core/src/frontend.ts) checks this by reading the URI through the injected file system; the matrix's row is *an unresolvable import path (a URI with no file behind it)*.

## Why it exists
`in` is a routing operator, not a declaration of a dependency the reader can verify by reading the file. What the importing file asserts is that a named entity is available; if the URI names nothing, the assertion is unsupported and every downstream question — what type this is, whether it satisfies the abstraction the signature expects — becomes unanswerable. Refusing at that point keeps the semantic representation from carrying a name that means nothing.

## Keep it or drop it
An organization may keep this rule or drop it, and the honest form of dropping it is not "accept the file anyway" but "resolve somewhere this toolchain does not look": a build system that assembles the tree before analysis, or a resolver that materializes a missing URI from a cache. What may not be done silently is to accept a unit whose imports cannot be found, because the semantic representation would then be the carrier of an unbacked claim.

## What this rule does not claim
- It does not claim the language refuses an unresolvable `in`. The language states the path's meaning; the refusal is this toolchain's.
- It does not claim what a missing file means for a build — whether it is a compile error, a fetch, or a cache miss is a build policy, and the [manifest handoff](../../../../docs/khayyam/modularity.handoff.md) is where that is being worked out.
- It does not claim a diagnostic message, a diagnostic code, or a recovery behavior. The diagnostics contract is deferred, so the label above is an implementation label and nothing more.

## Open questions
This rule's own open state lives in its [handoff](./unresolved-import.handoff.md).
