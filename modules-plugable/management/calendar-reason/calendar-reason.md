# Calendar Reason
A pluggable module giving organizations a vocabulary of **reasons for creating a calendar record** - cooking, event, enter/exit (attendance), start/end (work periods), packaging. Each reason is a classification of the calendar record, so it lives under `edges-loop/` with its own README; each carries its own organization policy. The folder is named `calendar-reason` so it does not mimic the core `calendar` domain.

## Why pluggable
Which reasons an organization needs, and which rules govern each (who may enter/exit, when packaging is allowed), are organization-specific policies: a difference in processing semantics → pluggable module; the calendar reason vocabulary itself stays attachable without forcing every organization to carry every reason. The calendar core (if any) stays in management; this module is pluggable.

The reason set is a rule vocabulary and each reason is attachable on its own.
