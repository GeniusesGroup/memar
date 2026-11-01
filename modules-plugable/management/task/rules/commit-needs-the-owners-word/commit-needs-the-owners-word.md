---
Title: "Task Rule — A Commit Needs the Owner's Word, and a Small Commit Needs No Task"
Start Date: 2026-11-01
---
# Task Rule — A Commit Needs the Owner's Word, and a Small Commit Needs No Task
A rule of this repository for committing the work of a task. The statements are the owner's, 2026-10-13 and 2026-10-15.

## The rule
- **Nothing is committed without the owner's say-so, and a sub-agent never commits.** A standing word, such as "commit when the chat is finished", is the say-so for that chat only, and for the files [that chat changed](../a-chat-commits-only-its-own-files/a-chat-commits-only-its-own-files.md).
- **A chat commits once it has said it has nothing left to do,** and not before.
- **Committing a batch, one edit, staging, or a lookup is done in place,** with no task and no sub-agent.

## Why it exists
A commit enters the history that others read and is not quietly taken back. A task exists so that its decisions persist; opening one with a sub-agent for a commit costs far more than the work.

## Keep it or drop it
An organization may let agents commit as they go, and then answers for a history shaped by chats that had not finished.

## What this rule does not claim
- It does not say how a commit is made; the root `--help` of `modules-plugable/computer/git/services/_host_git_cli.py` and that of its `commit` verb say that, and the skill's Closing section sends the agent there.
- This repository runs no check of it today.
