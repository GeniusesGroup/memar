# Account

An account is the bookkeeping holder of one countable quantity. It is not financial by nature: the quantity may be money, kilograms of steel, shares, bonds, capacity, or points. Wherever a system must keep, increase, decrease, transfer, or settle a quantity, an account is the node that holds its state.

## Model

- An account is a `thing`; its unit comes from the general edge `(thing)-[:count_unit_is]->(count_unit)`, declared once per account.
- The kernel of this domain is exactly one edge: [bookkeeping](edges/bookkeeping/README.md) — the realized effect of a transaction on this account.

## Policies (rules)

- Balance is not stored on the account node; it is the `Balance` snapshot of the account's latest bookkeeping record (invariant #8 in [topic-accounting-invariants.md](../topic-accounting-invariants.md)).
- Availability (blocked/holdable amounts) is NOT account state. It is evaluated from active rules (see `modules-plugable/economics/restriction`); there is deliberately no `AvailableBalance` field.
- A bookkeeping balance expresses holding/possession, not legal title. Legal ownership is modeled once in `rights/ownership` and may attach to any node, including accounts.
- Negative balance is neither allowed nor forbidden by the kernel; it is governed by pluggable rules (credit, overdraft policies).
- Everything else — settlement references, transfer limits, main/preferred account preferences, credit flags, cash capability — is pluggable and must not enter this module's kernel.

## Open questions

- `Field_AccountID` and the account UUID type carry legacy "financial" framing; naming cleanup pending.
