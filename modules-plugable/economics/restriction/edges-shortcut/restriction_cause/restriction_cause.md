# restriction_cause

## Dictionary

## Model

- `(transaction)-[:restriction_cause_is]->(case)`
- `(case)-[:restriction_cause_for]->(transaction)`

## Policies (rules)

- When a transaction get related `case` as `reference`
- When a transaction get related `rule` as `condition_is`

## Fields
