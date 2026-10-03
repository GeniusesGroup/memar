# Text type

## Model

- `(label)-[:text_type]->(---)`
- `(text)-[:text_type_is]->(text_type)`
- `(text)-[:text_type_is]->(label)-[:text_type]->(---)`

## Policies (rules)

- Each text MUST have a specific type.

## Open questions

- A text's type is a label, so the relation reads as the label classified and
  the text classified. Two of the three model lines above say so and the third
  (`(text)-[:text_type]->(text_type)`) says a separate node — one relation or
  two?
- Because the type is a label and not a value of the text domain, this folder's
  protocol cannot be converted until the label domain declares its identifier.
  See the handoff.
