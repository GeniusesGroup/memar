# Connection Handoff

## Topic & Purpose
Open questions about `modules/computer/connection` found while researching the request domain. This file did not exist; it starts with a pointer section only. The domain is still Go residue plus seven edge documents.

## Status
Active — pointer from Request Research 001 recorded; nothing else triaged.

## Open Questions

### From Request Research 001 (2026-10-19): the pipe end of the request chain
Pointer only; the reasoning is in [Request Research 001](../request/request.research.001.md#1-what-the-domain-is-for) and nothing in this domain changed.
- **The request–connection relation has two homes.** [`edges/request`](edges/request/request.md) says `(connection)-[:called]->(request)`; the request domain's `edges/connection` says `(request)-[:called_by]->(connection)`. Proposal: one home, the request domain, because the connection exists before any request and the later fact names the earlier. Retiring `edges/request` is request handoff question 10.
- **Standing and exercised permission.** [`edges/conditional`](edges/conditional/conditional.md) `(connection)-[:authorize_by]->(rule)` is the standing grant; the request's own `authorized_by` is the evidence of use. Two relations, as long as the request edge is renamed `permitted_by` (request handoff question 13).
- **The connection is registered by a request.** [`protocol/data_model.kh`](protocol/data_model.kh) carries `Field_RequestID` and the request time, so the handshake request cannot cite a connection that does not exist yet.
- **Both ends are software instances.** [`edges/connection_to`](edges/connection_to/connection_to.md) is instance to instance; a counter, a telephone line or paper (scenarios 3 and 9 of the research) have no software instances. Whether the domain generalises the channel is request handoff question 11.
- **Stream counters.** [`edges/metrics`](edges/metrics/metrics.md) `SucceedStreamCount` / `FailedStreamCount` are discoverable from request outcome events only if every request is recorded (request handoff question 3); keep them as engine state meanwhile.
- **Page visits are derived.** [`edges/page-visited`](edges/page-visited/page-visited.md) is the walk connection, request, service ("get page"), page; a candidate for `edges-shortcut/`.

## Related Artifacts
- [`connection.md`](connection.md)
- [`../request/request.research.001.md`](../request/request.research.001.md)
- [`../request/request.handoff.md`](../request/request.handoff.md)
