# Computer
computer (application, ...)

## Idea backlog
Review discipline per modules/management/vocabulary-discipline.handoff.md. Nothing below is ratified. Prefer existing homes over inventing new modules.

### Physical-store checkout invoice detail
- **Idea**: register a full invoice detail for a physical-store checkout point — the point-of-sale counter captures the complete invoice detail in one registration.

### Location services
- **Idea**: share location data with others by authorization; immobile (fixed) and simple mobile locations are private-leaning, while public locations should go to the universemodel service carrying more data than a bare location. The live variant adds subscription to a push-data topic for receiving real-time data, and lets an organization publish the live mobile location of its services (taxi, bus, train, ...).

### Product rejection with remedy
- **Idea**: a user rejecting invoice items must state why (e.g. not the product the org describes in its wiki); if the org approves the rejection, money transfers back to the user, otherwise the user can escalate through the justice service.

### Transaction comment and tags
- **Idea**: set or change a transaction's comment and tags (PUT `apis.sabz.city/financials/v1/{User-UUID}/transaction/{TransactionID}/`).

### Twitter-card HTML
- **Idea**: generate HTML that contains only Twitter-card (or other card-style) dynamic data for crawlers.
