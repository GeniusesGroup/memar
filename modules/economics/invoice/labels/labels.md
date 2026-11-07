# Invoice labels
Status-kind words for an invoice are declared once as code, **one file per word** under this folder (`paid.py`, `voided.py`, …; each `LABELS` takes `Status`). Attachment is only [Label edge](../../../knowledge/label/edges/label/label.md). Kind + rule + event: [Status](../../../../modules-plugable/knowledge/label/status/status.md).

Per-word prose folders (`paid/`, `paid-partially/`, `voided/`, `expired/`) hold reasons; they do not declare a second attach Model.
