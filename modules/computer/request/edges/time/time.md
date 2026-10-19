# Time

## Model

- `(request)-[:request_time]->(time)`
- `(time)-[:request_time]->(request)`

## Policies (rules)

- For each user MUST have dedicate time category.
- Use `minute` window to category user requests??
