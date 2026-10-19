# Pos relation staff

## Model

- Candidate (unconfirmed): `(pos)-[:relation_staff]->(user)` — a staff-restriction link on the register (direction unconfirmed).

## Policies (rules)

- "Provider or operator is to limit pos to specific staffs." — the register's provider/operator restricts which staff may operate it.

## Placement

- **Correct here — the staff limit is instantiated from the register capability**.
- **Not core `user`/staff domain:** staff stays the people domain and is referenced by identity (reference-not-embed); an org without POS has no such edge.
- **Not a new module:** one restriction link is a parameter of register operation (parameters vs semantics; prefer existing homes over inventing new modules).
- **Sibling:** [group](../group/group.md) restricts by *role* instead of named staff — same intent (who may operate), two selectors; keep them side by side and converge (see Open questions).
- If enforced as access control, the decision reads like the access-control example ("answer exam just when they are in the school") — the who-may-operate decision is rule material; the edge is the structural attachment (no bare edges; core never knows Rule).

## Open questions

- Staff selector vs [group](../group/group.md) role selector — one edge with a selector mode, or two distinct edges? One review (Receiving [pos.md](../../pos.md) backlog: "provider/operator limiting POS to specific staff or roles").
- Who may set/remove the limit, and what does it trigger (login gating? invoice signing?) — no-bare-edges test open.
- One POS to many staff, or many-to-many?
- Direction/naming unconfirmed — nothing ratified.

