# Optional

## Model

- Candidate (unconfirmed): a status/flag on the product-to-product relation marking it optional — the old protocol typed relations with `ProductRelation_Status_Optional` and a `RelationType` comment "Optional??" (see recovery note below).
- Reading: in a bundle/parent composition, this related product may be omitted (optional accessory/add-on rather than required component).

## Policies (rules)

- Bare source comment "Optional" — no who-may-create / what-it-triggers recorded; an edge status without semantics must not be ratified as-is (no bare edges).

## Placement

- **Not core `product` as a standalone edge:** an optional attachment is structure on an existing relation (parent/child or bundle), not a priceability capability.
- Likely a **status/flag on the relation** rather than its own edge — converges with the relation-status vocabulary of the old `ProductRelation` protocol; if optional-attachment gains processing (auto-add rules, pricing of add-ons), that processing is rule/bundle territory ([packages](../../../../../modules-plugable/economics/discount/packages/packages.md), [customable](../customable/customable.md)).

## Open questions

- Status of the relation vs a distinct `optional` edge — which is it?
- Map onto the parent/child model in [product.md](../../product.md): optional face of parent/child, or bundle-slot semantics (converge with [packages](../../../../../modules-plugable/economics/discount/packages/packages.md))?
- Relation to `Type_PreSale` / reserve flags in [product.go](../product.go) — unrelated, or one "commitment level" vocabulary?

