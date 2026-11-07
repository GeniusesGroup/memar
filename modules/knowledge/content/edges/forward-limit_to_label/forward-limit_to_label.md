# Forward limit to label

## Model

- `(comment)-[:forward_limit_to_label]->(user)`
- `(forward_limit_to_label)-[:preference_for]->(forward)`

## Policies (rules)

- e.g. Just a `user` or a set of users with indicated `label` can embed this `comment` elsewhere.
- e.g. just `1st friendship cycle` CAN forward to my comment.
