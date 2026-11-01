# Type is
This record is stored under that Type.

## Model
- `(thing)-[:type_is]->(type)`
- `(type)-[:classifies]->(thing)`

## Policies (rules)
- The relation is defined once, on thing. [A relation several domains need is defined once](../../../../../docs/modeling.md#a-relation-several-domains-need-is-defined-once). Every domain that retains a node may need to say under which Type that node was written. Copying the relation into each of those domains would be several edges for one concern.
- The far end is a Type ([Type](../../../../computer/type/type.md)), not a separate datatype node.
- Thing owns the relation. The domain owns the rule for when its own records may take it. The edge does not say what the thing is as a domain concept; it says which Type defines how it is stored.
