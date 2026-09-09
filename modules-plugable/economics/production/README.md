# Production

Production is a task label domain: a task may carry the `production` label with its sub-labels and status chain (see the task module backlog for the Production/Fabrication/Manufacturing distinction).

## Idea backlog from edge code comments

Raw proposals from comment notes inside edge .go files (comments remain in code as source). Review discipline per modules/management/vocabulary-discipline.handoff.md. Nothing below is ratified.

### Status chain - edges/dt-status.go
- **Idea**: Created, ManagerApprove, WarehouseApprove, ActiveWithApprove, ActiveWithoutApprove, ActiveWithOrderer, Inactive, Normal, Reject, Void.
- **Review questions**: approval-chain states (ManagerApprove/WarehouseApprove) - are they a workflow rule rather than statuses? Reconcile with the general status domain (knowledge/status); the same list appears in task-relation-production.go comments (management/task README).