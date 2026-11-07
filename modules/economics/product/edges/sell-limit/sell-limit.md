# Sell limit

## Model

- Candidate (unconfirmed): `(product)-[:sell_limit_is]->(group)` / `->(role)` / `->(user)` — mirrors the `Type_SellLimit_Group` / `Type_SellLimit_Role` / `Type_SellLimit_User` flags in [product.kh](../product.kh).

## Policies (rules)

- "limit sell to specific groups (roles, ...)" — only members of the listed groups/roles/users may buy the product.
- `Type_SellLimit_Role` is "base on product-role"; the same product-role basis drives `Type_NeedApprove`.

## Placement

- **Core `product` keeps only a structural rule attachment; the semantics belong to the rule domain.** Who-may-buy is organization policy, not product identity — the kernel must not learn it (Core never knows Rule). The precedent already filed in this folder is [customable](../customable/customable.md): `(product)-[:customable_by]->(rule)` with the rules-engine deciding.
- No dedicated module: "which groups may buy" is a *parameter* list, not a processing semantics (parameters-vs-semantics ⇒ one rules module + configuration). The three `Type_SellLimit_*` flags should migrate into rule configuration — the rule domain owns them.
- Not [restriction](../../../../../modules-plugable/economics/restriction/restriction.md): that module is quantity constraints on a target, not sales audience.
