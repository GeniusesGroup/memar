# Status
All quiddities even `label` itself CAN get `status` labels.

Status indicate base record status
It is like labeling records But it is systematic labels.
Labels check in business rules logic(Async), but status check in services logic(Sync).

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
- **Review questions**: reconcile with memar process/request lifecycle; is Compensated the transaction-side link (accounting-invariants #6)?

### Estate states - edges/estate-status.go
- **Idea**: Reserved, Occupied, Vacant, Closed.
- **Review questions**: these are user-claimed states over estates - same mechanism as the general status domain pointed at estates? Overlaps the estate spatial/identity work (estate.handoff.md).