# Process Handoff
Open work for `process.md`. Entries are mutable current state — revised as each item moves, removed when it resolves or is dropped. See [documentation-handoff.md](./documentation-handoff.md) for what a handoff is. Questions were relocated here from the document's per-topic Unresolved-questions lists when the documentation method removed those lists from body documents.

## Open Questions

### Expectations and Checks
2. Whether the four roles that share overloaded domain words (written expectation artifact, comparison procedure, enacted comparison, disposition) eventually need fixed Memar terms beyond the *expectation* / *check* pair clarified in the 2026-09-16 review — open only if that pair proves insufficient in practice; mirrored in `docs/modules/process/test.handoff.md`.

### Defect Resolution as an Inquiry
2. Whether the inquiry's candidates should be organized as a tree across separately asked questions — why the defect occurred, why it reached a participant, why it was not detected earlier, why it lasted as long as it did — rather than held as the competing candidates of a single question. The topic now requires plural candidates and a refuting observation each, and still returns one generating cause. Tracked from [Process Research 002](./process.changelog.md).
3. Whether the point at which a change would keep a class of these from arising is a decision the inquiry returns in its own right, or an interpretation each reader layers on its finding. The topic currently states the second without saying so.

### Intent
1. Whether every Process must have an identifiable intent, or whether intent is sometimes assigned only by an observer, after the fact.

### State and Transition
2. How the relationship between Process and State should be characterized more formally — a process transforms state, but State is not yet formally defined as its own concept in Memar.

### Requests, Cancellation, and Timeout
1. Whether Request should eventually become its own concept document (it currently appears only as a mechanism in *Process Is Not a Mechanism* and in sRPC's service-call machinery), or whether the treatment in process.md is its permanent home.

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
- **Graduation criterion for Defect Resolution as a standalone document**: the topic stays in this document while its content is the linking of already-owned rules (Expectations and Checks' inquiry boundary, Cognition's operations, the Research facet) to the defect situation. It graduates only if Memar-specific rules accrue that are not applications of those documents — for example, reproducibility requirements on the inquiry, or a defect-reporting contract between participants — at which point a module document under `docs/modules/` becomes warranted. Any proposed addition to the topic should first be tested against that rule: content that applies an inherited rule to defects belongs in the consuming document, not here.
- **Graduation criterion for Development as a standalone document**: the *Development as a Process* topic is carried as an umbrella adoption — a word that adds no content of its own, whose warranted content is exactly the Process topics applied to the entity being advanced. It graduates into its own document only if warranted content accrues that is **not** an application of those topics — a genuine question about development the Process topics cannot already answer. Candidate cases the protocol layer could still force: whether the stage/degree structure of a development needs more than the topics give (e.g. whether a target stage admits degrees of attainment beyond a process's outcome set), or whether the participant/agency structure of a long-running development program exceeds what *Agency and Development* plus the topics supply. Until then the topic stays in this document, and any proposed addition to it should first be tested against the umbrella rule: content that merely applies an inherited topic to developments belongs in the consuming protocol document, not here. (Same path Process itself took out of `system.md`.)
- If Concurrency, Coordination, or Events grow enough conceptual weight of their own — enough to be reasoned about independently of Process rather than only in relation to it — each may eventually justify a dedicated document, at which point process.md would shrink to reference them rather than define them in full, following the same source-of-truth pattern process.md itself now establishes relative to `system.md`. (Migrated from the document's retired `Future possibilities` section.)

### Threads the four-discipline survey left open
Recorded from the survey whose result is in [Process Changelog](./process.changelog.md#four-disciplines-surveyed-against-process-modeling-and-their-practices), so they are not re-derived from the documents:
- **Should the point at which a change would prevent a class of these from arising be a decision the inquiry returns in its own right**, or an interpretation its reader layers on the finding? The second is the current position and is stated nowhere.
- **Should a check's expectations carry a baseline and a declared limit** - what must not get worse on the way to the outcome - so a result is read against something declared before the work rather than against whichever number each reader prefers? And is that second half a concept Memar should name, or an application of [System -> The Inseparability of Capability and Constraint](./system.md#the-inseparability-of-capability-and-constraint) needing no name?
- **Is terminology.md complete without an entry for the problem a process serves**, given that four independent disciplines all needed the word and none found it? The absence was recorded as a finding rather than supplied, since defining it is the owner's.
- **Should Memar state anywhere that its scope includes problem solving as a subject**, or does [README -> Where Memar Stops](../README.md#where-memar-stops-and-where-work-continues) settle it by omission? A framework's limits are checkable only where it names them.

