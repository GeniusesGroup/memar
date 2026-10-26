# Task Rule — Tests come before the code of every service, and a run is scoped and bounded
Status: Draft

## The rule
- **Tests before code, for every service however small.** The expectations of a service are written as tests, and seen to fail, before any line of its code; a service with no test of its own is not done ([Test Practice → The Cycle](../../../../../modules/process/test/test.practice.md#the-cycle)).
- **The check after a change is scoped.** It is the tests of the module changed and of the modules whose files import it (found by searching the imports), never the project's whole suite. A whole-suite run is the owner's request or a release, never a step of a task.
- **A test has a stated time budget,** in seconds, as a constant `BUDGET_SECONDS` in each test file of the module; a test file with no budget is not done.
- **A run longer than its budget is stopped and reported,** not waited on: the command starts under a hard limit equal to the budget of the file it runs, at most 600 seconds (the tool's timeout, or the host's `timeout`), one file or class per command, and a run that reaches it is a finding with the test it was in, never a wait. A run is never left for hours.
- **The agent that delegates a test run reads the red run before it accepts a green one:** it sees the new tests fail against a stub, and re-runs the module's tests itself under the same limit.

## Why it exists
Sub-agents of the memory-layer task (20261023-T074642Z-5420) wrote services before their tests and ran suites for over 30 minutes, one of which stopped silently and was never explained. A green result nobody saw red is a claim, not evidence.

## How a check would run
A module's test file without a budget, a test commit that follows the code commit it covers, a task step that runs the whole suite, and a run that outlived its limit and was waited on, break the rule. Owed: no runner reads `BUDGET_SECONDS` yet, so whoever starts a run reads it and sets the limit on the command; which module owns a runner is the owner's to name.
