# Terminology Handoff

Open work for `terminology.md`. Entries are mutable current state — revised as each item moves, removed when it resolves or is dropped. See [documentation-handoff.md](./documentation-handoff.md) for what a handoff is.

## Open Questions

### Should the Scientific layer eventually be split into sub-tiers?
Should the Scientific layer eventually be split into mathematical/formal, empirical/scientific, and philosophical/foundational sub-tiers, or does the coarser single layer remain the right trade-off as Memar's documentation grows?

### Should terminology classification join document review checklists framework-wide?
Should terminology classification become part of document review checklists across all of Memar, not only as guidance within this document?

### Should Memar maintain a formal terminology registry?
Should Memar maintain a formal terminology registry?

### Can terminology analysis be partially automated?
Can terminology analysis be partially automated — for example, by detecting when a general concept's mentions in a document correlate almost entirely with mentions of a single specific vendor or tool (a possible automated signal for conceptual leakage)?

### How should AI systems implement terminology weighting in practice?
How should AI systems implement terminology weighting in practice, beyond the qualitative guidance given in [AI Implications](./terminology.md#ai-implications)?

### Should future documents tag their key terms by terminology layer?
Should future documents explicitly identify which terminology layer each of their key terms belongs to, as [this document](./terminology.md)'s own Protocol document arguably should have done and did not?

### Can terminology debt be measured?
Can terminology debt be measured, even approximately?

### Can terminology quality be objectively evaluated?
Can terminology quality be objectively evaluated, or is evaluation of terminology quality itself inescapably a matter of expert judgment?

### When is AI-assisted review superseded by sustained human external review?
At what point, if any, should AI-assisted review (see [On Independent Verification, Today](./terminology.md#on-independent-verification-today)) be considered to have been superseded by sustained human external review, and how would Memar recognize that point when it arrives?

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
