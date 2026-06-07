# Rule initiator - service

## Graph
- `(rule)-[:initiator_by_service]->(service)`
- `(service)-[:service_initiator_for]->(rule)`

## Policy (rule)
- The service initiator the process of rule
- Whenever the service called, the rule will be executed.
- e.g. `invoice.ChangeStatus()`, ... called

## Fields
- Like event dispatcher we need to let rule select when called e.g. before, async or after service logic execute.
