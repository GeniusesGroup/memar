# Repetitive

## Model

- `(task)-[:---]->(repetitive)`

## Policies (rules)

- It is task template and MUST made other related task when need to do the task in that period.
- Related task MUST made by rule domain by `rules-engine` not human process.
- e.g. `Monthly financial report` made this `Financial report - 2024/09`
- this task types MUST indicate internal process to executes by some related rule
- e.g. `CFO` or `C level role` MUST approve `Monthly financial report` related tasks.
