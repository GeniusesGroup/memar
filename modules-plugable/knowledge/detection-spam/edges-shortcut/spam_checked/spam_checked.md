# Spam checked

## Model

- `(---)-[:spam_checker]->(rule)-[:checked]->(text)`
- `(text)-[:spam_checked_by]->(rule)`
- `(rule)-[:spam_checked_for]->(text)`

## Policies (rules)

- This rule MAY labeled any text that checked with its rules as `spam`
