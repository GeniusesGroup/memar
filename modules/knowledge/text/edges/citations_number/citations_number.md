# Citations number

## Model

- `(text)-[:text_citation_gotten_from]->(text(reference))`
- `(text(reference))-[:text_citation_given_to]->(text)`

## Policies (rules)

- The relation is read per text: a request carries the text's identity, and the
  response carries the total number of citations.
