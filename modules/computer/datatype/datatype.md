# Datatype

Use a datatype node to identify any computer data type.

## Model

- `(software)-[:---]->(software_datatype)`

## Identifier

A datatype's identifier is its node identity in the graph, so `Field_DataTypeID`
returns the same `ThingUUID` every other node identifier in this repository
returns. It is **not** the behaviour a data type is required to have — see
[datatype.handoff.md](./datatype.handoff.md) for how this domain's node relates
to memar's `DataType` abstraction and its `Datatype_UUID`.
