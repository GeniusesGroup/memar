# Spam flaged rule

## Model

- `(---)-[:spam_checker]->(rule)-[:own]->(request)-><-[:spam]->(text)`
- `(text)-[:spam_flagged__rule_by]->(rule)`
- `(rule)-[:spam_flagged__rule_for]->(text)`
