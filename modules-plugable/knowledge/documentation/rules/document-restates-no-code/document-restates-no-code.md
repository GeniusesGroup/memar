---
Title: "Documentation Rule — A Document Restates No Code"
Status: Draft
Start Date: 2026-10-30
---

# Documentation Rule — A Document Restates No Code
A rule of this repository, held for [Documentation](../../documentation.md), which owns the claim in [A Fact in Code Is Written Once](../../documentation.md#a-fact-in-code-is-written-once). This rule states the check a reviewer applies to a document.

## The rule
- **A section whose sentences only describe a file's members** (its functions, fields, signatures, cases or values) is a copy of code. It is removed, or replaced by a link to the file.
- **A document says what its code cannot:** the reason, the trade-off, the audience and the history.
- **A document written for software is written after its abstraction in Khayyam,** not instead of it, and states only what the abstraction does not.

## Why it exists
The owner found a 64-line `store.md` that restated a Python contract. A restated fact has no way back to its source, and the next change to the code leaves it wrong while nothing fails.

## Keep it or drop it
An organization may document its code by restating it, and then keeps two places for each fact.

## What this rule does not claim
- It does not ban an example; [A Fact in Code Is Written Once](../../documentation.md#a-fact-in-code-is-written-once) separates real code from an example.
- Until a check exists that finds a document whose sections only describe a file's members (by taking the identifiers each section names and looking each up in the module's files), a reviewer applies the rule; `memar content check` does not.

Owed: documentation.restated-code-check
