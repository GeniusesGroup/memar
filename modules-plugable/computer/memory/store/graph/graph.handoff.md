# Graph Handoff

## Open

- **Per-edge key bytes.** Exact key layout under key-value for `(vertex, relation, …)` prefix listing — wait on key_value being usable; record only that listable prefix is required ([graph.md → Per-edge keys](./graph.md#per-edge-keys)). Volatile-backed v1 uses tag + length-prefixed `(vertex, relation)` + slot; key_value may restate the same prefix rule.
- **Compact↔per-edge migration.** Mechanism and who triggers it (consumer policy vs automatic degree threshold) — anticipated; not blocking the service surface.
- **Abstract ADT vs storage capsule docs.** Cross-links from `modules/computer/adt/graph/` into this module’s services — documentation pass.
- **Hard erase of an edge address.** Deferred with memory erasure (contract has no remove). Industry DELETE maps to `end_edge` or to replacing a compact adjacency value; not a separate `remove_edge` until erasure is ruled.

## Closed (this round)

- **Capsule vs pure layout (2026-11-01).** Decided Tentative: a capsule of **layouts + services** is justified; it adds no memory-contract operations or guarantees. Owner: task `20261101-T123647Z-15992`.
- **One layout for all domains.** Refused: domains do not each invent adjacency; they choose among layouts this module offers.
- **v1 adjacency service set (2026-11-01).** `put_edge` / `put_edges` / `list_sides` / `count_sides` / `get_side` / `set_side_fields` / `end_edge` + `side_ref`. Self-review + external API research; owner treated as approved.
- **MATCH ownership (2026-11-01).** Correction: MATCH/path are **in** this module (complete graph layer). Prior “query language elsewhere / non-goal” was wrong.
- **Structured match for agents (2026-11-01).** v1 ships structured `match` / `path` / `exists` / `expand` (not opaque Cypher strings). Inherited languages critiqued in `graph.md`. Text dialect that compiles into structured patterns is anticipated-work, not a blocker for implement `20261101-T130906Z-26736`.
- **Layout bound at lay-time.** Mixing layouts on one `(vertex, relation)` refused.
- **`side_ref` encoding (2026-11-01).** Compact: adjacency address + 8-byte slot (total-ordered). Per-edge: the edge address. Reverse `side_ref` stored in the side value so `set_side_fields` / `end_edge` update both directions in one batch. Task `20261101-T130906Z-26736`.
