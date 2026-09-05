# Meeting

## Model

- `(task)-[:meeting]->(---)`

## Policies (rules)

- When a task get `meeting` label this rule will called.
- Participant or meeting manager MUST do some stuff:
- MUST set task title as `minutes`
- MUST fill related `form` e.g. Meeting result, ...
