# Event

## Model

- `(timeline)-[:event_is]->(quiddity)` (note: LogActivity, ...)
- `(quiddity)-[:event_of]->(timeline)`
- `(timeline)-[:event_is]->(comment)` (note: `user tweet`, `user home timeline`)
- `(timeline)-[:event_is]->(form)`
- `(timeline)-[:event_is]->(question)`
- `(timeline)-[:event_is]->(product)`
- `(timeline)-[:event_is]->(invoice)` (note: `support`, `judge case`, ...)
- `(timeline)-[:event_is]->(object)` (note: income `SMTP` email, ...)
