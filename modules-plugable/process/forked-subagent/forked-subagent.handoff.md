# Forked Sub-Agent Handoff
Open work for [forked-subagent.md](./forked-subagent.md). Entries are mutable current state — revised as each item moves, removed when it resolves or is dropped. See [documentation-handoff.md](../../knowledge/documentation/handoff/handoff.md) for what a handoff is.

## Open Questions

### Is a fork's shared prefix a cache hit for every child, and for how long?
1. Whether the prefix is a cache hit for every child started within the cache's life, and what that life is (five minutes, one hour). The [Cost](./forked-subagent.md#cost) saving holds only for children started within it, so the answer decides how a parent paces its waves. Only the runtime's publisher can answer. *(Blocking: no.)*

### What happens to a running child when the parent's context is compacted?
1. Whether a child keeps the prefix it was started with, or is affected when the parent's earlier context is replaced by a summary. The fourth expectation ([The Expectation](./forked-subagent.md#the-expectation)) says a running child is unaffected by the parent's later turns; compaction is the case it does not settle. Memar's own rule after a compaction — re-read the skill and the plan — is written for the parent and says nothing of a child. *(Blocking: no.)*

### Can a child be told it is a fork and must not fork further?
1. Whether the runtime lets a child's task say that it is a fork and may not itself fork, to bound the tree of agents. Without it a parent cannot bound the cost of a wave. *(Blocking: no.)*

### Is the `fork` agent type some builds mention this capability?
1. The Agent tool's description in some builds mentions a `fork` agent type; in the build this was drafted against it was not offered. If it is this feature, its status (experimental, withdrawn, gated) decides whether Memar's practice can rely on it. *(Blocking: no.)*

### Where the document belongs
1. It is placed under `modules-plugable/process/` and labelled `guest` because its subject is an expectation about a runtime whose authority lies outside Memar, which is [Guest's test](../../../modules/knowledge/modularity/labels/guest.md#the-test). It is not a kernel module of Memar's, and it is not a concept, so it does not sit at the root of `docs/`. It is filed under the Memar category the surface attaches to (`process`), as every guest is ([Pluggable](../../../modules/knowledge/modularity/labels/pluggable.md)). Revisit if the owner prefers the agent runtime as a category of its own, which would move this document and not change its text. *(Blocking: no.)*

### Whether the skill should change when a runtime offers the fork
1. The skill's Delegation section links this document. When a runtime offers the fork, the section's sizing test (delegate by bytes read, one sub-agent per session, brief only) is written for cold starts and would need to say what a fork changes. Do not edit it before the capability exists; record here what the first real use shows. *(Blocking: no.)*

## Anticipated Work
- **The owner sends the request.** The English request to Anthropic, drafted at `.agents/tasks/20261013-T054743Z-12960/docs/feature-request-forked-subagents.md`, is the owner's to send; this document states the same expectation as Memar's. Record the reply, or that none came, against the questions above, and revise [The Expectation](./forked-subagent.md#the-expectation) if the reply changes what a runtime can promise.
- Prices: once a runtime publishes its write and read prices, restate [Cost](./forked-subagent.md#cost) with a worked example for K children and a prefix of the size Memar's skill and governing documents come to, and the break-even where reading an unused prefix costs more than a cold start.
