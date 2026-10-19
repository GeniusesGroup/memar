# Citations number

## Model

- `(text)-[:text_citation_gotten_from]->(text(reference))`
- `(text(reference))-[:text_citation_given_to]->(text)`

## Policies (rules)

- The relation is read per text: a request carries the text's identity, and the
  response carries the total number of citations.

## Open questions

- The same total is also reachable from a token's own surface, where it sits
  beside the token's weights and scores. Two homes for one number, or one
  number read once?
- Nothing in this relation states who may count: a text's citation count is
  public to whoever can read the text.
