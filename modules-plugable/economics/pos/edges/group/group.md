# Pos relation group

## Model

- Candidate (unconfirmed): `(pos)-[:relation_group]->(group)` — a role-group restriction link on the register (direction unconfirmed).

## Policies (rules)

- "Provider or operator is to limit pos to specific roles." — the register's provider/operator restricts which roles (groups) may operate it.

## Placement

- **Correct here — the role limit is instantiated from the register capability**.
- **Not [management/group](../../../../../modules/management/group/group.md):** group stays the membership domain and needs no POS-side edge; the register references the group by identity (reference-not-embed).
- **Not a new module:** one restriction link is a parameter of register operation (parameters vs semantics; prefer existing homes over inventing new modules).
- **Sibling:** [staff](../staff/staff.md) restricts by named staff instead of roles — same intent (who may operate), two selectors; keep them side by side and converge (see Open questions).
- If enforced as access control, the who-may-operate decision is rule material; the edge is the structural attachment the rule reads (no bare edges; core never knows Rule).

## Open questions

- Role selector vs [staff](../staff/staff.md) staff selector — one edge with a selector mode, or two distinct edges? One review (Receiving [pos.md](../../pos.md) backlog: "provider/operator limiting POS to specific staff or roles").
- Who may set/remove the limit, and what does it trigger (login gating? invoice signing?) — no-bare-edges test open.
- Which group vocabulary (roles vs ad-hoc groups) — does "roles" mean the group module's role taxonomy specifically?
- Direction/naming unconfirmed — nothing ratified.

