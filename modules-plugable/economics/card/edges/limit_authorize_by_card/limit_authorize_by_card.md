# Limit authorize by card

## Model

- `(account)-[:limit_authorize_by_card_to]->(card)`
- `(card)-[:limit_authorize_for]->(account)`

## Policies (rules)

- User MUST also SET MIN & MAX transfer amount.
