---
Title: "Task Rule — Queued Work Is Taken for One Project and Handed Out by One Topic"
Status: Draft
Start Date: 2026-11-01
---

# Task Rule — Queued Work Is Taken for One Project and Handed Out by One Topic
A rule of this repository for an agent asked to do some of the queued tasks. Moved on 2026-11-01 from the Handoff Practice.

## The rule
- **The agent asked to do queued tasks works them as the delegating agent,** taking from the one project it is told to name, with no default and no way to take from all. A delegating agent that does not know the project asks the owner.
- **The project is named with the flag for what the agent has,** a name or a folder, and never one in the other's place; a word is never reasoned about nor turned into a guessed path.
- **Tasks are taken in line order,** the highest priority first and the oldest first among equals. When the first in line carries a topic, that topic's queued tasks are taken next rather than unrelated ones that rank above them, and the higher-priority tasks passed over are said. A task of another topic fills what is left only when the delegating agent asks.
- **A batch of one topic goes to one fresh sub-agent,** each task in it keeping its own plan and report, and never one sub-agent tasks of different topics. The delegating agent works none of them in its own context.
- **Memar starts no agent;** the delegating agent starts each the way its runtime starts a sub-agent.
- **A claim left by an agent that died lapses,** since nothing keeps a claim fresh, and the task can then be taken or queued again.

## Why it exists
One run serves one project, and a guessed or spanning scope would hide which project the work lands in. Tasks of one topic share their reading, so one agent pays its load once, while each task keeps its own review.

## Keep it or drop it
An organization with one project and one topic needs none of it.

## What this rule does not claim
- It does not give the verbs, flags or the time a claim lasts; `memar task claims --help`, `memar task claim --help` and `memar project find --help` say them.
- This repository runs no check of it today.
