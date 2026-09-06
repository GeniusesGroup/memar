# Economics

Economics is the category for bookkeeping of any countable quantity: money, kilograms of steel, shares, bonds, capacity, points. Money is just one `count_unit`, not the center of this category. Wherever something must be kept, increased, decreased, transferred, or settled as a quantity, it belongs here.

## Core domains

A domain is core only by necessity: removing it would force the kernel to fabricate or distort another foundational concept (see [topic-core-vs-pluggable.md](topic-core-vs-pluggable.md)). Importance or prevalence is not the test.

- [account](account/README.md) — holds the bookkeeping state of one quantity with one count unit.
- [transaction](transaction/README.md) — a request by one or more users for a bookkeeping change; not an operation.
- [invoice](invoice/README.md) — a statement of what is claimable between parties; a common cause/reference of transactions.
- [product](product/README.md) — anything that can be priced; the subject an invoice bills and a transaction settles.

The load-bearing rules of these domains are collected in [topic-accounting-invariants.md](topic-accounting-invariants.md).

## Everything else is pluggable

`modules-plugable/economics/` holds capabilities that add semantics on top of the core: settlement, restriction, matching_system, account_relationship, cash, card, payroll, tax, vat, insurance-social, credit, securities, analytics, and more. Core domains must not know about them; connections happen through generic edges (e.g. `condition_is` to a rule node).

## Namespace note

`economics` is a browsing namespace for a repository with 500+ modules, not an ontological claim that e.g. Account "is a kind of economics". A module's placement indicates its primary integration point, not its identity owner.
