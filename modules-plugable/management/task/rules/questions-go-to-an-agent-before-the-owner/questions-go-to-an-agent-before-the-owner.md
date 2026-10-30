# Task Rule — A question reaches the owner only after an agent has tried it
Status: Draft

## The rule
Before an agent brings the owner a question — a line under a report's `Decisions needed`, its own written there first — it hands it to a newly started agent on the model that question needs ([the model rule](../model-follows-need/model-follows-need.md)), as `memar ai get-task-questions-answer-brief` says, and brings the owner only what that agent leaves to the owner. A sub-agent has no human to ask: what it would ask, it ends on as blocked or approval-required, with the question stated, and the task that delegated it asks.

## Why it exists
The owner's attention is the scarcest resource; a question an agent can settle from the documents does not need it.

## How a check would run
A `Decisions needed` line that no agent tried first breaks the rule. Moved on 2026-10-26 from the Memar skill (task 20261026-T120341Z-16244); this repository runs no automatic check of it today.
