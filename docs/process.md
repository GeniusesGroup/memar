---
Title: "Process"
Status: Draft
Start Date: "2026-08-15"
ID: "496320"
---

# Process

## Abstract
A **process** is a bounded progression of related activities, interactions, or changes that can be understood as belonging to a common intent or concern. A process describes something that happens, may happen, or is being carried out — it is concerned with behavior and progression, not with the static existence of things.

A process is not defined by the mechanism used to enact it. A transaction, a queue, a lock, a thread, a request, a workflow engine, and a Saga may each participate in the execution of a process, but none of them *is* a process, and none of them is an intrinsic requirement of one. This document exists to make that separation explicit, because a large share of avoidable complexity in system design comes from treating a mechanism's name as if it were the definition of the underlying problem.

## Introduction

### Motivation
This document originated from two public discussions about concurrency and distributed transactions (Saga patterns, distributed locking) in which the same pattern kept recurring: a technical mechanism was treated as though it were required by the nature of the problem, rather than as one possible answer to a question that had not yet been asked explicitly. "The operation failed, so we must roll back." "Multiple operations touch the same resource, so we must lock it." "The service is external, so we need a Saga." Each of these treats a mechanism as a starting point rather than a conclusion.

The purpose of this document is not to prescribe a particular execution mechanism or development technique. A process should be understood before selecting the mechanisms by which it may be initiated, coordinated, executed, continued, observed, interrupted, or completed. Many terms commonly used in software development describe mechanisms rather than the underlying process; treating a mechanism as the definition of the process creates a misleading mental model and can make a particular implementation technique appear universally necessary when it is not.

This document also absorbs the treatment of Failure's relationship to Process, to the extent needed here. The detailed conceptual treatment of Error remains out of scope and belongs to dedicated Error documentation.

### Methodology
This document was drafted through an extended dialectical session covering two public discussions (Saga/rollback, distributed locking), then reviewed against `system.md`, `protocol.md`, and `terminology.md` for cross-document consistency — since, by this project's own methodology, Process cannot be understood in isolation from System. That review surfaced a direct conflict with a decision `system.md` had already made and recorded: see *Process and System → Discussion → Rationale and Alternatives* below for the conflict and its resolution.

## Explanation

### Process Before Mechanism
The central design principle of this document is: **understand the process before selecting the mechanism.**

This means identifying what must happen, why it must happen, who participates, what conditions matter, what outcomes are valid, and which constraints must hold — before deciding whether a transaction, event, queue, lock, retry, scheduler, Saga, or other mechanism is appropriate.

```text
Intent
  ↓
Process
  ↓
Participants, activities, states, constraints, outcomes
  ↓
Required properties
  ↓
Possible mechanisms
  ↓
Implementation
```

This principle does not reject established mechanisms; it rejects using their names as substitutes for understanding. A technically sophisticated mechanism applied to the wrong process remains a wrong design. A simpler mechanism applied to a correctly understood process may provide stronger correctness, lower coordination cost, and greater clarity.

### Process Is Not a Mechanism
A transaction is not a process. A queue is not a process. A lock is not a process. A thread is not a process. A request is not a process. A workflow engine is not a process. A Saga is not a process. Each of these may participate in the execution or coordination of a process, but none defines the underlying concept. A request may initiate, advance, observe, modify, retry, or terminate a process, but the request itself is an interaction or representation of an interaction, not the process as a whole.

This distinction matters because mechanisms usually encode particular assumptions, so a mechanism useful for one process can be unnecessary, inappropriate, or even harmful for another. A failed operation does not inherently imply rollback. A repeated operation does not inherently imply that the server should retry it. Concurrent execution does not inherently imply a lock. An event does not inherently imply that the producer knows which consumers will react to it. The process must be understood independently of the mechanism before the mechanism is selected.

### Mechanism-First Reasoning
A recurring design error is to encounter a technical mechanism and search for a problem that appears to justify it — assuming, for example, that failure requires rollback, that concurrency requires locks, that repetition requires automatic retry, that distributed execution requires a distributed lock, that asynchronous behavior requires `async/await`, that communication requires an event broker, or that a distributed process requires a Saga because a database transaction cannot span an external boundary. These assumptions reverse the direction of reasoning shown above: the mechanism should be selected because the process requires a property that the mechanism can provide, not because the mechanism is commonly associated with the problem category.

This is not an argument against mechanisms. A financial process may still need a lock; a cross-service process may still need a Saga. The objective is to avoid making a mechanism an implicit requirement before the process has been understood — including in domains commonly considered sensitive or technically difficult, such as financial and distributed systems, where the instinct to reach for the "safe-sounding" mechanism is strongest and the cost of skipping the analysis is highest.

### Common Modeling Errors
Several recurring errors result from treating implementation terminology as if it were the underlying process model:

- **Treating Process as a linear sequence.** A process does not need to be a single ordered chain of steps; activities may be independent, concurrent, conditional, delegated, or repeated.
- **Treating Process as server-side execution.** A process may cross servers, clients, systems, participants, and time boundaries; the component that initiates a process does not necessarily execute it.
- **Treating failure as rollback.** Rollback is one possible response to failure, not the definition of failure or process recovery.
- **Treating retry as automatic.** Retry may be explicitly requested by a user, SDK, operator, scheduler, or another process; it does not inherently belong to the server that performed the previous attempt.
- **Treating concurrency as locking.** Concurrency is about simultaneous or overlapping progression; it does not imply shared state or shared mutable ownership. Locking is one possible mechanism for satisfying a particular constraint, not the definition of concurrency.
- **Treating Parallelism as a concept distinct from Concurrency.** The hazards commonly attributed only to execution on multiple physical cores can occur on a single core whenever activities can interleave; see *This Document Treats Concurrency as One Concept, Not Two* under Concurrency.
- **Treating events as commands to known consumers.** An event can expose a fact without the producer knowing which processes will react to it, and a consumer is not thereby made a continuation of the producer's process.
- **Treating event handling behavior as intrinsic to Event.** Whether an event handler blocks, alters, or otherwise affects another activity is a property of the dispatch and handling rules, not of the Event concept itself.
- **Treating asynchrony as a language primitive.** Asynchrony is a property of progression and waiting relationships; `async/await` is only one implementation representation of it.
- **Treating observation as the definition of the process.** A given observation should not automatically be elevated to the process's intrinsic definition.
- **Treating implementation boundaries as process boundaries.** A function, module, service, server, or deployment unit is not automatically a process boundary.
- **Treating a familiar pattern as a requirement.** Patterns and mechanisms are solutions to classes of problems; they should not become the starting point for defining the problem.

### Definition
A **Process** is a bounded progression of related activities, interactions, or changes that can be understood as belonging to a common intent or concern.

A process is the concept that gives related activities and changes a meaningful progression. Activities and changes are therefore parts or manifestations of a process, rather than an alternative definition of the process itself.

The definition deliberately does not require a process to be a sequence in the strict sense. Activities may be sequential, concurrent, overlapping, conditional, iterative, delegated, interrupted, or independently continued, and a process may have no single continuously executing component. A process does not derive its identity from the mechanism used to enact it — the same process may be implemented through different combinations of direct calls, messages, events, scheduled work, persistent state, distributed participants, or other mechanisms.

The defining question is therefore not *"which mechanism executes this?"* but *"what is happening, for what intent, involving which participants, under which constraints, and with which possible outcomes?"*

#### Discussion

##### Rationale and alternatives
- **Requiring Process to be a strict sequence (rejected).** `system.md`'s prior definition called Process "an organized sequence of activities or interactions." This document deliberately drops "sequence," because sequence is one possible shape a process can take, not a defining property — treating it as defining would make concurrent, event-driven, and independently-progressing processes look like deviations from the "real" definition rather than the ordinary cases they are.

##### Unresolved questions
1. Whether some weaker ordering property should remain part of the definition itself, rather than being pushed entirely into *Ordering* below.
2. Whether temporal progression is intrinsic to the definition of Process, or a property of its enactment.
3. Whether a Process can exist conceptually without an enactment, or whether the distinction should instead be between a Process definition and a Process instance.

### Process Definition and Process Instance
A process model describes the possible structure, behavior, constraints, and outcomes of a process. A particular enactment of that process may traverse only a subset of those possibilities.

Each **Process Instance** is therefore a particular realization of a process. It may activate only some activities, follow one of several possible paths, involve a subset of participants, encounter different conditions, or terminate at a particular outcome. The complete process model may describe possibilities that are not exercised by a particular instance, while an observed instance may reveal only a partial view of the process.

The distinction is important because a process model must not be confused with any single execution of it. A process definition describes what may be relevant to the process as a whole; an instance describes what is relevant to one occurrence. An instance does not need to realize every element represented by the process model.

This distinction also matters when a process is retried, repeated, or composed. A later attempt may be initiated as a new interaction or request while remaining part of the same higher-level process, and the higher-level process may retain knowledge of how many attempts have occurred or which part of its progression they belong to.

#### Discussion

##### Unresolved questions
1. Whether Memar should eventually distinguish more formally between a process definition, a process instance, and other possible representations of an enactment.

### Intent
Intent provides an important basis for identifying the boundary of a process. Two activities may occur close together in time and even use the same data while belonging to different processes; conversely, activities performed by different components may belong to one process when they collectively contribute to the same intent.

Within this document, **Intent** and **Purpose** are closely related rather than competing concepts. Both concern the outcome toward which a process is directed. The distinction is primarily one of expression and origin: an intent may be implicit, inferred, or held by a participant, while a purpose is an articulated account of what the process is for and what outcome it is organized toward. A process may therefore have a purpose even when no participant explicitly states an intent.

Identifying the purpose or intent of a process may itself require analysis. A process may have been established for one purpose and later acquire additional purposes or functions through interaction with other systems, participants, or processes. These later effects may become relevant to understanding the process even when they were not part of its original intent. Likewise, a process may be directed toward an intended outcome without successfully realizing that outcome. Purpose or intent therefore does not imply successful completion.

Intent should not be reduced to a user request — a process may be initiated by a person, another process, a system condition, a scheduled condition, an external event, or some other actor. Intent also does not necessarily determine implementation ownership: the participant that expresses an intent does not necessarily execute every activity required to fulfill it. This is what allows a process to cross component, service, machine, organizational, or temporal boundaries without losing its conceptual identity.

#### Discussion

##### Unresolved questions
1. Whether every Process must have an identifiable intent, or whether intent is sometimes assigned only by an observer, after the fact.

### Participants
A process may involve one or more participants. A participant may be a person, organization, system, component, service, device, or other entity capable of taking part in an activity or interaction relevant to the process. Participation does not imply implementation ownership.

A participant may initiate a process, provide information, perform an activity, authorize an action, observe an outcome, receive a result, request continuation, cancel a process, or delegate part of the process to another participant. A process should not be modeled as if one server, service, thread, or application necessarily owns its entire execution.

### Activities and Interactions
A process may contain activities and interactions. An **activity** is something performed as part of the process. An **interaction** describes a relationship between participants through which information, requests, decisions, results, or other relevant effects are exchanged. The activities of a process do not need to be executed by one participant or in one location.

An activity may produce a result that becomes relevant to another process without the originating process needing to know that process exists. This is particularly important when using events: a process can make a fact available without designing that fact as a command to a known consumer. For example, a process that records an order as finally paid may make that fact available to the system; other processes may independently use that fact for their own purposes, and the original process does not need to understand the internal behavior of those processes merely because they react to the same fact.

### State and Transition
A process may involve state. State represents conditions relevant to understanding the position or status of a process, and a process may move from one state to another as activities occur, information becomes available, conditions change, or decisions are made.

A state transition is not necessarily equivalent to the execution of one function or one request — it may result from multiple activities, asynchronous interactions, external decisions, or independently executed work. Likewise, the existence of a state does not imply that all transitions must be controlled by a single component. A useful process model therefore distinguishes between the state being represented, the conditions under which that state can change, the activities or interactions that may cause change, and the participants capable of causing or authorizing that change. The representation of state is an implementation concern unless the representation itself is part of the domain concept.

#### Discussion

##### Unresolved questions
1. Whether State and Transition are intrinsic concepts of Process or useful modeling dimensions that apply only to some processes.
2. How the relationship between Process and State should be characterized more formally — a process transforms state, but State is not yet formally defined as its own concept in Memar.

### Outcomes
A process may have one or more possible outcomes. An outcome is not necessarily a binary success or failure — a process may produce a completed outcome, a partial outcome, a pending condition, a cancelled outcome, a rejected outcome, or another domain-specific result.

The existence of multiple outcomes matters because it prevents process design from being reduced to:

```text
start → success
      → failure → undo
```

A process should instead describe the outcomes that are meaningful in its domain and the transitions by which those outcomes may be reached. The correct response to an unsuccessful activity is a property of the process, not a universal property of failure.

### Failure
Failure is a possible condition or outcome within a process, and it does not prescribe what should happen next. Depending on the process, a failure may result in another attempt, a request for human intervention, a pending state, compensation, cancellation, an alternative path, a partial but valid outcome, or termination — rollback is only one possible response among these.

The process should determine what the failure means and what consequences are valid; the implementation should not impose rollback merely because a mechanism such as a database transaction makes rollback convenient. The detailed definition and treatment of Error belongs to dedicated Error documentation; this document establishes only the relationship between failure and process.

### Continuation and Retry
A process may continue after an interruption or unsuccessful attempt, but continuation must not be assumed to be an automatic server-side retry. A retry may be initiated by any participant capable of requesting another attempt — a user interface, SDK, server component, scheduler, operator, another process, or another system — and the continued attempt does not necessarily execute in the same component, server, process, or location as the previous attempt.

> Retry is a possible request or strategy for continuing a process, not an intrinsic responsibility of the server that performed the previous attempt.

This distinction matters most when designing distributed systems: the location from which continuation is requested and the location in which the resulting work is executed are separate architectural decisions. A retry also does not imply that the process should return to its previous state — a new attempt may legitimately begin from a later state, use new information, or follow a different path.

A retry request typically carries the same intent and parameters as the request it follows, but it is not the same request occurrence — it is a new interaction that happens to refer back to an earlier one. This does not make the retry invisible to the higher-level process: a process can be fully aware that a given step is being retried, how many attempts have occurred, and which part of its progression they belong to, and can expose that information to other participants — awareness of retry is a property the process may carry, even though each individual attempt remains, on its own, a distinct occurrence rather than a replay of the same one.

### Cancellation
A process may be cancellable, but cancellation is not synonymous with rollback. Cancellation expresses a decision that the process should no longer continue according to some applicable rule; it does not necessarily mean that every effect already produced by the process should be removed. Whether cancellation is available, who can request it, when it is valid, and which effects can be reversed are properties of the process.

A system should not automatically replace a participant's ability to make a decision with an implementation-level rollback merely because an operation encountered difficulty. A process can instead be designed so that its current state and available actions are visible to a participant, allowing that participant to decide whether to continue, retry, or cancel where the domain permits such decisions.

### Concurrency
Activities within a process may be sequential, concurrent, overlapping, or independently progressing. Concurrency is a property of how parts of a process may progress relative to one another — it is not, by itself, evidence that mutual exclusion is required. Concurrency does not imply shared state either. Activities may progress concurrently while operating on independent state or independently owned resources.

A process that appears to operate on a shared resource may sometimes be redesigned so that the relevant work is partitioned by ownership, routed to a responsible participant, serialized by scheduling, or otherwise structured such that a lock is unnecessary. For example, if bookkeeping for each account can be assigned to one execution owner at a time — a server, worker, process, execution context, or another architecturally chosen unit — operations concerning different accounts may progress independently without requiring all participants to acquire the same lock.

The important question is therefore not *"where should we add a lock?"* but *"what concurrency constraints does the process actually require, and can the process be structured so that those constraints are satisfied without shared mutable ownership?"* Locking is one possible mechanism for satisfying a concurrency constraint; it is not the definition of concurrency and should not become its default representation.

This can be stated as an explicit chain of questions, each one skipped if the previous already resolves the concern:

```text
Do the concurrent activities share state?
        ↓
Do they share mutable state?
        ↓
Does that state need to satisfy the same invariant?
        ↓
Does maintaining that invariant require common ownership?
        ↓
Can the responsibility instead be partitioned?
        ↓
Can scheduling enforce that partition?
        ↓
Only if none of the above resolves it —
is synchronization actually required?
        ↓
Only then — is locking one possible mechanism?
```

Most concurrency questions are resolved well before the last two steps. Reaching directly for synchronization or locking skips the steps that, in many real designs, would have made them unnecessary.

#### This Document Treats Concurrency as One Concept, Not Two
Many explanations of concurrent systems introduce Parallelism as a second concept alongside Concurrency, distinguished by whether activities execute on more than one physical processing unit at the same time. This document does not adopt that split; it treats Concurrency as the single relevant concept, regardless of how many processing units are involved.

The reason is that the hazard usually attributed only to "parallel" execution does not require a second processing unit to occur. Consider two coroutines sharing a variable: the first begins an operation on that variable, then yields while it waits on a result from the second; the second coroutine — scheduled onto the very same CPU core, not a different one — begins the same operation on the same variable and corrupts its state before the first coroutine resumes and becomes aware of the change. Nothing about this requires two cores. A single core capable of switching between two units of work reproduces the same hazard usually described as a problem exclusive to parallel execution. Filing it under "Parallelism" and treating single-core code as exempt hides a hazard that is present as soon as activities can interleave at all — with or without a second processing unit.

Introducing a second word to carve out the multi-core case follows the same pattern this project has already flagged elsewhere: rather than working with a Concurrency broad enough to already cover the phenomenon, the ecosystem introduced a second term around a narrower slice of it — comparable to how an early, over-narrow definition of *inheritance* was left in place while *composition* was coined separately to say what a properly scoped original term could already have said.

What genuinely does vary, and does deserve modeling attention, is how many independent units of execution — Workers — a process's activities are distributed across, and how those Workers relate to physical execution resources. A Worker is a logical unit this model cares about; it may be registered and assigned its own identifier independently of how many CPU cores exist or which one it happens to run on at a given moment. A CPU core is a physical execution resource with its own identifier, assigned by the operating system or runtime rather than by the process model. The relationship between the two — one Worker pinned to one core, several Workers time-sharing one core, one Worker migrating across cores — is exactly the kind of choice *Mechanisms Are Not Obligations* already warns should not be assumed by default: pinning part of a process to one fixed Worker, for instance, can resolve a concurrency hazard without a lock, precisely because it removes the possibility of two activities touching the same state through two different Workers at once. This is a modeling decision worth considering regardless of how many cores are involved, not a technique that only becomes relevant once multiple cores are.

#### Others
- Go's goroutine scheduler is a useful illustration of what happens when this distinction is left implicit. It is widely liked for making concurrent code pleasant to write, and the M:N scheduling it performs across goroutines and OS threads is a reasonable implementation choice for many teams. But that scheduling does not remove the underlying concurrency hazards described above — it relocates them behind an abstraction. Without a further layer designed specifically to make that relocation visible and controllable, the ease of spawning goroutines readily produces exactly this class of hazard, along with unnecessary queuing and locking that a more deliberate Worker/core model would have avoided. A mechanism that is pleasant to use is not evidence that the concurrency the process actually requires has been modeled — the same *Process Before Mechanism* principle this document opens with.

### Ordering
A process may impose ordering constraints on some activities without requiring a total order over all activities. Two activities may need to occur in a particular order because one depends on the result of another, while other activities are independent and may proceed without ordering constraints. The existence of a process therefore does not imply a single linear execution sequence.

An implementation that serializes all activities may be correct, but serialization is an implementation choice unless the process itself requires it — unnecessary ordering can introduce unnecessary coordination, contention, and failure dependencies.

### Coordination
A process may require coordination among participants, but coordination does not prescribe a particular mechanism. Coordination may be achieved through direct interaction, state, ownership, scheduling, messages, events, agreements, or other means.

A process should first establish which participant must know what, which participant must decide what, which state must be consistent, which actions depend on others, which outcomes must be observed, and which actions may proceed independently. Only after these requirements are understood should an implementation mechanism be selected — this prevents a mechanism from creating coordination requirements that the process itself does not need.

### Events
An event can represent a fact that has occurred and make that fact available to other participants or processes, without the producer needing to know which processes will consume it. The act of emitting an event is therefore not, by itself, a command to a known consumer or a continuation of the originating process. This is what separates an event from a direct command.

An event is not inherently a continuation point of the process that emitted it. A process may emit an event and continue independently, or may complete while another independent process later reacts to the fact. A receiving process does not become a continuation, sub-process, or participant of the originating process merely because it reacts to the event.

For example, the fact that an order has reached a final paid state may be relevant to accounting, fulfillment, notification, analytics, or other processes; the process responsible for recording the order does not need to know how any of those processes operate, and a receiving process does not become part of the originating process merely because it reacts to the event. Events can therefore support independent processes without requiring the originating process to model all downstream behavior. The representation of an event — a message, record, callback, broker, log, or another mechanism — is an implementation concern unless the representation itself is part of the domain.

The effect of handling an event on the originating process is likewise not an intrinsic property of Event. An event-handling mechanism may allow the originating process to continue independently, or it may temporarily or conditionally affect its continuation. For example, a browser may dispatch an event to a handler that can prevent or alter some subsequent behavior. That blocking or alteration is a property of the dispatch and handling rules, not a defining property of Event itself. The behavior of an Event Handler therefore belongs to the rules of the mechanism or system in which the event is handled, rather than to the concept of Event alone.

### Asynchrony
Asynchrony should be understood as a relationship between the progression and waiting of activities, not as the presence of a particular programming-language construct. A process can be asynchronous when one participant can continue without waiting for another activity to complete, or when continuation can occur independently at a later point — this does not require a particular programming model such as `async/await`.

Conversely, using an asynchronous programming primitive does not by itself establish the conceptual structure of an asynchronous process; the primitive is an implementation representation. This distinction matters because programming-language terminology can create an overly narrow mental model of a broader system concept.

### Observation
A process can be observed from different perspectives. An observation describes what is relevant from the position and purpose of the observer, so different observers may identify different aspects of the same ongoing process. Observation is useful for understanding a process, but it should not be confused with the basis on which the process itself must be designed — a description of what can be observed from one position is not necessarily a definition of the process, and a property of a process as perceived by a particular participant should not automatically be treated as an intrinsic property independent of context.

What is typically observed is a process instance — one particular enactment — rather than the complete process model described in *Process Definition and Process Instance* above. An observer's account of "the process" is therefore often, more precisely, an account of one instance, or a partial view assembled from several. This does not make the underlying process observer-relative in every respect: the fact that a process admits multiple valid observations does not mean it has no structure independent of any observation. Observation affects what is relevant to a given observer at a given position; it does not mean reality has no structure that exists independently of that observation — different observations may reveal different, genuinely real, aspects of the same process, rather than each observer being free to define the process as anything they choose.

This distinction is relevant to architectural concepts such as modularity, cohesion, coupling, boundaries, and decomposition, which may depend on the question being answered, the concern being addressed, and the relationships that matter to the decision. The existence of multiple valid observations does not mean every decomposition is equally useful — it means the basis of the decomposition must be made explicit.

#### Modeling and Observation Form a Cycle, Not Two Separated Phases
Modeling and observation are not two strictly separated phases where modeling never asks what observation asks, or vice versa. A part is typically proposed first in whatever shape is simplest to record — a `username` field placed inside a `User` model, for instance — and only afterward examined: does this field's validation, versioning, or meaning actually vary independently of the concept currently holding it? If the observation surfaces such independence, the model is revised, and the revised model is itself later re-examined the same way. Modeling and observation are therefore a cycle that repeats over a model's life, not a one-time handoff from a design phase to a review phase.

Within that cycle, the two directions of questioning stay distinct even as they alternate. At development time, the question is not "does this boundary feel cohesive to someone?" but "how should this be structured so that the least coupling of any kind results?" — a question about the artifact being built, independent of any particular observer's perspective on it. At observation time, once a boundary already exists, a different question becomes available: for what concern, and for whom, does this boundary hold up or fail to? This second question is what turns an unfalsifiable claim like "this module has high cohesion" — which names no concern to check it against, and so cannot be shown wrong — into a checkable one: "this boundary was drawn for this concern, for this observer." The second form can be shown wrong; the first cannot, which is precisely why it is not useful as a design criterion, only as a prompt to ask the more specific question. See [Modeling → Domain Decomposition over Aggregate-Root Modeling](./modeling.md#domain-decomposition-over-aggregate-root-modeling) for a worked instance of this cycle, and [System → Responsibility](./system.md#system) for the corresponding claim stated as a property of System rather than of Process.

#### Discussion

##### Unresolved questions
1. Whether Observation should remain a topic within Process, or become a broader concept applicable to System, Model, and other entities as well.

### Feedback and Process
A process does not necessarily progress as a one-way chain from input to outcome. Its activities and outcomes may affect participants, the surrounding environment, or other processes, and those changes may subsequently influence the continuation, repetition, or future instances of the process.

This feedback is not merely an implementation detail. It may be part of the behavior that must be understood when modeling the process. A result of one process may become information or a condition that changes how the same process continues, how another process behaves, or whether a new instance is initiated.

Feedback also does not imply that the process contains a literal loop in its implementation. The effect may cross participants, systems, or process boundaries before influencing a later activity or instance.

This relationship makes Process inherently open to information from its environment: the process may change its future progression in response to what its previous activities or outcomes have caused or revealed.

### Process and System
A System and a Process are related but distinct concepts. A System is a bounded set of interacting elements whose behavior and constraints can be considered as a whole; a Process describes progression, interaction, or change that may occur within or across such a system. A process may involve multiple systems, and a system may contain multiple processes; a process may also cross a system boundary when the participants required to enact it belong to different systems.

Process should therefore not be defined as merely an internal operation of a System, nor should System be defined as merely a collection of Processes. The relationship is better understood through participation and context: a process may occur within one system, may span several systems at once, or may be examined using a system boundary that differs from the one an observer initially assumed — but a process is never meaningfully evaluated with *no* system context at all. Removing every system boundary from consideration does not make a process context-free; it makes it unanalyzable, for the same reason `system.md` gives for why a process needs a system: without a system to provide scope, boundary, and purpose, a progression of activities cannot be reasoned about or designed.

The detailed definition of System belongs to `system.md`, which keeps only what is specific to System's own perspective on this relationship (a system without processes is a heap, not a system; a system is defined by its processes as much as by its elements).

This does not mean that Process is subordinate to a particular fixed System boundary. The relevant system context may consist of one system, multiple systems, an environment, or another analytical boundary selected for the purpose of the analysis. A process can therefore be understood before the final system boundaries involved in its realization have been fully determined, while still requiring system context to be meaningfully analyzed.

#### Discussion

##### Rationale and alternatives
- **Keep Process defined inline in `system.md` (formerly the settled position; now superseded).** `system.md` previously rejected a standalone Process document with a specific argument: "Process cannot be defined without reference to System. A standalone Process document would either duplicate System's definition or silently depend on it, creating the same circular dependency problem this document exists to prevent." That argument is correct about *symmetric* duplication, but this document resolves it by making the dependency asymmetric and one-directional instead: `system.md` defines System and keeps only the System-specific half of the Process↔System relationship; this document defines Process in full, including the Process-specific half of that same relationship. Neither document re-derives the other's core definition. As of this revision, `system.md` has been updated accordingly — its own `### Process` section is now a short pointer here, and its Rationale and Alternatives entry now records this reversal explicitly rather than silently.
- **Define Process as a sub-concept under Protocol (rejected, inherited from `system.md`).** Protocol governs processes, but Process is not a sub-concept of Protocol — processes exist whether or not they are governed by protocols, and Process is a foundational concept that Protocol depends on, not the reverse. `protocol.md`'s own chain — "System → contains → Processes → governed by → Protocols" — is consistent with this document as long as "contains" is read as "provides context for" rather than "cannot exist independent of any system," which is the reading this document adopts above.

##### Unresolved questions
1. Whether the asymmetric-dependency approach above actually eliminates the circularity `system.md` originally warned about, or merely relocates it — this is a real risk, not a resolved one, and both documents now need to stay in sync as either one changes.
2. `system.md` still derives System's own existence from Process ("a system without processes is not a system... the interactions — which are processes — are what make the collection a system"). This document, symmetrically, no longer derives Process's meaning from a fixed System boundary. Whether this residual asymmetry is intentional and defensible, or whether `system.md`'s phrasing should be loosened to avoid making Process a hidden precondition for System's existence (mirroring what this document already avoids in the other direction), is not resolved here and would require a corresponding edit to `system.md` if pursued.

### Process and Structure
Structure describes the capabilities and constraints exposed and enforced by a system or other modeled entity — see [System → Structure](./system.md#structure) for the full treatment of why these two are inseparable rather than independent properties. Process describes how activities, interactions, and changes may progress within the possibilities and constraints provided by that structure. A process therefore operates in relation to structure, but structure does not dictate one unique process — the same structural capability may support multiple processes, and a process may require capabilities distributed across multiple structural boundaries.

This distinction prevents process design from being reduced to the existing organization of implementation components. A process may reveal that a current structure imposes unnecessary constraints, in which case changing the structure may be preferable to adding more coordination mechanisms to the process.

### Process and Boundary
A process boundary identifies which activities, interactions, participants, or states are being considered as part of one conceptual process. The boundary should be determined by the intent and relationships that make the activities meaningfully related, rather than by implementation boundaries alone — a process boundary does not necessarily correspond to a function, a class, a module, a service, a server, a database transaction, a request, a thread, or a deployment unit. Implementation boundaries may coincide with process boundaries, but this coincidence must be justified rather than assumed.

### Process Composition
Composition should not be inferred merely from the presence of several activities that happen to occur together, in sequence, or in reaction to one another. A process may contain many activities without any of them constituting an independently meaningful process in its own right. A sub-process becomes a useful, separately-nameable concept when it has a sufficiently independent intent, boundary, responsibility, outcome, or relationship to other processes to justify treating it as its own process — not merely because it can be pointed to as a distinguishable step.

A process may contain or depend upon other processes, and composition does not require the composed processes to lose their independent identity. A higher-level process may request another process to perform a task and use its outcome without taking ownership of every activity performed by that process. This allows processes to be composed through explicit relationships rather than by merging their internal behavior, and it makes it possible for independent processes to react to a shared fact without becoming a single process.

Composition includes nesting: a process may contain sub-processes, and a sub-process may itself contain further sub-processes, to any depth. A surgical operation contains the anesthesia-induction process, the incision process, the tissue-repair process, and the recovery-monitoring process — each of which contains its own sub-processes. A software request-handling pipeline contains authentication, authorization, validation, business logic, and response-serialization processes. Nesting is not limited to a fixed depth; the appropriate level of analysis depends on the decision being made.

#### Discussion

##### Unresolved questions
1. Whether Memar should eventually develop a more formal treatment of process composition — how processes combine, constrain, or interfere with one another.

### Process and Workflow
A **Workflow** is one possible representation or organization of a process, typically emphasizing the activities, transitions, responsibilities, and ordering used to guide its execution. Not every process is a workflow, and a process does not become a workflow merely because it can be represented as one.

A workflow may therefore be a useful representation of a process without becoming the definition of that process. The distinction follows the same concept-before-representation principle used throughout this document: the process is the subject being understood, while a workflow is one possible way of describing or directing its enactment.

### Process and Implementation
Implementation is one representation of a process, not the process itself. A process may be implemented using different technologies, execution models, deployment structures, or programming paradigms while preserving the same conceptual intent and relevant behavior. Conversely, two implementations that look similar at the code level may represent different processes if their intent, constraints, participants, or outcomes differ.

The implementation should be derived from the process model rather than used as the primary definition of the process. This does not make implementation constraints irrelevant — they may expose real limitations that must be incorporated into the final design — but they should not be mistaken for the conceptual definition of the process.

### Mechanisms Are Not Obligations
A mechanism useful in one process may be unnecessary in another process with superficially similar requirements, even in domains commonly considered sensitive or technically difficult, including financial and distributed systems. A financial process may not require a lock merely because multiple operations concern accounts — it may be possible to partition responsibility by account, route work to an execution owner, serialize work through scheduling, or otherwise structure the process so the relevant invariant is maintained without a shared lock. Likewise, a process involving an external service may not require a Saga merely because a database transaction cannot span the external boundary; the appropriate design depends on the actual process, its outcomes, its failure semantics, and the guarantees required by its participants.

### Process as a Basis for Architectural Decisions
A process can provide the context required to evaluate architectural decisions. Questions about modularity, ownership, coordination, communication, persistence, scheduling, concurrency, and recovery become more precise when the process that motivates the decision is explicit. Instead of asking *"should these components be coupled?"* one can ask *"which process requires these components to interact, what information must cross the boundary, and which relationships are actually necessary for that process?"* Instead of asking *"where should the lock be?"* one can ask *"which invariant must hold during this process, which participants can modify the relevant state, and can ownership or scheduling eliminate the need for shared concurrent access?"* Instead of asking *"should this failure trigger rollback?"* one can ask *"what does failure mean in this process, which effects remain valid, and what outcomes are available after the failure?"*

The process does not automatically answer these questions, but it gives them a meaningful context.

### Process Modeling
A process model should describe the aspects necessary to understand the process without prematurely committing to an implementation representation. Depending on the process, a useful model may identify its intent, participants, relevant activities and interactions, relevant state, meaningful transitions, constraints and invariants, dependencies, possible outcomes, failure conditions, cancellation conditions, continuation possibilities, concurrency relationships, ordering requirements, ownership or responsibility, and relevant observations.

Not every process requires all of these elements. The model should be driven by what must be understood about the process rather than by a fixed template, because forcing every process into the same representation can introduce distinctions that do not exist in the domain or hide distinctions that do.

### Relationship to Other Concepts
Process is closely related to many foundational concepts, but those concepts retain their own definitions:

- **System** provides a context within which processes may occur and with which processes may interact. [System → Responsibility](./system.md#system) defines what it means for a part's boundary within a larger System to be coherent, a question this document's own Observation topic also depends on.
- **Structure** provides capabilities and constraints relevant to what processes can do.
- **State** represents conditions relevant to the progression of a process.
- **Event** can communicate that something relevant has occurred without requiring the producer to know the consumers.
- **Error** describes a condition requiring its own conceptual treatment; within a process, an error may be a cause or expression of failure.
- **Concurrency** describes relationships between simultaneously or independently progressing activities.
- **Protocol** describes rules governing interactions between participants; a process may use protocols without being identical to them.
- **Module** provides a structural boundary for organizing capabilities or responsibilities; it is not inherently a process boundary. See [Modularity](./modularity.md) for the full treatment, including why a process boundary and a Module boundary must each be justified on its own terms rather than assumed to coincide.
- **Architecture** concerns the organization of a system and its relationships; processes provide important behavioral context for architectural decisions.
- **Implementation** realizes a process through concrete mechanisms and technologies.

The detailed definitions of these concepts belong to their respective documents. Process should remain the point at which their behavioral relationships can be understood.

#### Discussion

##### Unresolved questions
1. Whether Process should distinguish between internal activities and interactions with external participants, and if so, whether that distinction belongs in *Activities and Interactions* rather than here.
2. Whether scheduling should remain a topic within Process or become a separate foundational concept — this would also be where a formal Worker/CPU-core registration and identity model belongs, if the informal treatment under Concurrency needs to become more than illustrative.
3. Whether the distinction between Process and Protocol requires dedicated documentation beyond their current relationship.
4. Whether Workflow requires any further conceptual treatment beyond its role as a possible process representation.

## Results
Insufficient time has passed since this document was adopted to report real, observed outcomes from its use. This section will be filled in once there is such experience to draw on.

## Discussion

### Drawbacks
This document is large, covering a number of adjacent concepts (Concurrency, Coordination, Events, Asynchrony) that could each eventually justify their own document — this was a known and accepted risk from the outset. Extracting Process into its own document also reintroduces the drift risk `system.md`'s original Rationale and Alternatives warned about: two documents now each describe the Process↔System relationship from their own side, and each future change to either concept needs a corresponding check against the other.

### Rationale and alternatives
See *Process and System → Discussion → Rationale and alternatives* above for the central decision (standalone document vs. inline in `system.md`) and *Definition → Discussion → Rationale and alternatives* for the removal of "sequence" from the definition; both are topic-specific enough that they are documented at the topic level rather than repeated here.

### Prior art
The concept of process as distinct from sequence is foundational to process philosophy (Whitehead, *Process and Reality*, 1929) and to process algebra (CSP, π-calculus), both of which model progression, concurrency, and interaction without requiring a single total order. Business process management (BPM) and workflow literature address process composition and boundary questions from a more applied, organizational angle. The distinction between failure and rollback, and between concurrency and locking, draws on established distributed-systems literature on Sagas, compensating transactions, optimistic concurrency, and distributed leases — the latter is discussed directly in the public exchange that motivated this document, referencing Brendan Burns's *Designing Distributed Systems* on the difference between a lock as a permanent grant versus a lease that must be renewed and can silently expire.

### Unresolved questions
Topic-specific unresolved questions are recorded under their own topic's Discussion above, rather than repeated here.

### Future possibilities
If Concurrency, Coordination, or Events grow enough conceptual weight of their own — enough to be reasoned about independently of Process rather than only in relation to it — each may eventually justify a dedicated document, at which point this document would shrink to reference them rather than define them in full, following the same source-of-truth pattern this document itself now establishes relative to `system.md`.
