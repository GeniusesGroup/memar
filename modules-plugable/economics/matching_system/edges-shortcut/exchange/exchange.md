# Exchange Transaction

## Model

- `(transaction)-[:exchange]->(transaction)`
- `(??Dollar)<-[:currency]-(account)<-[:account__by]-(transaction)-[:deal]->(transaction)-[:account__from]->(account)-[:currency]->(??EURO)`

## Policies (rules)

## Fields
