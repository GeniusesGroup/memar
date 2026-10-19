# Pos status

## Model

- Candidate (unconfirmed): a POS status loop-edge — `CashLimitInactivated` (one status in the source; direction/shape unconfirmed).

## Policies (rules)

- Only the status name recorded — what the status blocks (cash sales? withdrawals?), who sets it, and when it clears, absent from the source (no bare edges).

## Placement

- **Correct here — a domain status belongs to the domain that defines it** (the status domain's rule: "A domain defines the statuses that belong to it as loop-edges under `<domain>/status/<name>/`" — [status](../../../../../modules/knowledge/status/status.md); the POS domain states its record here, [pos.md](../../pos.md) never repeats the list).
- **Not the status module's own list:** the general status domain holds the account of what a status is and the shared loop-edges; `CashLimitInactivated` is register vocabulary (placement by entry point; pluggable owns complete capability — edge + the cash-handling rules that read it).
- **Not a new module:** one status name is not processing semantics (parameters vs semantics; prefer existing homes over inventing new modules).
- Likely tied to the `CashAccount` guard world ([financial-account](../financial-account/financial-account.md)) — a cash-limited register's state; keep the vocabulary converging there (see Open questions).

## Open questions

- What does `CashLimitInactivated` block, and who moves it (rule event? manual toggle? automatic on hitting a cash limit)? — no-bare-edges test open.
- Relationship to the CashAccount guard ("one cash account cannot back two POSes" — candidate backlog prose in [financial-account](../financial-account/financial-account.md)) — same cash-limit concern, two expressions (status vs invariant)?
- Status vs label per [status](../../../../../modules/knowledge/status/status.md): sync service check or async business-rule label?
- Reconcile with the general status domain — own POS status set or shared labels?

