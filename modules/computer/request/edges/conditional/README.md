# Authorized

## Model

- `(request)-[:authorized_by]->(rule)`
- `(rule)-[:authorized]->(request)`

## Policies (rules)

- Store to know which `rule` allow this request to perform.
- rule_p.Field_AuthorizedBy
