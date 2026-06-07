# Execution - limit to label

## Graph
- `(rule)-[:execution__limit_to_label]->(label)`

## Policy (rule)
- Rule limit to the execute on nodes with related label.
- e.g. limit to nodes with `server` label that mean rule MUST not run on client hardwares.
- e.g. limit to nodes with `edge_server` label that mean rule MUST run on edge servers not cloud one.
