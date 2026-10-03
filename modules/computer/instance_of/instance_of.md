# Node
Node is running version of applications. Any application CAN have many running instance.

## Model

- `(software)-[:instance_of]->(software)`

## Policies (rules)

- A Software Instance (SI) node represents an instance of an off-the-shelf software product or equivalent proprietary item of software.

## Identity

`Field_InstanceUUID` is the running instance's own identity and resolves to `ThingUUID`, like every
other domain identity in this repository. The Go source already said so: `type UUID thing_p.UUID`,
"UUID as InstanceID or software(application) node instance".

## Address

A node's address is `Address`, a named `String`, and the record also carries the address in binary
form for the wire. The address *type* (domain name, host name, IPv4, IPv6, GP) is the separate
label space in [edges/net-address](edges/net-address/net-address.md); this edge carries the label
as `Field_LabelType` and the payload.

## Health

Health is a ping over the stream timeout mechanism. The ping request carries a time to live, and
that is the time domain's `Field_TimeToLive` from
[identity/time/edges/ttl](../../identity/time/edges/ttl/ttl.md), not a second TTL declared here.
The ping response carries the round trip time (`Observer_RoundTripTime`).

The health record itself is `NodeHealthDataModel`: the instance, the node on the other side of the
ping (`Observer_Health_SideNodeID`), the ping time, the jitter time, and the audit pair.

## Resource

`ResourceType` names what a resource is; the record carries a list of them and a parallel list of
amounts written as strings. The desired/actual duality is the label space in
[edges/node-resource](edges/node-resource/node-resource.md), not a value here.

## Audit log

`AuditLogDataModel` is memar's `ProcessLog_Event` and nothing more for now; the Go source carried
its own `TODO::: other condition`.

The audit-log configuration's policy, which the Go stated as a comment on a constant: **if any
mode is disabled the logger must not save that log type on the desired node, but it must still
dispatch it to any client that requested any types, even when the type is not enabled.**

## Peer services

Two peer services are specified here rather than implemented:

- **Ping peer**: endpoints use PING to verify that their peers are still alive, or to check
  reachability to a peer. If the payload is not empty, the recipient must generate a PONG frame
  containing the same data.
- **Sync time**: used to sync time between peers (Network Time Protocol). The Go body carried the
  same PONG comment as ping peer, which is almost certainly a copy.

## Node metrics and deployment

`edges/node-metric/` holds the node's own manifest, from which a server's main file is generated.
The settled content, from the Go source:

- The manifest's `AppID` is a SHA-512/256 hash of the domain name, and so acts as the
  application id too.
- `TechnicalInfo` is what the application *requests*, which may differ from the machine's real
  condition: shutdown delay (the server waits at least this long for active streams to finish),
  and the minimum hardware specification for each instance: CPU cores, CPU speed (Hz), RAM (bytes),
  GPU (Hz), network (bytes per second), storage (bytes, where the disk kind is indicated by the
  data-centers class).
- `NetworkInfo` is the rate limit policy, split by net owner type: application-wide
  (`MaxOpenConnection`, `ConnectionIdleTimeout`), guest (owner type 0), and registered (owner type
  1). Each bounds connections, connections per address, concurrent streams, stream connections
  per day, service calls per day, and bytes and packets sent and received per day. Zero means no
  limit, which is the Pay-As-You-Go strategy; an overflow on a daily counter drops on creation.
  **If the owner type is above 1, you must read the server code**; the Go said so in as many words.
- `DeployInfo` is where an instance may run outside the society it belongs to, the data-centers
  class (0 first class, 256 low quality, default 5), the maximum node number, and how long a node
  may be failed before it is replaced. The replacement timeout is a process convenience, not
  network-failure handling.
- `DataNodes` is the storage cluster's own manifest: data-centers class, total replication zones
  (default 3), node failure timeout in minutes (default 60), and the cache percentage at which
  records are garbage collected.

## Idea backlog

Review discipline per modules/management/vocabulary-discipline.handoff.md. Nothing below is ratified.

### Health and audit-log (data models with idea semantics)
- **Idea**: ping via stream timeout with TTL/RTT (health); audit-log config where disabled modes still must Dispatch to subscribed clients even when not saved locally.
- **Review questions**: audit-log dispatch semantics vs storage policy - rule or code?
