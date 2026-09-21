# Staff
Staff relates users to organizations as personnel.

## Idea backlog from edge code comments

Raw proposals from comment notes inside edge .go files (comments remain in code as source). Review discipline per [vocabulary-discipline.handoff.md](../vocabulary-discipline.handoff.md). Nothing below is ratified.

### Hiring pipeline - edges/staff.go
- **Idea**: hiring-interview pipeline labels (Requester, Referral, Talent/high-skill-match, then Need/Approve pairs for HR, Technical, Manager, Chief, Board interviews); rejection cooldowns (LockFor1/3/6/12Month); acceptance steps (Designation, Negotiation, Reserved, ContractProposal).
- **Review questions**: is the pipeline a status machine on a hiring Task, or labels? Do cooldowns belong to policy (rules) instead of labels?

### Staff relations - edges/staff-relation-group.go, edges/staff-relation-staff.go
- **Idea**: Evaluation (by staff itself, manager, other staff); Referral; PresentedID (staff-take-leave-alternate or replacement); HireFor/HireBy.
- **Review questions**: does Evaluation reuse the endorsement pattern from knowledge/skill?

### Lifecycle - edges/staff-status.go
- **Idea**: Status_Hire/Fire/End (death, end of contract); shift Active/Inactive commented out.
- **Review questions**: is End-of-contract a status or an event? Do shift states belong here or to shift?

### Leave taxonomy (currently misfiled) - modules/rights/ownership/edges-loop/task-relation-staff.go
- **Idea**: a full leave/reason taxonomy: Interview, OverTime, TakeLeave, Mission, Meeting, Negotiation, Deal, Study; leave types (Vacation, Travel, Rest, Study, Marriage, Casual, Sick, Pain, TemporaryDisability, AdverseWeather, Compensatory/TOIL, Sabbatical, Gift, Unpaid, Maternity, Paternity, Bereavement, PublicHoliday, ReligiousHolidays, JuryDuty, Protest, Volunteer).
- **Review questions**: this taxonomy lives in the ownership module but is HR material - the correct home is likely here as a task label set or a pluggable leave module; confirm against the rights-first ordering in [modules/rights/README.md](../../rights/README.md).