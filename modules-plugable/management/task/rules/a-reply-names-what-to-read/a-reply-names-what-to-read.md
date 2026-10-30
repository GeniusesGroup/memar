# Task Rule — A reply names the contents it asks to be read, with the reason
Status: Draft

## The rule
- **A reply is a content with exactly one `reply_to` edge, to the content it answers.** The edge is the address; the words of the reply never stand for it.
- **Every content on a Task's timeline has a number**: its place in the order of the timeline, from 1, assigned when it is placed, never reused and never changed, because nothing on a timeline is ended or erased. A number is read in the timeline of the Task the reply is on; one from another Task is written `<task id>:<number>`.
- **A reply that asks someone to read other contents names each by its number and gives the reason in the same line**: `read 14 — the check there is the one this verdict is against`. A number with no reason, a number that is not on the timeline when the reply is placed, and a reply that asks to "read the above" are defects.
- **A reply asks to read what its asker needs and no more.** The reader loads anything else by searching, as [the owner's ruling on context](../../../../../modules/management/task/task.handoff.md#owners-rulings-the-second-round-2026-10-18) says.

## Why it exists
An agent that comes to a chat late, or a fresh one, has only the plan and what it searches; a reply that points by number and reason lets it read the three contents that matter instead of the whole timeline, and lets a reader tell a stated need from a habit of loading everything.

## How a check would run
For a reply, read its edge and its lines; each number must be a content already placed in the named timeline and each must carry a reason. The statement is the owner's, recorded in [the Task handoff](../../../../../modules/management/task/task.handoff.md#critique-as-a-content-on-the-timeline-2026-10-30-tentative); this repository runs no automatic check of it today.
