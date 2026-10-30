---
Title: "Rule Rule — A Rule Is Code Where It Can Be"
Status: Draft
Start Date: 2026-10-30
---

# Rule Rule — A Rule Is Code Where It Can Be
A rule of this repository, held for [Rule](../../rule.md), which says that a Rule's executable form lives in a module's `rules/` folder beside the normative claim ([Normative Claim and Executable Form](../../rule.md#normative-claim-and-executable-form)). This rule says how far the condition itself is to be code and not prose, by the presumption of [A Fact in Code Is Written Once](../../../../../modules-plugable/knowledge/documentation/documentation.md#a-fact-in-code-is-written-once): everything is code unless shown otherwise.

## The rule
- **The condition of a rule is stated as code as far as it can be:** a check, a declaration or a rewrite in the module's `rules/` folder, in Khayyam, that a tool reads and enforces. A condition a program can decide is not left as a sentence.
- **The text of a rule says what code cannot:** the subject, why the condition exists, who may keep or drop it, and what it does not claim. A sentence that only restates the condition its code states is a copy.
- **A condition that cannot yet be code is marked as owed** with an `Owed: <id>` line, so that the gap between the text and the check is found from both sides.
- **A new rule states which part of it is code and which is text,** and a rule written wholly as text says why no part of it can be code.

## Why it exists
The owner, on 2026-10-30, after seven rules were added in one task as text: Memar is accumulating textual rules that nothing enforces, and a rule only text asks every agent to read and remember it. How rules are defined, and with what abstraction, is the Rule module's development, not settled here; the event domain is expected to bear on it.

## Keep it or drop it
An organization may hold its rules as prose alone; it then relies on every reader to apply them.

## What this rule does not claim
- It does not claim the notation of a rule as code; that is open in [Rule](../../rule.handoff.md) and the linter's authoring notation.
- It is enforced by no check this repository runs today.
