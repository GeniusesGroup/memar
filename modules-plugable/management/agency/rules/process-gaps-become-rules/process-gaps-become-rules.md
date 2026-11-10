---
Title: "Agency Rule — Process Gaps Become Rules"
Labels: Draft
Start Date: 2026-11-10
ID: 498421
---
# Agency Rule — Process Gaps Become Rules
A rule of this repository for what an agent does when ending a task, so a missing process rule does not recur on the next task.

## The rule
- **Before ending a task** (with its report and Status, as [A task ends with its report and Status](../../../task/rules/task-ends-with-report-and-status/task-ends-with-report-and-status.md) requires), the agent asks whether the work exposed a **process gap**: a step that Memar’s rules should have made automatic or obligatory, but that only the owner’s correction or an agent’s after-the-fact recall supplied.
- **If such a gap exists and no suitable rule already governs it**, the agent **adds the needed rule** in the module that owns the subject ([Which Module a Rule Belongs To](../../../../../modules/process/rule/rule.md#which-module-a-rule-belongs-to)), Draft unless the owner has ratified, and links it from that module’s rules index. Recording is not gated; removal is ([Documentation → Recording Is Not Gated; Removal Is](../../../../knowledge/documentation/documentation.md#recording-is-not-gated-removal-is)).
- **The lesson is also a content of the task** — typically `decision`, `changelog`, or `message` that states the gap and the rule path — so the timeline carries the lesson even if a later reader never opens the new rule file. The report’s left-open part names the rule path when one was added or is still owed.
- **A gap that is only this task’s instance** (no reusable process) is posted as task content and does **not** invent a rule. Prefer asking when the scope is unclear ([Ask rather than assume](../../../../../modules/knowledge/cognition/cognition.md#ask-rather-than-assume)).
- **Types and contracts the gap implied are declared in code** when the subject is software ([Document Restates No Code](../../../../knowledge/documentation/rules/document-restates-no-code/document-restates-no-code.md)): prose alone is not the closing of a process gap that needed a type or service surface.

## Why it exists
Owner (2026-11-10), from task `20261110-T102002Z-25056`: an agent stopped at prose for Format Adjuncts and waited for the owner to name missing types, manifest keys, and generator services. Later tasks must not depend on that recall. The same class of failure is a missing *process* rule about ending work itself.

## How a check would run
A task whose report or timeline records an owner correction of the form “you should have known / added a rule” and that ends without a new or cited rule path (or an explicit left-open that the rule is still owed) breaks this rule. No automatic check runs today.
