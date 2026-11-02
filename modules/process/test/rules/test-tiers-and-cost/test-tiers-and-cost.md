---
Title: "Test Rule — Tiers and Cost"
Labels: Draft
Start Date: 2026-10-30
---
# Test Rule — Tiers and Cost
A rule of this repository, held for the [Test](../../test.md) protocol. [Tiers with labeled seams](../../test.practice.md#tiers-with-labeled-seams) says checks differ in tier and that tiers are not mixed; this rule says what a Test of each tier may spend, so that a run stays small enough for an agent to wait on it. It came from a measurement of 2026-10-30: 120 test files took about 700 seconds alone, because most Tests built a git repository, started a `memar` process or composed the documents again for each Test, and an agent's context was spent waiting.

## The rule
- **A Test belongs to one of three tiers, and the tier is stated in the Test file.**
  - **Unit:** one service, in the process that runs it, with no subprocess, no git, no files outside a scratch folder and no wait on the clock. The memory the service reads and writes is an in-memory adapter ([Volatile](../../../../computer/memory/volatile/)), never a file system or a repository. Almost every Test is of this tier, and only this tier runs after a change.
  - **Integration:** several units together, still in one process. It runs when a module it spans changes.
  - **System:** real processes, real git or file-system media, real servers or real waits. It is rare, it states what only the real thing can show, and it runs on the owner's request, at a release, or when the adapter it exercises changes.
- **A service does not know its memory medium.** It takes the memory adapter it is given, so its Tests never have a file system or git on their path. A file system or git appears in the Tests of the adapter that owns that medium, once, as the conformance cases of [Memory](../../../../computer/memory/), and nowhere above it. A Test that needs a repository to check a service is a sign that the service reaches the medium itself, and the repair is in the service.
- **Cost is stated as what a Test spends, not as seconds.** A Test file declares, for each tier it holds, the most subprocesses it starts, whether it writes files, and whether it waits on the clock. A declared cost that a run exceeds is a failure of the Test, by the count the runner takes and not by a stopwatch, so a slow or busy machine does not change the verdict.
- **A fixture that costs is built once per run.** What is expensive to make (a repository, a composed document set, a command card, a `--help` text) is made once per run and shared or copied, never made in `setUp`. A Test that mutates it works on its own copy.
- **A Test does not call a command line it can call as a function.** The real command line is started by at most one Test per verb, to show the entry works.
- **An agent never waits without a bound.** A run by an agent is one scoped file, under a hard limit ([Tests First and Scoped](../tests-first-and-scoped/tests-first-and-scoped.md)). A file that reaches the limit is reported as the finding it is and is not waited on; the repair is the Test's cost, not a longer limit.
- **The runner prints each file's cost and tier, and runs files in parallel.** [`time_tests.py`](../../tests/time_tests.py) is the runner of this repository.

## Why this exists
The ecosystem divides tests the same way (unit, integration, end to end) because each tier fails for a different reason and costs a different amount; a repository that does not divide them pays the system tier's price on every change. The seconds a Test takes are an effect of the cost it declares and of the machine it runs on, so seconds are a poor thing to govern by; the number of processes, the writes to disk and the waits are the cause and the same on every machine. Writes to a file system are also a cost to the disk itself, which a repeated `git init` pays thousands of times a day.

## What this rule does not claim
- It does not claim every existing Test meets it. Tests that reach a file system or git through a service are repaired when the memory-adapter work lands, and until then they are tier system and are listed as such.
- It does not set a number of seconds. The hard limit an agent runs under is the one [Tests First and Scoped](../tests-first-and-scoped/tests-first-and-scoped.md) states, and it is a bound on waiting, not a budget to spend.
