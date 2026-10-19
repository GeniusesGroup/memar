# Task relation staff

## Model

- Candidate (unconfirmed): a task-to-staff relation — `(task)-[:relation_staff]->(staff)` — carrying one of the HR/leave labels below (source was `package label` holding comments only, no edge code).
- Sits beside the sibling task relations already reviewed in [ownership.md](../../ownership.md); [assigner](../assigner/assigner.md) in this folder carries the `Assigned` label.

## Policies (rules)

- **Activity labels**: Interview, OverTime, TakeLeave, Mission, Meeting, Negotiation, Deal, Study.
- **Take-leave labels** (usually four weeks of paid leave for each year of service; shift-workers are entitled to five weeks): Vacation, Travel, Rest, Study, Marriage, Casual.
- **Sick labels** (time off given by the company to allow employees to recover from an illness and take care of their health): Sick, Women period, ..., Pain, TemporaryDisability.
- **Other leave**: AdverseWeather (heavy snow, hurricane, or flash flooding makes travel to work extremely difficult, dangerous, or impossible), Compensatory (time off in lieu for employees who clocked in more hours than required), Sabbatical (companies whose employees served more than 3 years often grant it to reward loyalty and hard work), Gift (paid or unpaid time off gift), Unpaid (leave without pay).
- **FamilyEvents**: Maternity (recovery from delivery and care of the newborn), Paternity (granted to new fathers - husbands or partners of a pregnant woman, surrogate parent, or someone who adopted a child - to take care of their newborns), Bereavement (sudden leave on losing a loved one; most HRs give 3 to 7 days depending on the closeness of the relative).
- **Civic and other**: PublicHoliday (given by the government; must be observed by every institution - schools, banks, government offices, and private companies), ReligiousHolidays (Christmas, Eid, Easter, Holi, Yom Kippur - days the employee would want to spend with family and observe the festival), JuryDuty, Protest, Volunteer.

## Placement

- **Not an edge of ownership; strip.** Assignment and HR labels grant no ownership: rights come first and ownership arises from rights ([rights.md](../../../rights.md)) — an HR taxonomy must not become an ownership primitive. Removing it distorts nothing in ownership (core-by-necessity fails).
- The review already has an existing home: [staff.md](../../../../management/staff/staff.md) links this doc from its [Edges](../../../../management/staff/staff.md#edges) section as the misfiled HR taxonomy — the proposal (a task label set there or a pluggable leave module) is recorded under Open questions below; prefer that cross-reference over inventing a rights-side module.
- No bare edges: the source records labels only — no who-may-assign and no what-it-triggers — so the labels must not stand as ownership edges; the processing semantics, once defined, stay with the staff/HR capability that gives them meaning.

## Open questions

- Task label set inside [staff](../../../../management/staff/staff.md) vs a pluggable leave capability — which owner takes the processing?
- Reconcile with the rights-first ordering ([rights.md](../../../rights.md)): why do task-relations live under ownership at all — assignment is not ownership?
- Relation to [assigner](../assigner/assigner.md) ("Assigned") and to the sibling [group](../group/group.md) / [user](../user/user.md) docs — one task-relation mechanism or three?

