# Invoice Handoff

## Topic & Purpose
Load-bearing commercial decisions that attach to Invoice: adjustment/aggregation field naming, party-role distinctions (customer / buyer / consumer), and core-vs-optional placement relative to organizational purpose. Migrated from the Organization ideas backlog (2026-09-16).

## Status
Active — party-role and core-vs-optional decided; invoice adjustment field naming still open.

## Decisions

### From Organization ideas backlog

- **Invoice should not carry a `discount` field.** Omid's proposal: an aggregation method (`RulePrice() → money_p.Amount`) summing all rules that applied (vouchers + discounts + gift + auctions); counter-argument recorded: naming the field after its cause (`RulePrice`) imports causality into the model and breaks when an adjustment comes from something that is not a rule (cost allocation, carbon tax, currency adjustment) — alternatives `PriceAdjustment` / `AdjustmentAmount` left Pricing to reveal composition. *(naming — open for the org)*
- **Customer ≠ buyer ≠ consumer.** A restaurant order may be placed by one person and consumed by two; the model connects through *User* with distinct identity edges per role. Care applies even in examples — dozens of "financial account" kinds differ only in unit, not in the nature of the account concept. *(decided)*
- **Core vs. optional is relative to purpose.** Discount without which the organization still buys and sells; Product/Invoice/Account without which an ERP is unrepresentable — but the attribute is not intrinsic to the module (a charity or a government has "sales" too). *(decided)*

## Open Questions
- Field naming for the invoice adjustment aggregation (`RulePrice` vs. `PriceAdjustment`) and the quantity-bookkeeping concept's final name. *(from consolidated open-questions backlog #10 — invoice half)*

## Related Artifacts
- [`README.md`](README.md)
- [`../product/product.handoff.md`](../product/product.handoff.md)
- [`../../../modules-plugable/economics/pricing/edges/pricing/README.md`](../../../modules-plugable/economics/pricing/edges/pricing/README.md)
- Invoice party edges: [`edges/user-customer`](edges/user-customer/README.md), [`edges/user-buyer`](edges/user-buyer/README.md), [`edges/user-consumer`](edges/user-consumer/README.md)

## Notes
- Provenance: Organization ideas backlog → Commercial / organizational concepts (2026-09-16 migration).
- **Enterprise-software foundations are stable.** The bases of organizational systems have not changed in ~200 years when modeled correctly; the churn ("requirements") is evidence of a bad model, not of a changing business — DDD attempted this correction but propagated wrong readings (its examples blurred the concepts). *(Omid's working thesis)*
