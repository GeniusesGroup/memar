# Agency Handoff

Open work for `agency.md`. Entries are mutable current state — revised as each item moves, removed when it resolves or is dropped. See [documentation-handoff.md](./documentation-handoff.md) for what a handoff is.

## Open Questions

### Is Agency a property, capability, or condition?
The current model uses all three perspectives because each explains a different aspect. A future definition should determine whether one is primary.

### Is Agency intrinsic, relational, or both?
Current reasoning suggests both forms are valid. The model should determine whether they share a common primitive.

### Does self-directed action ever fully escape delegation, or does it only push the Principal inward?
A human pursuing a self-generated objective is used in [What Is Agency?](./agency.md#what-is-agency) as the paradigm case of intrinsic agency — agency with no external Principal. But the same act can be redescribed as a System (the person, taken as a whole) delegating to one of its own internal Systems (a motivational subsystem, a habit, a decision made by an earlier version of the same person) — in which case it is delegated agency after all, just with the Principal and Agent both inside the same boundary. This is a real open question about where the boundary of "external" is drawn, not a settled matter, and it should not be resolved implicitly by which example happens to be chosen. It connects to [Nested Agency](./agency.md#nested-agency) and to the recursive structure described there.

### Is Agent fundamentally a role?
Current modeling strongly suggests that Agent is often a relational role rather than an independent entity type. However, some contexts may justify using Agent as a conceptual entity. This should be established by modeling rather than terminology. A related, unresolved sub-question: if a System can exhibit intrinsic Agency with no Principal at all (see [What Is Agency?](./agency.md#what-is-agency)), is "Agent" still the right name for that System when it is acting on its own behalf, or does the word Agent only ever apply once a relationship exists — leaving intrinsic agency-exhibiting Systems simply as Systems, never as Agents, until they enter a relationship?

### What is the exact semantic direction of `agent_for`?
The relationship must be formalized so that its graph direction cannot be misunderstood — including whether the direction should read Principal → Agent or Agent → Principal, since natural-language phrasing ("A is agent for B") does not settle this by itself and different direction conventions have been used informally in early drafts of this model.

### Should the execution-responsibility relationship get a canonical edge name?
Whether Memar should eventually give the execution-responsibility relationship a canonical edge name, or keep it expressed through the existing Responsibility concept until the graph model demonstrates a need for a specific relation.

### Should Execution Agent become a formally defined concept in Process?
Whether Execution Agent should remain descriptive terminology or eventually become a formally defined concept in Process.

### How should responsibility changes be represented without conflating responsibility with implementation ownership?
How responsibility transfer, temporary reassignment, failure takeover, and concurrent replication should be represented without conflating responsibility with implementation ownership.

### What exactly constitutes intentionality?
The definition of Agency in [What Is Agency?](./agency.md#what-is-agency) rests on a System acting "intentionally toward objectives," and [agency.md](./agency.md) uses that phrase as load-bearing without fully defining it. A partial, working answer, stated in the body without treating it as settled: the chain "Principal's desired outcome → Agent's interpreted objective → intermediate goals → plan → action" (described in [Goals and Purpose](./agency.md#goals-and-purpose)) is at minimum a *necessary* structure for intentionality in this model — a System producing behavior with no such chain, however complex the behavior, would not on this account be exhibiting Agency, only behavior (see [Failure of Agency](./agency.md#failure-of-agency) and [What distinguishes Agency from mere behavior?](#what-distinguishes-agency-from-mere-behavior)). Whether that chain is also *sufficient* — whether any System that can be described as running it thereby has intentionality, regardless of what is actually happening inside it — is exactly the part that remains open, especially for software and AI systems, and is not resolved by this document.

### Can a System have Agency without goals?
If goals are intrinsic to Agency, the model must define what counts as a goal. If goals can be externally imposed, the relationship between Agency and Delegation must be clarified.

### What distinguishes Agency from mere behavior?
Not every System that produces behavior necessarily exhibits Agency. A more rigorous boundary is required than the partial answer offered under the intentionality question above.

### How does accountability propagate through delegated Agency?
Delegation does not necessarily transfer accountability. The model should establish explicit rules for responsibility and accountability propagation — including whether accountability can be split (partially transferred) rather than only wholly retained or wholly transferred, which the current model does not address.

### How does Agent/System/Principal relate to Khayyam's Type categories?
`type.md` defines four Type categories in Khayyam — Capsule, Method, Abstraction, and Scope. This document has not established where System, Agent, and Principal sit relative to that taxonomy, or whether they need to at all — Agency may be a cross-cutting concern that applies to instances of any Type category rather than a specialization of one particular category (a System with Agency could plausibly be modeled as a Capsule, but nothing here has tested that claim). This is flagged as a genuine gap rather than resolved, since answering it without the same care given to `type.md` itself risks forcing a fit that was not actually verified.

### Should Agent eventually become its own document once this cluster of concepts grows further?
The discussion that produced this document considered and rejected both `agent.md` (see [Methodology](./agency.md#methodology)) and `delegation.md` (see [Delegation](./agency.md#delegation)) as separate documents at this stage. Whether that remains correct once Role, Permission, and Contract are modeled as their own documents — at which point Agent might need to be defined independently to be referenced by all of them — is left open rather than decided now.

### Does a role imply a bounded knowledge space? (Specialization ≠ narrow knowledge)
- State: recovered 2026-09-17 from an audit of the retired `project instruction and skills - chats.md` chat. In a Role-vs-Knowledge discussion, a claim was reached and refined under the owner's pushback: specialization identifies areas of focus, not the limits of required knowledge — `React Developer` does not mean the knowledge required for the role is React (the industry's habitual `Role → required-knowledge-subset → entire knowledge` reduction, the same error repeated for AI agents named after domains, e.g. "Database Agent"). The refinement, owner-directed: even `Specialization = areas of focus` fails for multipotentialite thinkers whose breadth comes not from accumulated volume but from setting aside upstream abstractions and exercising critical/adaptive/systems thinking — so a role constrains *primary focus*, never the knowledge space an agent (human or AI) must be able to draw on. This document models Role as a position in a relationship ([Agent as a Relational Concept](./agency.md#agent-as-a-relational-concept)) and lists Knowledge as non-substitutable with the other agency concepts, but never states the role/knowledge-boundary claim itself.
- Next: when [Role](#should-agent-eventually-become-its-own-document-once-this-cluster-of-concepts-grows-further) or the role/knowledge relationship is next documented, state the claim there — likely as a failure mode of role-based knowledge scoping; the multipotentialite counter-case is the boundary test any formulation must survive.

### Does this document's own existence count as an instance of the Hybrid Agency it describes?
This is a genuine reflexive question rather than a rhetorical one: the process that produced this document involved a human Principal setting direction, one AI system drafting and revising collaboratively, and a second AI system (performing an earlier edit) reorganizing and extending it against a separate specification — which maps fairly directly onto the [Hybrid Agency](./agency.md#hybrid-agency) and [Multi-Agent Systems](./agency.md#multi-agent-systems) topics in the body. Whether that mapping holds up, and whether it is useful, has not been tested.

### Do the Working Principles hold up as later documents are written against them?
- State: moved here 2026-09-10 from the removed `Results` section (three-section skeleton migration): whether the working principles in [Working Principles](./agency.md#working-principles) hold up is watched as later documents (Role, Permission, Contract) are written against this document.
- Next: evaluate each new document written against this one for whether the principles required exception or restatement; record findings in this handoff and route any resulting change through a changelog entry.

## Anticipated Work

- Define `role.md`, `permission.md`, and `contract.md` if they prove dense enough to warrant their own documents — concepts mentioned during the discussion that produced this document as ones that may eventually reference Agency rather than redefine it; consistent with the Delegation decision in [Delegation](./agency.md#delegation), the same "can it be defined without first defining Agency?" test should be applied to each before splitting it out. (From the document-level Future possibilities.)
- Produce a worked example connecting this document to `type.md` — resolving the open question [How does Agent/System/Principal relate to Khayyam's Type categories?](#how-does-agentsystemprincipal-relate-to-khayyams-type-categories) about where System, Agent, and Principal sit relative to Capsule, Method, Abstraction, and Scope — which would let later documents stop treating that relationship as an open question. (From the document-level Future possibilities.)
- State a positive composition rule for how Delegation, Responsibility, Authority, Capability, Context, Knowledge, and Trust combine into a coherent delegation, replacing the current pairwise non-equivalence statements (recorded as a drawback in the [Agency Changelog](./agency.changelog.md)) with something closer to a checklist or a formal condition. (From the document-level Future possibilities.)
