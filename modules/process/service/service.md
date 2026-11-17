# Service
## Model
- `(thing)-[:service_is]->(service)` — owned on thing as [service_is](../../identity/thing/edges/service_is/service_is.md); reverse `(service)-[:offers]->(thing)`

## Changelog
- 2026-11-13: Defined [Service Call Name](services/call-name/protocol/call-name.kh) from `Details.Domain` and inherited `Name`, with invalid components and collisions refused. An independent review approved the contract, including its handling of empty components. The Python legacy bridge supplies provisional details and does not implement Khayyam reflection.
- 2026-11-17: An independent review approved the Service Contract clarification that Handler carries invocation errors separately from service-specific Response output (task `20261117-T052819Z-23492`).
