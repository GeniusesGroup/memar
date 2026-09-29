# Networking Connection Handoff

Open work for `protocols/networking-connection.md`. Entries are mutable current state — revised as each item moves, removed when it resolves or is dropped. See [documentation-handoff.md](../documentation-handoff.md) for what a handoff is.

## Open Questions

### The state-exposure surface
- State: what a connection component must expose to layers above (read-only state query, events, subscriptions) and in what form — interacts with the Event concept in [process.md](../process.md#events); not yet specified.
- Next: joint session with the Event topic.

### Per-exchange explicit bounds
- State: whether the caller-meaningful time-bound case needs a dedicated parameter convention in [sRPC](./sRPC.md), or remains an application-level modeling choice.
- Next: decide when the first caller-meaningful-bound service is designed.

### Quantifying the per-connection resource argument
- State: how much state a kernel-managed socket costs at high connection counts versus the userspace realization is recorded as motivation only; the quantification belongs to the realization's own document.
- Next: benchmark during the userspace transport work.

### A terminology entry for "stateless"
- State: given how much confusion the hidden-state arrangement has produced, whether "stateless" deserves an explicit entry in [terminology.md](../terminology.md) is undecided. The HTTP instance of the slogan versus cookie reconstruction now lives in [http.md](./http.md); this question is about the general term.
- Next: propose during the next terminology revision.

## Anticipated Work

- The userspace transport realization under Networking's position topic.
- The state-exposure surface once the Event model settles.
- A terminology entry for stateless if the ecosystem confusion justifies one.
