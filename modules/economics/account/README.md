# Account

An account is the bookkeeping holder of one countable quantity. It is not financial by nature: the quantity may be money, kilograms of steel, shares, bonds, capacity, or points. Wherever a system must keep, increase, decrease, transfer, or settle a quantity, an account is the node that holds its state.

## Model

- An account is a `thing`; its unit comes from the general edge `(thing)-[:count_unit_is]->(count_unit)`, declared once per account.
- The kernel of this domain is exactly one edge: [bookkeeping](edges/bookkeeping/README.md) — the realized effect of a transaction on this account.

## Policies (rules)

- Balance is not stored on the account node; it is the `Balance` snapshot of the account's latest bookkeeping record ([bookkeeping](edges/bookkeeping/README.md) §8; [account.handoff.md](account.handoff.md)).
- Availability (blocked/holdable amounts) is NOT account state. It is evaluated from active rules (see `modules-plugable/economics/restriction`); there is deliberately no `AvailableBalance` field.
- A bookkeeping balance expresses holding/possession, not legal title. Legal ownership is modeled once in `rights/ownership` and may attach to any node, including accounts.
- Negative balance is neither allowed nor forbidden by the kernel; it is governed by pluggable rules (credit, overdraft policies).
- Everything else — settlement references, transfer limits, main/preferred account preferences, credit flags, cash capability — is pluggable and must not enter this module's kernel.

## Discussion

### Drawbacks

- "Current balance" costs a lookup of the account's highest-index bookkeeping record; every read path must know the convention.
- Keeping availability out of account state makes "can this transfer pass?" a rule evaluation, not a field check — slower and harder to explain in tools.

### Rationale and alternatives

- The kernel was reduced to one edge (bookkeeping) by removing everything a pluggable module can express: settlement references, transfer limits, preferences, blocks, credit flags. Each of these was an account field in the legacy model.
- Storing balance on the account node was rejected: it duplicates ledger truth and invites drift; the per-record snapshot ([bookkeeping](edges/bookkeeping/README.md) §8) already answers point-in-time queries.
- Holding vs legal title was separated deliberately: nominee/custody cases prove balance and ownership are different facts.

### Prior art

- The classic ledger "account page" — here the page is the set of bookkeeping edges and the account is just the node they hang from.
- Core banking systems keep status/holds as account fields; this model moves them to rules on purpose.

### Unresolved questions

- Should the account expose a cached "last index" pointer for O(1) balance reads, or is that purely an engine detail?
- `Field_AccountID` and the account UUID type carry legacy "financial" framing; rename pending.

### Future possibilities

- Account grouping (sub-ledgers, multi-account persons) as pluggable relationship modules, not new core types.
