---
Title: "Khayyam Rule — Code Scope Placement"
Status: Draft
Start Date: 2026-09-26
ID: "497330"
---

# Khayyam Rule — Code Scope Placement
Khayyam's rules live one rule per folder under [`modules/khayyam/rules/`](../README.md), and this is the rule for where a code scope may be declared in the sources this repository's toolchain accepts. It is a compiler-gate rule of this toolchain, not a statement of the language and not a claim about what a Scope is: [Type → Scope — Type as Semantic Boundary](../../../../docs/type.md#scope--type-as-semantic-boundary) owns the category, and it states that the realizations sit at different levels.

## The rule
A `sc` declaration appears only inside a method body. A top-level `tp {name} sc { }` is refused by this toolchain with the implementation label `scope-placement`.

## Why it exists
A code scope is inert until a library-provided method drives it — [Khayyam → Scope](../../../../docs/khayyam/khayyam.md#scope) says so, and the reason is that the language ships no control-flow keywords of its own. A method body is where this repository's control flow is declared, so it is where a scope has something to be driven from. The rule is a tool's because that is as far as the argument reaches: the same reasoning, carried one step further, would forbid a file-level `sc` in *any* Khayyam, and no document makes a claim about the reach of every possible Khayyam.

## Keep it or drop it
An organization may keep this rule or drop it, and dropping it is a real option rather than a formality: the Scope category is not exhausted by a method body, and a language or tool with a namespace or module-visibility boundary has a Scope realization this rule forbids. A second toolchain accepting a top-level `sc` would be making its own rule, not contradicting this one.

## What this rule does not claim
- It does not claim the language restricts where a `sc` may be written. The language states no placement, and the sentence that once said otherwise has left the language documents.
- It does not claim the restriction is inherent to Scope. [Type → Scope](../../../../docs/type.md#scope--type-as-semantic-boundary) is the level at which a need for a boundary outside a Method would be reconsidered.
- It does not change what this toolchain does. [core/src/parse.ts](../../core/src/parse.ts) still refuses a top-level `sc` with the label `scope-placement`, [core/test/refusal.test.ts](../../core/test/refusal.test.ts) still carries the top-level refuse row under that label, and [core/test/form.test.ts](../../core/test/form.test.ts) the in-body accept row.

## Open questions
This rule's own open state — including the M1 limitation on what the accept row actually proves — lives in its [handoff](./scope-placement.handoff.md).
