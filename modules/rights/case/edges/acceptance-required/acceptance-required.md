# Acceptance required
Not a prerequisite that a registry inquiry imposes on other cases.

## Model

- A candidate edge `(case)-[:acceptance_required]->(case)` was drafted so a later case would stay in draft until an earlier case, in particular a registry inquiry, was accepted.
- The 2026-09-27 input rejects that use. A registry inquiry is its own claim. It is not a draft-gate that must exist before other cases.

## Policies (rules)

- A case is not held in draft because an inquiry is missing, unanswered, or rejected.
- The draft chain may change after an inquiry, or it may not exist yet, because the filer may not know the defendant.
- This revision records no other job for the edge. An implementer does not write it to make one case wait on an inquiry.
- Shared draft stays the status marker this phase already uses. A case the parties never take to a filing stays in shared draft. Leaving it there is not a status, a vote, or a shortcut.

## Placement

- **Not the inquiry gate.** The gate was the whole responsibility this file had. That responsibility is withdrawn.
- **Nearest alternative rejected:** treating every [petition-next](../petition-next/petition-next.md) edge as a completion gate. Order is still not acceptance.
- What would restore this edge: a wait between two cases that is not the inquiry prerequisite and that has its own who-may-create rule. None is recorded.

## Open questions

- None for the inquiry. A different wait is not invented here.
