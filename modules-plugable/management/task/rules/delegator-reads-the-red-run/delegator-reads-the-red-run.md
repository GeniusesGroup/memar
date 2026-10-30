# Task Rule — A delegating agent sees a run red before it accepts it green
Status: Draft

## The rule
When a step that writes code is delegated, the delegating agent accepts its green result only after it has seen the new tests fail against a stub (in the sub-agent's report, or by running them itself), and it re-runs the module's tests itself under the limit of [Tests First and Scoped](../../../../../modules/process/test/rules/tests-first-and-scoped/tests-first-and-scoped.md). The plan of the step names the command and its limit.

## Why it exists
A green result nobody saw red is a claim, not evidence; the delegating agent of the memory-layer task (20261023-T074642Z-5420) re-ran three classes of a suite that ran over 30 minutes and accepted the rest on the report.

## How a check would run
A delegated step's report without a red run, or a plan without the command and limit, breaks the rule. This repository runs no automatic check of it today.
