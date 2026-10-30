# Task Rule — A task ends with its report and Status
Status: Draft

## The rule
Before ending work on a task — finished or not — write its report, with its Status, and set its plan's Status to agree, as `memar task --help` says: a task left Active after its check passed reads to every later task as work still owed. Each pass, local or delegated, has a finite boundary, the same acceptance check, and a named end, the Status its report states: Complete, Blocked, or Active ([Status](../../../../knowledge/documentation/documentation.md#status)). Errors and exhausted budgets are never reported as Complete ([Acceptance Criteria](../../../../../docs/agency.md#acceptance-criteria)).

## Why it exists
A later task reads the Status to know whether work is owed.

## How a check would run
A folder whose report and plan Status disagree, or an ended task with Status Active, breaks the rule. Moved on 2026-10-26 from the Memar skill (task 20261026-T120341Z-16244); this repository runs no automatic check of it today.
