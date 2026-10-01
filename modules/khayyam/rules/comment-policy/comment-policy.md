---
Title: "Khayyam Rule — Comment Policy"
Status: Draft
Start Date: 2026-09-26
ID: "497329"
---

# Khayyam Rule — Comment Policy
Khayyam's rules live one rule per folder under [`modules/khayyam/rules/`](../README.md), and this is the rule for what this repository's Khayyam sources carry in prose: the header every file opens with, and where documentation is allowed to live. It is an organizational rule, stated in the tool's own catalog because the tool is where an organization keeps the ones it holds itself to. How the prose is *marked* is a separate rule, the [comment forms](../comment-forms/comment-forms.md).

## The rule
- Every `.kh` file in this repository opens with the repository's license header, carried in a `/* … */` block comment, and the `LEGAL` reference it names is kept resolvable.
- Documentation is carried in comments where a documentation method does not yet exist for the thing being described.
- A type's human-facing text — its name, its summary, the note a user or a maintainer reads — is a value one of the type's own methods writes, not a comment. [Khayyam → Self-Documenting Code and Naming](../../../../docs/khayyam/khayyam.md#self-documenting-code-and-naming) states that mechanism; this rule is where the fallback lives while the methods are still being written.

## Why it exists
The header is the one piece of prose every reader of a `.kh` file meets first, and a file that carries it and a file that does not are not two styles of the same thing — one of them is out of compliance with the repository's terms. The documentation clause exists because the ported corpus arrived with 392 comment blocks that are, today, the only human-readable account of most of the abstraction layer; a rule that forbade comments before the methods existed would have deleted them, and a rule that said nothing would have let the comment become the permanent answer.

## Keep it or drop it
This is deliberately a rule an organization may drop, and this organization may be the one that drops it. An organization may forbid comments outright and require every type's human-facing text to come from its own methods — that is the direction the Khayyam library is being taken, and the declarations that shape takes are already in `modules/computer/datatype/protocol/detail.kh`. What may not happen by accident is the middle state this rule currently describes: comments as a permanent fallback, with the methods never written.

## What this rule does not claim
- It does not claim a comment form. That is the [comment forms rule](../comment-forms/comment-forms.md).
- It does not claim the language states anything about documentation, density, or headers; it states none of them.
- It does not claim that a comment is a bad way to write prose. It claims which prose lives where in this repository, today.

## Open questions
This rule's own open state — including the documentation-density question — lives in its [handoff](./comment-policy.handoff.md).
