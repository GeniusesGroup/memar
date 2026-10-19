# Rule Authorization

## Model

- `(rule)-[:authorization_for]->(thing)`
- `(thing)-[:authorization_by]->(rule)`

## Policies (rules)

- thing can be any module or record UUID such as group, task, thing, channel, label, form

## TODO

- For authorization purpose, Let use other domain UUID e.g. `label_p.UUID` or `form_p.UUID`, ... as RuleUUID??

## Fields
