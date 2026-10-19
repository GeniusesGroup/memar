# Human code
The human-language sentence of a law: the normative text a person reads.

## Model
- `(law)-[:human_code_is]->(text)`

## Policies (rules)
- This is the human-language sentence. [Computer code](../computer_code/computer_code.md) is the machine-checkable form of the same norm. The word code alone is not an edge: it does not say which of the two it is.
- Human-readable law text in a human language (English, Persian, …).
- This field is the normative sentence. Labels, goal, explanation, and executive guarantee are the other companions.
- Before a binding signature, this text may change. Once a binding signature is open, this text stays as signed. Later precision is a new law node.
