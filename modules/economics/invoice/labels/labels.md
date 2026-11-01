# Invoice labels
Status-kind words for an invoice are declared once as code in [`invoice_statuses.py`](invoice_statuses.py) (`LABELS`, each taking `Status`). Attachment is only [Label edge](../../../knowledge/label/edges/label/label.md). Kind + rule + event: [Status](../../../knowledge/status/status.md#what-a-status-is).

Per-word prose folders (`paid/`, `paid-partially/`, `voided/`, `expired/`) hold reasons and open questions; they do not declare a second attach Model.

## Open questions (cross-state)
- The e-commerce chain proposal (UserCheckout, PendingReview, Packaging, Shipping, Done) and the legacy numbered list (created, ManagerApprove, WarehouseApprove, ActiveWithApprove, ActiveWithoutApprove, ActiveWithOrderer, Inactive, Normal, Reject, Void) - if ratified, each becomes a `LabelDefinition` in `invoice_statuses.py` (and a prose folder only where needed). Open: is the chain an invoice-core status machine or a pluggable retail specialization (`transaction.handoff.md` §1)?
