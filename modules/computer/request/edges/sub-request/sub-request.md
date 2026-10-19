# Sub request

## Model

- `(request)-[:sub_request_of]->(request)`
- `(request)-[:sub_request_is]->(request)`

## Policies (rules)

- e.g. financial transaction request has sub request such as withdraw, deposit, reference, send notification, ...
