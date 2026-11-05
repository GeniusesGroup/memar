---
Title: "Test Rule — Tests First and Scoped"
Labels: Draft
Start Date: 2026-10-30
---
# Test Rule — Tests First and Scoped
A rule of this repository, held for the [Test](../../test.md) protocol. Tests before the work is the protocol's own claim ([The Expectation Is Written Before the Work](../../test.md#the-expectation-is-written-before-the-work)); this rule adds how a run is bounded, which the protocol leaves to the organization. It applies only to work whose product is software, a throwaway script included; the protocol does not. The third and fourth clauses are the test step of [Modularity Rule — A Refactor Moves in Order](../../../../knowledge/modularity/rules/refactor/refactor.md).

## The rule
- **Every service has its tests before its code, however small,** and the new tests are seen to fail before any line of the service ([Test Practice → The Cycle](../../test.practice.md#the-cycle)). A service with no test of its own is not done.
- **The rule binds every script a task writes, not only Memar's own code.** A one-time script that moves, converts or repairs records is software: its pure parts (splitting, grouping, naming, the status it sets) are written as functions with their tests first, the tests are seen to fail, and only then the script that opens files and runs; the script runs a dry run before it changes anything. A task keeps such a script in its `services` folder and its tests in `tests` (never in a `docs` folder), and the delegating agent reads the red run before accepting the green one.
- **While the task is under way, a change is checked by its own unit tests only:** the test file of the service changed, one file per command. The tests of the modules that import it, any slow or heavy test, and any suite that spans folders are not run after a step, because a step that is not the last will change the same code again and the run will have to be repeated.
- **They run once, in the task's last step, before the task is closed, and only when the agent is sure the work is finished:** the tests of the modules whose files import what the task changed (found by searching the imports), never the project's whole suite; a whole-suite run is the owner's request or a release. A failure there is debugged then, by running the failing test alone; a run is not repeated to see whether it is still red. A sub-agent given one step of a task runs only the unit tests of its step and hands back; the delegating agent runs the heavier set once at the end.
- **A test file states its time budget** in seconds, as a constant `BUDGET_SECONDS`; a file without one is not done.
- **A run longer than its budget is stopped and reported,** not waited on: it starts under a hard limit equal to the budget of the file it runs, at most 600 seconds (the tool's timeout, or the host's `timeout`), one file or class per command. A run that reaches the limit is a finding naming the test it was in. A run is never left for hours.

## Why it exists
Sub-agents of the memory-layer task (20261023-T074642Z-5420) wrote services before their tests and ran suites for over 30 minutes, one of which stopped silently and was never explained. In the move of the filesystem services (task 20261105-T054954Z-15064) a sub-agent ran 78 importer test files in the middle of the task, while services were still to be moved; the owner (2026-11-05) ruled that heavy tests run once at the end.

## Keep it or drop it
An organization may choose other bounds and remain conformant to the protocol; it then states them where its tests are kept.

## What this rule does not claim
- It does not claim what a green suite establishes; that is [What a Passing Suite Establishes](../../test.md#what-a-passing-suite-establishes).
- No runner reads `BUDGET_SECONDS` yet, so whoever starts a run reads it and sets the limit on the command; which module owns a runner is the owner's to name.

Owed: test.budget-runner
- That a delegating agent reads a red run before accepting a green one is [the task rule](../../../../../modules-plugable/management/task/rules/delegator-reads-the-red-run/delegator-reads-the-red-run.md), not this one's.
