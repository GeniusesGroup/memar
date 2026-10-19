# Address (node)

## Model

- `NodeAddressDataModel` — a node's address record: `Field_InstanceUUID`, `Field_LabelType` (the address-type label; the label space itself is [edges/net-address](../net-address/net-address.md)), `GetAddress() Address` (a named `String`), `GetAddressBinary() AddressBinary` (an `Array_Dynamic`, for the wire), plus the request/audit pair.
- The peer surface is two business services: register a node's addresses, and get a neighbor node's addresses (`GetAddresses() Array_Address`). Both were empty interfaces in the Go.

## Policies (rules)

- The domain document states the split this edge inherits: this record carries the label and the payload; the type vocabulary (domain name, host name, IPv4, IPv6, GP) lives in net-address.

## Placement

- An `edges/` relation of `instance_of`: the near end is the node (`Field_InstanceUUID`), the far end is the address typed by a label. Two distinct nodes if the address is a node of its own; an attribute record otherwise — the bucket question below decides which, and nothing moves until it does.

## Open questions

- Is the address a node of its own — then `(instance)-[:address]->(address)` — or an attribute record on the instance? The source declares a record and two business services; no relation label exists.
- `BS_RegisterNodeAddresses` had empty request and response bodies in the Go; who may register a neighbor's addresses, and what that registration triggers, is stated nowhere.

## Source

> Source: `modules/computer/instance_of/edges/address/protocol/data_model.kh`, `modules/computer/instance_of/edges/address/protocol/bs.kh`, `modules/computer/instance_of/edges/address/protocol/dt-address.kh` (in code).
