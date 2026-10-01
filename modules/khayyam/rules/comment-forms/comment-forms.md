---
Title: "Khayyam Rule — Comment Forms"
Status: Draft
Start Date: 2026-09-26
ID: "497328"
---

# Khayyam Rule — Comment Forms
Khayyam's rules live one rule per folder under [`modules/khayyam/rules/`](../README.md), and this is the rule for the comment forms this repository's toolchain recognizes. It is a rule of a tool, not a statement of the language: [Khayyam → Language Keyword in a Glance](../../../../docs/khayyam/khayyam.md#language-keyword-in-a-glance) fixes the declarations a program may contain, and how a tool reads the prose between them is the tool's own condition over the characters it is given.

## The rule
- `//` runs to the end of the line.
- `/*` runs to the first following `*/`; block comments do not nest, so the first `*/` closes whichever comment is open.
- An unterminated block comment is refused, beside an unterminated string.
- A comment is trivia: it contributes no declaration, no field, no composition entry, and no command, and it may stand wherever trivia may stand — including inside a `cp`, `ab`, `sc`, or `mt` block. In particular, a `//` line inside an `ab` composition block is not a composition entry.

## Why it exists
A scanner has to answer for every character a file carries, and `//` and `/* … */` are this toolchain's answer. The rule exists so that the answer is a decision on record rather than a property of the implementation: both forms were already implemented before anything stated why, in the scanner here and in the TextMate grammar under `.agents/vscode/extensions/khayyam-language/`, so each had chosen privately and the two choices agreed by accident. A rule an organization can keep or drop is still better than an accident, because the next toolchain's author can see the choice, disagree with it, and write down their own.

## Keep it or drop it
An organization may keep this rule, answer it differently, or drop it: a second toolchain is free to nest block comments, to add a third form, to require a header, or to refuse comments outright — that last being the direction this repository's own library is being taken, where every type's human-readable text is a value one of its own methods writes. What is not free is reading one repository's `.kh` files under two different comment rules without saying which is which.

## What this rule does not claim
- It does not claim the language states a comment form. The language documents none; this document is where the choice lives instead.
- It does not claim what a comment says, whether a file carries one, or how much a declaration is written down — that is the [comment policy rule](../comment-policy/comment-policy.md).
- It does not claim this repository's forms are the right ones. It records the ones this toolchain uses.

## Open questions
This rule's own open state lives in its [handoff](./comment-forms.handoff.md).
