---
Title: "Task Rule — The Owner Gets One Digest, Not a Question per Task"
Start Date: 2026-11-01
---
# Task Rule — The Owner Gets One Digest, Not a Question per Task
A rule of this repository for what a delegating agent brings the owner when its tasks end. Moved on 2026-11-01 from the Handoff Practice.

## The rule
- **Last, the delegating agent runs `memar task get-decisions-digest` for its own conversation and gives the owner that one digest.** It gathers every task's `Decisions needed` into one list, each task's entries under its title, priority, Status and report; marks every failed hand-back; and flags a task not Complete that looks finished or abandoned. A Complete task is in it only when it holds decisions or a failed hand-back.
- **The owner's review of a day is the same command for that day:** every task that changed, one by one with a summary of its Result, read by the owner and an agent together.
- **The agent then archives and closes the tasks the owner confirms finished, and no other.** A project that wants its finished tasks kept sets so in its preferences and closes none.
- **Which questions reach the owner, and which an agent settles itself, is set elsewhere:** [Cognition Practice → Norm Application Points](../../../../../docs/cognition.practice.md#norm-application-points) and [a question reaches the owner only after an agent has tried it](../questions-go-to-an-agent-before-the-owner/questions-go-to-an-agent-before-the-owner.md).

## Why it exists
The owner's attention goes only where it is needed: one list of decisive questions, each with its options and a recommendation, instead of thirty reports.

## Keep it or drop it
An organization may read every report; it then reads thirty where one list would do.

## What this rule does not claim
- It does not give the options of the digest or of the archive and close verbs; their `--help` says them.
- This repository runs no check of it today.
