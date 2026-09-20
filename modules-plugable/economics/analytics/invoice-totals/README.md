# Invoice totals

Discovered/derived invoice totals (item counts, suggested/discounted/rule/payable prices). Analytics is always pluggable: this record exists to avoid client fetch/recompute and is not acquired claim structure, so it cannot live under core Invoice.

## Model

- `(invoice)-[:invoice_summary]->(---)`
