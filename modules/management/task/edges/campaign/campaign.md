# Campaign

## Model

- `(task)-[:product]->(campaign)` (note: select or limit products for a campaign)
- `(task)-[:label]->(campaign)` (note: select or limit categories for a campaign)
- `(task)-[:group]->(campaign)` (note: To send SMS or ... to all user joined group. Join can be optional. DeJoin mechanism must be exist.)
