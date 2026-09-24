# Staff status

## Model

- Candidate (unconfirmed): employment lifecycle status set on staff: `Status_Hire`, `Status_Fire`, `Status_End` (code constants in [edges-loop/staff-status.go](../../edges-loop/staff-status.go)).
- Shift states `Status_Active` / `Status_Inactive` are commented out of the set and marked `Shift` — not staff lifecycle as recorded.

## Policies (rules)

- `Status_End` — "death, end of contract, ..." — terminal end of the employment relation.
- `Status_Active` / `Status_Inactive` — commented out with the note `Shift`.

## Placement

- **Correct here — the employment lifecycle is the staff capability's own** (module skeleton: `staff/edges-loop/`; hire/fire/end are what staff exists to record; prefer existing homes over inventing new modules).
- The source still lives in code at [edges-loop/staff-status.go](../../edges-loop/staff-status.go) (cited as `edges/staff-status.go`; moved into `edges-loop/` by commit be2f0810) — this doc records the vocabulary, the code stays untouched.
- Commented-out shift states belong to [shift](../../../shift/shift.md) if ever ratified — the code itself marks them `Shift`; keep lifecycle (staff) and shift (shift) separate.

## Open questions

- Is End-of-contract a status or an event (the domain backlog asked the same)?
- Do shift states belong here or to [shift](../../../shift/shift.md)?
- Status vs label vs edges-loop type — which mechanism carries this set (static embedding vs runtime type upgrade is open in [group.md](../../../group/group.md))?
- Who may hire/fire/end — a rule (core never knows Rule), not status-set code.

