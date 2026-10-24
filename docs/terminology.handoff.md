# Terminology Handoff
Open work for `terminology.md`. Entries are mutable current state — revised as each item moves, removed when it resolves or is dropped. See [documentation-handoff.md](../modules-plugable/knowledge/documentation/handoff/handoff.md) for what a handoff is.

## Open Questions

### Should the Scientific layer eventually be split into sub-tiers?
Should the Scientific layer eventually be split into mathematical/formal, empirical/scientific, and philosophical/foundational sub-tiers, or does the coarser single layer remain the right trade-off as Memar's documentation grows?

### Should terminology classification join document review checklists framework-wide?
Should terminology classification become part of document review checklists across all of Memar, not only as guidance within this document?

### Can terminology analysis be partially automated?
Can terminology analysis be partially automated — for example, by detecting when a general concept's mentions in a document correlate almost entirely with mentions of a single specific vendor or tool (a possible automated signal for conceptual leakage)?

### Can terminology debt be measured?
Can terminology debt be measured, even approximately?

### Can terminology quality be objectively evaluated?
Can terminology quality be objectively evaluated, or is evaluation of terminology quality itself inescapably a matter of expert judgment?

### When is AI-assisted review superseded by sustained human external review?
At what point, if any, should AI-assisted review (see [On Independent Verification, Today](./terminology.md#on-independent-verification-today)) be considered to have been superseded by sustained human external review, and how would Memar recognize that point when it arrives?

### Is borrowing a mathematical term for a non-mathematical relation a named error?
The owner named the borrowing of a mathematical term for a relation outside mathematics as an error that reproduces itself across a domain, the way *energy* is borrowed outside physics (recorded 2026-10-08 in the `organization` project, `bundles/supply-chain/supply-chain.changelog.md`, *Deliberation*, attributed to Omid Hekayati; the instance was "the supply chain is a subset of the value chain", where neither chain's activities contain the other's). This document governs what a Scientific-layer term means, but not what happens when the term is carried into a relation where its defining properties do not hold. Open: whether this is stated here as a rule on the Scientific layer — a borrowed term keeps its defining properties or is not used — or recorded as a fallacy in the practice-layer catalog that [Cognition → Named Errors](./cognition.md#named-errors-biases-and-fallacies) leaves to practice; and how a reviewer tells a borrowing from a legitimate use of the same term with its properties intact.

## Anticipated Work
- A Word-Weight Rebalancing mechanism for AI systems (see [AI Implications](./terminology.md#ai-implications)), specifying concretely how a Memar document's Definitions would be loaded as higher-precedence context, how conflicts with a person's own usage would be surfaced, and how the mechanism's actual effect would be evaluated rather than assumed.
- Framework-wide terminology registry.
- Automated terminology conflict detection.
- Automated conceptual-leakage detection, flagging documentation where a general concept is discussed almost exclusively in terms of one specific vendor or tool.
- AI-assisted concept tracing.
- Concept-to-technology mapping tools.
- Terminology linting as part of document review tooling.
- Auto-generated Memar glossary, tagged by terminology layer.
- Terminology debt assessment tooling.
- Architectural terminology review workflows.
- A documented convention, once document contributor governance is finalized, for distinguishing AI-assisted internal critique from sustained human external review in a contributor's listed effort — so that a reader can tell, at a glance, how much of "public scrutiny" a given document has actually received.
- Recognition mechanism for review graduation: Terminology already defines the threshold (sustained human external review superseding interim AI critique) but not how supersession is recognized and recorded. Task stays deliberately open — no session closes it unilaterally.
- Proposed recognition record (proposal only, no new required field): each document's changelog states review classes received — AI-assisted internal critique versus sustained human external review — via existing Contributors roles and Cited sources; `approved` continues to record only the internal second-party check and is never read as external supersession. Pending contributor-governance finalization.
