# Terms

## Model

- `(contract)-[:terms]->(text)` (note: HTML, CSS, JS base)
- `(contract)-[:terms]->(object)` (note: Solidity PL is other option)

## Policies (rules)

- If the `contract` have `template` label, terms will be in blank format
- If the `contract` don't have `template` label, terms will just data to fill base terms.
