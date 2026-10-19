# Node metric

## Model

- The node's own manifest record (Go residue, no Khayyam form): society, domain name, `AppID` (SHA-512/256 of the domain name, acting as the application id too), email, icon, per-language `AppDetail`, `RequestedPermission` service ids, and the information blocks `TechnicalInfo`, `NetworkInfo`, `DeployInfo`, plus the storage cluster's `DataNodes`. The settled content of each block is in the [domain document](../../instance_of.md) under *Node metrics and deployment*.
- `make-main-file.kh` (Go residue) generates a server's `main.go` from a template that instantiates that manifest and starts the server: networks (TCP 80/443, UDP 53), the storage cluster manifest, and the datastore.

## Policies (rules)

- The Go comments, settled in the domain document: `TechnicalInfo` is what the application *requests*, which may differ from the machine's real condition; zero in a rate limit means no limit (the Pay-As-You-Go strategy); an overflow on a daily counter drops on creation; for net owner types above 1 the Go said "read server codes"; the node-failure timeout is a process convenience, not network-failure handling.

## Placement

- This folder holds no relation at all: it is a deployment manifest plus a main-file generator, content the module skeleton would place under `services/` or `internal/`, not `edges/`. Recorded rather than moved — the Phase 0 wrong-kind-folder pass owns that decision.

## Open questions

- Bucket: no two-node relation exists here (see Placement), so `edges/` is proven wrong by the folder's own contents.
- The manifest's domain-name hash (SHA-512/256) disagrees with `software/edges/manifest`'s SHA-256 of the same input.
- Only Go residue exists; a conversion re-models the manifest from the domain document, not from the struct.

## Source

> Source: `modules/computer/instance_of/edges/node-metric/manifest.kh`, `modules/computer/instance_of/edges/node-metric/make-main-file.kh` (in code).
