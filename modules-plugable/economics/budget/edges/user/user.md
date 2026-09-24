# Transaction relation user

## Model

- Candidate (unconfirmed): `(transaction)-[:relation_user]->(user)` carrying responsibility labels `Rectifier`, `Executor`, `Quality_Controller` — users holding specific responsibility over a budget's transactions (direction unconfirmed).

## Policies (rules)

- Header comment "Budget relation:::" scopes the three roles to budget transactions.
- `Rectifier` / `Executor` / `Quality_Controller` recorded without semantics — what each role may do (approve? perform? audit?), absent from the source (no bare edges).

## Placement

- **Correct here — the budget-responsibility link is instantiated from the budget capability**.
- **Not core `transaction`/`user`:** core moves money between accounts without knowing budget roles (core never knows Rule; reference-not-embed — budget names users by identity).
- **Not the general role/delegation machinery:** these are budget-scoped *responsibility labels on transactions*, a parameter vocabulary of this capability (parameters vs semantics; prefer existing homes over inventing new modules). If they must *enforce* who may act, that decision is rule material to record first (no bare edges).
- **Not a new module:** three labels on one relation are not independent processing semantics.

## Open questions

- Receiving [budget.md](../../budget.md) review question: are these role labels or the general role/delegation machinery? Budget-role and budget-label vocabulary converges in [budget.md](../../budget.md) Open questions (one home, incl. the Materials/Labor list shared with the transaction shortcut comments).
- What does each role trigger — Rectifier corrects, Executor performs, Quality_Controller approves? Record before ratifying (no bare edges).
- Are the roles statuses (sync service checks) or labels (async business-rule checks) per [status](../../../../../modules/knowledge/status/status.md)?
- Direction/naming unconfirmed — nothing ratified.

