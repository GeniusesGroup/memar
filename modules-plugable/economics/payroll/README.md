# Payroll

Payroll is the pluggable organization-side view of work: who was a member on a given date, which work invoices exist, totals per period. The economic primitives are NOT owned here — the employee sells a service, the organization buys it; a payslip is one or more invoices between them (see [invoice](../../../modules/economics/invoice/README.md)).

## Model

- [salary](edges-shortcut/salary/README.md) — shortcut labeling a transaction as a salary payment.

## Policies (rules)

- `salary` is currently modeled as a shortcut over `(transaction)-[:account__from]->(account)-[:own_by]->(organization)` + `account__to` → person → `staff_of` → organization. If it stays pure derivation, it carries no processing; if payroll rules attach (period, deductions), it graduates to a real edge.

## Discussion

### Drawbacks

- The name "payroll" suggests a large subsystem (HR/payroll suites); this module is deliberately small, which may confuse adopters.

### Rationale and alternatives

- A full salary domain was rejected: salary, bonus, reimbursement, loan repayment are all invoice/transaction compositions; only membership-over-time and work-invoice analytics need a home.
- An `organizational_accounting` umbrella was rejected: aggregation by theme ("things about organizations") is exactly the anti-pattern the boundary rules forbid.

### Prior art

- ERP payroll modules — replaced here by composition of invoice + staff relations + analytics.

### Unresolved questions

- Is `salary` a shortcut or a real edge? Its endpoint `(___)` is still undecided.
- Payroll-specific analytics: inside this module (payroll meaning) vs category analytics — apply the analytics ownership rule.

### Future possibilities

- Period/cutoff rules as a pluggable rule module over payroll invoices.
