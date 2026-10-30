---
ID: 20261030-T051911Z-13004
Title: Develop the Rule domain: how rules are defined as code and with what abstraction, together with the Event domain
Status: Queued
Start Date: 2026-10-30T05:19:12Z
Project: C:\Sync\Persons\Geniuses.Group\github.com\memar
Parent: 20261026-T200841Z-21460
Conversation: 20261022-T182206Z-3248
Priority: 5
Labels:
  - design(01a14a04-6531-73d5-8eeb-6e37ddce016d)
  - memar-modules(01a14a13-19fb-729d-838f-ca7b1fd0e043)
---
# Develop the Rule domain: how rules are defined as code and with what abstraction, together with the Event domain

## Request
The owner (2026-10-30) wants the Rule domain (`modules/process/rule/`) developed: how rules are defined, and with what abstraction, so that a rule is code as far as it can be ([A Rule Is Code Where It Can Be](/modules/process/rule/rules/rule-is-code/rule-is-code.md)) and not a text every agent must remember. He knows the problem has to be settled together with the Event domain (a rule reacts to events: a commit, a task closing, a file changing). Read `rule.md`, `rule.research.001.md`, the linter's authoring notation (`modules/computer/linter/linter.md#how-a-governance-rule-is-authored`), the Event module, and the queued task 20261024-T053310Z-22628 on the no-code rule mechanism, whose decision table this must reconcile with or take over. Write the abstraction in Khayyam first, as the [abstraction-first rule](/modules/computer/software/rules/abstraction-first/abstraction-first.md) says, and have a fresh agent approve it before any code.

**Check (done when):** the abstraction of Rule (and its link to Event) in Khayyam, approved by a fresh reviewer; `rule.md` and its handoff updated; the existing textual rules classified as wholly code, partly code or text with the reason; follow-up implement tasks queued; at most 10 lines under `## Decisions needed`.

**Model facts:** the owner reviews; the judgment is open; every rule in Memar rests on it: standard level, deep if the owner asks.

## Why
Seven textual rules were added in one task and nothing enforces them; the owner wants the rules themselves to be code.

## Steps
1. (local) Read the Rule and Event documents and the queued rule-mechanism task; record how they overlap.
2. (delegated, fresh reviewer, critique) Review the proposed abstraction.
3. (local) Apply findings, update documents, queue follow-ups.

## Next
Step 1.
