# Cost

## Model

- `(batch)-[:cost]->(account)`

## Policies (rules)

- The cost structure and the pricing chain are declared in [data_model.kh](protocol/data_model.kh).
- The cost and pricing chain are the money story of the batch's identity: the edge and its chain fields travel together in this module.

## Source

> Source: `modules-plugable/economics/batch/edges/cost/protocol/data_model.kh` (in code).
