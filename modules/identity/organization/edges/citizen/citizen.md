# Citizenship

## Model

- Candidate (unconfirmed): `(user)-[:citizen]->(organization)` — user–organization label `Citizen` (source was the organization-to-user relation file). Example form recorded in the source: `[User, Organization, Label] >> ["Omid", "Universe", "Citizen"]`.
- Voting-rights lifecycle riding on the same relation: voting rights, permanently entitled to vote, temporary voting rights, suspension of voting rights, permanent loss of voting rights — count, direction, and states unconfirmed.

## Policies (rules)

- "Citizen" carries a voting-rights lifecycle: permanently entitled to vote → temporary voting rights → suspension of voting rights → permanent loss of voting rights.
- No who-may-grant/what-it-triggers recorded in the source — the label must not be ratified until those exist (no bare edges).

## Placement

- **Correct here** — the user–organization member relation is identity's own: `User`/`Organization` sit under identity while `Group` sits under [management/group](../../../../management/group/README.md) (see [organization.md](../../organization.md) § "Organization vs. Group"); citizenship *is* that member relation, so the structural label attachment stays in this module.
- **The voting-rights semantics are not this module's.** Franchise (who votes, when rights suspend) is a capability evaluation, not organization identity — its home is the existing rights domain ([rights](../../../../rights/rights.md), cf. [law/voting](../../../../rights/law/labels/voting/voting.md)); organization carries only the label the evaluation reads. Parameters vs semantics: the lifecycle stages are parameter states of one relation until proven to need distinct processing — no new module on their account (prefer existing homes).
- Not a bare edge: who may set `Citizen`, and what granting/suspending triggers, must be defined before the edge exists (no bare edges).
