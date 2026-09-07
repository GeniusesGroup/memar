# Concurrency Realization Changelog

## Changelog

### Initial draft — substrate, channel contract, pooling default
- Time: 2026-09-06T00:00:00Z
- Type: Added
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — claimed, argued
  - [Super Z](../../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — reviewed, rewrote

#### What changed
Initial Draft with three realization rules — user-space-thread substrate, channels-as-signals (never channel-as-store), pooled execution units — plus the substrate-hostile-operation obligation for framework libraries.

The positions were brought from public concurrency discussions: channels are signals, not stores (buffer sizes in the millions as a recurring production failure; the ring-buffer internals of a mainstream channel implementation read as evidence the structure was built for coordination); user-space threading as the required substrate (kernel-thread-per-activity re-pays the cost M:N runtimes exist to remove); worker pools over spawn-per-request (per-request goroutine starvation and tail-latency collapse at scale, the reason high-performance servers pool) (Omid Hekayati).

The concept-level treatment (kept in process.md's Concurrency topic, where the Worker/core model and the locking decision chain already live) was split from realization-level rules (this document), both cross-linked; the channel rule was stated deliberately stricter than the ecosystem idiom and the divergence recorded against Go specifically; the signaling-primitive contract was kept as an unresolved question tied to process.md's Event concept (Super Z).

---

### Documentation-method migration: rejected alternatives and anticipated work relocated
- Time: 2026-09-06T00:00:00Z
- Type: refactor
- Propagates to:
  - concurrency.handoff.md: Done - anticipated work recorded there under `Anticipated Work`.
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) - claimed, decided
  - [Super Z](../../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) - moved

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
