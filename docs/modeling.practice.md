---
name: modeling
description: Defines the concrete, step-by-step procedure for running a Memar modeling session — discovering a model from scratch, refining an existing one, or critically reviewing a model (including one published by another organization) — and for placing a new edge or relation. Use this file to do the work. Open modeling.md only when a step names a section to check.
---

# Modeling Practice
> **Purpose:** This practice defines how a Memar modeling session is carried out in practice — the concrete steps, checklists, and session-quality signals referenced by [modeling.md](./modeling.md).
> **Nature:** This is a *Practice* — a method commonly used for this type of work, not a claim about knowledge, skill, or capability.

Discovering a model from an unstructured requirement, refining an existing model, and critically reviewing a model someone else proposed — including a model published as open data by another organization — are not separate activities. They share the same procedure below. Whatever the starting point, the same critical scrutiny applies to a concept whether it was proposed by you or by someone else: the modeling phase is where the smallest mistake is cheapest to catch and most expensive to leave uncaught, since everything downstream — every implementation decision — builds on top of it.

---

## Model Reading
Before critiquing or extending anything:
1. Identify all nodes already in the model — or, if starting from an unstructured requirement instead of an existing model, all candidate concepts the requirement implies.
2. Identify all edges and loop-edges already present (see [Edge Types and Their Traditional Counterparts](./modeling.md#edge-types-and-their-traditional-counterparts)).
3. Trace the model's "story" — what reality does it claim to describe?
4. Note initial questions or confusions without resolving them yet.

Produce a neutral restatement of what the model appears to say before judging any part of it.

## Starting a New Requirement
When there is no existing model to read — only an unstructured requirement, a lengthy specification document, a stakeholder interview, or an undocumented system — ask, before proposing any node:

- What information must the system know to fulfill this requirement?
- For each piece of information: is it acquired or discovered?
- What responsibilities are implied by this requirement — what rules, validations, or lifecycle transitions does it require?
- Which of those responsibilities could plausibly evolve independently of the others?
- Does a similar responsibility already exist elsewhere in the graph, under a different name?
- Which of the concepts under discussion are derived or contextual views of another concept, rather than fundamental concerns in their own right?
- What relationships connect these concepts, and what do those relationships encode?

These questions do not replace the fuller procedure below — they exist to give a modeler a starting point rather than a blank page. The wording supplied by a requirement, stakeholder, or existing model is evidence to investigate, not an authoritative model boundary. A proposed concept should remain provisional until its responsibility, relationships, and behavioral consequences have been examined.

## The Modeling Workflow
A modeling or review session typically follows this workflow:
1. Extract or list concepts, responsibilities, constraints, and relationships (from the requirement, or from the model being reviewed).
2. Treat every concept as provisional rather than accepted — including concepts that already exist in a model someone else proposed.
3. Challenge each concept (see [Challenging a Proposed Concept](#challenging-a-proposed-concept) below).
4. Audit the graph's nodes and relationships (see the audits below).
5. Examine the graph for responsibility boundaries.
6. Identify concerns that appear to have independent responsibilities or lifecycles.
7. Delay implementation decisions until the graph stabilizes and major assumptions have been challenged.

During this process, assumptions are targets for investigation rather than facts to be recorded. The purpose is not to collect concepts but to eliminate incorrect ones. A session is successful when it improves understanding of the domain — new questions, rejected assumptions, clarified terminology, and refined boundaries are all valid outcomes; producing implementation artifacts is not required. Continue until the domain can be explained using stable concepts, stable relationships, and clear responsibility boundaries. Only then should implementation-oriented activities begin.

## Challenging a Proposed Concept
For every concept under discussion, ask:
- Does an equivalent concept already exist?
- Is this concept merely a contextual view of another concept?
- Is it introducing a new responsibility or only a new name?
- Does it have an independent lifecycle?
- Does it enforce rules that no existing concern already owns?
- Would the system lose architectural clarity if this concept disappeared?

A concept that cannot justify its existence should not become — or remain — an independent abstraction.

## Testing an Assumption
When a stakeholder, or a model already in front of you, states something as a fact (e.g. "We need a Comment model" or a node simply named `Comment`), do not record or accept it — test it:
- Why is this different from the closest existing concept?
- Which responsibility exists here that does not already exist elsewhere?
- Is this a domain concept, or merely a presentation distinction?

## Node Classification Audit
For each node, classify it as one of:

| Type | Indicator |
|------|-----------|
| Independent concept | Has meaning on its own; survives the [Challenging a Proposed Concept](#challenging-a-proposed-concept) test |
| Relationship mistaken for a node | Only meaningful between two other things; should be an edge |
| Data mistaken for a node | Holds no responsibility of its own; should be an attribute or a reference to an already-independent node (see the Attribute-or-Edge Test) |
| Loop-edge mistaken for a node, or vice versa | A classification that was promoted too early, or a genuine independent concept still expressed only as a label |
| Mixed | Contains more than one of the above — a warning sign in itself |

Flag any node that is unclassifiable, mixed, or misclassified. A mixed node should almost always be decomposed into separate nodes connected by an explicit relationship.

## Premature Classification Check
Before relying on a classification, look for the signs that the label arrived before the rules that would justify it:

- The session is arguing about the word while agreeing about the behavior and the relationships. The definition is what is owed; the label follows from it, never the reverse.
- A category tree, or an inheritance-shaped hierarchy, exists whose members were never derived from observed shared properties.
- "Is X a Y?" cannot be answered without inventing caveats. The candidate is likelier a Role, a Rule, or a loop-edge than a type — see [Relationship Audit](#relationship-audit) step 1 and the `Rule as concept` row in [Common Modeling Anti-Patterns](#common-modeling-anti-patterns).
- Cases keep landing in neither of two categories, and the fix proposed is a third category. A continuum, not a missing class, is the likelier reading; add a category only after the boundary has been examined.
- One artifact needs a different label in each context. Either the labels name roles and belong on edges, or the scheme does not match the domain; distinguish which before re-labelling.

A label that survives this check still has to complete the sentence stated in [Modeling → Classification Emerges From Rules and Relations](./modeling.md#classification-emerges-from-rules-and-relations-not-from-intrinsic-labels). Completing it is the promotion test; failing to complete it is not a naming problem to argue further but a signal that the rules and relationships have not yet been discovered.

## Relationship Audit
For each edge or loop-edge:
1. Does it genuinely connect two independent concepts, or is one side of it actually data or a disguised classification?
2. Is it actually encoding a rule or constraint disguised as a relationship (e.g. an edge named `validates` that is silently hiding a validation rule)?
3. Is its cardinality correct and justified?
4. Is its direction meaningful? Would the reverse direction also be valid, or even more natural?
5. If it is a shortcut edge, can it still be re-derived from other edges already in the graph — has it drifted into becoming a source of truth?

## Placing a relation
When adding an edge or loop-edge, follow these steps. Do not open [modeling.md](./modeling.md) to reconstruct them. Open [A Relation Several Domains Need Is Defined Once](./modeling.md#a-relation-several-domains-need-is-defined-once) only to check that the statement there still matches this procedure.
1. Name the relation in one sentence, apart from the domain that raised it.
2. Search the graph for a relation that already does that job, including under another name.
3. Ask which other domains need that same relation. The question is about the relation, not about the event that creates it in the domain under discussion.
4. If several domains need it, define it once in the domain that already covers every record those domains are. A shared status marker — draft on a law, a contract, a comment, an invoice — is defined once with the shared statuses. A record taking another's place is defined once on thing. A relation only one domain needs stays in that domain.
5. Leave each domain the rule for when its own records may take the shared relation. Do not copy the edge into each domain.

## Single Responsibility Check
Each node should represent one coherent idea. Signs of a mixed responsibility:
- The node's name uses "and" or "or".
- Different discussions of the node focus on different, unrelated aspects of it.
- Some of its relationships pertain to one aspect, others to a completely different aspect.
- Its definition requires multiple unrelated clauses to state.

The remedy is decomposition: separate nodes, connected by an explicit relationship.

## Implementation Contamination Check
Verify the model has not been shaped by a source outside the domain itself — whether the model is your own or another organization's:

| Source | Contamination sign |
|--------|---------------------|
| Database | Tables become concepts; normalization drives boundaries instead of responsibility |
| UI | Screens become concepts; display needs drive structure |
| API | Response/request shapes dictate concept design |
| Framework or language | Class-inheritance or language-feature constraints appear as if they were domain constraints |

If contamination is found, separate which parts of the model reflect reality from which parts reflect an implementation concern that leaked upstream into the model.

## Completeness Check
Ask:
- What questions can this model answer?
- What questions can it *not* answer, but should be able to?
- Are there orphaned concepts with no relationships at all?
- Are there relationships that are implied by the requirement but not yet represented?

## Common Modeling Anti-Patterns

| Anti-pattern | Description | Detection |
|---|---|---|
| God concept | One node that means almost everything | Connected to nearly everything; vague, hard-to-state definition |
| Data as concept | An attribute promoted to its own node | The node has no responsibility or rules of its own, only values |
| Rule as concept | A constraint turned into a node | The node actually represents a "must/should/cannot" statement |
| Unnecessary reification | An edge turned into a node without a genuine independent responsibility | The node's sole purpose is connecting two other nodes |
| Implementation mirror | The model copies a database, API, or UI shape | Structure matches a technical artifact more closely than it matches the domain |
| Terminology drift | A name no longer matches its definition | The definition of X actually describes Y |

## Severity Levels
When flagging a concern during a session, grade it:

| Severity | Meaning | Action |
|---|---|---|
| Critical | The model is fundamentally misstructured | Must be redesigned before proceeding |
| High | A significant issue that will cause real problems | Should be fixed before building further on top of it |
| Medium | A notable issue, but the model is still usable | Fix in the next iteration |
| Low | A minor, optional improvement | Address when convenient |
| Observation | Not necessarily an issue, worth noting | Keep in mind |

## Early Indicators of Modeling Progress
Before graph stability can be observed, look for:
- Fewer newly introduced concepts per session.
- Increasing agreement on concept meanings.
- Reduction of duplicate terminology.
- Reduction of exceptional behaviors.
- Ability to explain the domain using fewer fundamental concepts.

These indicators do not prove model maturity, but they often signal convergence.

## Expected Output of a Session
A modeling or review session is successful if it produces:
- New questions.
- Clarified terminology.
- Rejected assumptions.
- Refined relationships.
- Improved responsibility boundaries.

A session does not need to produce implementation artifacts, database schemas, APIs, or finalized abstraction definitions.
