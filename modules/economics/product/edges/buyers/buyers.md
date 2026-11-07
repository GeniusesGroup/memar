# Buyers

## Model

- Candidate (unconfirmed): `(product)-[:buyers]->(group)` — the group related to the product as its buyers audience (source was a product-to-group label file).

## Policies (rules)

- Bare label "Buyers" among Comment / QA / Buyers — no rules recorded in the source.

## Placement

- **Not core `product`.** Who bought a product is *derived* from invoice items; product stays priceable without any buyers edge (core-by-necessity fails).
- **Proposed: derive, do not store.** The buyer fact already lives on `(invoice)-[:buyer]->(user)` ([user-buyer](../../../invoice/edges/user-buyer/user-buyer.md)); a product-level "buyers" group is either (a) an analytics/derived output (analytics is always pluggable) or (b) a shortcut owned and maintained by invoice/transaction — never a product-kernel edge (shortcut edges stay with the capability that gives them meaning).
