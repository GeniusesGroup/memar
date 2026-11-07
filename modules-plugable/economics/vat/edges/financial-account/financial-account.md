# Tax relation financial account

## Model

- Candidate (unconfirmed): `(tax)-[:relation_financial_account]->(account)` carrying the label `TaxDepositAccount` (direction unconfirmed) — the account where tax amounts settle.

## Policies (rules)

- Only `TaxDepositAccount` recorded — deposit semantics (which leg of the tax posting lands there, when), absent from the source (no bare edges).

## Placement

- **Correct here — the tax-account link is instantiated from the tax capability** (placement by entry point; pluggable owns complete capability — edge + tax posting rules that read it live together).
- **Not core `account`:** the account kernel holds ledgers without knowing taxes (core-by-necessity fails; an org without this module deposits tax to a plain account); the tax side names *which* account serves the role — reference-not-embed.
- **Parallel to POS's account roles:** the POS module owns its own account-role labels ([financial-account](../../../pos/edges/financial-account/financial-account.md) — CashAccount/DepositAccount/RefundAccount) — same shape (capability names its accounts), two vocabularies; converge only if a shared account-role vocabulary emerges (prefer existing homes).
- **Not a new module:** one labeled relation is parameters, not independent processing (parameters vs semantics).
