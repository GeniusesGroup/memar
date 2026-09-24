# Answer result

## Model

- Candidate (unconfirmed): answer result labels — Correct (Passed) / Wrong (Failed).
- Candidate (unconfirmed): a list-service sketch `LIST_RespondentIDs_BY_AnswerID` with `AnswerBy` returning the answering user.

## Policies (rules)

- Labels recorded: Correct (Passed), Wrong (Failed).
- A list sketch names `LIST_RespondentIDs_BY_AnswerID` and `AnswerBy` as the answering user. No who-may-set or trigger rule is recorded.

## Placement

- Stays with the answer module: these are result labels of an answer, a value list rather than a separate capability.
- Whether Correct/Wrong is a scored result or a binary label is open below; that choice does not move the vocabulary.

## Open questions

- is Correct/Wrong a scored result (criterion points) or a binary label?

