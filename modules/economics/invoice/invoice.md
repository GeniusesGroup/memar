# Invoice
Main purpose of invoice use to ChangeOwner of products.

## Definition in Memar
An invoice is a statement of what is claimable between parties: a seller's assertion of what it delivered and at what price. A payslip is not a special concept - it is one or more invoices where the employee is the seller of a service and the organization the buyer. Tax and social insurance are not kernel concepts either: they are pluggable modules that listen to events and produce invoices (VAT instead adds a line to an existing invoice). Transactions settle invoices; invoices are a common cause behind `transaction_reference_is`. The status words of an invoice are declared in [labels](labels/labels.md).

## Discussion

### Drawbacks

- Reading payslips/taxes as "just invoices" loses the ready-made vocabulary users expect; the UI must reassemble those labels.

### Rationale and alternatives

- A dedicated `salary`/`payslip` concept was rejected: the employee is the seller of a service and the organization the buyer; a payslip is a view over invoices between them.
- Tax as a kernel field was rejected: a tax module is a pluggable listener that produces invoices (VAT instead adds a line to an existing invoice), so each jurisdiction ships its own module without touching core.

### Prior art

- Mandatory government charges are modeled neutrally as forced purchases of a government-offered product - invoice/product primitives, no legitimacy judgment inside the model.

### Future possibilities

- Invoice-transaction settlement tracking as an analytics module.
