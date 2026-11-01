# Voting
Binding signatures are open on this law. The payload stays as what was signed.

Declared as a Status-kind label in [`law_statuses.py`](../law_statuses.py). What a status is, and how attachment works, is [Status](../../../../knowledge/status/status.md#what-a-status-is) via [Label edge](../../../../knowledge/label/edges/label/label.md).

## Model
- `(law)-[:label]->(voting)` with `(voting)-[:label]->(Status)` on the definition.

## Policies (rules)
- The companions are present.
- The payload stays as signed.
- Public critique of the proposition can run in this same period. A reaction in that critique is a reading signal. The signature is the vote.
