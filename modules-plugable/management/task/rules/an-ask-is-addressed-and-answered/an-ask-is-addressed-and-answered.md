# Task Rule — An ask is addressed to a participant and only that participant answers it
Status: Draft

## The rule
- **Anyone who is on the Task may reply to any content of its timeline, and a reply binds nobody.** A reply that needs someone to act is an *ask*: it names the participant, or the role, whose action it asks.
- **Only the addressee's own act answers an ask**: it does what is asked and says so in a reply, or declines in a reply that gives the reason, or hands the ask to another participant in a reply that names that participant. Silence is not acceptance ([Task → Assign task rules](../../../../../modules/management/task/task.md#assign-task-rules)).
- **What needs a participant's action is discovered and never stored**: the asks addressed to it that no reply of its own answers. A chat that takes up a Task reads the plan and these asks, and what they list, so that every agent of a chat learns what needs its action from replies.
- **A role is addressed, not a living agent.** A Task outlives its workers ([A Task may live as long as the organization](../task-outlives-its-workers/task-outlives-its-workers.md)), so an ask to a role is answered by the agent that holds the role when it is read; with two holders either may answer and the first reply answers it, and with none it stays open and `list` shows it. A critic called by an ask becomes a participant by that call. An open ask on a Complete Task is shown by `list`, and acting on it reopens the Task by a Request.
- **A reply that tells the original agent to act again is an ask to the role that made the examined content**; it states what is to be done and which numbers to read ([A reply names what to read](../a-reply-names-what-to-read/a-reply-names-what-to-read.md)).

## Why it exists
A chat is not a record ([One timeline per Task](../one-timeline-per-task/one-timeline-per-task.md)), so what a participant owes cannot live in a chat's memory or in a message sent outside the timeline; the timeline's own replies are the one place every participant already reads.

## How a check would run
For a participant, list the contents addressed to it with no later reply of its own on the chain; each is an open ask. A Task whose asks cannot be found this way breaks the rule. The statement is the owner's, recorded in [the Task handoff](../../../../../modules/management/task/task.handoff.md#critique-as-a-content-on-the-timeline-2026-10-30-tentative); this repository runs no automatic check of it today.
