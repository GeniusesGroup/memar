# Computer code
Machine-checkable realization of the law text, realized by edges to [Rule](../../../../computer/rule/rule.md) nodes.

## Model
- `(law)-[:computer_code_is]->(text)`

## Policies (rules)
- A computer-readable form that an independent evaluation can run (IDL or another executable encoding).
- Opening a binding signature includes this field together with the other companions.
- The field is realized by edges to Rule nodes. A Rule added after the signature is a new law, because the Rule set is inside the payload digest.
- Stays as signed once a binding signature is open.
