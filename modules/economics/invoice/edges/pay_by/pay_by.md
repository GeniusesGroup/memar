# Pay by

## Model

- `(invoice)-[:pay_by]->(transaction)`
- `(transaction)-[:reference]->(invoice)`
- `(pos)-[:pos_issued]->(invoice)`

## Policies (rules)

- It can any pay type as Direct by buyer, Supporter, Sponsor, ...
