# Forward limit to label

## Model

- `(comment)-[:forward_limit_to_label]->(user)`
- `(forward_limit_to_label)-[:preference_for]->(forward)`

## Policies (rules)

- e.g. Just a `user` or `group` with indicated `label` can embed this `comment` in other `timeline`.
- e.g. just `1st friendship cycle` CAN forward to my comment.
