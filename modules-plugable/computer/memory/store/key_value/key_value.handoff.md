# Key-Value Handoff
Open work for `modules-plugable/computer/memory/store/key_value/key_value.md`. Entries are mutable current state — revised as each item moves, removed when it resolves or is dropped. See [documentation-handoff.md](../../../../knowledge/documentation/handoff/handoff.md) for what a handoff is.

## Decisions

### The design of the capsule (2026-10-24, Tentative)
Written in [Key-Value](key_value.md) by task `20261024-T160311Z-25344`, with a fresh sub-agent's critique applied; the owner has ruled that the module is its own on `page` and a capsule of the contract, and has not reviewed the design below.
- The structure is a copy-on-write B+tree with two alternating meta pages, because an immutable root is the snapshot, the order and the token the contract asks for, and uniqueness is one point lookup; a log-structured design is a capsule of its own for a write-heavy class.
- The empty key is a key, the lowest; the first draft refused it for a circular reason and the critique removed the reason.
- `Length` and `KeyNumbers` are not offered; `Delete` and `Erase` wait for the erasure rule.
- Uniqueness is a key the consumer names, written with an `absent` expectation in the batch of the pair it protects; its release is a tombstone the consumer writes.

## Open Questions

### What does the memory contract answer for a `changes` token older than the store keeps, and does `changes` return the state it answers up to?
- State: this capsule keeps a log of the keys each commit wrote, trimmed to a declared horizon, so a token beyond it cannot be answered. The owner ruled on 2026-10-25 that the answers of a process are its own and that no common error stands for different subjects, so the answer is one of `changes` alone and not Unavailable (which is transient). The critique also found that `changes` as stated returns no token of the state it reached, so a derived structure cannot tell which state it was brought to, and that a horizon is a limit every adapter with bounded history declares. Both belong to the contract's own protocol, not to a capsule.
- Question for the owner: is the answer named `TooOld` (or another name) an answer of `changes` in the memory contract, with the horizon a declared limit, and does `changes` answer with the token it reached?
- Next: ruling; then the contract's document states them and this capsule points there.
- Asked: 2026-10-24, Claude (task `20261024-T160311Z-25344`), for Omid Hekayati; recorded in [Memory Handoff](../../../../../modules/computer/memory/memory.handoff.md#what-does-the-contract-answer-for-a-changes-token-older-than-the-store-keeps).

### Is a range of keys with values from one state a derived read of the contract?
- State: the Go-era use of a store is a range with values. `list` then `get` may fall on two states, and the read that checks `state` before and after is derivable from the contract's operations, so it adds no semantics, only cost. It names nothing of keys, so by the ruling that a capsule adds no abstraction it belongs to the contract or nowhere. Its answer is unbounded unless it takes a byte limit.
- Question for the owner: does the contract offer such a read (with a byte bound), or is the state-checked `list` and `get` the way?
- Next: ruling; the capsule offers no read of its own meanwhile.

### Does the page store beneath state the three needs of the engine?
- State: the engine needs `Flush` as a barrier, a declared answer to whether one page write can tear, and growth by a write after the last position. `page/protocol/page.kh` declares one page with offset reads and writes, a locker and `NonVolatile`, not a store of positions that grows; the contract's dense instance says nothing of growth. This is the same ground as the open question of which of `block` and `page` is the foundation.
- Next: the build task states the needs as the capsule's check at opening; when the page and block modules are converted, the one that is the foundation declares them.

### Does `record` use this capsule for any ordered structure?
- State: the first draft listed the indexes of `record` as a use. The memory model gives the labels of `record` to `index`, which rests on `changes`, and `index` is not decided to need ordered keys.
- Next: stated, if at all, where `index` is written.

## Anticipated Work
- The build of the capsule, queued as a task with its plan written whole.
- A counted tree, if a consumer needs the key count; a log-structured capsule for a class whose writes outrun path copying; sharing the store between processes.
