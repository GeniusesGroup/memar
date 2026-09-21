# Limit max event

## Model

- `(timeline)-[:limit_max_event]->(---)`
- `(limit_max_event)-[:preference_for]->(event)`

## Policies (rules)

- Limit max event in two way:
- 1- auto delete old event e.g. post notification in social apps but why need this?? delete data?? really??
- 2- no event can register when timeline is full
