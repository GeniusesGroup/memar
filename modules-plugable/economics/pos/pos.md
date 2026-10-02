# POS
The [point of sale (POS)](https://en.wikipedia.org/wiki/Point_of_sale) or point of purchase (POP) is the time and place at which a retail transaction is completed. At the point of sale, the merchant calculates the amount owed by the customer, indicates that amount, may prepare an invoice for the customer (which may be a cash register printout), and indicates the options for the customer to make payment.

Issuer and editor edges on an invoice ([pos-issuer](edges/pos-issuer/README.md), [pos-editor](edges/pos-editor/README.md)) belong here: invoices exist without a register, so POS must own those relations rather than Invoice growing POS branches.

## point of service

The point of sale is often referred to as the point of service because it is not just a point of sale but also a point of return or customer order. POS terminal software may also include features for additional functionality, such as inventory management, CRM, financial, or warehousing.

## Idea backlog (non-edge source)

Raw proposal from a comment note in `card/_import/financial-account-card/service-announce-account-owner.go` (no such file yet) — a non-edge source, left in place (nothing below is ratified).

### Invoice-detail request
- **Idea**: send a request from POS (by user physical card) or mobile app to the Org software to get invoice detail.
- **Review questions**: POS capability or card capability — the source lived under [card](../card/_import/financial-account-card/) `_import`, but the actor is the POS/mobile channel: which module instantiates the request? Physical card vs mobile app = one service with channel parameters, or two paths (parameters vs semantics)?
