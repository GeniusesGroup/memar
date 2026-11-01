---
Title: "Task Rule — Commits Are Few and Readable"
Start Date: 2026-11-01
---
# Task Rule — Commits Are Few and Readable
A rule of this repository for the shape of a task's commits. The statements are the owner's, 2026-10-14 and 2026-10-15.

## The rule
- **A commit made by mistake or left incomplete, before it is pushed, is amended or folded,** and is not followed by a second commit.
- **After committing, the status is read:** a file the same task staged and left out is a defect.
- **Commits are grouped by top folder and are few,** since each costs history and review.
- **A move that git must record as a rename is committed alone,** as a pure move with no other edit, so that git sees a rename and not a deletion and an addition; the repairs the move makes necessary follow in a later commit.

## Why it exists
A history of fixes upon fixes cannot be read, and a rename mixed with edits is recorded as lost and new files, which loses the file's history.

## Keep it or drop it
An organization that squashes on merge may drop the first and third clauses.

## What this rule does not claim
- It does not give the commands: amending, folding and staging are described by `--help` of `modules-plugable/computer/git/services/_host_git_cli.py`.
- This repository runs no check of it today.
