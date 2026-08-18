---
Title: "Agency"
Status: Draft
Start Date: 2026-08-15
ID: 496330
---

# Agency

## Abstract
Agency is modeled here as a fundamental concept for understanding systems that can act, make decisions, assume responsibilities, or act on behalf of another system. AI Agent is treated as one manifestation of Agency, not as its definition — Agent is an older and more general concept than Artificial Intelligence, and reducing it to AI discards accumulated knowledge about delegation, responsibility, authority, representation, decision-making, trust, and contracts. The document's central claim is that most problems attributed to AI Agents — ambiguous delegation, missing context, undocumented knowledge, unclear acceptance criteria — predate AI and are not solved by changing tools; they are solved by modeling Agency correctly. `Agent` and `agent_for` are treated as relational: a System occupies the Agent or Principal position within a relationship rather than becoming a new kind of entity by doing so. Delegation, Responsibility, Authority, Capability, Context, Knowledge, Trust, and Accountability are modeled as distinct, non-substitutable concepts whose conflation is identified as a recurring source of failure. The document closes with open questions — most centrally, whether Agency is a property, a capability, or a relational condition, and whether Agent is fundamentally a role rather than a type — that are deliberately left unresolved rather than forced to a premature answer.

## Introduction

### Motivation
This document defines and models **Agency** as a fundamental concept for understanding systems that can act, make decisions, assume responsibilities, or act on behalf of another system.

The purpose of this document is not to define AI agents specifically. AI agents are only one possible manifestation of agency.

The broader purpose is to establish a conceptual foundation that allows human, organizational, software, artificial-intelligence, and hybrid forms of agency to be understood through a common model.

This distinction is important because the current ecosystem frequently treats the term *Agent* as if it were a concept introduced by Artificial Intelligence. It is not.

Agent is an older and more general concept. AI Agent is a specialization or manifestation within that broader conceptual space.

Reducing the concept to AI unnecessarily discards accumulated knowledge about delegation, responsibility, authority, representation, decision-making, trust, contracts, and interaction between systems.

Therefore:

> **Agency should be modeled before AI Agent.**

### Methodology
This document follows the general modeling principles of Memar:
- Definitions take precedence over terminology.
- Concepts should be distinguished from their representations.
- Relationships should not be modeled as entities merely because they have names.
- Properties should not be confused with entities.
- Domain structure should be discovered independently from implementation structure.
- Industry terminology is not authoritative when it conflicts with a clearer conceptual model.
- Historical knowledge should not be discarded merely because a newer technology introduces new terminology.

Consistent with the first principle above — definitions take precedence over terminology — this document is titled `agency.md` rather than `agent.md`. An earlier draft of this work was organized around Agent as the primitive concept, with Agency, Delegation, Authority, and the rest introduced as things an Agent needs. That ordering was reconsidered once it became clear that almost none of those surrounding concepts are intrinsic properties of an Agent; they are properties of Agency itself — answers to the question "what does a System need in order to be able to act, whether or not that action is on behalf of another System?" Agent, by contrast, turned out to name a *position* a System occupies (see [The `agent_for` Relationship](#the-agent_for-relationship)), not an independent primitive. Naming the document after the property rather than the position follows the same pattern already used elsewhere in Memar, where a document is named after a principle rather than an artifact (e.g. Modularity rather than Module) once that principle is recognized as the more fundamental concept.

The following scope statement follows the same modeling principles.

**This document covers:**

- Agency
- Agent
- Principal
- The `agent_for` relationship
- Delegation
- Responsibility
- Authority
- Goals and purpose
- Capability
- Constraints
- Context
- Knowledge
- Execution
- Decision-making
- Trust
- Contracts
- Accountability
- Human agency
- Organizational agency
- Software agency
- AI agency
- Hybrid agency
- Multi-agent relationships
- The relationship between agency and autonomy

**This document does not attempt to define:**

- a particular AI architecture,
- a particular agent framework,
- prompt engineering,
- model architectures,
- LLM implementation details,
- a specific software implementation of agents,
- or a particular organizational methodology.

Those may depend on Agency, but they do not define Agency.

## Explanation

### The Central Distinction
A recurring source of confusion is treating the following concepts as interchangeable:

- System
- Agent
- Agency
- Role
- Autonomy
- Delegation

They are related, but they are not equivalent.

A **System** is an entity or organized whole with some boundary, capabilities, behavior, and constraints.

**Agency** concerns the capacity or condition through which a system can act.

An **Agent** identifies a system participating in an agentive relationship or otherwise exhibiting agency.

A **Role** describes a position a system occupies within a particular relationship or context.

**Delegation** describes the transfer or assignment of responsibility and/or authority from one participant to another.

**Autonomy** concerns the degree to which a system can determine or execute its actions without direct control over each individual action.

These distinctions must remain explicit.

### What Is Agency?
A preliminary definition for Memar is:

> **Agency is the capacity or condition of a system to act intentionally toward objectives within a boundary of capabilities, knowledge, authority, and constraints.**

This definition is deliberately broader than "acting on behalf of another."

A system may exhibit agency without having been explicitly delegated a responsibility by another system.

For example, a human may pursue a self-generated objective without acting on behalf of another person or organization.

Likewise, an autonomous system may pursue an objective without receiving an individual instruction for every action it takes.

Therefore, delegation is not a necessary condition for all forms of agency.

However, delegation becomes fundamental when agency exists **on behalf of another system**.

This distinction allows both intrinsic and relational manifestations of agency to be represented without forcing one to replace the other.

#### Agency as a Property of Systems
Agency can also be considered independently of delegation.

A system may possess or exhibit agency even when no external Principal is present.

This allows the model to represent:

```text
System
   │
   └── Agency
```

without requiring:

```text
Principal
   │
   └── Agent
```

The two structures are compatible.

This distinction prevents delegated agency from being treated as the only possible form of agency.

#### Agency as a Relationship-Enabled Property
At the same time, when one System acts on behalf of another, the agentive relation establishes a specific context of Agency.

Therefore:

```text
Intrinsic Agency
```

and:

```text
Relational / Delegated Agency
```

should not necessarily be treated as mutually exclusive types.

A delegated Agent may possess its own Agency and exercise it in fulfillment of another System's responsibility.

This is a central principle of the model:

> **An Agent may receive responsibility without receiving an algorithm.**

#### Discussion

##### Unresolved questions
- **Is Agency a property, capability, or condition?** The current model uses all three perspectives because each explains a different aspect. A future definition should determine whether one is primary.
- **Is Agency intrinsic, relational, or both?** Current reasoning suggests both forms are valid. The model should determine whether they share a common primitive.
- **Does self-directed action ever fully escape delegation, or does it only push the Principal inward?** A human pursuing a self-generated objective is used above as the paradigm case of intrinsic agency — agency with no external Principal. But the same act can be redescribed as a System (the person, taken as a whole) delegating to one of its own internal Systems (a motivational subsystem, a habit, a decision made by an earlier version of the same person) — in which case it is delegated agency after all, just with the Principal and Agent both inside the same boundary. This is a real open question about where the boundary of "external" is drawn, not a settled matter, and it should not be resolved implicitly by which example happens to be chosen. It connects to [Nested Agency](#nested-agency) and to the recursive structure described there.

### Agency Is Not the Same as Autonomy
Agency and autonomy are related but distinct. A system can have agency while operating under substantial constraints. For example, a contractor may have responsibility for constructing a building while being constrained by:
- a contract,
- building regulations,
- budget,
- schedule,
- safety requirements,
- architectural specifications,
- and decisions made by the client.

The contractor can still determine many aspects of execution.

Therefore:

> **Delegated responsibility does not imply direct control over execution.**

Conversely, autonomy does not by itself establish agency.

A system may perform autonomous internal operations without those operations constituting meaningful agency in the relevant context.

Autonomy is therefore better understood as a characteristic of how agency is exercised rather than as a synonym for agency.

### Agent and Agency
Agency and Agent must not be collapsed into the same concept. Agency describes a capacity, condition, or property of a system. Agent identifies a system participating in an agentive context. A useful conceptual distinction is:

```text
System
   │
   └── exhibits / possesses ──► Agency
```

and, in a relational context:

```text
System A ───── agent_for ─────► System B
```

where the systems occupy different positions in the relationship.

The system acting as the agent may be called the **Agent** in that relationship.

The system on whose behalf it acts may be called the **Principal**.

This means that Agent should not automatically be modeled as a separate kind of entity.

A human does not become a new entity when becoming an Agent.

A software system does not become a new entity when acting as an Agent.

Rather, the same system participates in an agentive relationship or exhibits agency.

### Agent as a Relational Concept
The term Agent is frequently used as though it describes an intrinsic type.

That assumption is not always appropriate.

Consider a human being.

The same human may:

- act independently,
- act on behalf of a customer,
- act on behalf of an organization,
- act as a representative,
- delegate work to another person,
- supervise another Agent,
- or act as Principal in another relationship.

The underlying system has not changed into a different entity.

Its **position in a relationship** has changed.

Therefore, in a graph-oriented model, Agent is often better understood as a role emerging from a relationship rather than as a separate node.

For example:

```text
System A ───── agent_for ─────► System B
```

Here:

- `System A` may occupy the Agent role.
- `System B` may occupy the Principal role.
- `agent_for` is the relationship.
- Neither Agent nor Principal needs to be modeled as an additional node merely because those terms describe the endpoints' roles.

This distinction is important because modeling every named role as a node can obscure the actual domain structure.

#### Agency and Roles
Roles should be distinguished from entities.

A person may occupy different roles in different contexts.

For example:

```text
Person
  │
  ├── Agent for Customer
  ├── Principal for Contractor
  └── Member of Organization
```

The person remains the same system.

The relationships change.

This prevents organizational models from confusing:

> who something is

with:

> what position it currently occupies.

The same principle applies to software and organizations.

#### Discussion

##### Unresolved questions
- **Is Agent fundamentally a role?** Current modeling strongly suggests that Agent is often a relational role rather than an independent entity type. However, some contexts may justify using Agent as a conceptual entity. This should be established by modeling rather than terminology. A related, unresolved sub-question: if a System can exhibit intrinsic Agency with no Principal at all (see [What Is Agency?](#what-is-agency)), is "Agent" still the right name for that System when it is acting on its own behalf, or does the word Agent only ever apply once a relationship exists — leaving intrinsic agency-exhibiting Systems simply as Systems, never as Agents, until they enter a relationship?

### The `agent_for` Relationship

`agent_for` is a relationship between systems.

It should therefore be modeled as an edge rather than as a node unless a separate requirement establishes that the relationship itself must be represented as an entity.

Conceptually:

```text
Principal System
       │
       │ agent_for
       ▼
Agent System
```

The direction of the relationship must be defined carefully.

The relationship expresses that one system acts on behalf of another.

For example:

```text
Customer ───── agent_for ───── Contractor
```

can represent a contractor acting on behalf of a customer, depending on the chosen direction convention.

Because directional semantics matter, the final graph representation must establish the direction explicitly rather than relying on the English phrase alone.

The important point is conceptual:

> **Agent-for-ness is a relationship, not an additional entity that must exist between the systems.**

#### A General Model of Agency
The current conceptual model can be summarized as:

```text
                         SYSTEM
                           │
                     exhibits / has
                           │
                           ▼
                        AGENCY
                           │
          ┌────────────────┼────────────────┐
          │                │                │
       Purpose         Capability        Knowledge
          │                │                │
          └────────────────┼────────────────┘
                           │
                      enables action
                           │
                           ▼
                         AGENT
                           │
                within a relationship
                           │
                           ▼
                 ┌─────────────────┐
                 │   agent_for     │
                 └─────────────────┘
                           │
                           ▼
                       PRINCIPAL
```

The diagram is conceptual rather than a final graph schema.

In particular, `Agent` and `Principal` may represent roles occupied by Systems rather than independent node types.

#### A More Precise Relational Model
A more graph-oriented representation is:

```text
System A
   │
   │ agent_for
   ▼
System B
```

where the interpretation of the endpoints depends on the relation.

For example:

```text
System A = Principal
System B = Agent
```

The same System B may simultaneously participate in another relationship:

```text
System B
   │
   │ agent_for
   ▼
System C
```

In that second relationship:

```text
System B = Principal
System C = Agent
```

Therefore:

> **Principal and Agent are relational positions, while System is the underlying entity.**

This distinction should be preserved unless future modeling demonstrates that an independent Agent concept is necessary.

#### Discussion

##### Rationale and alternatives

- **Modeling `agent_for` as a node, with Agent and Principal as its endpoints (an earlier draft; not chosen)**: an earlier pass at this model treated Agent and Principal as intrinsic entity types connected by the relationship, and separately treated the relationship as something that might need to be modeled as its own entity because it carries qualifiers (a status, a scope, a time bound). Both moves were reconsidered. If `A ── agent_for ──► B` can be represented directly as a graph edge, there is no reason to create an intermediate `AgentFor` node merely because the relationship has a name — the same reasoning that keeps other named relationships in Memar as edges rather than nodes. And once `agent_for` is an edge rather than a node, Agent and Principal stop being types a System belongs to and become the labels for the two endpoints of that edge — which is what forced the reconsideration described in [Agent as a Relational Concept](#agent-as-a-relational-concept) and in [The Central Distinction](#the-central-distinction).
- **Treating Agent as the primitive concept of this document (rejected — see also [Methodology](#methodology))**: once `agent_for` is understood as an edge between two Systems, Agent is no longer a natural candidate for the document's primitive concept, since it names a position on an edge rather than a node. The candidates for primitive status become Agency, System, and Relation instead — which is the reasoning that produced this document's own title.

##### Unresolved questions

- **What is the exact semantic direction of `agent_for`?** The relationship must be formalized so that its graph direction cannot be misunderstood — including whether the direction should read Principal → Agent or Agent → Principal, since natural-language phrasing ("A is agent for B") does not settle this by itself and different direction conventions have been used informally in early drafts of this model.

### Principal

A **Principal** is a system on whose behalf another system acts.

Principal is therefore relational.

A system is not necessarily a Principal by intrinsic type.

A human can be a Principal.

An organization can be a Principal.

A software system can potentially be a Principal.

Another Agent can also be a Principal when it delegates work to a subordinate Agent.

This permits nested agency:

```text
System A
   │
   └── agent_for ──► System B
                       │
                       └── agent_for ──► System C
```

The resulting structure must not be interpreted as requiring only human principals.

The model is intentionally system-general.

### Nested Agency

An Agent may itself be a system capable of delegating responsibility to another Agent.

Therefore:

```text
Principal
    │
    └── Agent A
            │
            └── Agent B
```

is not conceptually problematic.

Agent A can simultaneously be:

- an Agent with respect to its Principal,
- a Principal with respect to Agent B,
- and a System with respect to its own internal structure.

This is one reason why Agent should not be modeled as a special immutable entity type.

The same system can occupy multiple positions simultaneously.

#### Multi-Agent Systems

Multiple Agents may cooperate within a shared system.

A multi-agent system can contain:

- multiple human Agents,
- multiple software Agents,
- AI Agents,
- organizational Agents,
- or combinations of these.

Each Agent may have:

- different responsibilities,
- different capabilities,
- different authority,
- different knowledge,
- different constraints,
- and different relationships.

The system should therefore be modeled as a network of relationships rather than as a collection of identical "agents."

For example:

```text
Principal
   │
   ├── agent_for ──► Agent A
   │                    │
   │                    └── agent_for ──► Agent B
   │
   └── agent_for ──► Agent C
```

The graph expresses the structure more directly than a flat list of Agents.

#### Agency and Internal Systems

An Agent may itself contain multiple internal systems.

For example:

```text
AI Agent
│
├── Model
├── Memory
├── Tool System
├── Policy System
├── Knowledge System
├── Planner
└── Executor
```

Likewise:

```text
Organization
│
├── People
├── Processes
├── Policies
├── Knowledge
├── Software
└── Infrastructure
```

Both can exhibit Agency at different levels.

The existence of internal systems does not eliminate the Agency of the enclosing system.

This creates a recursive structure:

```text
System
   └── Agent
         └── System
               └── Agent
```

Such recursion should be considered normal rather than exceptional.

### Intrinsic and Delegated Agency

The distinction between intrinsic and delegated agency is useful, but it should not be interpreted as two fundamentally different kinds of agency.

#### Intrinsic agency

A system acts toward objectives without another system assigning that particular responsibility.

Examples include a human pursuing a personal objective or an autonomous system pursuing an internally established objective.

#### Delegated agency

A system acts on behalf of another system.

The principal establishes some responsibility, objective, authority, or expectation, while the Agent determines at least part of the execution.

The two can coexist.

A delegated Agent may exercise substantial autonomy in deciding how to fulfill the delegated responsibility.

Therefore:

> **Delegation establishes a relationship; it does not prescribe every action.**

### Agency in Process Execution
Agency is not limited to situations in which one System delegates work to another System through a Principal–Agent relationship. A process can also depend on a System being capable of taking responsibility for a bounded portion of the process progression and determining how that responsibility is executed. See [Process → Concurrency](./process.md#concurrency) for the Process-side treatment this topic supplies the Agency grounding for — in particular, the Worker/CPU-core distinction and the escalating decision chain there (shared state → shared mutable state → shared invariant → common ownership → partitionable responsibility → scheduling → synchronization → locking) are a Concurrency-specific instance of the general responsibility-before-synchronization principle this topic states below, under *Agency Before Synchronization*.

This distinction is important because the Agent relationship used to describe representation (`agent_for`) is not the only relationship through which Agency becomes relevant. A process may assign execution responsibility to a System without that System becoming a representative of the process, a domain entity, or a Principal's Agent in the narrower representational sense.

For example, a process may require that, at a particular time, one execution Agent is responsible for advancing the state associated with Account `123`:

```text
Account 123
     │
     │ execution responsibility
     ▼
Agent 847
```

The Account is a domain entity. Agent 847 is an acting system. The assignment between them is a relationship; it does not imply that an `Account Service` is the permanent owner of all Account processing, nor that the Account itself is an Agent.

The assignment may later change:

```text
Account 123
     │
     ├── responsibility → Agent 847
     │
     └── responsibility → Agent 912   (after reassignment)
```

The important property is not the identity of the particular Agent but the existence of a well-defined responsibility boundary at the time the process is progressing. This makes Agency useful for modeling execution independently of the mechanism used to realize it.

#### Execution Agent
An **Execution Agent** is an Agent that assumes responsibility for advancing some bounded part of a Process. The term describes a use of Agency, not a new entity type.

An Execution Agent may be represented by many different mechanisms, including a Worker, Actor, process, thread, service instance, device, human operator, or another system. None of those representations is intrinsically an Agent merely because it has the corresponding implementation name. See [Process → Concurrency](./process.md#concurrency) for Worker's own treatment there, including its distinction from a physical CPU core.

Conversely, a Worker can be an expression of Agency when it is not merely an execution primitive but a bounded acting unit with an identifiable responsibility, relevant capabilities, available knowledge, and authority to perform the work assigned to it.

This gives a useful conceptual distinction:

```text
Agency
   ↓
Agent
   ↓
Execution responsibility
   ↓
Possible implementation representations
   ├── Worker
   ├── Actor
   ├── Process
   ├── Thread
   ├── Service instance
   └── other execution mechanism
```

The list is intentionally not a taxonomy of Agents. It is a list of possible representations of an Agent's execution role.

#### Agency and Ownership of Process State
When an Execution Agent is responsible for a portion of a process, the useful question is not simply where the code runs. It is which Agent is responsible for advancing the relevant state and maintaining the invariants that apply to that responsibility.

This distinction matters for Concurrency. If two independent activities operate on different independently responsible state, they may progress concurrently without requiring coordination merely because they execute at the same time. If two activities can modify the same state under the same invariant, the model should first ask whether responsibility can be partitioned so that one Agent is responsible for that state at a time.

This is not equivalent to saying that every entity must have one permanent Worker. Responsibility may be assigned temporarily, partitioned, migrated, replicated, or otherwise structured according to the process requirements. The important point is that the assignment itself is modeled before the execution mechanism is chosen.

#### Dynamic Assignment
Execution responsibility does not need to be permanently attached to an Agent.

A system may increase or decrease the number of Execution Agents while preserving the conceptual Process. The assignment of responsibility can therefore change independently of the identity of the domain entities being processed.

For a partitionable process, a mapping mechanism such as Consistent Hashing may be used to map process-relevant identities or partitions to available Agents. The mapping is an implementation mechanism; the underlying model is the allocation of responsibility among Agents.

For example:

```text
Account ID / Partition Key
          │
          ▼
   Responsibility Map
      │           │
      ▼           ▼
  Agent 847    Agent 912
```

If the number of Agents changes, the mapping can be recalculated with limited reassignment rather than requiring every Agent to coordinate over every account. This does not make Consistent Hashing a requirement of Agency. It illustrates how an Agency-first model can make scaling and reassignment questions explicit before a particular mechanism is selected.

#### Agency Before Synchronization
When multiple Agents can affect the same process state, synchronization may be necessary. But synchronization should be considered only after the responsibility structure has been examined.

The conceptual order is:

```text
Process
   ↓
Relevant state and invariants
   ↓
Responsible Agents
   ↓
Responsibility partitioning
   ↓
Required communication and coordination
   ↓
Synchronization mechanisms, if still required
```

This order prevents a lock, queue, mailbox, scheduler, or transactional mechanism from silently becoming the model of responsibility itself.

A Single Writer arrangement, an Actor-style mailbox, or a Worker assigned to a partition can each be useful realizations of this principle. None should be mistaken for the principle itself.

#### Discussion

##### Rationale and alternatives
- **Treating Worker as the primitive execution concept (rejected).** Worker is useful implementation vocabulary, but its meaning varies across runtimes and frameworks. The underlying question is whether an acting system has a bounded execution responsibility. Worker is therefore treated as a possible representation of an Execution Agent rather than the conceptual primitive.
- **Treating Actor as the primitive execution concept (rejected).** Actor Model provides valuable accumulated knowledge about isolated state, communication, and independent execution, but `Actor` carries a particular model of execution. Agency is intentionally broader: an Agent may be human, organizational, software, AI, hybrid, or another acting system, and an execution Agent need not be implemented using the Actor Model.
- **Treating `agent_for` as the relationship for every execution responsibility (rejected).** `agent_for` describes acting on behalf of another System. An Execution Agent may instead be responsible for advancing a process or managing a partition of state without representing another System in that sense. The process model therefore needs a distinct responsibility relationship rather than stretching `agent_for` beyond its meaning.

##### Unresolved questions
1. Whether Memar should eventually give the execution-responsibility relationship a canonical edge name, or keep it expressed through the existing Responsibility concept until the graph model demonstrates a need for a specific relation.
2. Whether Execution Agent should remain descriptive terminology or eventually become a formally defined concept in Process.
3. How responsibility transfer, temporary reassignment, failure takeover, and concurrent replication should be represented without conflating responsibility with implementation ownership.

### Delegation

Delegation is a mechanism through which a system assigns responsibility, authority, or an objective to another system.

Delegation is therefore a fundamental aspect of Agency rather than an independent domain that must necessarily be modeled separately.

A delegation can establish:

- what the Agent is responsible for,
- what authority the Agent receives,
- what boundaries apply,
- what objectives must be achieved,
- what constraints must be respected,
- what information is available,
- and what outcomes are expected.

Delegation does not necessarily specify the execution procedure.

In fact, an Agent that must receive instructions for every individual action has very little meaningful execution autonomy.

A useful conceptual model is:

```text
Principal
   │
   │ delegates responsibility / authority
   ▼
Agent
   │
   │ determines execution
   ▼
Actions
   │
   ▼
Outcome
```

The Principal defines or establishes part of the problem space.

The Agent operates within that space.

#### Discussion

##### Rationale and alternatives

- **A separate `delegation.md` document (considered, then rejected)**: an earlier draft of this work proposed splitting Delegation out into its own document, on the reasoning that Delegation was substantial enough in volume to justify a dedicated file. That reasoning was reconsidered and rejected: volume is not the criterion Memar uses for whether something is an independent Concept. The relevant question is whether Delegation can be defined without first defining Agency — and it cannot. Asking "what is Delegation?" already presupposes a System capable of Agency assigning some of it to another System; the definition is not self-standing. Delegation is therefore modeled as a chapter of Agency rather than as an independent document, at least until some future need demonstrates otherwise.

### Responsibility

Responsibility defines what an Agent is expected to take care of or accomplish.

Responsibility should not be confused with:

- Authority
- Capability
- Accountability
- Action

An Agent may have responsibility without having sufficient authority.

An Agent may have authority without being responsible for a particular outcome.

An Agent may have capability without being responsible for using that capability.

These distinctions matter when designing systems.

A common organizational failure occurs when responsibility is assigned without corresponding authority or capability.

For example:

```text
Responsibility
       +
   insufficient
       │
   Authority
       +
   insufficient
       │
   Capability
       ↓
Failure
```

Agency therefore requires more than merely naming an Agent.

The surrounding conditions of agency must also be coherent.

### Authority

Authority defines the scope within which an Agent is permitted or entitled to make decisions or take actions.

Authority is not equivalent to responsibility.

A system may be responsible for an outcome while requiring escalation before taking certain actions.

Authority can therefore be bounded by:

- domain,
- time,
- resources,
- monetary limits,
- policies,
- safety constraints,
- legal constraints,
- organizational rules,
- or another Principal.

Authority may also be revoked or changed.

Therefore, Agency should account for the temporal and contextual nature of authority.

### Capability

Capability describes what a system is able to do.

Capability is not responsibility.

For example, a software system may be technically capable of deleting data without being authorized or responsible for doing so.

Likewise, an Agent may be responsible for producing a result without possessing all capabilities necessary to accomplish it directly.

This distinction is essential:

```text
Capability ≠ Authority ≠ Responsibility
```

These concepts may interact, but they should not be merged.

A coherent delegation generally requires sufficient alignment between them.

### Goals and Purpose

Agency involves directed action.

Directed action normally requires some notion of purpose, objective, goal, or desired state.

However, these concepts should not automatically be treated as identical.

A Principal may establish a desired outcome.

An Agent may translate that outcome into intermediate goals.

The Agent may then choose actions to achieve those goals.

For example:

```text
Principal
   │
   │ desired outcome
   ▼
Agent
   │
   ├── interprets objective
   ├── establishes intermediate goals
   ├── plans
   └── executes
```

This distinction becomes particularly important for AI systems.

Giving a model a prompt does not necessarily mean that the prompt itself contains the complete executable specification of the Agent's behavior.

The surrounding Agent may use:

- persistent knowledge,
- tools,
- policies,
- context,
- memory,
- feedback,
- and internal procedures.

Therefore, a prompt is not synonymous with Agency.

#### Discussion

##### Unresolved questions

- **What exactly constitutes intentionality?** The definition of Agency in [What Is Agency?](#what-is-agency) rests on a System acting "intentionally toward objectives," and this document uses that phrase as load-bearing without fully defining it. A partial, working answer, offered here without treating it as settled: the chain "Principal's desired outcome → Agent's interpreted objective → intermediate goals → plan → action" (described above) is at minimum a *necessary* structure for intentionality in this model — a System producing behavior with no such chain, however complex the behavior, would not on this account be exhibiting Agency, only behavior (see [Failure of Agency](#failure-of-agency) and the next question below). Whether that chain is also *sufficient* — whether any System that can be described as running it thereby has intentionality, regardless of what is actually happening inside it — is exactly the part that remains open, especially for software and AI systems, and is not resolved by this document.
- **Can a System have Agency without goals?** If goals are intrinsic to Agency, the model must define what counts as a goal. If goals can be externally imposed, the relationship between Agency and Delegation must be clarified.
- **What distinguishes Agency from mere behavior?** Not every System that produces behavior necessarily exhibits Agency. A more rigorous boundary is required than the partial answer offered above.

### Execution

Agency becomes observable through action.

Execution describes how an Agent transforms responsibility, goals, knowledge, capabilities, and constraints into actions and outcomes.

Execution may include:

- interpretation,
- planning,
- decision-making,
- action,
- observation,
- adaptation,
- evaluation,
- and feedback.

The exact mechanisms depend on the Agent.

A human Agent may reason consciously.

An organization may use procedures and committees.

A software Agent may execute algorithms.

An AI Agent may combine a model, tools, memory, policies, and orchestration.

The implementation differs.

The conceptual structure does not necessarily need to differ.

#### Agency Is Not Command Execution

A simplistic model of an Agent is:

```text
Command → Execution → Output
```

A richer model is:

```text
Purpose
   ↓
Responsibility
   ↓
Authority + Constraints
   ↓
Context + Knowledge + Capability
   ↓
Interpretation
   ↓
Planning
   ↓
Decision
   ↓
Execution
   ↓
Observation
   ↓
Evaluation
   ↓
Feedback / Adaptation
   ↓
Outcome
```

This model explains why effective interaction with Agents involves much more than command syntax.

It also explains why AI Agent engineering should not be reduced to prompt construction.

Prompting is one representation mechanism inside a much larger agentive system.

### Decision-Making

Decision-making is a central manifestation of agency.

However, Agency does not require unrestricted decision-making.

An Agent may make decisions within a constrained decision space.

For example:

```text
Authority Boundary
┌──────────────────────────────┐
│        Agent decisions       │
│                              │
│    ┌────────────────────┐    │
│    │ permitted decisions│    │
│    └────────────────────┘    │
│                              │
└──────────────────────────────┘
```

Some decisions may require escalation to the Principal.

Therefore, escalation is not necessarily a failure of agency.

It may be a designed part of the Agent's authority boundary.

### Context

An Agent cannot reliably act without some context relevant to its responsibility.

Context may include:

- current state,
- historical information,
- environmental conditions,
- constraints,
- goals,
- relevant entities,
- relationships,
- previous decisions,
- policies,
- contracts,
- and available knowledge.

Context is not necessarily equivalent to memory.

Memory is one possible mechanism for retaining information.

Context is the information relevant to action at a particular point.

This distinction is especially important when interacting with AI systems.

A request that omits necessary context may produce an apparently reasonable but incorrect result.

The problem is not necessarily the intelligence of the Agent.

The problem may be insufficiently specified agency.

### Knowledge

Knowledge influences what an Agent can understand, decide, and execute.

Knowledge may exist:

- inside the Agent,
- in external systems,
- in organizational documentation,
- in shared repositories,
- in contracts,
- in policies,
- in other Agents,
- or in the environment.

Therefore, knowledge should not be assumed to reside exclusively inside the Agent.

This is particularly important for organizations.

An organization whose important knowledge exists only inside individuals has weak knowledge continuity even if those individuals are highly capable.

The same principle applies to AI Agents.

An AI system may appear highly capable while lacking the domain knowledge required to perform a particular responsibility reliably.

#### Agency and Knowledge Flow

A system's effective Agency depends partly on how knowledge flows between its participants.

A healthy system allows knowledge to move across relevant boundaries.

An unhealthy system allows knowledge to become trapped inside individual Agents or organizational silos.

This can produce:

```text
Agent A
   │
   │ knowledge trapped
   X
Agent B
```

instead of:

```text
Agent A
   │
   │ shared knowledge
   ▼
Knowledge Space
   ▲
   │
Agent B
```

This is one reason Knowledge Management is not merely an administrative concern.

It is part of the infrastructure through which collective Agency operates.

### Agency and Knowledge Management

Many failures attributed to AI Agents are not fundamentally AI problems.

They may be manifestations of weaknesses in:

- Knowledge Management
- responsibility definition,
- delegation,
- documentation,
- organizational modeling,
- communication,
- or development frameworks.

AI can increase the speed at which an organization produces outputs.

It can therefore also increase the speed at which an organization produces poorly understood outputs.

In this sense:

> **AI may reveal weaknesses in organizational knowledge and mental models more clearly than previous tools did.**

This is related to the concept of Cognitive Debt.

Cognitive Debt can emerge when an organization repeatedly obtains answers without developing understanding of why those answers are correct.

The phenomenon is not inherently new.

AI can merely make it more visible and more scalable.

#### Cognitive Debt and Agency

Cognitive Debt can emerge when a system repeatedly accepts outputs without developing sufficient understanding of the reasoning, assumptions, or knowledge behind those outputs.

This is not unique to AI.

AI simply makes it easier to obtain outputs without performing the corresponding cognitive work.

The resulting failure may appear as an AI problem:

> "The AI produced something nobody understands."

But the deeper problem may be:

> "The organization has no mechanism for transferring and preserving understanding."

This connects Agency directly to Knowledge Management.

### Contracts

A Contract establishes expectations between participants.

A contract may define:

- responsibility,
- authority,
- obligations,
- constraints,
- expected outcomes,
- acceptance criteria,
- failure conditions,
- communication requirements,
- or escalation procedures.

A contract does not necessarily need to be a legal document.

Software interfaces, organizational agreements, and machine-readable policies may also establish contractual expectations.

Therefore, contractual structure should be understood conceptually before its representation is selected.

#### Acceptance Criteria

An Agent cannot reliably determine whether it has successfully completed a responsibility if success is undefined.

Acceptance criteria provide a way to establish what constitutes an acceptable outcome.

For example:

```text
Responsibility
      │
      ▼
Expected Outcome
      │
      ▼
Acceptance Criteria
      │
      ▼
Evaluation
```

This is particularly important when delegating work to AI Agents.

A vague request such as:

> "Improve this document."

does not necessarily define:

- what should improve,
- what must remain unchanged,
- what quality means,
- what scope is permitted,
- or how success will be evaluated.

The resulting ambiguity should not automatically be classified as a failure of the Agent.

It may be a failure in delegation or specification.

### Communication

Agency frequently requires communication between systems.

Communication may transfer:

- goals,
- responsibility,
- authority,
- context,
- knowledge,
- feedback,
- results,
- warnings,
- or requests for escalation.

Communication quality therefore affects agency quality.

A poorly specified instruction can produce poor outcomes even when the Agent has sufficient capability.

For example:

> "I will send the files again, but before that we still need to work on the new document."

contains several ambiguities.

A more precise communication would identify the document explicitly.

The difference is not merely linguistic quality.

It changes the information available to the Agent.

Therefore, writing is part of the mechanism through which agency is coordinated.

#### Writing as Delegation

A written request is often a mechanism for delegating work.

Therefore, writing quality directly affects delegation quality.

Consider:

> "I will send the files again, but before that we still need to work on the new document."

The Agent may reasonably need to determine:

- Which files?
- Which document?
- What does "new" refer to?
- What work remains?
- Is the previous document relevant?
- Is the sender referring to a document created during the current interaction?

The problem is not necessarily linguistic correctness.

The problem is insufficient identification of concepts and relationships.

A better request names the relevant entities explicitly.

For example:

> "I will resend the files that need modification. Before modifying them, we still need to continue working on `agency.md`, the document we are currently developing."

The second request reduces unnecessary inference.

This illustrates a general principle:

> **The more important an entity is to a delegated task, the more important it is to identify that entity explicitly.**

#### The Cost of Ambiguity

When an instruction is ambiguous, the Agent must infer missing information.

Inference is not inherently bad.

A capable Agent should be able to infer ordinary contextual information.

However, unnecessary ambiguity creates additional uncertainty.

This is especially dangerous when:

- the task is consequential,
- multiple interpretations are plausible,
- the Agent has significant authority,
- the context is large,
- or the cost of an incorrect interpretation is high.

Therefore, effective delegation does not mean eliminating all inference.

It means eliminating **unnecessary inference**.

### Documentation as an Agency Mechanism

Documentation should not be treated merely as an archival activity.

Documentation externalizes knowledge that would otherwise remain inside individual systems.

This allows Agents to operate with shared context.

A documented organization can therefore distribute knowledge across multiple Agents.

An undocumented organization forces Agents to reconstruct context repeatedly.

This applies equally to:

- human teams,
- organizations,
- software systems,
- AI systems,
- and hybrid systems.

Consequently:

> **Documentation is one of the mechanisms through which knowledge becomes available to Agency beyond the individual Agent.**

### Trust

Agency creates a need for trust.

A Principal must determine whether an Agent can be trusted to:

- interpret responsibility correctly,
- respect constraints,
- make appropriate decisions,
- protect information,
- produce acceptable outcomes,
- report failures,
- and escalate appropriately.

Trust does not mean blind acceptance.

A mature agentive system should distinguish:

- Trust
- Verification
- Validation
- Observation
- Audit

A highly trusted Agent may still require verification for high-impact actions.

Similarly, a low-trust Agent may require extensive supervision.

#### Verification and Validation

Verification asks whether the Agent's behavior or output conforms to defined requirements.

Validation asks whether the result actually satisfies the intended need.

The distinction is important because an Agent can satisfy an explicit specification while the specification itself is wrong.

For example:

```text
Agent
  │
  ├── satisfies specification
  │
  └── produces result
             │
             └── does not satisfy actual need
```

This is another reason why Agency cannot be reduced to execution.

The Principal and other participants remain responsible for defining and validating the problem itself.

### Accountability

Accountability concerns who is answerable for decisions and outcomes.

Accountability should not automatically be assigned to the Agent merely because the Agent performed the action.

An Agent may operate under:

- delegated responsibility,
- delegated authority,
- explicit constraints,
- incomplete information,
- or instructions from a Principal.

Therefore, accountability must be modeled separately from Agency.

This is particularly important for organizations using AI.

Delegating execution to an AI Agent does not necessarily transfer organizational accountability to the AI.

#### Discussion

##### Unresolved questions

- **How does accountability propagate through delegated Agency?** Delegation does not necessarily transfer accountability. The model should establish explicit rules for responsibility and accountability propagation — including whether accountability can be split (partially transferred) rather than only wholly retained or wholly transferred, which the current model does not address.

### Human Agency

Humans are examples of systems capable of agency.

Human agency can be:

- intrinsic,
- delegated,
- individual,
- organizationally situated,
- collaborative,
- constrained,
- or distributed.

A human can simultaneously be:

- an Agent,
- a Principal,
- a manager,
- a customer,
- a contractor,
- or another role.

These roles arise from relationships and context.

They do not necessarily define separate entity types.

### Organizational Agency

An organization can also exhibit agency.

An organization can:

- establish goals,
- make decisions,
- assume responsibilities,
- enter contracts,
- delegate authority,
- employ Agents,
- create policies,
- acquire knowledge,
- and act toward objectives.

This means Agency does not require an individual human mind.

Organizational Agency can emerge from the coordinated activity of many systems.

Therefore:

> **The boundary of an Agent does not necessarily coincide with the boundary of a biological individual.**

### Software Agency

Software can act as an Agent when it performs actions toward objectives within defined capabilities and constraints.

Examples include:

- automated services,
- workflow systems,
- schedulers,
- monitoring systems,
- decision systems,
- and autonomous software components.

However, automation alone does not necessarily establish Agency.

A system that performs a fixed transformation may simply be executing a defined function.

The distinction depends on the conceptual responsibility and action boundary being modeled.

Therefore, not every automated component should automatically be called an Agent.

### AI Agency

AI Agency is Agency manifested through systems containing artificial intelligence.

An AI Agent may include:

- an AI model,
- tools,
- memory,
- knowledge sources,
- policies,
- execution mechanisms,
- feedback mechanisms,
- and other software components.

The model itself should not automatically be equated with the entire Agent.

This distinction is fundamental.

A model is a component.

An Agent is a system capable of acting within a defined context.

Therefore:

```text
AI Model
    │
    ├── may contribute intelligence
    │
    ▼
AI Agent
    │
    ├── Context
    ├── Knowledge
    ├── Tools
    ├── Policies
    ├── Authority
    └── Execution
```

This is analogous to the distinction between a human brain and the entire human system.

The intelligence-producing component is not necessarily identical to the Agent as a whole.

#### Model, Mind, and Body Analogy

A useful conceptual analogy for AI systems is the distinction between:

- Model
- Agent
- Environment

An AI model may be analogous to a cognitive component.

The surrounding Agent may provide:

- memory,
- tools,
- context,
- policies,
- communication,
- execution,
- observation,
- and persistence.

The environment provides the external world in which actions have consequences.

This suggests a conceptual structure:

```text
Environment
     ▲
     │ observations
     │
     ▼
Agent
 ┌───────────────────────────┐
 │ Context                   │
 │ Knowledge                 │
 │ Capabilities              │
 │ Policies                  │
 │ Decision Process          │
 │ Execution                 │
 │ AI Model                  │
 └───────────────────────────┘
     │
     │ actions
     ▼
Environment
```

The analogy should not be interpreted literally.

Its purpose is to prevent a common category error:

> **The intelligence-producing mechanism is not necessarily the Agent itself.**

### Hybrid Agency

Agency may be distributed across multiple kinds of systems.

For example:

```text
Human
  │
  ├── establishes objective
  │
  ▼
AI Agent
  │
  ├── analyzes
  ├── plans
  └── recommends
  │
  ▼
Human
  │
  └── authorizes action
```

This is neither purely human nor purely artificial agency.

It is a hybrid arrangement.

Such arrangements should not require inventing entirely new conceptual categories.

The same principles of:

- responsibility,
- authority,
- capability,
- context,
- knowledge,
- communication,
- trust,
- verification,
- and accountability

remain applicable.

### Agency and Organizational Boundaries

Organizations frequently establish artificial boundaries around responsibilities.

Such boundaries can be useful.

However, they may also prevent knowledge from flowing between Agents.

This is especially visible in technical organizations where roles such as:

- Frontend Engineer
- Backend Engineer
- AI Engineer
- Platform Engineer

can become treated as if they were fundamentally different kinds of Engineers.

A classification may be useful for organizing skills or expertise.

It becomes harmful when it prevents communication or implies that knowledge outside the classification is irrelevant.

Agency therefore requires attention to the boundaries around responsibility and knowledge.

### False Taxonomies

A recurring problem in technology ecosystems is the creation of classifications that are useful for a local purpose but become mistaken for models of reality.

A classification is not necessarily wrong merely because it is artificial.

A false taxonomy can be useful.

The problem arises when the taxonomy hides relationships or prevents knowledge from flowing across its boundaries.

For example, Frontend and Backend may be useful skill classifications.

They become problematic when they imply that:

- modeling belongs only to Backend,
- semantics belongs only to Frontend,
- architecture belongs to one side,
- or a person in one classification should not participate in another domain's reasoning.

This is a form of conceptual fragmentation.

Agency should therefore not be modeled through rigid professional categories.

The same applies to AI Agent terminology.

The same pattern recurs across the technology ecosystem well beyond Frontend and Backend, which suggests it is a general failure mode rather than a coincidence tied to one classification:

- **SOA and Microservices.** When "Microservices" displaced "Service-Oriented Architecture" as the dominant vocabulary, a large body of accumulated knowledge about service boundaries, contracts, and coordination — much of it hard-won through SOA's own failures — was widely treated as obsolete simply because the newer term did not use it. The ecosystem then repeated several of SOA's mistakes under the new name. This is the same failure this document identifies for Agent and AI Agent in [Historical Continuity](#historical-continuity): a new term is mistaken for a new concept, and the old concept's accumulated knowledge is discarded along with the old word.
- **Relation (in the relational/SQL sense) and Aggregate Root (in Domain-Driven Design).** Both are classifications developed for a local purpose — a query model in one case, a consistency boundary in the other — that are sometimes treated as if they were the actual structure of the domain being modeled, rather than one useful projection of it. Confusing the classification for the domain is the same error described generally in this section.
- **Content and Semantic.** As with Frontend/Backend, an informal convention has grown up in parts of the ecosystem that "Semantic" concerns belong to Content-adjacent (often front-end-adjacent) work, and that back-end work does not need to engage with meaning or semantics at all. This is a false taxonomy in the same sense used above: not wrong to have a Content classification, but harmful once it is read as implying that semantic modeling is irrelevant outside it.

These are noted here as instances of the same pattern, not analyzed in depth — a full treatment of any one of them belongs in a document about that specific concept, not in Agency.

### Historical Continuity

AI Agent terminology should not erase the conceptual history of Agency.

Concepts such as:

- representation,
- delegation,
- authority,
- responsibility,
- contract,
- trust,
- decision-making,
- organizational behavior,
- and human agency

predate current AI systems.

When a new technology receives an old conceptual name, the correct response is not necessarily to redefine the entire concept around the new technology.

Instead:

> **The new technology should first be located within the existing conceptual space.**

This allows accumulated knowledge to remain available.

### Why AI Does Not Create the Underlying Problem

Many problems associated with AI Agents existed before AI.

Examples include:

- ambiguous delegation,
- unclear responsibility,
- insufficient context,
- poor documentation,
- weak knowledge management,
- unclear acceptance criteria,
- inappropriate authority,
- poor communication,
- lack of verification,
- and organizational silos.

AI can amplify these problems because it increases execution speed and lowers the cost of producing outputs.

Therefore:

> **AI may amplify an existing organizational problem without being its root cause.**

Replacing an AI tool may change the symptoms without changing the underlying system.

### Interaction With an Agent

Effective interaction with an Agent requires more than issuing commands.

The interaction should establish enough information for the Agent to perform its responsibility.

Important dimensions include:

1. **Purpose**
2. **Responsibility**
3. **Expected outcome**
4. **Context**
5. **Available knowledge**
6. **Constraints**
7. **Authority**
8. **Acceptance criteria**
9. **Communication channel**
10. **Failure and escalation behavior**

These principles apply whether the Agent is:

- a person,
- a team,
- an organization,
- software,
- or an AI system.

This is why learning how to interact with AI Agents should not begin with AI-specific tricks alone.

It should begin with understanding Agency.

### Prompt Engineering and Harness Engineering

Prompt Engineering and Harness Engineering may describe useful practices.

However, they should not be mistaken for the foundational theory of interaction with Agents.

They operate at a lower level.

The broader conceptual structure includes:

```text
Agency
   │
   ├── Delegation
   ├── Responsibility
   ├── Authority
   ├── Context
   ├── Knowledge
   ├── Capability
   └── Communication
          │
          └── Prompt / Harness / Interface
```

Therefore, AI-specific techniques should be evaluated according to the agentive model rather than becoming substitutes for it.

### Agency and Development

Software development itself can be understood as a network of Agents.

For example:

```text
Organization
    │
    ├── delegates responsibility to
    │
    ▼
Development Team
    │
    ├── delegates responsibility to
    │
    ▼
Engineer
    │
    ├── delegates execution to
    │
    ▼
Software Agent
    │
    └── uses
         └── AI Model
```

The resulting system is not simply "developers using AI."

It is a hierarchy and network of agency.

Each level introduces:

- responsibility,
- authority,
- knowledge,
- context,
- constraints,
- communication,
- and potential failure.

This provides a more general model for understanding AI-assisted development.

### Agency and System Design

Agency should be considered when modeling any system in which one component or participant acts on behalf of another.

Relevant questions include:

- Who can act?
- On whose behalf?
- For what purpose?
- With what responsibility?
- With what authority?
- With what capability?
- With what knowledge?
- Under what constraints?
- How is success determined?
- What happens when the Agent cannot act?
- Who receives the result?
- Who evaluates the result?
- Who is accountable?
- Can the Agent delegate further?
- Can authority be revoked?
- How is trust established?

These questions are more fundamental than selecting a particular agent framework.

### Common Modeling Errors



#### Treating AI Agent as the Primitive

Incorrect conceptual direction:

```text
AI Agent
    ↓
everything else
```

Preferred direction:

```text
Agency
    ↓
Agent
    ↓
AI Agent
```

#### Treating Agent as a Separate Entity Type

A person does not become a new entity merely because they become an Agent.

A software system does not necessarily become a different entity either.

The agentive role may emerge from the relationship.

#### Treating `agent_for` as an Entity

If the relationship can be represented directly as:

```text
A ── agent_for ──► B
```

there is no reason to create an intermediate `AgentFor` node merely because the relationship has a name.

#### Confusing Capability With Authority

Being able to perform an action does not mean being permitted to perform it.

#### Confusing Authority With Responsibility

Being permitted to act does not mean being responsible for the outcome.

#### Confusing Autonomy With Agency

A system can exercise autonomy within an agentive relationship.

Delegation and autonomy are not opposites.

#### Confusing the AI Model With the AI Agent

The model is a component of some AI Agents.

It is not necessarily the complete Agent.

#### Treating Prompt Engineering as the Theory of Agent Interaction

Prompts are one communication mechanism.

They do not define the complete structure of Agency.

#### Treating Worker or Actor as the Primitive
Worker and Actor can be useful names for implementation mechanisms, but neither defines Agency.

A Worker may represent an Execution Agent when it carries a bounded responsibility for advancing part of a process. An Actor may represent an Execution Agent when the Actor Model is the chosen execution model. Neither term should be used as a substitute for first asking what responsibility exists, which system assumes it, and what authority and capability are required.

Therefore:

```text
Agency
   ↓
Agent
   ↓
Execution responsibility
   ↓
Worker / Actor / other representation
```

The reverse direction is unsafe:

```text
Worker / Actor
   ↓
therefore Agent
```

The implementation name alone does not establish the conceptual role.

#### Treating Execution Ownership as Domain Ownership
An Agent responsible for advancing the state of a domain entity does not thereby become the domain owner of that entity.

For example:

```text
Account 123 ── execution responsibility ──► Agent 847
```

does not mean:

```text
Account 123 ── owned by ──► Agent 847
```

The execution responsibility may be temporary, partitioned, migrated, failed over, or rebalanced. The domain entity remains the same entity throughout those changes.

Likewise, one Agent may be responsible for many domain entities. Modeling a separate permanent Agent boundary for every domain concept merely because the implementation currently processes that concept would confuse execution structure with domain structure.

#### Treating `agent_for` as Every Responsibility Relationship
`agent_for` expresses a system acting on behalf of another system. It should not be stretched to represent every situation in which an Agent has responsibility for advancing a process.

An Execution Agent may be responsible for a process partition without representing another System in a Principal relationship. The distinction should remain explicit so that representational Agency and execution responsibility do not collapse into one relationship.

#### Treating Organizational Problems as AI Problems

An AI Agent can reveal failures in:

- knowledge management,
- documentation,
- responsibility,
- communication,
- modeling,
- and development processes.

Replacing the AI tool may therefore leave the underlying problem unchanged.

### Agency and Boundaries

Agency always operates within some boundary.

A boundary may define:

- available capabilities,
- accessible knowledge,
- permitted actions,
- authority,
- resources,
- time,
- environment,
- or responsibility.

An Agent may be autonomous inside its boundary while being constrained outside it.

Therefore, a meaningful description of an Agent should include not only what it can do, but also where its Agency stops.

This is particularly important when Agents interact.

### Failure of Agency

Agency can fail in multiple ways.

#### Specification failure

The responsibility is ambiguous.

#### Context failure

The Agent lacks necessary information.

#### Knowledge failure

The relevant knowledge is unavailable or incorrect.

#### Capability failure

The Agent cannot perform the required action.

#### Authority failure

The Agent is responsible but lacks permission.

#### Constraint conflict

The required outcome conflicts with applicable constraints.

#### Communication failure

Information is lost or misunderstood between participants.

#### Evaluation failure

The output is accepted without adequate validation.

#### Accountability failure

No participant is clearly responsible for evaluating or owning the outcome.

These failures should not automatically be attributed to the Agent itself.

The failure may exist elsewhere in the agentive system.

### Agency as a Systemic Property

Agency should therefore be evaluated as part of a system rather than only at the Agent boundary.

A useful abstraction is:

```text
Agency Quality
    =
    Agent Capability
    +
    Context
    +
    Knowledge
    +
    Authority
    +
    Responsibility
    +
    Communication
    +
    Evaluation
    +
    Organizational Support
```

This is not intended as a mathematical equation.

It expresses the principle that effective Agency is systemic.

A highly capable Agent placed inside a poorly designed system may still produce poor outcomes.

### Implications for AI Agent Adoption

Organizations adopting AI Agents should not begin only by asking:

> Which AI Agent should we use?

They should also ask:

- What responsibility are we delegating?
- What knowledge is required?
- Where is that knowledge maintained?
- What authority is being granted?
- What constraints apply?
- What decisions may the Agent make?
- What decisions require human escalation?
- What constitutes success?
- How will results be verified?
- Who remains accountable?
- How will knowledge produced by the Agent become organizational knowledge?
- How does this Agent interact with existing human and software Agents?

Without these questions, AI adoption can increase execution speed without increasing organizational capability.

### The Broader Principle

The central lesson of Agency is not about AI.

It is about understanding how systems act.

Humans have always delegated work to other humans.

Organizations have delegated work to employees, contractors, institutions, and other organizations.

Software has delegated work to services and automated processes.

Modern AI introduces systems that can perform increasingly broad forms of interpretation, planning, and execution.

The technology is changing.

The underlying problem is not entirely new.

Therefore:

> **The principles governing effective interaction with Agents should be more durable than the technologies through which Agents are implemented.**

### Relation to Memar

Agency should be treated as a foundational conceptual area within Memar.

It connects naturally to several other concepts:

```text
Agency
   │
   ├── System
   ├── Process
   ├── Relation
   ├── Responsibility
   ├── Authority
   ├── Capability
   ├── Knowledge
   ├── Context
   ├── Contract
   ├── Trust
   ├── Error
   ├── Module
   └── Organization
```

The exact relationships between these concepts should be established by their respective definitions rather than assumed from conventional terminology.

In particular, Agency should not become a container into which every concept related to people, organizations, or AI is placed.

Its scope should remain centered on the capacity and structure of systems that act.

#### Discussion

##### Unresolved questions

- **How does Agent/System/Principal relate to Khayyam's Type categories?** `type.md` defines four Type categories in Khayyam — Capsule, Method, Abstraction, and Scope. This document has not established where System, Agent, and Principal sit relative to that taxonomy, or whether they need to at all — Agency may be a cross-cutting concern that applies to instances of any Type category rather than a specialization of one particular category (a System with Agency could plausibly be modeled as a Capsule, but nothing here has tested that claim). This is flagged as a genuine gap rather than resolved, since answering it without the same care given to `type.md` itself risks forcing a fit that was not actually verified.

### Terminology

The following terminology principles should be maintained. This list has been extended from an earlier draft to cover every concept that receives its own topic above; the earlier version defined Agency, Agent, Principal, `agent_for`, Delegation, Responsibility, Authority, Capability, Context, Knowledge, and Autonomy, but left Trust, Contract, Accountability, Execution, Decision-Making, Goal, and Communication undefined here despite each having a full topic elsewhere in this document — an inconsistency between the glossary and the body that is corrected below.

The following terminology principles should be maintained:

#### Agency

The capacity or condition through which a system can act intentionally toward objectives within defined capabilities, knowledge, authority, and constraints.

#### Agent

A system that exhibits Agency, especially a system occupying the agent position in an agentive relationship.

#### Principal

A system on whose behalf another system acts.

#### `agent_for`

A relationship connecting a system acting as an Agent to a system for which it acts.

#### Delegation

The assignment or transfer of responsibility, authority, or objectives from one system to another.

#### Responsibility

The domain of outcomes or activities for which an Agent is expected to act.

#### Authority

The permitted scope of decisions or actions available to an Agent.

#### Capability

What a system is able to do.

#### Context

Information and conditions relevant to the Agent's current action.

#### Knowledge

Information or understanding available to support interpretation, decision, and action.

#### Autonomy

The degree to which an Agent can determine or execute actions without direct specification of each individual action.

These definitions remain subject to refinement as the conceptual model develops.

#### Goal / Purpose

A desired outcome or objective toward which an Agent's action is directed; may originate with a Principal (as a delegated objective) or be self-generated (as an intrinsic objective) — see [Goals and Purpose](#goals-and-purpose) and [Intrinsic and Delegated Agency](#intrinsic-and-delegated-agency).

#### Execution

The process through which an Agent transforms responsibility, goals, knowledge, capabilities, and constraints into actions and outcomes, including interpretation, planning, decision-making, action, observation, adaptation, and evaluation — see [Execution](#execution).

#### Decision-Making

The exercise of choice by an Agent within a bounded decision space, which may include escalation to the Principal for decisions outside that boundary — see [Decision-Making](#decision-making).

#### Trust

A Principal's assessment of whether an Agent can be relied upon to interpret responsibility correctly, respect constraints, make appropriate decisions, and report failures — distinct from Verification, Validation, Observation, and Audit — see [Trust](#trust).

#### Contract

A structure establishing expectations between participants, which may define responsibility, authority, obligations, constraints, expected outcomes, acceptance criteria, failure conditions, and escalation procedures; not necessarily a legal document — see [Contracts](#contracts).

#### Accountability

Who is answerable for decisions and outcomes; not automatically assigned to the Agent merely because the Agent performed the action, and must be modeled separately from Agency — see [Accountability](#accountability).

#### Communication

The transfer of goals, responsibility, authority, context, knowledge, feedback, results, warnings, or requests for escalation between participants in an agentive relationship — see [Communication](#communication).

#### Execution Agent
An Agent that assumes responsibility for advancing a bounded part of a Process. This is a descriptive use of Agent, not a separate entity type; Worker, Actor, process, thread, service instance, or another mechanism may represent an Execution Agent.

#### Execution Responsibility
The relationship through which an Agent is responsible for advancing a bounded part of a Process or managing relevant process state. It is distinct from `agent_for`, which expresses acting on behalf of a Principal.

### Working Principles
Until the open questions are resolved, the following principles provide a stable working model:

1. **Model Agency before AI Agent.**
2. **Do not redefine Agent around Artificial Intelligence.**
3. **Treat Agent and Agency as distinct concepts.**
4. **Treat Agent as potentially relational rather than automatically as an entity type.**
5. **Model `agent_for` as a relationship, not a node.**
6. **Treat Principal and Agent as relational positions where appropriate.**
7. **Do not equate Delegation with direct control.**
8. **Do not equate Autonomy with Agency.**
9. **Do not equate Capability with Authority.**
10. **Do not equate Authority with Responsibility.**
11. **Do not equate an AI Model with an AI Agent.**
12. **Treat knowledge and context as essential parts of effective Agency.**
13. **Treat documentation as a mechanism for distributing knowledge among Agents.**
14. **Treat acceptance criteria as part of effective delegation.**
15. **Do not attribute systemic failures automatically to the Agent.**
16. **Preserve historical knowledge about Agency when modeling AI Agents.**
17. **Use technology-specific terminology only after establishing the underlying concept.**
18. **Prefer relationships over artificial entity boundaries when the domain supports them.**
19. **Do not allow professional or technological taxonomies to become false models of responsibility or knowledge.**
20. **Keep the conceptual model independent of implementation technologies.**
21. **Model execution responsibility as a relationship before selecting Worker, Actor, Queue, Lock, Scheduler, or other execution mechanisms.**
22. **Treat Worker and Actor as possible representations of Execution Agents, not as definitions of Agency.**
23. **Do not use `agent_for` to represent every responsibility relationship; acting on behalf of a Principal and being responsible for process execution are related but distinct relationships.**
24. **Allow execution responsibility to be dynamically assigned, transferred, partitioned, or rebalanced without changing the identity of the domain entities being processed.**
25. **Do not infer domain ownership from execution responsibility; an Execution Agent may process many domain entities and responsibility may move between Agents.**
26. **Distinguish `agent_for` from execution responsibility so that representation and processing do not collapse into one relationship.**

### Conclusion

Agency is broader than AI.

Agent is broader than AI Agent.

The emergence of increasingly capable AI systems does not eliminate the accumulated knowledge about systems that act, represent, decide, delegate, assume responsibility, exercise authority, and interact with other systems.

It makes that knowledge more important.

A useful conceptual starting point is therefore not:

> "How do we use AI Agents?"

but:

> **"What does it mean for a system to act?"**

From that question, we can reason about:

- who acts,
- on whose behalf,
- why they act,
- what they are responsible for,
- what authority they possess,
- what they are capable of,
- what they know,
- what constraints they face,
- how they communicate,
- how their actions are evaluated,
- and how responsibility and knowledge move through the larger system.

AI Agents can then be understood as one contemporary manifestation of a much broader phenomenon.

The objective is not to make AI fit an old vocabulary merely for historical consistency.

The objective is to avoid throwing away valid knowledge simply because a new technology has made an old concept fashionable again.

**Agency should therefore be modeled as a general property and structure of acting systems, with AI treated as one of its manifestations rather than its definition.**

## Results
Insufficient time has passed since this specification was adopted to report real, observed outcomes from its use. This section will be filled in once there is such experience to draw on — in particular, whether the working principles in [Working Principles](#working-principles) hold up as later RFCs (Role, Permission, Contract) are written against this document, and whether the `agent_for` direction convention (still an open question above) causes confusion in practice once it is fixed.

## Discussion

### Drawbacks
- **Intentionality is load-bearing but only partially grounded.** The core definition of Agency in [What Is Agency?](#what-is-agency) depends on the word "intentionally," and while [Goals and Purpose](#goals-and-purpose) offers a partial, working account (a Principal-objective → Agent-interpretation → goals → plan → action chain as a necessary condition), that account is not verified as sufficient, and the document proceeds to use the term throughout as though it were settled. A reader applying this model closely will hit this gap directly.
- **The number of concepts introduced without a closed set of relationships between them is large.** Delegation, Responsibility, Authority, Capability, Context, Knowledge, Trust, Contract, and Accountability are each modeled as distinct, but this document only states pairwise non-equivalences (Capability ≠ Authority ≠ Responsibility, Authority ≠ Responsibility, Autonomy ≠ Agency) rather than a positive account of how the full set composes. A reader cannot currently derive, from this document alone, what combination of these concepts is sufficient for a coherent delegation — only a list of ways delegation can fail when one is missing (see [Failure of Agency](#failure-of-agency)).
- **Every example of Agency in this document is drawn from human or organizational contexts, translated to software and AI by analogy.** The contractor, the customer, the engineer, the company — these carry intuitions about intention, understanding, and trust that may not transfer cleanly to a software or AI Agent, and this document does not test where the analogy breaks, only asserts that the underlying structure is shared. This is consistent with the document's stated purpose (model Agency before AI Agent), but it does mean the AI-specific claims here are less load-tested than the human and organizational ones.

### Rationale and alternatives
- **Organizing this document as a flat sequence of independently-numbered sections, in an earlier draft (rejected at this revision)**: the version of this document produced before it was brought into the Explanation-facet structure used 65 sequentially numbered top-level sections with no grouping. That structure made it difficult to see which concepts were sub-parts of which — for example, that Verification and Validation exist to qualify Trust, or that the nine items under Common Modeling Errors are a single coherent unit rather than nine independent topics. Migrating to the current facet's topic/sub-topic structure, with each topic carrying its own `#### Discussion` where it has open questions or rejected alternatives specific to it, was chosen over keeping the flat structure and only reformatting the front matter, because the flat structure was itself judged to be part of what made prior open questions and rejected alternatives hard to keep attached to the specific claim they concern.
- **Keeping this document's original social-media motivation (a short public post plus follow-up comments, aimed at a general technical audience) merged into this RFC, rather than as a separate artifact (rejected)**: the discussion that produced this document's content began as planning for a public post about AI Agents. That framing — persuading a general audience, in a small number of short comments — was deliberately not carried into this document. An RFC answers to different requirements (completeness, precision, exposed open questions) than a public post does (brevity, a single strong claim, a call to action), and conflating the two would have forced this document to either under-explain its concepts for the sake of readability or over-explain them for the sake of a general audience. The public-facing material remains a separate artifact outside Memar's documentation set.

### Prior art
This document has not yet been checked against, or explicitly positioned relative to, several existing bodies of work that plausibly overlap with it and are worth investigating before this document is considered stable:

- **Principal-agent theory**, from economics, which has a long-standing formal treatment of delegation, information asymmetry, and misaligned incentives between a Principal and an Agent — much of it directly relevant to the Delegation, Trust, and Accountability topics above, and not yet cross-referenced here.
- **Agent-oriented programming and multi-agent systems research**, a decades-old field in computer science and AI concerned with formalizing exactly the kind of Agent/Principal/Delegation structure this document models informally. This document's claim that "Agent is older than AI" would be considerably stronger with direct engagement with this literature rather than only the general historical argument made in [Historical Continuity](#historical-continuity).
- **Speech act theory and philosophy of action**, which has its own long-standing treatment of intentionality — directly relevant to the open question left in [Goals and Purpose](#goals-and-purpose).

None of these are cited yet because none have been verified against this specific model closely enough to cite responsibly. Listing them here as Prior Art to investigate, rather than silently omitting them, is intended to make the gap visible rather than to imply it does not exist.

### Unresolved questions
- **Should Agent eventually become its own document once this cluster of concepts grows further?** The discussion that produced this document considered and rejected both `agent.md` (see [Methodology](#methodology)) and `delegation.md` (see [Delegation](#delegation)) as separate documents at this stage. Whether that remains correct once Role, Permission, and Contract are modeled as their own RFCs — at which point Agent might need to be defined independently to be referenced by all of them — is left open rather than decided now.
- **Does this document's own existence, as one artifact among several produced through a multi-participant, multi-AI drafting process, count as an instance of the Hybrid Agency it describes?** This is noted as a genuine reflexive question rather than a rhetorical one: the process that produced this document involved a human Principal setting direction, one AI system drafting and revising collaboratively, and a second AI system (performing this edit) reorganizing and extending it against a separate specification — which maps fairly directly onto the Hybrid Agency and Multi-Agent Systems topics above. Whether that mapping holds up, and whether it is useful, has not been tested here.

### Future possibilities
- **`role.md`, `permission.md`, and `contract.md`** were each mentioned during the discussion that produced this document as concepts dense enough that they may eventually warrant their own RFCs, referencing Agency rather than redefining it — consistent with the Delegation decision in [Delegation](#delegation), the same "can it be defined without first defining Agency?" test should be applied to each before splitting it out.
- **A worked example connecting this document to `type.md`** — resolving the open question in [Relation to Memar](#relation-to-memar) about where System, Agent, and Principal sit relative to Capsule, Method, Abstraction, and Scope — would let later RFCs stop treating that relationship as an open question.
- **A positive composition rule for how Delegation, Responsibility, Authority, Capability, Context, Knowledge, and Trust combine into a coherent delegation**, replacing the current pairwise non-equivalence statements (noted as a Drawback above) with something closer to a checklist or a formal condition.
