# Resource (node)

## Model

- `NodeResourceDataModel`: `Field_InstanceUUID`, `Field_LabelType`, `GetResourceTypes() Array_ResourceType` (`ResourceType` over a `U8`), `GetResourceAmounts() Array_ResourceAmount`, and the request/audit pair.
- Per the domain document: amounts are written as strings, and the desired/actual duality is the label space in [edges/node-resource](../node-resource/node-resource.md), not a value here.

## Policies (rules)

- The source states none: the two parallel lists have no pairing rule, no unit, and no writer.

## Placement

- An `edges/` relation of `instance_of` with the node-resource label space as its classification; two distinct nodes only if the resource is one — which nothing states.

## Open questions

- Two parallel arrays with no contract that `types[i]` and `amounts[i]` describe the same entry, and amounts as strings rather than the settled `Decimal_Quantity` — the same primitive question `inventory.handoff.md` records for its `Stock()` and `Amount()`.
- The Go declared `Type() label_p.UUID` beside `ResourceType() []ResourceType`: a label-type surface and a resource-type list under one word, which rule 3 (full domain-qualified names) will not keep.

## Source

> Source: `modules/computer/instance_of/edges/resource/protocol/data_model.kh`, `modules/computer/instance_of/edges/resource/protocol/dt-resource_type.kh` (in code).
