# Conditional (generic Rule attachment)

Invoice does not own Rule. This is the same generic `condition_is` attachment Transaction already uses: the rules-engine evaluates; discount, VAT, and restriction keep their own complete enforcement.

## Model

- `(invoice)-[:condition_is]->(rule)`
- `(rule)-[:is_condition_for]->(invoice)`

## Policies (rules)

- Use incompatibility status when a bad rule is requested against the invoice.
- Do not grow invoice-specific enforcement names here; those capabilities live in their pluggable modules.

## Open questions

- Do the rules of a deferred-payment sale — the approver's warning that the product's price moved strongly in recent months, instalments indexed to a chosen price index — attach here, or do instalments live in credit or settlement? No method can be forced; the rules make the problem visible and offer methods — [deferred-payment sales](../../../../../modules-plugable/economics/price-index/price-index.md#deferred-payment-sales).
