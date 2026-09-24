# Sell limit

## Model

- Candidate (unconfirmed): `(product)-[:sell_limit_is]->(group)` / `->(role)` / `->(user)` — mirrors the `Type_SellLimit_Group` / `Type_SellLimit_Role` / `Type_SellLimit_User` flags in [product.go](../product.go).

## Policies (rules)

- "limit sell to specific groups (roles, ...)" — only members of the listed groups/roles/users may buy the product.
- `Type_SellLimit_Role` is "base on product-role"; the same product-role basis drives `Type_NeedApprove`.

## Placement

- **Core `product` keeps only a structural rule attachment; the semantics belong to the rule domain.** Who-may-buy is organization policy, not product identity — the kernel must not learn it (Core never knows Rule, decided in [rule.handoff.md](../../../../computer/rule/rule.handoff.md)). The precedent already filed in this folder is [customable](../customable/customable.md): `(product)-[:customable_by]->(rule)` with the rules-engine deciding.
- No dedicated module: "which groups may buy" is a *parameter* list, not a processing semantics (parameters-vs-semantics ⇒ one rules module + configuration). The three `Type_SellLimit_*` flags should migrate into rule configuration — this answers the standing review question in [product.md](../../product.md) ("Do SellLimit flags belong here or to the rule domain?") toward **rule domain**.
- Not [restriction](../../../../../modules-plugable/economics/restriction/restriction.md): that module is quantity constraints on a target, not sales audience.

## Open questions

- Separate edge, or converge into the existing `customable` / generic `condition_is` attachment (one structural edge, many rules)?
- Product-role basis is shared with `Type_NeedApprove` — is `product-role` itself a missing edge (see [product.md](../../product.md) backlog)?
- Direction and naming (`sell_limit_is` vs flag-space) unconfirmed — nothing ratified.

