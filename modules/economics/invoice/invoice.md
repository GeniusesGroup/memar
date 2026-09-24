# Invoice

Main purpose of invoice use to ChangeOwner of products.

## Definition in Memar

An invoice is a statement of what is claimable between parties: a seller's assertion of what it delivered and at what price. A payslip is not a special concept - it is one or more invoices where the employee is the seller of a service and the organization the buyer. Tax and social insurance are not kernel concepts either: they are pluggable modules that listen to events and produce invoices (VAT instead adds a line to an existing invoice). Transactions settle invoices; invoices are a common cause behind `transaction_reference_is`.

## Discussion

### Drawbacks

- Reading payslips/taxes as "just invoices" loses the ready-made vocabulary users expect; the UI must reassemble those labels.

### Rationale and alternatives

- A dedicated `salary`/`payslip` concept was rejected: the employee is the seller of a service and the organization the buyer; a payslip is a view over invoices between them.
- Tax as a kernel field was rejected: a tax module is a pluggable listener that produces invoices (VAT instead adds a line to an existing invoice), so each jurisdiction ships its own module without touching core.

### Prior art

- Mandatory government charges are modeled neutrally as forced purchases of a government-offered product - invoice/product primitives, no legitimacy judgment inside the model.

### Unresolved questions

- Invoice lifecycle (issued/partially-paid/voided/expired) is documented per state in `status/<state>/` - reconcile with the general status domain.
- Can an invoice exist with zero products (a pure claim)?
- Partial payment: multiple settling transactions against one invoice - is the "partially paid" state invoice-side or analytics-side?

### Future possibilities

- Invoice-transaction settlement tracking as an analytics module.

## Idea backlog

Review discipline per modules/management/vocabulary-discipline.handoff.md. Nothing below is ratified.

**Deferred to a dedicated data-model pass**: real structs (item/summary price chains, bookkeeping storage) are not ideated here; only their idea comments are listed below.

Status vocabulary is NOT restated here - the per-state folders under `status/<state>/` are the single home for each status.

### POS-Bank invoice services
- **Idea**: "send request from POS to Bank to approve the invoice" - approval as an external party handshake over the invoice, not an invoice-kernel action.
- **Review questions**: does bank approval become an invoice status/rule condition (rule domain - Core never knows Rule) or stay inside a pluggable POS-banking capability? Who may set it, and what does it trigger?

### POS-Bank invoice detail
- **Idea**: "send request from POS to Bank to get invoice detail".
- **Review questions**: plain read of an invoice the parties already share (service/GUI, no model change) versus a distinct claim/acknowledgement that would need an edge of its own?

### Invoice analytical query
- **Idea**: query endpoint `/invoice-analytical?ids=123,456,789&type=total_discount&` aggregating invoice facts such as `total_discount`.
- **Review questions**: analytics is always pluggable - does this surface live in a pluggable analytics capability instead of the invoice kernel? Does `total_discount` derive from pricing/discount rules rather than invoice state?
