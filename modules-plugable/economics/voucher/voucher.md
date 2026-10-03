# Voucher

## Model

- `(rule)-[:voucher]->(---)`
- The edge's endpoint is a subject the voucher applies to, and the conditions on it are the rule's facets: estate, groups, user, user type, products, labels, invoice (its id, its conditions, its type, its usage cap), POS, duration, value.
- A place condition is an estate, and an estate here is a region rather than a specific point: a rule may depend on where a service was consumed — the source or the destination of a taxi journey, carried as a service product on an invoice. Discount states the same condition the same way; the two are one concept and this module's Go carried the sentence verbatim.
- `value` is where the bond is stated: what the voucher is worth (`Field_Worth`), what fraction of a price it may take (`Field_Proportion`), and in which currency — the currency is the count unit the worth is measured in, not a field of the worth itself.

## Policies (rules)

- Voucher is a bond of the redeemable transaction type which is worth a certain monetary value and
- which may be spent only for specific reasons or on specific products
