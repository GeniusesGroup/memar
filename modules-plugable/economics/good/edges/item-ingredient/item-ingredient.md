# Item ingredient

## Model

- `(invoice_item)-[:invoice_item_ingredient]->(---)` — the record and its query services are declared in [protocol](protocol/data_model.kh).

## Policies (rules)

- Chosen ingredients ride on the invoice line at order time — [good.md](../../good.md) states this is "the same capability at order time, not Invoice kernel".

## Placement

Ingredient choice is a capability of the good module realized at order time; the edge and its query services travel together in this module.
