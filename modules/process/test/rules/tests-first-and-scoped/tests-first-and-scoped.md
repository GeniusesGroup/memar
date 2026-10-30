---
Title: "Test Rule — Tests First and Scoped"
Status: Draft
Start Date: 2026-10-30
---

# Test Rule — Tests First and Scoped
A rule of this repository, held for the [Test](../../test.md) protocol. Tests before the work is the protocol's own claim ([The Expectation Is Written Before the Work](../../test.md#the-expectation-is-written-before-the-work)); this rule adds how a run is bounded, which the protocol leaves to the organization. It applies only to work whose product is software; the protocol does not.

## The rule
- **Every service has its tests before its code, however small,** and the new tests are seen to fail before any line of the service ([Test Practice → The Cycle](../../test.practice.md#the-cycle)). A service with no test of its own is not done.
- **The check after a change is scoped:** the tests of the module changed and of the modules whose files import it (found by searching the imports), never the project's whole suite. A whole-suite run is the owner's request or a release.
- **A test file states its time budget** in seconds, as a constant `BUDGET_SECONDS`; a file without one is not done.
- **A run longer than its budget is stopped and reported,** not waited on: it starts under a hard limit equal to the budget of the file it runs, at most 600 seconds (the tool's timeout, or the host's `timeout`), one file or class per command. A run that reaches the limit is a finding naming the test it was in. A run is never left for hours.

## Why it exists
Sub-agents of the memory-layer task (20261023-T074642Z-5420) wrote services before their tests and ran suites for over 30 minutes, one of which stopped silently and was never explained.

## Keep it or drop it
An organization may choose other bounds and remain conformant to the protocol; it then states them where its tests are kept.

## What this rule does not claim
- It does not claim what a green suite establishes; that is [What a Passing Suite Establishes](../../test.md#what-a-passing-suite-establishes).
- No runner reads `BUDGET_SECONDS` yet, so whoever starts a run reads it and sets the limit on the command; which module owns a runner is the owner's to name.

Owed: test.budget-runner
- That a delegating agent reads a red run before accepting a green one is [the task rule](../../../../../modules-plugable/management/task/rules/delegator-reads-the-red-run/delegator-reads-the-red-run.md), not this one's.
