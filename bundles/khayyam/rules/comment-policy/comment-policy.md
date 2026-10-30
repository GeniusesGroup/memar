---
Title: "Khayyam Rule — Comment Policy"
Status: Draft
Start Date: 2026-09-26
ID: "497329"
---

# Khayyam Rule — Comment Policy
Khayyam's rules live one rule per folder under [`bundles/khayyam/rules/`](../README.md), and this is the rule for what this repository's Khayyam sources carry in prose: the header every file opens with, and where documentation is allowed to live. It is an organizational rule, stated in the tool's own catalog because the tool is where an organization keeps the ones it holds itself to. How the prose is *marked* is a separate rule, the [comment forms](../comment-forms/comment-forms.md).

## The rule
- Every `.kh` file in this repository opens with the repository's license header, carried in a `/* … */` block comment, and the `LEGAL` reference it names is kept resolvable.
- A `.kh` file carries no other comment: a type's human-facing text — its name, its summary, the note a user or a maintainer reads — is a value one of the type's own methods writes ([Khayyam → Self-Documenting Code and Naming](../../../../docs/khayyam/khayyam.md#self-documenting-code-and-naming)), and a comment that says it is refused by the [Type Rule — No Comments in Code](../../../../modules/computer/type/rules/no-comments-in-code/no-comments-in-code.md), which owns that condition.

## Why it exists
The header is the one piece of prose every reader of a `.kh` file meets first, and a file that carries it and a file that does not are not two styles of the same thing — one of them is out of compliance with the repository's terms. The documentation clause that once allowed a comment where no documentation method existed was retired on 2026-10-30 at the owner's word: the ported sources' comments are repaired when a task changes a file, and no new comment is written.

## Keep it or drop it
An organization may drop the header and allow comments; it then keeps a second place for every fact a type says of itself, which the Type rule above is written against.

## What this rule does not claim
- It does not claim a comment form. That is the [comment forms rule](../comment-forms/comment-forms.md).
- It does not claim the language states anything about documentation, density, or headers; it states none of them.
- It does not claim that a comment is a bad way to write prose. It claims which prose lives where in this repository, today.

## Open questions
This rule's own open state — including the documentation-density question — lives in its [handoff](./comment-policy.handoff.md).
