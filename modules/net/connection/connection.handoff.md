# Networking Connection Handoff
Open work for `modules/net/networking-connection.md`. Entries are mutable current state — revised as each item moves, removed when it resolves or is dropped. See [documentation-handoff.md](../../../modules-plugable/knowledge/documentation/handoff/handoff.md) for what a handoff is.

## Open Questions

### Quantifying the per-connection resource argument
- State: how much state a kernel-managed socket costs at high connection counts versus the userspace realization is recorded as motivation only; the quantification belongs to the realization's own document.
- Next: benchmark during the userspace transport work.

### A terminology entry for "stateless"
- State: given how much confusion the hidden-state arrangement has produced, whether "stateless" deserves an explicit entry in [terminology.md](../../../docs/terminology.md) is undecided. The HTTP instance of the slogan versus cookie reconstruction now lives in [http.md](../../../modules-plugable/net/http/http.md); this question is about the general term.
- Next: propose during the next terminology revision.

## Anticipated Work
- The userspace transport realization under Networking's position topic.
- A terminology entry for stateless if the ecosystem confusion justifies one.
