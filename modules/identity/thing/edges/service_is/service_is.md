# Service is
This record is offered or invoked as that Service.

## Model
- `(thing)-[:service_is]->(service)`
- `(service)-[:offers]->(thing)`

## Policies (rules)
- The relation is defined once, on thing. [A relation several domains need is defined once](../../../../../docs/modeling.md#a-relation-several-domains-need-is-defined-once). Every domain that retains a node may need to say which Service it is offered or invoked as. Copying the relation into each of those domains would be several edges for one concern.
- The far end is a Service ([Service](../../../../process/service/service.md)), not a separate `software_service` node.
- Thing owns the relation. The domain owns the rule for when its own records may take it. The edge does not say what the thing is as a domain concept; it says which Service defines how it is offered or invoked.
