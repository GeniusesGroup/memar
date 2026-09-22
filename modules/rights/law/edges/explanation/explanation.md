# Explanation
Definitions of the words used in the law text, written into the payload people will sign.

## Model
- `(law)-[:explanation_is]->(text)`

## Policies (rules)
- Every word used in the law text is defined here before a binding signature is opened.
- This field holds what statute books put in articles, notes, and rider-clauses.
- Coverage is stated in the law text or here.
- Before a binding signature, this field may change. Once a binding signature is open, it stays as signed. A later change is a new law node.
