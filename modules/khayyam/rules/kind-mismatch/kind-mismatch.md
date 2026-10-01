---
Title: "Khayyam Rule — Kind Mismatch"
Status: Draft
Start Date: 2026-09-26
ID: "497334"
---

# Khayyam Rule — Kind Mismatch
Khayyam's rules live one rule per folder under [`modules/khayyam/rules/`](../README.md), and this is the third of the four import-resolution rules. It is a compiler-gate rule of this toolchain, not a statement of the language: [Khayyam → Import Mechanism (`in`)](../../../../docs/khayyam/khayyam.md#import-mechanism-in) offers two line forms, a `tp` form and a `vr` form, and whether the form matches what the target declares is a tool's condition.

## The rule
An `in` declaration whose form disagrees with the declared kind of the named entity refuses the unit, with the implementation label `kind-mismatch`: a `tp … in` naming something the target declares with `vr`, or a `vr … in` naming something it declares with `tp`. [core/src/frontend.ts](../../core/src/frontend.ts) checks the declared form of the target declaration against the form of the inclusion.

## Why it exists
The two forms are not interchangeable spellings; they say different things about where the name comes from and what may be done with it. A type is a modeled concept that a signature may name; a variable is a value. Accepting the wrong form would import a name into a position where its meaning was never stated, and the error would surface as a type mismatch at some unrelated use — or, worse, not at all, since a name that resolves to something of the wrong kind can still look like a name.

## Keep it or drop it
An organization may keep this rule or drop it, and the way to drop it is to widen what an inclusion may name — a `vr` form that may also bring in a type, or a single form that names either. That is a language question, not a tool question, because it changes what a program may say; what a tool may do is decide whether to enforce the distinction its language draws, and an organization whose language draws none has nothing to enforce.

## What this rule does not claim
- It does not claim the language refuses a mismatched inclusion. It states the two forms and what each includes; whether they may be mixed is not stated.
- It does not claim a `vr` and a `tp` are the same kind of thing with different syntax. [Type → Type Categories Are Not a Hierarchy](../../../../docs/type.md#type-categories-are-not-a-hierarchy) is the level that owns that question.
- It does not claim a diagnostic message, a code, or a recovery behavior; the diagnostics contract is deferred and the label is an implementation label.

## Open questions
This rule's own open state lives in its [handoff](./kind-mismatch.handoff.md).
