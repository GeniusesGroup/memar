# Task Rule — A reply chain ends by a reply that asks nothing, or by the owner
Status: Draft

## The rule
- **A chain is a content and every reply that follows it through `reply_to`.** It ends when the asker places a closing reply addressed to no one (the verdict is accepted, or nothing more is asked), or the authority the Task answers to does. A critic's verdict is addressed to the asker, so it does not end the chain; silence does not end it.
- **A chain that goes on without new ground is handed to that authority.** When the same two participants, or the same participant and role, have exchanged more replies than the limit, with no new content read and no change made since the last, the next reply is a question to the authority ([Questions go to an agent before the owner](../questions-go-to-an-agent-before-the-owner/questions-go-to-an-agent-before-the-owner.md) first), and the chain is suspended until it is answered. The limit is a parameter set where the organization configures; the value this rule proposes is three.
- **An open ask does not end a Task unless the check depends on it.** The agent that ends a Task lists its open asks under what is left open; one the check depends on keeps the Task Active, or Blocked when the wait is on an answer.
- **A closed chain is not edited.** A new ask on the same ground is a new reply to the closing one.

## Why it exists
Two agents can ask each other for one more look without end, each time at the cost of a fresh start; a rule that says what ends a chain, and who is asked when it does not end, is what keeps the cost bounded without hiding the disagreement.

## How a check would run
An open chain is listed with the age of its last reply; a Task may live long, so age alone expires nothing. A chain longer than the limit with no question to the authority breaks the rule. The statement is the owner's, recorded in [the Task handoff](../../../../../modules/management/task/task.handoff.md#critique-as-a-content-on-the-timeline-2026-10-30-tentative); this repository runs no automatic check of it today.
