# IBAN

## Model

- `(account)-[:iban_is]->(uri(text))`
- `(uri(text))-[:iban_for]->(account)`
