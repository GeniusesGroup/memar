# Task relation skill

## Model

- Candidate (unconfirmed): `(task)-[:requires]->(skill)` (name/direction unconfirmed) carrying a requirement-level label — source was a label-only file, no edge code. Pairs with the task-assignment rule in [task.md](../../task.md): assign users whose skills match the task's skill requirements.

## Policies (rules)

- `Mandatory` — "MUST, obligatory, compulsory, binding, required, inescapable, unavoidable, requisite, necessary, essential, imperative".
- `SHOULD` — "nice to have, optional, Conditional,".
- `MAY` — "not needed,".

## Placement

- **Correct here — the task's skill-requirement vocabulary is the task capability's own** (module skeleton: `task/edges/`; assignment-by-skill is defined in task.md; prefer existing homes over inventing new modules).
- Not [knowledge/skill](../../../../knowledge/skill/skill.md): skill identity/proficiency stays there; this edge only records *how required* a skill is for one task (entry point is the task).
- The RFC-2119-shaped level set is generic constraint vocabulary — if other domains (rights law, rule conditions) reuse it, it rises to the rule/constraint domain as *configuration* of this edge, not a forked copy (parameters-vs-semantics).
- Who assigns which level, and whether `Mandatory` blocks completion — policy → rules (core never knows Rule).

## Open questions

- Is this a general constraint vocabulary reusable beyond tasks (rights law, rule domain) — one shared MUST/SHOULD/MAY set with per-edge application?
- Levels as labels on one task-skill edge vs three edge kinds?
- Direction/naming unconfirmed — nothing ratified.

