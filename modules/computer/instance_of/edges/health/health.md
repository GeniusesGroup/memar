# Health (node)

## Model

- `(instance)-[:health]->(side_node)` — `NodeHealthDataModel` composes `Field_InstanceUUID`, `GetSideNodeID() MemoryAddress` (the node on the other side of the ping), `GetPingTime() Duration`, `GetJitterTime() Duration`, and the request/audit pair.
- `BS_Ping_Request` carries `Field_TimeToLive` — the time domain's TTL from [identity/time/edges/ttl](../../../../identity/time/edges/ttl/ttl.md), not a second TTL declared here; `BS_Ping_Response` carries `GetRoundTripTime() Duration`.
- The wire frame (Go residue in `services/ping/`) is a `pingFrame` whose `ID()` is a unix time in the first eight bytes; its `Do()` was empty.

## Policies (rules)

- The domain document's specification: ping runs over the stream timeout mechanism; endpoints use PING to verify a peer is alive or to check reachability, and a non-empty payload must be answered with a PONG frame carrying the same data. Whether ping runs on a schedule or on demand is stated nowhere.

## Placement

- Two distinct nodes — the instance and the side node (`MemoryAddress`) — so an ordinary `edges/` relation of `instance_of`. The TTL is imported from identity/time by path; no foreign type is embedded.

## Source

> Source: `modules/computer/instance_of/edges/health/protocol/data_model.kh`, `modules/computer/instance_of/edges/health/protocol/business-services.kh`, `modules/computer/instance_of/edges/health/services/ping/frame-ping.kh` (in code).
