# Invoice

Main purpose of invoice use to ChangeOwner of products.

## Definition in Memar

An invoice is a statement of what is claimable between parties: a seller's assertion of what it delivered and at what price. A payslip is not a special concept — it is one or more invoices where the employee is the seller of a service and the organization the buyer. Tax and social insurance are not kernel concepts either: they are pluggable modules that listen to events and produce invoices (VAT instead adds a line to an existing invoice). Transactions settle invoices; invoices are a common cause behind `transaction_reference_is`.

## Open questions

- Invoice lifecycle (issued/partially-paid/voided/expired) currently lives as edge labels here; check against the general status domain.
