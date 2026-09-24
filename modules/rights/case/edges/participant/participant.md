# Case relation user

## Model

- Candidate (unconfirmed): `(case)-[:participant]->(user)` carrying the justice-role labels below (source is a `package label` iota set plus scattered decision/responsibility notes — no edge code).

## Policies (rules)

- Participant roles: `Judge`, `Jury` ("a body of citizens sworn to give a true verdict according to the evidence presented in a court of law"), `Plaintiff` ("a person who brings an action in a court of law"), `Defendant` ("the person being sued or accused"), `Suspect` (present but commented out in the source), `Lawyer` ("the lawyer representing the defendant"), `TrialAttorney`, `Counsellor`, `JudicialOfficer` (bailiff noted: "an officer of the court who is employed to execute writs and processes and make arrests etc."), `Witness`.
- Decision-vocabulary notes (commented, unlinked): `Dismissal` ("a judgment disposing of the matter without a trial"), `Invalidate`, `Guilty`, `Conditionally` ("it will only be true if something else happens first").
- Responsibility notes: "Types of responsibility, including relative or joint liability".
- "organization that claim service must call."
- No who-may-assign/what-it-triggers recorded — the labels must not be ratified as edges (no bare edges).

## Placement

- **Correct here** — justice roles annotate the case–user relation this folder owns; entry point is the case, and the capability (relation + role vocabulary) stays together. Not [management/role](../../../../management/role/role.md): that module assigns *organizational* roles with their own processing, while these labels name participants of one case instance (prefer the existing home).
- The decision/responsibility notes are case-outcome vocabulary: they belong with the case — the no-finality principle in [case.md](../../case.md) demands an explicit state machine before any of them exists as a state; never bare edges until who-may-decide/what-it-triggers is defined (core never knows Rule).
- Not a new module: a label set alone is parameters, not processing (parameters vs semantics) — configuration beside the relation until processing proves distinct.

## Open questions

- Are participant roles the same mechanism as [management/role](../../../../management/role/role.md), or case-specific?
- Do decision types need an explicit state machine (the no-finality principle in [case.md](../../case.md))?
- Liability vocabulary intersects the rights-domain-boundaries handoff open question ([rights-domain-boundaries.handoff.md](../../../rights-domain-boundaries.handoff.md)).
- Is `Suspect` (commented out) a planned role or a deliberately rejected one?
- Direction and naming unconfirmed — nothing ratified.

