# Pos relation financial account

## Model

- Candidate (unconfirmed): `(pos)-[:relation_financial_account]->(account)` carrying account-role labels `CashAccount` / `DepositAccount` / `RefundAccount` (direction unconfirmed).

## Policies (rules)

- Backlog-recorded guard prose (candidate — appears in the domain backlog since `334d6e2c` 2026-09-09, not found in any tracked `.go` source): CashAccount requires the target account to carry the `cash_account` label; one cash account cannot back two POSes — the exclusivity rule is an invariant candidate.
- Source itself records only the three role labels (no bare-edge semantics beyond them).

## Placement

- **Correct here — the POS-account roles are instantiated from the POS capability**.
- **Not core `account`:** the account kernel holds ledgers without knowing registers (core-by-necessity fails; reference-not-embed — POS names accounts by identity); an org without POS deposits/refunds through plain accounts.
- **Not a new module:** three role labels are parameters of the register capability (parameters vs semantics; prefer existing homes over inventing new modules).
- **Guard is rule material:** "one cash account cannot back two POSes" — an invariant to record as rule/processing before ratifying the edge (no bare edges; core never knows Rule). If enforced, edge + guard processing stay together (pluggable owns complete capability).
- Sibling vocabulary: [financial-account](../../../vat/edges/financial-account/financial-account.md) (`TaxDepositAccount`) — same shape (capability names its accounts), two vocabularies; converge only if a shared account-role set emerges.
