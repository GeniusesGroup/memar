# Endorsement
Endorsement refers to transfer transaction ownership to another entity, serving as a legal verification. In old financial system it MUST be done by signing the back of a check.

## Dictionary

## Model

- `(transaction)-[:endorsement_in_favor_of]->(transaction)`
- `(transaction)-[:is_endorsement_for]->(transaction)`

## Policies (rules)

- a `transaction` CAN have more than one `endorsement` to split first transaction quantity.
- TODO::: Is it shortcut edge?? `SUSPENDED_BY`

## Fields
