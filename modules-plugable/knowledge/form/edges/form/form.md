# Form relation form

## Model

- Candidate (unconfirmed): a form-to-form relation carrying kind labels — `Alternative`, `EasierAlternative`, `HarderAlternative`, `SameForm_DifferentOrder`, `Basic`, `SamePurpose_MoreQuestion` (direction unconfirmed).
- The source sits in `package label`, so the six strings may be label names attached to one generic form-to-form edge rather than six distinct edges.

## Policies (rules)

- No rules recorded: who may set a kind, and what a kind triggers (grouping? ordering constraint? recommendation?), are absent from the source (no bare edges).

## Placement

- **Correct here — the form-to-form relation stays with the form capability** (module skeleton: `form/edges/`); placement by entry point — the relation is instantiated from a form; prefer existing homes over inventing new modules).
- **Not a new module:** six kind labels are a *parameter* vocabulary on one relation (parameters vs semantics ⇒ one form capability plus per-organization kind configuration); an edge becomes a module only when it carries independent processing semantics — none recorded.
- **Not the rule domain:** kinds like Alternative/Basic do not decide who may answer a form; where access or prerequisite decisions appear they stay generic rule attachments this capability reads (core never knows Rule; a pluggable likewise keeps policy out of its kernel while owning the complete edge + processing together).

## Open questions

- One edge with a kind/label field, or one edge per kind — labels-on-edge vs distinct edges?
- `Basic` — prerequisite ("take this form first") or difficulty baseline? A prerequisite implies ordering processing that must be recorded before the edge may exist (no bare edges).
- `SameForm_DifferentOrder` / `SamePurpose_MoreQuestion` — an alternative-form assembly or recommendation feature? What triggers it, and who maintains it?
- Direction/naming unconfirmed — nothing ratified.

