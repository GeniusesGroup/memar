# Paid
Declared as a Status-kind label in [`invoice_statuses.py`](../invoice_statuses.py). Attachment: `(invoice)-[:label]->(paid)` — [Label edge](../../../../knowledge/label/edges/label/label.md).

Final state: the customer has fully paid the invoice amount. A paid invoice can only be viewed - it can neither be deleted nor cancelled (`transaction.handoff.md` §6: no rollback; corrections are compensating records).

**Review question**: is "paid" one state or a pair (fully-paid vs partial) with a quantity field? See [paid-partially](../paid-partially/README.md).
