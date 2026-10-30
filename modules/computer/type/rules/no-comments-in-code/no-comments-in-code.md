# Task Rule — Code carries no comment; a type says what it is through its detail methods
Status: Draft

## The rule
- **Khayyam code carries no comment** (no `//` line and no `/* */` block; in Python no `#` line beyond the license line, and no docstring that says what the code does). What a type says of itself is said by its [`detail.kh`](../../../../../modules/computer/type/protocol/detail.kh) methods (`Summary`, `Overview`, `UserActionNote`, `DevActionNote`, `Domain`), and every type follows them; a comment is a second, unchecked place for the same fact.
- **The same holds for every realization of it, Python and any other,** with one exception: a reason is written in code only where [A Fact in Code Is Written Once](../../../../knowledge/documentation/documentation.md#a-fact-in-code-is-written-once) lets a reason stand there — a trade-off, a history or a warning that no declaration can hold, and never a statement of what the code does. A docstring that restates a signature or a member is a comment.
- **A new or changed file follows the rule; old files are repaired when a task changes them,** never in a sweep that touches files for no other reason.

## Why it exists
The owner's ruling of 2026-10-26, after the memory-layer task wrote its code with comments and docstrings beside its declarations. That the ban reaches a realization in another language is this text's stricter reading, stated for the owner to confirm; until he rules, it binds.

## How a check would run
Search a changed `.kh` file for a comment marker, and a changed realization for a comment or docstring that says what the code does. This repository runs no automatic check of it today.
