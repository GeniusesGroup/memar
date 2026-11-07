# Pos relation staff

## Model

- Candidate (unconfirmed): `(pos)-[:relation_staff]->(user)` — a staff-restriction link on the register (direction unconfirmed).

## Policies (rules)

- "Provider or operator is to limit pos to specific staffs." — the register's provider/operator restricts which staff may operate it.

## Placement

- **Correct here — the staff limit is instantiated from the register capability**.
- **Not core `user`/staff domain:** staff stays the people domain and is referenced by identity (reference-not-embed); an org without POS has no such edge.
- **Not a new module:** one restriction link is a parameter of register operation (parameters vs semantics; prefer existing homes over inventing new modules).
- **Sibling:** [group](../group/group.md) restricts by *role* instead of named staff — same intent (who may operate), two selectors; keep them side by side and converge.
- If enforced as access control, the decision reads like the access-control example ("answer exam just when they are in the school") — the who-may-operate decision is rule material; the edge is the structural attachment (no bare edges; core never knows Rule).
