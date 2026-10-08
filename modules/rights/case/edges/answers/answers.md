# Answers
A case brought in response to another case.

## Model

- `(case)-[:answers]->(case)`
- The source is the answering case. The target is the case it answers.

## Policies (rules)

- The answering case has its own plaintiff and defendant. The plaintiff of the answer may be the defendant of the target. That crossing is the point of a separate case: the part is on the claim, not on the petition.
- The answering case has its own service, its own votes, and its own ruling shortcut.
- The answering case is not placed in the target's [petition-next](../petition-next/petition-next.md) path by this edge. Whether it may also be placed there is open.
- A third party's attack after a ruling is a new case, and the claim type is annulment of that ruling. During the proceeding, a third-party objection is a linked claim heard together. Each of those reasons is its own edge. This file does not decide that `answers` is either of them. Links between claims are pluggable. There is no generic edge meaning only that two claims are related. A vote on the linked case is not a vote on this one.
- One answering case has one `answers` target.

## Placement

- **Pluggable.** A response is its own reason between two claims. It is not an order inside the filer's petition, it is not a generic related edge, and it is not a role. The file stays at the mirrored path. Links between claims are pluggable.
- **Nearest alternative rejected:** a counterclaim flag on the same case. One case has one plaintiff set and one defendant set. A flag cannot swap those parts for a second claim. A second case can.
- **Nearest alternative rejected:** reusing `petition_next` for the answer. That path is the filer's order. The answer is the other party's complaint.

## Open questions

- None that make `answers` the third-party link, the annulment link, or a generic related edge. Those reasons are their own edges. Whether an answering case may also sit on the petition path stays unsettled on [petition next](../petition-next/petition-next.md). It does not block this edge.
