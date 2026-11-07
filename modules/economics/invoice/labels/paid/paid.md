# Paid
Declared as a Status-kind label in [`paid.py`](../paid.py). Attachment: `(invoice)-[:label]->(paid)` — [Label edge](../../../../knowledge/label/edges/label/label.md).

Final state: the customer has fully paid the invoice amount. A paid invoice can only be viewed - it can neither be deleted nor cancelled (no rollback; corrections are compensating records).
