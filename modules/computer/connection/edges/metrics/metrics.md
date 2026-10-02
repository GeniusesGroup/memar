# Metrics

## Model

- `(connection)-[:metrics]->(time)`
- Edge/property payload (protocol [`ConnectionMetrics`](protocol/data_model.kh)): `MaxBandwidth`, `BytesSent`/`PacketsSent`, `BytesReceived`/`PacketsReceived`, `FailedPacketsReceived`/`NotRequestedPacketsReceived` (firewall counters against attack types), `SucceedStreamCount`/`FailedStreamCount`.

## Policies (rules)

- Commit note in protocol: "Delete `timing` in favor of calendar-event" — the timing field is out of the data model.
- Callback hooks on the connection: `StreamSucceed`, `StreamFailed`, `PacketReceived(packetLength)`, `PacketSent(packetLength)` — implemented in [connection-metric.kh](internal/connection-metric.kh).

## Placement

- **Core `connection` keeps the raw counters as engine state; firewall/attack semantics read from them would be a pluggable.** Byte/packet counters are state of the pipes themselves — core-by-necessity detail of the connection; reading them as attack detection or firewall policy is processing that installs and removes as a whole (pluggable security/firewall capability attaching to connection), and any aggregation over the counters is always pluggable analytics. Entry point: connection — never split counter storage from the connection while it is engine detail.

## Open questions

- Is timing really replaced by calendar-event?
- Are failed-packet counters firewall policy or engine detail?

## Source

> Source: `modules/computer/connection/edges/metrics/` (in code).
