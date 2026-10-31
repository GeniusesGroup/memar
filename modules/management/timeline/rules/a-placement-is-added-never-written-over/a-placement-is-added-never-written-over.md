# Timeline Rule — A placement is added, never written over
Status: Draft

## The rule
- **A content placed in a timeline (a plan, a report, a critique, an answer, a change record, a question, a message) is added as a new placement and never written over an earlier one.** A correction is a new content that replies to the one it corrects; the words the owner or a critic wrote stay as they stand.
- **The timeline's identity is the UUID of the node it belongs to** (a task, a group, a person), and placing takes no knowledge of what that node is: the service that places is the timeline's, and the service that creates the content is the content's.
- **The number of a placement is the timeline's next number across all kinds; the check that a caller read the latest is made against the latest placement of the same kind only.**

## Why it exists
An agent replaced a task's `plan.md` and the owner's critique in it was lost on 2026-10-30. A message whose meaning is edited can change the course of the whole task, which is why a fork from a middle content, not an edit, is the remedy to be added later. The owner ruled on 2026-10-31 that adding a content is not the task domain's.

## How a check would run
A service or an agent that writes over a placement, or that places in a timeline through a service of another domain, breaks the rule. This repository runs no automatic check of it today.
