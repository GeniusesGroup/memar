# Knowledge Handoff

Open work for `knowledge.md`. Entries are mutable current state — revised as each item moves, removed when it resolves or is dropped. See [documentation-handoff.md](./documentation-handoff.md) for what a handoff is.

## Open Questions

### What IS the minimum viable knowledge unit?
- The granularity principle argues for fine units, but practical experience is needed to identify the optimal balance between expressiveness and complexity. Is the unit a Concept? An Assertion? A property change? Does the answer vary by domain?

### Can snapshot-style state ever be completely eliminated?
- For legal holds, regulatory compliance, financial audits, and clinical trials, point-in-time global state is a genuine requirement. Is there a hybrid model where logical snapshots coexist with task-centric evolution?

### How do we handle concurrent knowledge modification without locking semantics?
- If two people simultaneously edit the definition of a protocol or a standard, how do we reconcile? (This is the same fundamental problem as database concurrency, not unique to knowledge graphs.)

### Are there domains where hierarchical classification IS actually optimal?
- The classification principle argues against single hierarchies universally, but configuration management, biological taxonomy, and library classification may be sufficiently hierarchical that tree projection IS the natural knowledge model. Where is the crossover point?

### Does the Task concept itself decompose further?
- If Task is not primitive, what is? How far down does decomposition go before reaching truly atomic knowledge primitives?

### How do cultural factors affect principle adoption?
- Research indicates that national culture, professional norms, and organizational climate significantly impact knowledge-sharing behavior. Do the principles need cultural localization, or are they genuinely universal? (The localization question, as a practice, belongs to the Organization project; it is recorded in `knowledge.md` because it tests the domain-independence claim.)

## Anticipated Work

- **Content Domain Model**: [Content](./content.md) now defines Content, Semantic, Reference, and composition; the knowledge-side integration (how Knowledge units, Assertions, and Distinctions map onto Content and Relation) should be worked out against it.
- **Task Domain Model**: defining Task, Decision, Discussion, Outcome and their relationships — possibly as compositions of more primitive concepts.
- **Versioning Strategy**: how versioning works in a non-file-centric system (content versions vs. snapshot versions vs. logical timestamps).
- **Migration Path**: how organizations transition from current tooling to principle-aligned systems incrementally (the organizational-side program belongs to the Organization project).
- **AI Integration Patterns**: how AI systems consume knowledge structured by these principles, and how AI can assist in maintaining it (relationship inference, context extraction, duplicate detection).
- **Knowledge Practices**: the companion [Knowledge Practice](./knowledge.practice.md) develops the followable procedures `knowledge.md`'s principles presuppose — questioning, researching, and evaluating knowledge.
