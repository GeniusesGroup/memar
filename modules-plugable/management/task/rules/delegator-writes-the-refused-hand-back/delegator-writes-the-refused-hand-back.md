# Task Rule — Where the harness refuses a sub-agent's report, the delegating agent writes it
Status: Draft

## The rule
A delegated step is done only when its `report.md` exists. Where the harness refuses the sub-agent's write of it, the sub-agent hands back its report as text, and the delegating agent writes it as that task's `report.md`, starts it with the line `Written by the delegating agent from the sub-agent's hand-back.`, marks what it could not check, and says in its own report that it did so.

## Why it exists
The harness refused several sub-agents of the memory-layer task their report write; the delegating agent wrote the reports from the hand-backs, with no rule saying that this is what to do and no mark of whose words they were.

## How a check would run
A delegated task folder with no `report.md`, or one written by the delegating agent without saying so, breaks the rule. This repository runs no automatic check of it today.
