# Item ingredient

## Model

- `(invoice_item)-[:invoice_item_ingredient]->(---)` — target candidate (unconfirmed): the protocol keys the record on `Field_InvoiceID` + `Field_InvoiceItemID` + `IngredientID product_p.UUID` + quantity + status, i.e. the ingredient is typed as a product UUID — see [data_model.kh](protocol/data_model.kh).
- Query services: `LIST_ProductIDs_BY_InvoiceID` (product IDs an invoice claims) and `LIST_IngredientIDs_BY_InvoiceID_AND_ProductID` (ingredient IDs chosen on one invoice line for one product).

## Policies (rules)

- Chosen ingredients ride on the invoice line at order time — [good.md](../../good.md) states this is "the same capability at order time, not Invoice kernel".
- The source recorded only the two read queries — no who-may-create / what-it-triggers rules; pick semantics unconfirmed (no-bare-edges test open).

## Placement

- **Correct here — `modules-plugable/economics/good/edges/item-ingredient` (already its home).** Pluggable owns complete capability: ingredient choice is a good-module capability realized at order time (stated in [good.md](../../good.md)); the edge and its query services travel together — never "edge here, behavior there".
- **Not core `invoice`:** an invoice claims priceable lines without knowing ingredients (core-by-necessity fails); an organization without physical goods removes the module whole (removable ⇒ pluggable).
- **Not core `product`:** ingredient composition is physical-goods semantics, not priceability — product stays the unit of priceability; good/service were deliberately kept pluggable (see [product.md](../../../../../modules/economics/product/product.md)).
- **Not a bare edge:** ingredient/material vocabulary already lives in this module ([material](../material/); good.md backlog) — the queries are reads over that capability (parameters vs semantics ⇒ no separate module).

## Open questions

- Endpoint: protocol types `IngredientID` as a product UUID and also carries `Field_LabelUUID` — ingredient-as-product vs ingredient-as-label ([knowledge/label](../../../../../modules/knowledge/label/label.md))?
- Recipe vs choice: product-level [material](../material/) (the base/ingredient model) versus this order-time choice — one capability observed at two times, or two distinct edges?
- Status lifecycle (`Field_Status`, [dt-status.kh](protocol/dt-status.kh)) — who moves it and what triggers the move (no-bare-edges test)?
- [transaction.md](../../../../../modules/economics/transaction/transaction.md) filed these listings as "data-model pass material" — do they survive the pass as this edge's protocol API?

