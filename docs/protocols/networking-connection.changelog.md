# Networking Connection Changelog

## Changelog

### Initial draft — connection state ownership and liveness budgets
- Time: 2026-09-06T00:00:00Z
- Type: Added
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — claimed, argued
  - [Super Z](../../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — reviewed, rewrote

#### What changed
- Initial Draft defining the connection concept in Networking's packet model and the framework's core rule: connection state is owned by the component that runs the protocol logic and is exposed to layers above; timeouts and liveness are the owning component's budgets; blocking-read as an interface failure, not a property of networking (Omid Hekayati).
- The positive contract (connection concept, state-ownership-with-exposure rule, half-open resolution rule) was stated as the complement to networking.md's position on the traditional network stack (Super Z).
- The blocking-read failure was linked to the interface-design level rather than to a specific language (Super Z).
- Frame-level mechanics were kept out of scope per protocol-document ownership (Super Z).

#### Deliberation
- The positions were brought from public discussions: the blocking-socket-read critique (no first-class "no data yet" outcome; goroutine-spawning and read-deadline answers are workarounds around a mis-shaped interface) and the stateful/stateless contradiction (HTTP called stateless while its specifications define persistent state; Transport state re-created badly at the Application layer) (Omid Hekayati).
- The timeout-as-component-budget rule was contributed, later formalized in process.md's context critique (Omid Hekayati).

---

### Documentation-method migration: rejected alternatives and anticipated work relocated
- Time: 2026-09-06T00:00:00Z
- Type: refactor
- Propagates to:
  - networking-connection.handoff.md: Done - anticipated work recorded there under `Anticipated Work`.
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) - claimed, decided
  - [Super Z](../../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) - moved

#### What changed
- The body's `Discussion` wrappers dissolved entirely, per the finalized documentation method (documentation-explanation.changelog.md, same date) (Omid Hekayati - decided; Super Z - applied).
- The topic-level `Discussion`'s evidence paragraph (QUIC's userspace model as existence proof; the "stateless HTTP" contradiction visible in the cookie and session specifications) folded into its topic as inline evidence (Super Z).
- The document-level `Drawbacks` removed from the body; its content preserved below without loss (Super Z).
- Rejected-alternative reasoning moved from the body's `Rationale and alternatives` sections into this entry's `Considered and not done`, without loss (Super Z).
- Anticipated work moved from the body's `Future possibilities` into the paired handoff's `Anticipated Work` (Super Z).

#### Considered and not done
- **Keep the socket arrangement and expose state through side-channels (rejected)**: side-channel views of kernel state drift from the state itself by construction - exactly the failure the ownership rule prevents. (Omid Hekayati)
- **Declare connections an application-layer concept only (rejected)**: the same state-sharing need exists at every layer maintaining per-peer context; dissolving the concept upwards would forbid stating Transport-level rules where they are true. (Omid Hekayati)
- **Specify the userspace TCP realization in this document (rejected)**: the realization is one implementation of this contract; mixing them couples the contract to one codebase's decisions. (Omid Hekayati)

#### Considered and not done (from the removed document-level Drawbacks section)
- **Exposing connection state widens the component's surface.** A component that hides state has a narrow interface by construction; one that exposes it must keep that exposure stable and correct. The framework takes this cost deliberately - invisibility is what produced the shadow-copy failures - but it is a cost. (Omid Hekayati)
- **The realization does not exist yet.** The positions here are currently ahead of the code that would validate them; the socket arrangement, whatever its faults, is running infrastructure today. (Omid Hekayati)
