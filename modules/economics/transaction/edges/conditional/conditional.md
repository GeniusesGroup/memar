# Conditional transaction

## Dictionary

conditional  [-ʃənl]   
adj.
1. qualified by reservations
2. imposing or depending on or containing a condition

## Model

- `(transaction)-[:condition_is]->(rule)`
- `(rule)-[:is_condition_for]->(transaction)`

## Policies (rules)

- The conditional `rule` can also have relation with other domain such as `contract`
- e.g. if the `invoice` get `delivered` `status`, the `transaction` will be processed.
- A `conditional` transaction can get an `instant_withdrawal` label too, to show that it can be settled instantly.
- `rule` is the first-class node of [modules/computer/rule](../../../../computer/rule/README.md); evaluating the condition is the rules-engine's job, not this edge's (cross-checked 2026-09).
- The kernel defines no behavior for condition satisfaction; the rule and its owning pluggable module decide what transactions/bookings follow.

## Fields
