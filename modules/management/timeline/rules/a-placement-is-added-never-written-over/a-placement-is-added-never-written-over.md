# Timeline Rule — A placement is added, never written over
Status: Draft

## The rule
- **A content placed in a timeline (a critique, an answer, a question, a message) is added as a new placement and never written over an earlier one.** A correction is a new content that replies to the one it corrects; the words the owner or a critic wrote stay as they stand.
- **The timeline's identity is the address of the node it belongs to**, and placing takes no knowledge of what that node is: the service that places is the timeline's, and the service that creates the content is the content's.
- **The number of a placement is the timeline's next number across every placement; no placement is checked against "the latest of the same kind"**, since a later content of a kind does not void an earlier one ([Timeline → The current content of a kind](../../timeline.md#the-current-content-of-a-kind)).

## Why it exists
A critique written over by a later edit was lost on 2026-10-30. A message whose meaning is edited can change the course of the whole exchange, which is why a fork from a middle content, not an edit, is the remedy to be added later.

## How a check would run
A service or an agent that writes over a placement, or that places in a timeline through a service of another domain, breaks the rule. This repository runs no automatic check of it today.
