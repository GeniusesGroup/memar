# Task Rule — Where the harness refuses a sub-agent's report, the delegating agent writes it
Status: Draft

## The rule
A delegated step is done only when a report content of kind report exists on its timeline. Where the harness refuses the sub-agent's post of it, the sub-agent hands back its report as text, and the delegating agent posts it as that task's report content (`memar conversation post --timeline ID --kind report`), starts it with the line `Written by the delegating agent from the sub-agent's hand-back.`, marks what it could not check, and says in its own report that it did so.

## Why it exists
The harness refused several sub-agents of the memory-layer task their report write; the delegating agent wrote the reports from the hand-backs, with no rule saying that this is what to do and no mark of whose words they were.

## How a check would run
A delegated task with no report content, or one posted by the delegating agent without saying so, breaks the rule. This repository runs no automatic check of it today.
