# Computer
computer (application, ...)

## Idea backlog

Review discipline per modules/management/vocabulary-discipline.handoff.md. Nothing below is ratified. Prefer existing homes over inventing new modules.

### Physical-store checkout invoice detail
- **Idea**: register a full invoice detail for a physical-store checkout point — the point-of-sale counter captures the complete invoice detail in one registration.
- **Review questions**: invoice-detail capture is [invoice](../economics/invoice/invoice.md) semantics — is the checkout point only a [device](device/device.md), leaving no computer-service role here? If terminals themselves need identity, does that ride the existing device module rather than a new service?

### Location services
- **Idea**: share location data with others by authorization; immobile (fixed) and simple mobile locations are private-leaning, while public locations should go to the universemodel service carrying more data than a bare location. The live variant adds subscription to a push-data topic for receiving real-time data, and lets an organization publish the live mobile location of its services (taxi, bus, train, ...).
- **Review questions**: does location data belong to identity analytics ([geography-coordinate](../../modules-plugable/identity/analytics/geography-coordinate/protocol/data_model.kh)) with sharing as a rule attachment rather than a computer service? Who owns the push topic — [notification](notification/notification.md) or the capability that publishes the feed? Is the private/public split a difference of parameters (one module + configuration) or of processing semantics?

### Product rejection with remedy
- **Idea**: a user rejecting invoice items must state why (e.g. not the product the org describes in its wiki); if the org approves the rejection, money transfers back to the user, otherwise the user can escalate through the justice service.
- **Review questions**: rejection lifecycle belongs to [invoice](../economics/invoice/invoice.md), the refund to [transaction](../economics/transaction/transaction.md), and approve-or-escalate to a rule reaction (core never knows rule) — what, if anything, stays in computer? Where does "justice service" live as an existing home — [rights](../rights/rights.md)?

### Transaction comment and tags
- **Idea**: set or change a transaction's comment and tags (PUT `apis.sabz.city/financials/v1/{User-UUID}/transaction/{TransactionID}/`).
- **Review questions**: comment and tags are [transaction](../economics/transaction/transaction.md) annotations — core fields, a rule-driven tag vocabulary, or a pluggable tagging capability? Is the REST shape only a www-layer concern above whatever module owns the data?

### Twitter-card HTML
- **Idea**: generate HTML that contains only Twitter-card (or other card-style) dynamic data for crawlers.
- **Review questions**: is card HTML a www rendering concern, or does card metadata belong to a landing/content capability elsewhere?
