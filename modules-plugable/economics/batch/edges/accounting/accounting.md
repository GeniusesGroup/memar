# Accounting

## Model

- `(batch)-[:accounting_for]->(product)`
- `(product)-[:accounting_by]->(batch)`

## Policies (rules)

- ProductInventory or good stock
- It can use for product inventory for each batch of products
- Same product can owned by different organization
- So a product CAN own different batch(account) for different owner too not only different warehouse or lot or ...
