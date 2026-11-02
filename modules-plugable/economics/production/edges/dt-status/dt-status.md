# Dt status

## Model

- Candidate (unconfirmed): a production Status-kind [label](../../../../../modules/knowledge/label/label.md) set — `Created`, `ManagerApprove`, `WarehouseApprove`, `ActiveWithApprove`, `ActiveWithoutApprove`, `ActiveWithOrderer`, `Inactive`, `Normal`, `Reject`, `Void` (ten words in one source `const`-comment list; `type Status qs_p.Status` aliases a shared Status catalog — shape unconfirmed).

## Policies (rules)

- Approval-chain words in the list: `ManagerApprove`, `WarehouseApprove` — two human approval gates before activation.
- Activation variants: `ActiveWithApprove`, `ActiveWithoutApprove`, `ActiveWithOrderer` — three ways a production may go active.
- The identical nine-word list (without `Void`) also appears in [task production](../../../../../modules/management/task/edges/production/production.md) Policies — one vocabulary, two homes of record until reconciled.

## Placement

- **Correct here — the domain declares its own Status-kind words** ([Documentation → Status](../../../../../modules-plugable/knowledge/documentation/documentation.md#status): each as `Label_<Word>` under that domain's `labels/` taking `Label_Status`; production states its candidate here, [production.md](../../production.md) never repeats the list).
- **Not general thing/labels words:** production approval words are production vocabulary (placement by entry point; pluggable owns complete capability — the labels + the approval rules that read them).
- **Not [management/task](../../../../../modules/management/task/edges/production/production.md):** task-side production vocabulary is the task work relation; this dt-status set is the economics-production lifecycle — reconcile the two lists to one home rather than drift (receiving [production.md](../../production.md) backlog question; prefer existing homes over inventing new modules).
- Approval words (`ManagerApprove`/`WarehouseApprove`) may be rule material rather than Status-kind labels — record before ratifying (no bare edges; core never knows Rule).

## Open questions

- Are the approval-chain states (`ManagerApprove`/`WarehouseApprove`) a workflow rule rather than Status-kind labels?
- Own production Status-kind set under production `labels/`, or shared words under `thing/labels/` ([Documentation → Status](../../../../../modules-plugable/knowledge/documentation/documentation.md#status))? The quiddity-status alias (`qs_p.Status`) hints at sharing — confirm.
- Same list as task-side [task production](../../../../../modules/management/task/edges/production/production.md) (nine words) plus `Void` here — one list or two (production lifecycle vs task work)?
- What distinguishes `Normal` from `Active*` — a resting state after activation, or a synonym?

