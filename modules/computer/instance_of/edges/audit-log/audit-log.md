# Audit log

## Model

- `(software_instance)-[:time]->(audit_log)`

## Policies (rules)

- time usually be daily
- edge will be point to a object that bundle the time period logs
