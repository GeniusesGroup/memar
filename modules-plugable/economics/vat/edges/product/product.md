# Tax relation product

## Model

- Candidate (unconfirmed): `(tax)-[:relation_product]->(product)` — tax applied to a product; the source records no labels of its own, only a reuse note.

## Policies (rules)

- "All `tax` labels can use here too." — the catalog in [tax](../tax/tax.md) (VAT, CustomsDuties, environmental family, blank = exempt) also binds product-to-tax; one vocabulary, two attachment points.

## Placement

- **Correct here — the tax-product link is instantiated from the tax capability** (placement by entry point; pluggable owns complete capability — edge + rate/exemption logic that reads it live together).
- **Not core `product`:** the product kernel stays priceability; taxability is jurisdiction semantics an org removes with this module (removable ⇒ pluggable; core never knows Rule — who-may-exempt is rule material).
- **Not a new module:** the relation reuses the existing catalog (parameters vs semantics ⇒ one tax capability plus configuration; prefer existing homes over inventing new modules).
