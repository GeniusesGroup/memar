---
ID: 20261026-T200841Z-21460
Title: Rules that make every task develop abstractions first in Khayyam, tests before code, and keep documents free of code; enforce them in the Memar skill
Status: Complete
Start Date: 2026-10-26T20:08:41Z
Project: C:\Sync\Persons\Geniuses.Group\github.com\memar
Parent: 20261023-T074642Z-5420
Conversation: 20261022-T182206Z-3248
Priority: 10
Labels:
  - design(01a14a04-6531-73d5-8eeb-6e37ddce016d)
---
# Rules that make every task develop abstractions first in Khayyam, tests before code, and keep documents free of code; enforce them in the Memar skill

## Request
The owner (Omid Hekayati, 2026-10-26) found that the memory-layer task (20261023-T074642Z-5420) was built against Memar's own principles: code first; a 64-line `modules/computer/memory/store/store.md` that restates a Python contract; a 158-line `modules/computer/memory/store/protocol/store.py` whose error type `Unavailability` sits in `protocol/` and not in an `errors` folder; protocols and abstractions written in Python when they are to be developed in Khayyam (stable enough to replace the Markdown documents); comments in code; sub-agents that wrote services without tests first or ran suites for 30 minutes; every sub-agent run on the strongest model. He wants the fault stopped for **every** task, not repaired in one: hard rules in `modules-plugable/management/task/rules/` that the Memar skill (`.agents/skills/memar/SKILL.md`) makes every agent carry out.

Write, as rules in that folder (one rule per folder, as the existing ones stand; read `modules-plugable/management/task/rules/README.md` and two neighbours first), and make the skill, `memar task ensure --help` and the contexts the tools print cite them (each rule written once, cited elsewhere, as `model-follows-need` is):
1. **Abstraction first.** Before any code of a requirement, the skeleton of its abstraction is written in Khayyam (the types, their `detail.kh` methods per `modules/computer/type/protocol/detail.kh`, the services per `modules/process/service/protocol/service.kh` and `modules/process/services/protocol/services.kh`) and approved by a fresh agent that did not do the work (the reviewer rule), and by the owner where the existing rules send it to him; no code of the requirement is committed to a module before. Protocols and abstractions are Khayyam, not Python and not Markdown; Python is a realization of a stated abstraction.
2. **Errors** of a module are declared in its `errors` folder, not in `protocol` (see how existing modules do it, for example `modules-plugable/computer/memory/store/index/errors`).
3. **No comments in Khayyam code**; what a type says of itself is said by its `detail.kh` methods, and every type follows them. Settle with the owner's wording whether the ban reaches Python and other realizations (recommend: the same, a reason written only where `A Fact in Code Is Written Once` allows it).
4. **A document does not restate code** (`modules-plugable/knowledge/documentation/documentation.md#a-fact-in-code-is-written-once`): a check that finds a document whose sections only describe a file's members.
5. **Tests before code, for every service however small, and tests are scoped**: the check run after a change is the tests of the module changed (and its declared dependents), never the project's whole suite; a test has a stated time budget; a run longer than it is stopped and reported, never waited on for hours; the delegating agent reads the red run before it accepts a green one. Say where a module's tests state their budget and how a runner stops a process over it.
6. **The model of a sub-agent follows `model-follows-need`**: a delegated plan states who checks the result; the delegating agent names the lowest level the rule allows and never the strongest by habit (the delegations of 20261023-T074642Z-5420 all ran on the strongest model, a fault). Strengthen that rule or the delegation rule only where it failed.
7. **Hand-backs**: where the harness refuses a sub-agent's report write, the delegating agent writes it; say so in the delegation rule.

Also write an audit in `docs/`: which of these rules the output of 20261023-T074642Z-5420 and its four sub-tasks (20261026-T144222Z-11720, 20261026-T150608Z-8256, 20261026-T181945Z-16468, 20261026-T192807Z-36152) breaks, file by file, as the input of the queued task "Redo the memory store contract". Do not edit the memory files; that task does.

Model facts (`model-follows-need`): the owner reviews the rules in person; the judgment is open (deciding what the rules are); an error is costly because every task works by them: standard level.

## Check (done when)
The rules exist and `memar content check` on them is clean; the skill, `memar task ensure --help` and the printed contexts cite them; the audit is in `docs/`; a fresh sub-agent that did not write them reviewed them against this Request and its findings are applied; the changes are committed in a few commits by folder with `_host_git_cli.py` after `memar content check` (leave out files with problems that are not yours; the checkout holds many uncommitted files of other tasks: never touch them).

## Report shape
Standard `report.md`; at most 10 lines under `## Decisions needed` for what only the owner can settle.

## Why
The owner's trust, and the cost of fixing bad work later, which is higher than writing it well first. Priority 10.

## Steps
1. (local) Read the existing rules, the skill, `documentation.md#a-fact-in-code-is-written-once`, `detail.kh`, the reviewer and delegation rules.
2. (local) Write the audit; draft each rule (Markdown documents with changelog records, as the folder does).
3. (delegated, fresh reviewer, kind critique) Review against the Request.
4. (local) Apply findings; update the skill and printed contexts; check; commit.

## Next
Step 1.
