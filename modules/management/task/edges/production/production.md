# Production

## Model

- Candidate (unconfirmed): `(task)-[:production]->(task)` — production relations between tasks (direction/name unconfirmed; source was a task-edge label file).
- `Production` doubles as a *task label*: "Production is also other label for a task" — parallel to the "a project is itself a Task" seed in [task-concept](../task-concept.md).

## Policies (rules)

- "Other labels suggest to users when a task related to a `production` labeled task!" — related labels are *suggested*, not forced.
- Manufacturing uses tangible raw materials to create goods (lumber, minerals); Fabrication involves combining different parts to form a finished product; Production uses both tangible raw materials and intangible resources (money or credit).
- Production product lines: CustomProduction, MassProduction; ByProduct.
- "Some product as material need or pend on other production,.e.g. car needs engine, ..."
- job-order; production-planning.
- Production statuses: Created, ManagerApprove, WarehouseApprove, ActiveWithApprove, ActiveWithoutApprove, ActiveWithOrderer, Inactive, Normal, Reject.

## Placement

- **Correct here — production work is task-side.** The vocabulary describes *work* (job-order, production-planning, approval statuses of making) and the task module is its existing home (module skeleton: `task/edges/`); no new module is warranted (prefer existing homes over inventing new modules).
- **Not `economics/product`:** the product-side material questions have their own per-edge doc — [material](../../../../economics/product/edges/material/material.md) ("Material or Ingredient") — keep product identity there and this task-side relation here; no second copy of the product questions.
- The label-suggestion behavior ("other labels suggest to users") is a view/projection concern — pluggable GUI, never task-kernel code; approval statuses stay open against the general status domain (see Open questions below); any "MUST approve before Active" enforcement is rule material (core never knows Rule).

## Open questions

- Production as task *kind* (label / edges-loop type) vs an edge to a production/product node — which is it? ("project IS a task" precedent.)
- Material dependency / ByProduct / product lines: task-side relation or product-side identity? Converge with [material](../../../../economics/product/edges/material/material.md) — one home, not two.
- Production statuses vs the general status domain (knowledge/status): own status set or labels?
- Suggestion of labels: GUI projection or stored semantics?

