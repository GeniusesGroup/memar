# Form relation group

## Model

- Candidate (unconfirmed): `(form)-[:relation_group]->(group)` — the bare note "link to group" (direction unconfirmed).

## Policies (rules)

- Only "link to group" recorded — who may link, and what linking triggers (audience? ownership? prerequisite cohort?), are absent from the source (no bare edges).

## Placement

- **Correct here — the group link stays with the form capability** (placement by entry point: the link is instantiated from a form; pluggable owns complete capability — the edge and any answering-session processing it feeds live together, never "edge here, behavior there").
- **Not [management/group](../../../../../modules/management/group/group.md):** group stays the membership domain and needs no form-side edge; the form references the group by identity (reference-not-embed).
- **Not a new module and not bare-shipped:** a single unannotated link is not a module candidate (prefer existing homes over inventing new modules). If "link to group" means who may answer — cf. the [access-control](../../../../../modules-plugable/management/access-control/access-control.md) example "answer exam just when they are in the school" — that decision is rule material; the edge then exists as the structural attachment the rule reads, with semantics recorded first (no bare edges).

## Open questions

- What is the link for — form audience (who answers), ownership (who maintains), or cohort/class assignment?
- Is this the structural half of an access rule, with the who-may-answer decision living in the rule domain?
- Who may set/remove the link, and what does it trigger (no bare edges)?
- Direction/naming unconfirmed — nothing ratified.

