# Management
[Management](https://en.wikipedia.org/wiki/Management) is the administration of organizations. It is the process of managing the resources of businesses, governments, and other organizations.

## Manage

Manage (Managing) involves Planning, Controlling, Organizing, Coordinating, Leading, Monitoring and Implementing strategies in an organization towards achieving its desired goals & objectives.

According to [Henri Fayol](https://en.wikipedia.org/wiki/Henri_Fayol), management operates through five basic functions: planning, organizing, commanding, coordinating and controlling.
- Planning: Deciding what needs to happen in the future and generating action plans (deciding in advance).
- Organizing (or staffing): Making sure the human and nonhuman resources are put into place.
- Commanding (or leading): Determining what must be done in a situation and getting people to do it.
- Coordinating: Creating a structure through which an organization's goals can be accomplished.
- Controlling: Checking progress against plans.

Note: "leading/commanding" here is Fayol's observable managerial activity. The popular umbrella concept "Leadership" is deliberately **not** a modeled entity in this module.

## Organize

to make the necessary arrangements so that an activity can happen effectively

## Staff and line

[Staff and line](https://en.wikipedia.org/wiki/Staff_and_line) are names given to different types of functions in organizations. A line function is one that directly advances an organization in its core work.

## Idea backlog

Review discipline per [vocabulary-discipline.handoff.md](vocabulary-discipline.handoff.md). Nothing below is ratified. The organization module has no module.md of its own yet, so its items are held here at the category level.

### Organization lifecycle
- **Idea**: organizations can just have a finish date and can't be deleted — "Organizations can just have finish date, and can't be delete data! Due some legal complexity we think delete org is not reality and must warn user on register service!!"; reopening is restricted: "Just justice MS can do this operation.".
- **Review questions**: finish-date-not-delete — lifecycle status or a registration rule (warn-on-register)? Justice-ministry-system-only unblock — an authorization rule (core never knows Rule)? Concept home for Organization vs Group: [identity/organization](../identity/organization/organization.md).

### Calendar
- **Idea**: visibility labels Public, Private, Official; service-availability windows: "what days in weekday in utc time week this department or role active to provide services" and "what hours in a day this department or role active to provide services".
- **Review questions**: do these labels belong to the [calendar](calendar/calendar.md) module (its backlog already routes reason labels to a pluggable), or to department/role availability as rules over time? UTC-weekday semantics vs [shift](shift/shift.md)?

### Calendar event labels
- **Idea**: one cross-domain time-label dump:
  - Task/production/batch domain — e.g. staff(123) ManualStart the specific shift (as a task type); what hours in a day this staff must active to provide services or do projects. Labels: ExpectedTime, Deadline, ManualStart, ManualTemporaryEnd, ManualEnd, Start, TemporaryEnd, End. It can also be just preference, not real action event: staff-shift-preference.
  - Product domain — product-duration (Can USE valid after 7 days from purchase time); product-reserve-validity (Can BUY 15 minutes from add to invoice time); product-timing (what hours in a day the service active to provide services); product-time-validity (flight departure and arrival time, concert start and end time, ...).
  - Open: notification serve or silent.
  - Invoice domain — invoice-Item-reserve-time; ActionTime.
  - Earth UTC day — Holiday, Anniversary, UnexpectedClosure.
  - Quiddity level — "it will change the status of the thing to Expired after specified time; e.g. the `rule`(123) or `order`(456) or `form`(789) or `question`(147) MUST invalid after certain of time": Validity.
  - Form — form-start-point (Also can use `Start` or `End` instead of introduce new label).
  - Network Connection — LastUsage (Also can use `Start` or `End` instead of introduce new label).
  - User — Birthday; VerifiedDate (User got famous blue badge (tick) like instagram, twitter, ...).
- **Review questions**: the set spans task, product, invoice, knowledge and identity — should each cluster move to its owning domain's labels instead of one calendar-event home (no cross-domain label dumping)? Do Start/End subsume form-start-point and LastUsage (the comment itself suggests it)? Event lifecycle vs [timeline](timeline/timeline.md)? Validity-with-expiry vs the rule domain's time limits?
