# Detection toxicity

## Model

- `(rule)-[:detection_toxicity]->(---)`

## Policies (rules)

- detection_spam or toxicity_checker
- The word Toxic is registered in [thing labels](../../../thing-labels/thing-labels.md). This edge is a rule that may test for that word. The word is not this edge.
