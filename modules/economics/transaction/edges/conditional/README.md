# Conditional transaction


## Dictionary
conditional  [-ʃənl]   
adj.
1. qualified by reservations
2. imposing or depending on or containing a condition

## Graph
- `(transaction)-[:condition_is]->(rule)`
- `(rule)-[:is_condition_for]->(transaction)`

## Policy (rule)
- The conditional `rule` can also have relation with other domain such as `contract`
- e.g. if the `invoice` get `delivered` `status`, the `transaction` will be processed.
- A `conditional` transaction can get an `instant_withdrawal` label too, to show that it can be settled instantly.

## Fields
