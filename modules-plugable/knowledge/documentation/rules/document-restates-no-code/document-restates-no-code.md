---
Title: "Documentation Rule — A Document Restates No Code"
Start Date: 2026-10-30
---
# Documentation Rule — A Document Restates No Code
A rule of this repository, held for [Documentation](../../documentation.md), which owns the claim in [A Fact in Code Is Written Once](../../documentation.md#a-fact-in-code-is-written-once). This rule states the check a reviewer applies to a document.

## The rule
- **A document restates no type, field, edge, edge table, service signature, case or value that code (`.kh`, `.py`) declares,** in a table, a list or a sentence, whether the section holds other matter or not. It links to the file that declares it. A section that restates one is cut to a link.
- **A type that has no code yet goes to code first,** in its module's `protocol/` or `edges/` folder, and the document links to it; a model written as tables or prose in a `.md` is a design not yet finished, not a document.
- **A document says what its code cannot:** the concept, the reason, the trade-off, the audience and the rule.
- **A document written for software is written after its abstraction in Khayyam,** not instead of it, and states only what the abstraction does not.

## Why it exists
The owner found a 64-line `store.md` that restated a Python contract. A restated fact has no way back to its source, and the next change to the code leaves it wrong while nothing fails.

## Keep it or drop it
An organization may document its code by restating it, and then keeps two places for each fact.

## What this rule does not claim
- It does not ban an example; [A Fact in Code Is Written Once](../../documentation.md#a-fact-in-code-is-written-once) separates real code from an example.
- Until a check exists that finds a document that restates a file's members (by taking the identifiers each section names and looking each up in the module's files), a reviewer applies the rule; `memar content check` does not.

Owed: documentation.restated-code-check
