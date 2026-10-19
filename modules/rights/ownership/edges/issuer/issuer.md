# Issuer

## Model

- `(ownership)-[:issuer_is]->(organization)`
- `(organization)-[:issuer_of]->(ownership)`

## Policies (rules)

- e.g. Use to get notify about status of the CryptoKeys e.g. revoked notification, ...
