# Invoice pre-order
A [pre-order](https://en.wikipedia.org/wiki/Pre-order) is an order placed for an item that has not yet been released.

## Model

- `(invoice)-[:pre_order]->(___)`
- `(time{future})<-[:shipped_in]-(invoice)-[:invoice_item]->(product)->["produce-_in]->(time{future})`

## Policies (rules)

## Fields
