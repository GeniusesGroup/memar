# Reply limit to label

## Model

- `(comment)-[:reply_limit_to_label]->(label)`
- `(reply_limit_to_label)-[:preference_for]->(reply)`

## Policies (rules)

- Just a `user` or `group` with indicated `label` can made a `comment` relation to the `comment` with `reply` edge.
- e.g. just `1st friendship cycle` CAN reply to my comment.
