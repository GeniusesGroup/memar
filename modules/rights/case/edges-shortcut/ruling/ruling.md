# Ruling
The seated persons' consensus on one case, recomputed from that case's votes. It is a shortcut. The votes are the source of truth. A past majority is not its own edge.

## Model

- Shortcut: `(case)-[:ruling_accept]->(---)` or `(case)-[:ruling_reject]->(---)`
- There is no abstention. Each seated person chooses [vote accept](../../edges/vote-accept/vote-accept.md) or [vote reject](../../edges/vote-reject/vote-reject.md) and explains the choice.
- Continuation depends on the vote margin, not on wealth. While the margin sits near the middle, continuation is allowed. When the same-way share is large, continuation stops. The examples of about 20 percent from the middle, and about 80 percent the same way, are examples. They belong in pluggable policy. They are not kernel constants, and this file does not store them.
- The shortcut is one of the two positions when continuation has stopped under that margin rule. The kernel does not require an odd pool, and it does not stop at 5 or at 11, 13, or 15.

## Policies (rules)

- The shortcut is a cache. Rewriting it does not delete or flip any vote.
- A missing shortcut means the case is unanswered, or continuation is still allowed. Silence is not a rejection.
- The shortcut does not store a quantity and does not substitute a service. It is accept or reject of the claim as filed. Accept means that filed service, with no attachment. A reject may point at one request. Distinct requests on those rejects stay rejects. The shortcut does not read them as accept, and it does not invoke them. A consensus of those requests is not this shortcut. It is a later case. Conditional accepts are not reused as this shortcut's outcome.
- Opened sources treat a partial grant as relief on the same claim. That shape is a recorded departure. This shortcut does not grant part of the claim.
- An alternate request is a `computer/request` a reject may point at. This shortcut does not take that request as a field. When this shortcut is reject, nothing executes, including when the claimant never files a later case.
- A party's score does not weight a vote, and it does not weight this shortcut.
- When continuation has stopped on accept, the filed service executes automatically. That execution is a service invocation the system compels. The defendant is not the voluntary caller. The input is not only a number. A public apology is a compelled write of a text on that person's timeline, addressed to the claimant. That write is another compelled service, not a second procedure and not a second shortcut. A stop on reject executes nothing.
- A later break, a third-party objection or another attack, requires a reversal of that execution. The reversal is a note for the transaction domain. This file does not invent the transaction rules. `settlement_for` is not recorded as that path.
- The margin rule stops continuation on this case. It does not stop a later case. On a consensus case the filed service is one request an earlier reject already points at. This shortcut on that case is accept or reject of that one service. That case does not grow a new attached request. Conditional accept is not used on it. If the claimant never files, nothing executes.
- The case remains a case. The ruling does not replace it.
- Words that mean the result can never change are not used. An earlier majority that is now a minority is a fact about the votes. The shortcut shows the current margin result only. No history edge stores the past majority.
- One shortcut on one case does not rule another case. After a ruling exists, a third party's attack is a new case, and the claim type is annulment of that ruling. That reason is its own pluggable edge. This shortcut is not deleted by that sentence.
- What would falsify the rule that continuation stops on the margin and not on wealth: continuation that stops because the party's wealth or fees are exhausted while the margin still allows continuation; or the numbers 20 and 80 stored as kernel constants. Model v4 point 11.
- What would falsify the rule that a final shortcut executes, and that a later break reverses it: a ruling that is final under the margin rule and does not execute; or a later break that leaves the execution in place with no reversal. Model v4 point 12.
- What would falsify the rule that no service runs without the judges' votes on that exact invocation: One executable service runs on the original case without any case whose judges voted on that exact invocation. Critique v4. That merged service is the consensus shortcut the pilot has not adopted; this file rejects it above.
- What would falsify the rule that this shortcut does not substitute a service: `ruling_accept` runs a service invocation that no single judge's vote edge individually accepted as filed. Critique v3. The conditional accept behind it is a proposal the pilot has not adopted.

## Placement

- **A shortcut under `edges-shortcut/`.** The consensus is discovered from the vote edges. It must not become the source of truth. Delete the shortcut and the votes still decide. The marker is not a status. Shared draft stays the only status this phase uses. `ruling_accept` and `ruling_reject` are not registered under the status module.
- **Nearest alternative rejected:** a ruling node. The node would have no lifecycle the votes do not already have.
- **Nearest alternative rejected:** an average of the amounts judges would accept, and a claimant-chosen figure standing in for the ruling.
- **Nearest alternative rejected:** several positive votes at several amounts or at several services.
- **Rejected:** a consensus shortcut that merges attached requests, or conditional accepts, into one executable service on this case. The later case carries its own fresh votes.
- **Nearest alternative rejected:** a history edge beside the shortcut. The votes are enough.
- **Nearest alternative rejected:** stopping continuation because the parties stop paying. The stop is the margin.

## Open questions

- The vote-to-request pointer is a proposal. This shortcut does not draw that edge. On the consensus case the ballot is fresh accept or reject of the one filed service, and that case grows no new request.
