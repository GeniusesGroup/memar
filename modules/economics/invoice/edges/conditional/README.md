# Conditional (generic Rule attachment)

Invoice does not own Rule. This is the same generic `condition_is` attachment Transaction already uses: the rules-engine evaluates; discount, VAT, and restriction keep their own complete enforcement.

## Model

- `(invoice)-[:condition_is]->(rule)`
- `(rule)-[:is_condition_for]->(invoice)`

## Policies (rules)

- Use incompatibility status when a bad rule is requested against the invoice.
- Do not grow invoice-specific enforcement names here; those capabilities live in their pluggable modules.
