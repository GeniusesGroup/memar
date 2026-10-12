# Concurrency Realization Changelog

## Changelog

### Initial draft — substrate, channel contract, pooling default
- Time: 2026-09-06T00:00:00Z
- Type: Added
- Contributors:
  - [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) — claimed, argued
  - [Super Z](../../../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — reviewed, rewrote

#### What changed
- The initial draft established three realization rules — user-space-thread substrate, channels-as-signals (never channel-as-store), pooled execution units — plus the substrate-hostile-operation obligation for framework libraries.
- Concept-level treatment was split from realization-level rules: the concept level was kept in process.md's Concurrency topic (where the Worker/core model and the locking decision chain already live), the realization level in this document, both cross-linked (Super Z).
- The channel rule was stated deliberately stricter than the ecosystem idiom, and the divergence recorded against Go specifically (Super Z).
- The signaling-primitive contract was kept as an unresolved question tied to process.md's Event concept (Super Z).

#### Deliberation
- The positions were brought from public concurrency discussions (Omid Hekayati):
  - channels are signals, not stores — buffer sizes in the millions as a recurring production failure; the ring-buffer internals of a mainstream channel implementation read as evidence the structure was built for coordination.
  - user-space threading as the required substrate — kernel-thread-per-activity re-pays the cost M:N runtimes exist to remove.
  - worker pools over spawn-per-request — per-request goroutine starvation and tail-latency collapse at scale, the reason high-performance servers pool.

---

### Documentation-method migration: rejected alternatives and anticipated work relocated
- Time: 2026-09-06T00:00:00Z
- Type: refactor
- Propagates to:
  - concurrency.handoff.md: Done - anticipated work recorded there under `Anticipated Work`.
- Contributors:
  - [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) - claimed, decided
  - [Super Z](../../../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) - moved

#### What changed
- The body's `Discussion` wrappers dissolved entirely, per the finalized documentation method (documentation-explanation.changelog.md, same date) (Omid Hekayati - decided; Super Z - applied).
- The topic-level `Discussion`'s evidence paragraph (the channel implementation's ring-buffer source as structural evidence; worker pools as the converged answer) folded into its topic as inline evidence (Super Z).
- The document-level `Drawbacks` removed from the body; its content preserved below without loss (Super Z).
- Rejected-alternative reasoning moved from the body's `Rationale and alternatives` sections into this entry's `Considered and not done`, without loss (Super Z).
- Anticipated work moved from the body's `Future possibilities` into the paired handoff's `Anticipated Work` (Super Z).

#### Considered and not done
- **Adopt the ecosystem's channel idiom wholesale (rejected)**: the idiom's failures are documented above; a framework spanning storage, networking, and GUI cannot keep "channel as data structure" available without inheriting its bugs. (Omid Hekayati)
- **Kernel threads as the default substrate (rejected)**: re-pays the cost user-space threading exists to remove; Networking's position records the parallel judgment for protocol logic. (Omid Hekayati)
- **Leaving pooling per-application (rejected)**: the pool-vs-spawn decision determines load behavior and belongs to the framework's defaults, overridable by configuration. (Omid Hekayati)

#### Considered and not done (from the removed document-level Drawbacks section)
- **The channel rule removes an idiom some developers find ergonomic** — accepted deliberately: the failure modes are load-dependent and therefore arrive after the code review that could have caught them. (Omid Hekayati)
- **The pooling default removes a pattern (spawn-per-request) that is genuinely simpler to write for small systems** — accepted deliberately for the same reason. (Omid Hekayati)

---

### Foreign blocking code narrowed to the detection the substrate rule does not cover
- Time: 2026-10-05T09:41:00Z
- Type: Changed
- Propagates to:
  - concurrency.md: Pending — the detection half is named as the entry's residue; it is not written.
- Contributors:
  - [Space Bunny Alpha](../../../CONTRIBUTORS.md#space-bunny-alpha) (space-bunny via [OpenCode](../../../CONTRIBUTORS.md#opencode)) — argued, drafted, applied

#### What changed
- `concurrency.handoff.md`: "Foreign blocking code" narrowed. Two of the entry's three terms are already answered by the substrate topic's own obligation — an operation that would block a kernel thread is either realized through the substrate's suspension mechanism or explicitly documented as substrate-hostile, so a call into a foreign library takes one of the same two branches, and the documentation expectation is stated rather than open. What the topic names nowhere is detection: how the substrate learns that a foreign call has blocked its carrier, and whether a detected block is reacted to or only surfaced. What also remains is whether the obligation reaches third-party code whose documentation Memar cannot write.
- No other entry moved. The signaling primitive's contract and the substrate-configuration exposure question are untouched; the first still has no contract anywhere, and the second is a decision about the first realization.

---

### Review of the uncommitted changes of 2026-10-12
- Time: 2026-10-12T09:46:30Z
- Type: Reviewed
- Contributors:
  - [Claude](../../../CONTRIBUTORS.md#claude) (Sonnet-5.5) — reviewed

#### What changed
- Reviewed; no change needed. `concurrency.handoff.md` differs from HEAD by the corrected opening path (`modules/computer/concurrency.md`), a relative link to Runtime, and the narrowing of "Foreign blocking code". The narrowing matches the entry above that records it and the substrate topic of `concurrency.md` (the two-branch obligation, no detection mechanism named); the anchor resolves.
