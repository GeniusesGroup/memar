# Label allowed

## Model

- `(label)-[:label_allowed_in]->(module(vertices))`
- `(module(vertices))-[:allowed_label_is]->(label)`

## Open questions

- is module-scoping enforced at registration time or per-assignment?

## Source

> Source: `modules/knowledge/label/edges/label-allowed/protocol/data_model.go` (in code).
