# Translation

## Model

- `(text)-[:translation_is]->(text)`
- `(text)-[:translation_for]->(text)`

## Policies (rules)

- Translation use in `Localization`
- A `thing` relate to each localization text by `title` and those `text` relate to each other by this label.
