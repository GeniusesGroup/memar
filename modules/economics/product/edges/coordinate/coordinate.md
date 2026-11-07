# Coordinate

## Model

- Not a graph edge — a *lookup recipe*: resolve RoleID → related UserIDs → each user's Coordinate (domain location).
- Coordinate data already has homes: [geography-coordinate](../../../../../modules-plugable/identity/analytics/geography-coordinate/protocol/data_model.kh) (identity analytics) and the provider/user location edge [coordinate-gps](../../../../identity/object/edges/coordinate-gps/protocol/data_model.kh). The `Type_Transport` flag in [product.kh](../product.kh) shows the same concern surfacing as "InvoiceID use to retrieve coordinate domain".

## Policies (rules)

- Source recorded only the recipe; no creation/removal semantics — an edge without who-may-create/what-it-triggers must not exist.

## Placement

- **Not an edge; strip from the product model.** The coordinate lookup is a GUI concern stripped from the model: it is a derived query (role → members → coordinates), owned by whoever serves the view:
  - coordinate values: identity analytics (`geography-coordinate`, pluggable);
  - the role-based resolution: [management/role](../../../../management/role/role.md) membership + GUI layer.
- Root-vs-pluggable verdict: **not in root `product`; not a new capability either** — no module is needed for a recipe over existing data.
