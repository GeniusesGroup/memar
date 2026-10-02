# Tax relation product

## Model

- Candidate (unconfirmed): `(tax)-[:relation_product]->(product)` — tax applied to a product; the source records no labels of its own, only a reuse note.

## Policies (rules)

- "All `tax` labels can use here too." — the catalog in [tax](../tax/tax.md) (VAT, CustomsDuties, environmental family, blank = exempt) also binds product-to-tax; one vocabulary, two attachment points.

## Placement

- **Correct here — the tax-product link is instantiated from the tax capability** (placement by entry point; source `vat/edges/tax-relation-product.go` (no such file yet), deleted at `334d6e2c` 2026-09-09; pluggable owns complete capability — edge + rate/exemption logic that reads it live together).
- **Not core `product`:** the product kernel stays priceability; taxability is jurisdiction semantics an org removes with this module (removable ⇒ pluggable; core never knows Rule — who-may-exempt is rule material).
- **Not a new module:** the relation reuses the existing catalog (parameters vs semantics ⇒ one tax capability plus configuration; prefer existing homes over inventing new modules).

## Open questions

- Blank tax label = VAT-exempt ([tax](../tax/tax.md)) — exemption rides on this product link? Confirm the exempt path (product link vs invoice-line check).
- "up to two tax labels" scope — per product here? (Pairs with the scope question on [tax](../tax/tax.md).)
- Rate application over time (retroactive rate changes?) — rule/event material to record before ratifying (no bare edges).
- Naming unconfirmed — nothing ratified.

