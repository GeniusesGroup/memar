---
Title: "Type Rule — No Comments in Code"
Status: Draft
Start Date: 2026-10-30
---

# Type Rule — No Comments in Code
A rule of this repository, held for [Type](../../type.md), whose human-facing identity is written by the type's own methods ([Khayyam → Self-Documenting Code and Naming](../../../../../docs/khayyam/khayyam.md#self-documenting-code-and-naming)). It applies to code, in every language this repository's code is written in, and to nothing that is not code. It is held by Type because what a type says of itself is Type's, and the exception it admits is the documentation module's claim: Python is used only because it compiles and runs today, and no habit of it is wanted.

## The rule
- **Code carries no comment, except the license header below.** In Khayyam: no `//` line and no `/* */` block. In Python: no `#` line, and no docstring. In any other language: its comment forms.
- **What a type says of itself is said by its [`detail.kh`](../../protocol/detail.kh) methods** (`Summary`, `Overview`, `UserActionNote`, `DevActionNote`, `Domain`), and every type follows them. A comment is a second, unchecked place for the same fact.
- **The one exception is the license header** a file opens with, and any exception a rule of the owning module states for a reason that [A Fact in Code Is Written Once](../../../../../modules-plugable/knowledge/documentation/documentation.md#a-fact-in-code-is-written-once) allows: a trade-off, a history or a warning that no declaration can hold, never a statement of what the code does.
- **A new or changed file follows the rule;** older files are repaired when a task changes them, not in a sweep that touches files for no other reason.

## Why it exists
The owner's ruling of 2026-10-30: every Memar rule applies in every language. The memory-layer task (20261023-T074642Z-5420) wrote comments and docstrings beside its declarations. The Khayyam [comment policy](../../../../../bundles/khayyam/rules/comment-policy/comment-policy.md) allowed comments as a fallback until the methods exist; this rule is the direction that rule names, and the conflict is recorded in that rule's handoff.

## Keep it or drop it
An organization may allow comments in its code and remain conformant to Memar's concepts; it then keeps a second place for every fact a type says of itself.

## What this rule does not claim
- It does not claim the signature of the method that writes the text; that is still [open in Khayyam](../../../../../docs/khayyam/khayyam.md#self-documenting-code-and-naming).
- It is enforced by no check this repository runs today; the comment forms a scanner recognizes are the [comment forms rule](../../../../../bundles/khayyam/rules/comment-forms/comment-forms.md).
