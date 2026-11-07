# Task Rule — A chat opened for a task whose result is not needed is opened independent and left alone
Status: Draft

## The rule
- **A chat opened for work whose result the opening chat does not need is opened independent:** its task is opened with no `--parent`, and the agent app's chat is started so that it is not a side or child session of the opening chat, where the app offers the choice (a standalone chat, no report back to the opener). This holds for every agent. Most such chats are opened because a context is large or the work is unrelated, and a chat that is not independent only sends the opener messages it does not need, each of which costs.
- **Once it is open, read nothing from it, poll it for nothing, and do not follow it up or ask it for news.** The owner answers its questions there, and a task that needs its outcome reads its report.
- **Work that continues a task is not such a chat's task:** it goes to a chat on the same task ([later work returns to its task](../later-work-returns-to-its-task/later-work-returns-to-its-task.md)).

## Why it exists
Each look, and each message the opener receives from a chat it does not need, spends its context for nothing.

## How a check would run
A task's chat that reads, polls or asks a chat it opened for an independent task, or opens it as its child, breaks the rule. Moved on 2026-10-26 from the Memar skill (task 20261026-T120341Z-16244), amended 2026-11-06; this repository runs no automatic check of it today.
