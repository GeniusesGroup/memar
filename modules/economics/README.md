# Economics

Economics is a **browsing namespace** for bookkeeping of any countable quantity: money, kilograms of steel, shares, bonds, capacity, points. Money is just one `count_unit`, not the center of this category. Wherever something must be kept, increased, decreased, transferred, or settled as a quantity, it belongs here.

`economics` is not an ontological claim that e.g. Account "is a kind of economics". A module's placement indicates its primary integration point, not its identity owner. Load-bearing rules live **inside** each owning domain — not in category-level doctrine files.

## Core domains (index)

A domain is core only if removing it would force the kernel to fabricate or distort another foundational concept (core-by-necessity). Importance or prevalence is not the test. Current economics cores (subject to a future repo-wide placement audit; that session's working brief is ephemeral and must not live under `modules/`):

- [account](account/README.md) — holds the bookkeeping state of one quantity with one count unit. Decisions: [account.handoff.md](account/account.handoff.md).
- [transaction](transaction/README.md) — a request by one or more users for a bookkeeping change; not an operation. Decisions: [transaction.handoff.md](transaction/transaction.handoff.md).
- [invoice](invoice/README.md) — a statement of what is claimable between parties; a common cause/reference of transactions. Decisions: [invoice.handoff.md](invoice/invoice.handoff.md).
- [product](product/README.md) — anything that can be priced; the subject an invoice bills and a transaction settles. Decisions: [product.handoff.md](product/product.handoff.md).

Kernel edge: [bookkeeping](account/edges/bookkeeping/README.md). Cross-domain UUID references follow that edge's rule. Cross-unit exchange: [matching_system](../../modules-plugable/economics/matching_system/README.md). Availability/restrictions: [restriction](../../modules-plugable/economics/restriction/README.md). Fees/rules: [rule](../computer/rule/README.md).

## Everything else is pluggable

`modules-plugable/economics/` holds capabilities that add semantics on top of the core: settlement, restriction, matching_system, account_relationship, cash, card, payroll, tax, vat, insurance-social, credit, securities, analytics, and more. Core domains must not know about them; connections happen through generic edges (e.g. `condition_is` to a rule node). Analytics is always pluggable (discovered/derived data — never core).

## Agreed next steps

Order settled in the modeling sessions (2026-08/09); each step's findings land in the module docs:

1. Finalize the [bookkeeping](account/edges/bookkeeping/README.md) edge: fields, sign convention, cardinality, ordering/concurrency, reversal/finality, TransactionIndex as contract-or-detail.
2. Cross-check rule-engine mechanics (triggers, authority/priority, idempotency, races, dependent transactions) — see [rule README](../computer/rule/README.md) and [rule.handoff.md](../computer/rule/rule.handoff.md).
3. Design [restriction](../../modules-plugable/economics/restriction/README.md) on top of the settled rule mechanics.
4. Keep [settlement](../../modules-plugable/economics/settlement/README.md) separated from clearing and matching; test against bank, warehouse, and securities scenarios.
5. Re-review [invoice](invoice/README.md)/[product](product/README.md)/[money](../../modules-plugable/economics/money/README.md) against tax, rent, penalties, and rounding contracts.
6. Then securities/custody, credit, payroll, analytics.
7. Repo-wide placement audit (move early-development edges that fail core-by-necessity into `modules-plugable/`) — run as a dedicated session from the ephemeral working brief (gitignored); do not reintroduce a category-level doctrine file under `modules/`.
