# Goal
A root-level account of why the law was written, so execution cannot drift from that reason.

## Model
- `(law)-[:goal_is]->(text)`

## Policies (rules)
- This companion is present when a binding signature is opened.
- Goal is the reason the law was written. It travels in the payload so the reason is not lost.
- It does not outrank [human code](../human_code/human_code.md) or [computer code](../computer_code/computer_code.md). If following the goal would produce a result those two refuse, the record is not ready for a signature.
- A goal that only states the reason more generally than the sentence is still a goal.
- This companion stays as signed once a binding signature is open.
