# Dt status

## Model

- Candidate (unconfirmed): a production status loop-edge set — `Created`, `ManagerApprove`, `WarehouseApprove`, `ActiveWithApprove`, `ActiveWithoutApprove`, `ActiveWithOrderer`, `Inactive`, `Normal`, `Reject`, `Void` (ten statuses in one source `const`-comment list; `type Status qs_p.Status` aliases the quiddity-status type — shape unconfirmed).

## Policies (rules)

- Approval-chain statuses in the list: `ManagerApprove`, `WarehouseApprove` — two human approval gates before activation.
- Activation variants: `ActiveWithApprove`, `ActiveWithoutApprove`, `ActiveWithOrderer` — three ways a production may go active.
- The identical nine-status list (without `Void`) also appears in [task production](../../../../../modules/management/task/edges/production/production.md) Policies — one vocabulary, two homes of record until reconciled.

## Placement

- **Correct here — the domain defines its own status loop-edges** (the status domain's rule: "A domain defines the statuses that belong to it as loop-edges under `<domain>/status/<name>/`" — [status](../../../../../modules/knowledge/status/status.md); production states its record here, [production.md](../../production.md) never repeats the list).
- **Not the status module's own list:** the general status domain holds the account of what a status is and the shared loop-edges; production approval statuses are production vocabulary (placement by entry point; pluggable owns complete capability — edge + the approval rules that read it).
- **Not [management/task](../../../../../modules/management/task/edges/production/production.md):** task-side production vocabulary is the task work relation; this dt-status set is the economics-production lifecycle — reconcile the two lists to one home rather than drift (receiving [production.md](../../production.md) backlog question; prefer existing homes over inventing new modules).
- Approval statuses (`ManagerApprove`/`WarehouseApprove`) may be rule material rather than plain statuses — record before ratifying (no bare edges; core never knows Rule).

## Open questions

- Are the approval-chain states (`ManagerApprove`/`WarehouseApprove`) a workflow rule rather than statuses?
- Reconcile with the general status domain ([status](../../../../../modules/knowledge/status/status.md)) — own status set or shared labels? The quiddity-status alias (`qs_p.Status`) hints at sharing — confirm.
- Same list as task-side [task production](../../../../../modules/management/task/edges/production/production.md) (nine statuses) plus `Void` here — one list or two (production lifecycle vs task work)?
- What distinguishes `Normal` from `Active*` — a resting state after activation, or a synonym?

