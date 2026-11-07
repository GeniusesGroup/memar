# Transaction relation user

## Model

- Candidate (unconfirmed): `(transaction)-[:relation_user]->(user)` carrying responsibility labels `Rectifier`, `Executor`, `Quality_Controller` — users holding specific responsibility over a budget's transactions (direction unconfirmed).

## Policies (rules)

- Header comment "Budget relation:::" scopes the three roles to budget transactions.
- `Rectifier` / `Executor` / `Quality_Controller` recorded without semantics — what each role may do (approve? perform? audit?), absent from the source (no bare edges).

## Placement

The budget-responsibility link is instantiated from the budget capability; budget names users by identity.
