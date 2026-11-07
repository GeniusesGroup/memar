# Reply

## Model

- `(comment)-[:reply_to]->(comment)`
- `(comment)-[:reply_of]->(comment)`

## Policies (rules)

- When a `comment` made a `reply` relation to other comment, It MUST not force to be relate to a shared audience too.
- When a `comment` just a reply to other `comment` and not relate to a shared audience, It is standalone `thread`
