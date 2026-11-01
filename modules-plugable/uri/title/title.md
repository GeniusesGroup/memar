# Title

## Model

- `(uri(text))-[:title_for]->(thing)`
- `(thing)-[:title_is]->(uri(text))`

## Policies (rules)

- or DisplayName or human usage name
- `thing` CAN be any other domain e.g. `user`, `product`, `knowledge`, ...

## Related Artifacts

- Title Handoff
- [`protocol/`](protocol/) - the abstraction, in Khayyam
