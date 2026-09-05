# Pos editor

## Model

- `(invoice)-[:edit_by_pos]->(pos)`
- `(pos)-[:edit_invoice]->(invoice)`

## Policies (rules)

- Usually return from purchase
