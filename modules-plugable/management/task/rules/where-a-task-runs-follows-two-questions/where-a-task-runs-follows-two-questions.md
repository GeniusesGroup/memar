---
Title: "Task Rule — Where a Task Runs Follows Two Questions"
Start Date: 2026-11-01
---
# Task Rule — Where a Task Runs Follows Two Questions
A rule of this repository for a conversation that hands a task to another agent. Moved on 2026-11-01 from the Handoff Practice.

## The rule
- **Two questions decide, and both answers are written in the plan:** does the conversation need the task's result, and does the task need the owner (questions, critique, back-and-forth)?
- **A result needed and no owner needed: a sub-agent that returns only its hand-back.**
- **The owner needed, whether or not the conversation waits: a new chat.** Whether the task needs the owner alone decides a new chat; a chat with nothing to ask the owner only gives the owner one more chat to watch.
- **A task whose result the conversation does not need is independent:** its plan is written whole and the conversation is done with it. Its chat is opened when it needs the owner; otherwise it goes to a sub-agent once the conversation's own work leaves room, or stays queued. A chat opened for it is then [left alone](../opened-chat-is-left-alone/opened-chat-is-left-alone.md).
- **A conversation that waits for tasks in new chats cannot learn that they ended,** so it asks the owner to tell it.

## Why it exists
A conversation that takes in several tasks' reading and the owner's answers grows large, and every later turn pays for all of it.

## Keep it or drop it
An organization may run every task in one conversation, and then pays one growing context for all.

## What this rule does not claim
- It does not say how a chat is opened or briefed; `memar ai get-new-chats-ask --help` and `memar ai get-task-plan-carry-out-brief --help` say that.
- It does not say how a task that is waited on is recorded: [a blocking task is recorded in Depends_on](../a-blocking-task-is-recorded-in-depends-on/a-blocking-task-is-recorded-in-depends-on.md).
- The owner's words never pick where a task runs; "open a task" or "ask an agent" name the work, not the place.
- This repository runs no check of it today.
