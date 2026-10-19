# Explanation
Definitions of the words used in the law text, written into the payload people will sign.

## Model
- `(law)-[:explanation_is]->(text)`

## Policies (rules)
- Every word used in the human code is defined here before a binding signature is opened.
- A definition that changes who the sentence binds, or what it counts, belongs in the human code. This companion defines the words without moving that coverage.
- Before a binding signature, this field may change. Once a binding signature is open, it stays as signed. A later change is a new law node.
