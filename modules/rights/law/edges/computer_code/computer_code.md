# Computer code
Machine-checkable realization of the law text, realized by edges to [Rule](../../../../computer/rule/rule.md) nodes. The human-language sentence is [human code](../human_code/human_code.md). The word code alone names neither.

## Model
- `(law)-[:computer_code_is]->(text)`

## Policies (rules)
- A computer-readable form that an independent evaluation can run (IDL or another executable encoding).
- A form that no input can satisfy is not opened for a binding signature. That is the same failure as human code and computer code stating different norms.
- Opening a binding signature includes this field together with the other companions.
- The field is realized by edges to Rule nodes. A Rule added after the signature is a new law, because the Rule set is inside the payload digest.
- Stays as signed once a binding signature is open.
