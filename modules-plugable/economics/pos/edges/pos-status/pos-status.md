# Pos status

## Model

- Candidate (unconfirmed): a POS Status-kind [label](../../../../../modules/knowledge/label/label.md) — `CashLimitInactivated` (one word in the source; whether it takes `Status` unconfirmed).

## Policies (rules)

- Only the status word recorded — what it blocks (cash sales? withdrawals?), who attaches or withdraws it, and when it clears, absent from the source (no bare edges).

## Placement

- **Correct here — a domain Status-kind word belongs with the domain that owns the claim** ([Documentation → Status](../../../../../modules-plugable/knowledge/documentation/documentation.md#status): general words under `thing/labels/`, domain-specific ones under that domain's `labels/` as `Label_<Word>` taking `Label_Status`; the POS domain states its candidate here, [pos.md](../../pos.md) never repeats the list).
- **Not a general Status-kind word on thing:** `CashLimitInactivated` is register vocabulary (placement by entry point; pluggable owns complete capability — the label + the cash-handling rules that read it).
- **Not a new module:** one status word is not processing semantics (parameters vs semantics; prefer existing homes over inventing new modules).
- Likely tied to the `CashAccount` guard world ([financial-account](../financial-account/financial-account.md)) — a cash-limited register's state; keep the vocabulary converging there (see Open questions).

## Open questions

- What does `CashLimitInactivated` block, and who moves it (rule event? manual toggle? automatic on hitting a cash limit)? — no-bare-edges test open.
- Relationship to the CashAccount guard ("one cash account cannot back two POSes" — candidate backlog prose in [financial-account](../financial-account/financial-account.md)) — same cash-limit concern, two expressions (Status-kind label vs invariant)?
- Is `CashLimitInactivated` Status-kind (takes `Label_Status`) or another label kind ([Documentation → Status](../../../../../modules-plugable/knowledge/documentation/documentation.md#status))?
- Own POS Status-kind set under POS `labels/`, or a shared word under `thing/labels/`?

