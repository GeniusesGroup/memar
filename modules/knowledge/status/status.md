# Status
All quiddities even `label` itself CAN get `status` labels.

Status indicate base record status
It is like labeling records But it is systematic labels.
Labels check in business rules logic(Async), but status check in services logic(Sync).

## What a status is
A status is a loop-edge. The edge type is the status, and the edge terminates on the record it marks: `(record)-[:draft]->(---)`. Code uses that edge type.

Memar's [classification test](https://github.com/GeniusesGroup/memar/blob/main/docs/modeling.md#classification-emerges-from-rules-and-relations-not-from-intrinsic-labels) keeps a status as a loop-edge. A marker such as active or archived has no lifecycle of its own, so it stays the edge rather than becoming a node on the far side of a generic `status` edge. A generic `(record)-[:status]->(draft-node)` would promote the marker into a concept it does not independently carry.

The move from one status to another is an event. A rule may allow or block that event. The rule lives with the event.

### Where a status is defined
This module holds the account of what a status is, and the shared loop-edges whose type is the same for every domain, under `edges-loop/`. A domain defines the statuses that belong to it as loop-edges under `<domain>/status/<name>/`. The domain's main document states the record. It does not repeat the status list.

### Asking which records carry a status
All laws that carry draft are the laws with that loop-edge:

`MATCH (law)-[:draft]->()`

The rows are laws. Draft is the predicate: the edge type. That type is already the code identity of the status. The query reads it. It does not add a draft node to the graph.

A status becomes a node when other records take the status itself as their subject — a lifecycle of draft apart from the records that carry the edge. A scan for those records is the edge type used as a type.

## Policies (rules)

- all edges e,g, `draft` MUST have `status` label.
- All edges CAN indicate which `user` set the status, When the status set, and the chain of changes to specific status

## Idea backlog from edge code comments

Raw proposals from comment notes inside edge .go files (comments remain in code as source). Review discipline per modules/management/vocabulary-discipline.handoff.md. Nothing below is ratified.

### Quiddity states - edges/quiddity-status.go
- **Idea**: Expired; Locked/Closed (quiddity must not be used or edited for some reason); Failure; PermanentInactivated; TemporaryInactivated; Revoked; provenance states ManuallyAdded (data belongs to another app/org, added by users via GUI) and ManuallyVerified (manually added data verified in some way); CreationTime/CreatorId fields noted.
- **Review questions**: are Locked/Closed/Failure distinct states or one Suspended with a reason? Do provenance states belong to audit-log?

### Request states - edges/request-status.go
- **Idea**: Approving (awaiting approval), Rejected, Processing (in progress/pending), Processed (completed), Failed, Canceled, Compensated.
- **Review questions**: reconcile with memar process/request lifecycle; is Compensated the transaction-side link ([transaction.handoff.md](../../economics/transaction/transaction.handoff.md) §6)?

### Estate states - edges/estate-status.go
- **Idea**: Reserved, Occupied, Vacant, Closed.
- **Review questions**: these are user-claimed states over estates - same mechanism as the general status domain pointed at estates? Overlaps the estate spatial/identity work (estate.handoff.md).