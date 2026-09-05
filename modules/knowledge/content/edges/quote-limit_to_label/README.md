# Quote limit to label

## Model

- `(comment)-[:quote_limit_to_label]->(user)`
- `(quote_limit_to_label)-[:preference_for]->(quote)`

## Policies (rules)

- e.g. Just a `user` or `group` with indicated `label` can embed this `comment` in other `comment`.
- e.g. just `1st friendship cycle` CAN quote to my comment.
