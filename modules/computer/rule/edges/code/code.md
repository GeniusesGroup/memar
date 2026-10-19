# Rule code

## Model

- `(rule)-[:code_is]->(object)`
- `(object)-[:is_code_for]->(rule)`

## Policies (rules)

- Use to store executable logic on portable binaries like WASM, ...
- Logic (any statement) CAN write in general purpose language or DSLs.
