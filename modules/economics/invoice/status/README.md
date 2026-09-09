# Invoice Status

Statuses live in their own folder per state (`paid/`, `paid-partially/`, `voided/`, `expired/`) - one folder and one README per state; this file only holds cross-state questions.

## Open questions (cross-state)

- The e-commerce chain proposal (UserCheckout, PendingReview, Packaging, Shipping, Done) and the legacy numbered list (created, ManagerApprove, WarehouseApprove, ActiveWithApprove, ActiveWithoutApprove, ActiveWithOrderer, Inactive, Normal, Reject, Void) - if ratified, each becomes its own folder here. Open: is the chain an invoice-core status machine or a pluggable retail specialization (accounting-invariants #1)?
- Reconcile with the general status domain (knowledge/status).