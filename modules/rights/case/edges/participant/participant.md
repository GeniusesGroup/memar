# Case relation user

## Model

- Unratified inventory, not an edge to write: a source note once sketched `(case)-[:participant]->(user)` with the labels below. Phase 0 does not implement that edge. The model is [plaintiff](../plaintiff/plaintiff.md), [defendant](../defendant/defendant.md), and [judge](../judge/judge.md).

## Policies (rules)

- Participant roles: `Judge`, `Jury` ("a body of citizens sworn to give a true verdict according to the evidence presented in a court of law"), `Plaintiff` ("a person who brings an action in a court of law"), `Defendant` ("the person being sued or accused"), `Suspect` (present but commented out in the source), `Lawyer` ("the lawyer representing the defendant"), `TrialAttorney`, `Counsellor`, `JudicialOfficer` (bailiff noted: "an officer of the court who is employed to execute writs and processes and make arrests etc."), `Witness`.
- Decision-vocabulary notes (commented, unlinked): `Dismissal` ("a judgment disposing of the matter without a trial"), `Invalidate`, `Guilty`, `Conditionally` ("it will only be true if something else happens first").
- Responsibility notes: "Types of responsibility, including relative or joint liability".
- "organization that claim service must call."
- No who-may-assign/what-it-triggers recorded — the labels must not be ratified as edges (no bare edges).
- The case–user model writes [plaintiff](../plaintiff/plaintiff.md), [defendant](../defendant/defendant.md), and [judge](../judge/judge.md). An implementer does not write `participant`. Any user type may be plaintiff or expert. One case has one defendant. Expert is not its own edge. A person who votes is seated on the judge edge. Judge, Plaintiff, and Defendant on this list are names of those three edges, not a second attachment. Jury, Suspect, Lawyer, TrialAttorney, Counsellor, JudicialOfficer, and Witness may exist as pluggable edges, each added for its own reason. They are not kernel, and this revision does not write them. A judge may say the claim needs ten jurors. That module assigns people by its own rules and may update their social rank for taking part. The rank rule is not designed here.
- What would falsify the rule that none of Jury, Suspect, Lawyer, TrialAttorney, Counsellor, JudicialOfficer, and Witness is kernel: one of those seven as a kernel edge. Model v4 point 16. Each of those seven may still be a pluggable edge when its own reason is stated, as the open questions below record.

## Placement

- **Correct here** — justice roles annotate the case–user relation this folder owns; entry point is the case, and the capability (relation + role vocabulary) stays together. Not [management/role](../../../../management/role/role.md): that module assigns *organizational* roles with their own processing, while these labels name participants of one case instance (prefer the existing home).
- The decision/responsibility notes are case-outcome vocabulary: they belong with the case — the no-finality principle in [case.md](../../case.md) demands an explicit state machine before any of them exists as a state; never bare edges until who-may-decide/what-it-triggers is defined (core never knows Rule).
- Not a new module: a label set alone is parameters, not processing (parameters vs semantics) — configuration beside the relation until processing proves distinct.
- Phase-0 draft: one participant edge with many labels cannot say that the same user is plaintiff on one case and defendant on another. The part is the edge type, per case. This file remains the unratified inventory. It is not a shape an implementer writes beside the three edges.

## Open questions

- Are participant roles the same mechanism as [management/role](../../../../management/role/role.md), or case-specific?
- Do decision types need an explicit state machine (the no-finality principle in [case.md](../../case.md))?
- Liability vocabulary intersects the rights-domain-boundaries handoff open question ([rights-domain-boundaries.handoff.md](../../../rights-domain-boundaries.handoff.md)).
- Is `Suspect` (commented out) a planned role or a deliberately rejected one?
- Direction and naming unconfirmed — nothing ratified.
- None of Jury, Suspect, Lawyer, TrialAttorney, Counsellor, JudicialOfficer, and Witness is a kernel edge. Each may be a pluggable edge when its own reason is stated. The glosses are not that reason.
