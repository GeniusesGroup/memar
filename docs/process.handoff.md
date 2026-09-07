# Process Handoff

Open work for `process.md`. Entries are mutable current state — revised as each item moves, removed when it resolves or is dropped. See [documentation-handoff.md](./documentation-handoff.md) for what a handoff is. Questions were relocated here from the document's per-topic Unresolved-questions lists when the documentation method removed those lists from body documents.

## Open Questions

### Definition
1. Whether some weaker ordering property should remain part of the definition itself, rather than being pushed entirely into the *Ordering* topic.
2. Whether temporal progression is intrinsic to the definition of Process, or a property of its enactment.
3. Whether a Process can exist conceptually without an enactment, or whether the distinction should instead be between a Process definition and a Process instance.

### Process Definition and Process Instance
1. Whether Memar should eventually distinguish more formally between a process definition, a process instance, and other possible representations of an enactment.

### Intent
1. Whether every Process must have an identifiable intent, or whether intent is sometimes assigned only by an observer, after the fact.

### State and Transition
1. Whether State and Transition are intrinsic concepts of Process or useful modeling dimensions that apply only to some processes.
2. How the relationship between Process and State should be characterized more formally — a process transforms state, but State is not yet formally defined as its own concept in Memar.

### Requests, Cancellation, and Timeout
1. What the wire-level contract for cancellation across a process or network boundary should look like — request shape, authorization to cancel, acknowledgment, and what the requester may conclude from no response. Deferred to [sRPC's handoff](../protocols/sRPC.handoff.md), which carries the framework's application protocol.
2. The distinction between a *cancelled process* and *abandoned in-flight work*: when a caller gives up, who decides whether the higher-level process is cancelled, still progressing elsewhere, or merely detached from this attempt — and where that decision is recorded? The document's Process Instance and Retry sections give the vocabulary but not the rule.
3. Whether Request should eventually become its own concept document (it currently appears only as a mechanism in *Process Is Not a Mechanism* and in sRPC's service-call machinery), or whether the treatment in process.md is its permanent home.

### Observation
1. Whether Observation should remain a topic within Process, or become a broader concept applicable to System, Model, and other entities as well.

### Process and System
1. Whether the asymmetric-dependency approach actually eliminates the circularity `system.md` originally warned about, or merely relocates it — a real risk, not a resolved one; both documents need to stay in sync as either changes.
2. `system.md` still derives System's own existence from Process ("a system without processes is not a system... the interactions — which are processes — are what make the collection a system"). process.md, symmetrically, no longer derives Process's meaning from a fixed System boundary. Whether this residual asymmetry is intentional and defensible, or whether `system.md`'s phrasing should be loosened, is not resolved and would require a corresponding edit to `system.md` if pursued.

### Process Composition
1. Whether Memar should eventually develop a more formal treatment of process composition — how processes combine, constrain, or interfere with one another.

### Relationship to Other Concepts
1. Whether Process should distinguish between internal activities and interactions with external participants, and if so, whether that distinction belongs in *Activities and Interactions* rather than in the relationship topic.
2. Whether scheduling should remain a topic within Process or become a separate foundational concept. The Agency and Execution Responsibility section establishes the conceptual distinction between an Execution Agent and its implementation representation; a future scheduling document may formalize Worker identity, registration, placement, migration, and CPU-core relationships without making those mechanisms part of the Process definition.
3. Whether the distinction between Process and Protocol requires dedicated documentation beyond their current relationship.
4. Whether Workflow requires any further conceptual treatment beyond its role as a possible process representation.

## Anticipated Work

- If Concurrency, Coordination, or Events grow enough conceptual weight of their own — enough to be reasoned about independently of Process rather than only in relation to it — each may eventually justify a dedicated document, at which point process.md would shrink to reference them rather than define them in full, following the same source-of-truth pattern process.md itself now establishes relative to `system.md`. (Migrated from the document's retired `Future possibilities` section.)
