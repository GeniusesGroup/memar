# Account Handoff

## Topic & Purpose
Load-bearing decisions for the Account domain: quantity-general bookkeeping holder (not money), unit ownership, balance vs availability, and naming. Consolidated from Account & Transaction modeling sessions (2026-08) and the Organization ideas backlog (2026-09-16 migration).

## Status
Active — kernel practiced in README; naming and AvailableBalance trust still open.

## Decisions

### From accounting invariants (formerly `modules/economics/accounting-invariants.md`)

#### 4. Unit belongs to the account, not the transaction
The count unit is declared once per account via the general `(thing)-[:count_unit_is]->(count_unit)` edge. Both accounts of one transaction MUST share the same count unit; the transaction stores only a quantity.

#### 8 (account-side). Availability is not account state
`AvailableBalance`-style values are derived from mutable global constraints (legal blocks, pending reservations) and MUST NOT be stored as account fields; they are evaluated from rules (see `modules-plugable/economics/restriction`). Balance snapshot as a bookkeeping-record fact lives on the [bookkeeping](edges/bookkeeping/README.md) edge.

### From Organization ideas backlog

- **Account ≠ money.** An Account maintains the state of *a quantity*; a Transaction records changes to quantities. The quantity may be currency, kilograms of iron, shares — the bookkeeping structure is the same. The name "Accounting" was deliberately avoided because it carries a money reading; the generalized concept is closer to "bookkeeping of quantities and their changes". *(naming — open)*
- **Unit homogeneity.** A single accounting Transaction is same-unit (bookkeeping needs summable/balanceable changes); unit belongs to the Account — defined once — not repeated per Transaction. Cross-unit operations (1000 EUR ↔ 1000 kg iron) belong to a higher **Trade/Exchange** concept linking two homogeneous Transactions. *(decided)* — exchange ownership: [`matching_system`](../../../modules-plugable/economics/matching_system/README.md).
- **Identity for non-UUID records** (e.g. a check number) draws from the `uri` domain (as with usernames), not a bespoke field on Transaction/Account. *(decided)*
- **Core vs. optional is relative to purpose.** Discount without which the organization still buys and sells; Product/Invoice/Account without which an ERP is unrepresentable — but the attribute is not intrinsic to the module (a charity or a government has "sales" too). *(decided)* — Account is core here by necessity (removing it forces fabrication of another foundational quantity-holder); a future repo-wide placement audit may still re-check edges nested under this module.

## Ambiguities Resolved
- Per-change `(quantity, unit)` on the transaction — resolved: rejected; the unit is a stable account property; repeating it per transaction adds no information and permits unbalanced mixed-unit transactions.
- Per-account `AvailableBalance` as legacy model (~10 years old) — resolved: rejected because a global constraint (one judicial block of 1000) copied per account multiplies it (100 accounts × 1000). See restriction module and wage garnishment / bank levy regulation precedent (e.g. US 31 CFR 212.7).

## Open Questions
1. Final name for the quantity-bookkeeping concept (avoid money-only "Accounting") — *(naming — open)*.
2. **"AvailableBalance" trust question** and precise effect of pending Transactions on the Account before AvailableBalance is treated as fundamental truth — *(open; also on bookkeeping)*.
3. Should the account expose a cached "last index" pointer for O(1) balance reads, or is that purely an engine detail?
4. `Field_AccountID` and the account UUID type carry legacy "financial" framing; rename pending.

## Assumptions
- Holding/possession (bookkeeping balance) ≠ legal title (`rights/ownership`).
- Negative balance is neither allowed nor forbidden by the kernel; pluggable rules govern credit/overdraft.

## Key Definitions Established
- Account: bookkeeping holder of one countable quantity with one count unit — not financial by nature.

## Proposed Next Steps
1. Close naming (open #1) with dictionary + rename guard.
2. Define pending-transaction effect on availability jointly with restriction and bookkeeping (open #2).

## Related Artifacts
- [`README.md`](README.md)
- [`edges/bookkeeping/README.md`](edges/bookkeeping/README.md)
- [`../transaction/transaction.handoff.md`](../transaction/transaction.handoff.md)
- [`../../../modules-plugable/economics/restriction/README.md`](../../../modules-plugable/economics/restriction/README.md)

## Notes
- Provenance: former `accounting-invariants.md` §§4, 8 (account-side) + Organization ideas backlog Account bullets.
