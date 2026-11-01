---
Title: "Task Rule — Old Task Folders Are Swept by the Owner's Ruling"
Start Date: 2026-11-01
---
# Task Rule — Old Task Folders Are Swept by the Owner's Ruling
A rule of this repository for the folders the daily sweep leaves behind. The statements are the owner's, 2026-10-13.

## The rule
- **A task whose plan has no text is treated as finished,** since no plan will be written for it.
- **A task about another repository, the organization repository for one, is moved to that repository's task folder for review there,** since this side cannot see whether it was done.
- **A finished folder goes to the recycle bin** with `memar git trash-task-folder`, not by hand.
- **A plan that holds several tasks is checked task by task,** and the checking agent does the small leftovers itself.

## Why it exists
A folder swept without a rule is either kept forever or lost with work in it; each clause names a case the sweep met.

## Keep it or drop it
A project that wants every finished task kept sets so in its preferences and closes none.

## What this rule does not claim
- It does not say how the sweep finds a folder; `memar git sweep-idle-task-folders --help` says that.
- This repository runs no check of it today.
