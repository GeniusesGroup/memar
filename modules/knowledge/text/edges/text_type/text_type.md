# Text type

## Model

- `(label)-[:text_type]->(---)`
- `(text)-[:text_type_is]->(text_type)`
- `(text)-[:text_type_is]->(label)-[:text_type]->(---)`

## Policies (rules)

- Each text MUST have a specific type.
