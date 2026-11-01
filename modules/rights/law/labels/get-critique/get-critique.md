# Get-critique
The law is open for public critique, and its companions can still change.

Declared as a Status-kind label in [`get_critique.py`](../get_critique.py). What a status is, and how attachment works, is [Status](../../../../knowledge/status/status.md#what-a-status-is) via [Label edge](../../../../knowledge/label/edges/label/label.md).

## Model
- `(law)-[:label]->(get-critique)` with `(get-critique)-[:label]->(Status)` on the definition.

## Policies (rules)
- People publish reasons and react to those reasons.
- A reaction here is not a signature.
- Companions can still change. A binding signature waits until the payload is the one people will sign.
- A critique may include scenarios that show what the computer code does, stated in human language and generated from that code. Those scenarios are not part of the payload digest. Changing a scenario does not make a new law.
