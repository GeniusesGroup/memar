---
Title: "Rule"
Status: Draft
Start Date: 2026-09-29
ID: 497407
---

# Rule

## Abstract
A **Rule** in Memar is a stated condition — on structure, flow, naming, or behavior — that an owner introduces for a subject they govern. A Rule is not part of a language's grammar, not part of a protocol's wire contract by default, and not universal truth: it is an authored, replaceable claim whose normative statement cites the document that owns its subject, and whose executable form lives in a Module's `rules/` folder beside that Module's `protocol/` folder. A **rule engine** is the mechanism that evaluates Rule artifacts against runtime or analysis input; a **linter** is one enforcement surface for governance-tier Rules on source. This document defines the concept; [Rule Research 001](./rule.research.001.md) records the terminology inquiry that informed it.

## Introduction

### Motivation
The term *rule* is used throughout Memar — in modularity, modeling, type theory, protocol documents, Khayyam language docs, and the `organization` repository — but no single document yet states what a Rule is, who may introduce one, where it lives, or how it relates to linters and rule engines. Without that, three failures recur: Khayyam-specific practice is mistaken for a language property; document-level normative passages accumulate in concept and protocol documents with no executable home; and "rule engine" is treated as a synonym for "any conditional logic" rather than as a named evaluation mechanism.

[Modularity → Rules as a Provisional Term](./modularity.md#rules-as-a-provisional-term) named the architectural role — behavior attachable to a Module without becoming part of its essential identity — but left the term provisional. [Modeling → Separating Structure (Code) from Policy (Rule)](./modeling.md#separating-structure-code-from-policy-rule) names a graph-node framing of the same concern. This document unifies placement, ownership, and enforcement without choosing between the module-attachment and graph-node framings; that reconciliation remains open in the paired [handoff](./rule.handoff.md).

### Methodology
The definition is derived from practice already exercised in this repository: Khayyam's [rules catalog](../modules/khayyam/rules/README.md), the [Linter](./protocols/computer/linter.md) protocol's compiler-versus-governance split and authorship members, `modules/process/rule/` and `modules/process/rules-engine/` as evaluation abstractions, and the owner's position that any Module may carry a `rules/` folder the way every Module carries `protocol/`. Terminology was checked against external prior art in [Rule Research 001](./rule.research.001.md) (SBVR, the Business Rules Group, production-rule literature).

## Explanation

### What a Rule Is
A Rule is a **stated condition** whose truth or satisfaction can be checked, evaluated, or enforced against some input — source text, a graph of modeled entities, a wire frame, a process state. It answers a question of the form "given this subject, must / may / must not this hold?"

A Rule is distinguished from neighboring terms as follows:

- **Constraint** — a condition that must hold for a subject to be valid. In Memar, a constraint is often one *kind* of Rule (structural, invariant, relational). Not every Rule is a constraint: a Rule may also prescribe preferred form, trigger an action, or rewrite source without stating a validity boundary.
- **Policy** — high-level guidance that may be discretionary and need not be directly checkable ([Protocol → Protocol vs Policy](./protocol.md#protocol-vs-policy)). Policy may *motivate* Rules; a Rule is the practicable, checkable statement derived from or aligned with policy.
- **Convention** — a practice an owner adopts without claiming it is the only legitimate practice. Conventions are often governance-tier Rules an organization may keep or drop ([documentation-explanation → Conventions](./documentation-explanation.md#conventions)); disabling them does not change what programs or artifacts *may exist*, only how well they are kept.
- **Protocol** — declarative rules governing one or more Processes within a System ([Protocol → What is a Protocol?](./protocol.md#what-is-a-protocol)). A protocol document may *contain* Rules at document level until they are relocated; the protocol's identity is the contract for a process, not the folder layout of its Rules.

Two Rule *roles* appear repeatedly in Memar and must not be conflated:

1. **Ontology rules** — decide whether something may exist at all (existence, resolution, well-formedness). Disabling an ontology rule changes what artifacts are admitted. These are enforced by compilers, parsers, resolvers, and validators at the "compiler gate" tier.
2. **Governance rules** — decide how already-admitted instances must flow, name, relate, or present ([Linter → Linter versus compiler](./protocols/computer/linter.md#linter-versus-compiler)). Disabling a governance rule changes posture, not existence. These are enforced by linters, formatters, tidy tools, and organizational configuration.

A single authored Rule declares which tier it belongs to. The [Linter](./protocols/computer/linter.md) protocol's test applies: if turning the check off would admit something the owning specification says cannot exist, the Rule is ontology wearing a governance label.

### Rules, Code, and Services
A Rule states a **condition** — what must, may, or must not hold for a subject. It is not a substitute for the code, modules, and services that realize work in a repository.

Generating, scaffolding, or rewriting source is a **capability of a service** — for example a Memar server endpoint an agent or tool invokes — not a Rule. Producing an abstraction such as `Observer_X` from a naming pattern is mechanical work a service performs when it receives a request; it is not manual application of Rule text.

A Rule may be **enforced** by a service: the service evaluates the condition and returns diagnostics, permits compilation, or triggers a rewrite. The service's behavior — how it parses, generates, or applies a transformation — lives in **code**; the Rule text states only the condition being checked.

Rule-making must not take the place of everything else. Each repository's modules, protocols, and services remain the primary home for what the system does; `rules/` holds the checkable conditions an owner attaches to those subjects.

### Who Owns and Introduces Rules
A Rule is **introduced by an owner** — typically an organization (for example Geniuses.Group for this repository's Khayyam rules) or a Module maintainer — and is **not** part of the language, protocol, or concept itself unless the owner explicitly elevates it to that status through the normal documentation process.

Consequences:

- Another organization may define a different Rule set for the same language, protocol, or codebase. That is a supported outcome, not a fork of the subject ([Khayyam rules → This set is a floor, not a ceiling](../modules/khayyam/rules/README.md#this-set-is-a-floor-not-a-ceiling)).
- A Rule's normative claim states *what* is required and *why*; the owner's identity is recorded in the Rule artifact and its changelog, not inferred from toolchain behavior.
- Concept and protocol documents own **definitions** of their subjects. When they also state Rules at document level, those Rules are **candidates for relocation** to a Module `rules/` folder (see [Handoff → Follow-up work](./rule.handoff.md#follow-up-work-relocate-document-level-rules)).

### Where Rules Live: `rules/` Beside `protocol/`
Modularity is not defined by directories, but Modules in this repository are **represented** with a consistent layout: implementation and contracts under `modules/<path>/`, with `protocol/` holding the Module's protocol surface. **Any Module may carry a `rules/` folder beside `protocol/`**, holding that owner's executable Rules for the Module's subject.

Each Rule in `rules/` is a folder (or equivalent unit) containing at minimum:

- a main document naming the Rule and stating what it is, why it exists, what it does not claim, and its enforcement class;
- a citation to the document that owns the Rule's **normative claim** (the concept doc, protocol doc, or type doc where the subject is defined);
- the enforcement class: compiler gate, governance report, source rewrite, resolver behavior, or rule-engine evaluation — as appropriate to the subject;
- scope: unit, repository, organization, or runtime graph — as appropriate.

The `rules/` folder is an **index of executable conditions**, not a second protocol folder. `protocol/` states what the Module exposes; `rules/` states what an owner requires when checking or evaluating work against that Module.

`modules/khayyam/rules/` is the reference catalog for Khayyam-shaped Rules in this repository. `modules/process/rule/` and `modules/process/rules-engine/` declare evaluation abstractions for process-domain rule engines; they are mechanisms, not the definition of Rule itself.

### Normative Claim and Executable Form
A Rule has two parts that must stay linked:

1. **Normative claim** — the subject-matter statement in the document that owns the concept, type, or protocol (what must hold and why).
2. **Executable form** — the check, gate, rewrite, or engine binding in `rules/`, citing that claim.

The [Linter → A rule's home is its subject's document](./protocols/computer/linter.md#a-rules-home-is-its-subjects-document) principle applies to the **normative claim**. The linter (or other tool) owns the **check**, not the claim. As Rules migrate into `rules/` folders, the claim may remain in the subject document with a pointer to the executable Rule, or move with the Rule while the subject document links back — but the two must not drift apart.

Until a shared notation exists ([Linter handoff → rule-authorship notation](./protocols/computer/linter.handoff.md#the-rule-authorship-notation)), governance Rules authored for linter consumption should carry the members stated in [Linter → How a governance rule is authored](./protocols/computer/linter.md#how-a-governance-rule-is-authored): Subject, Tier, Default, Override.

### Rule Engines
A **rule engine** is a system that **evaluates** Rule artifacts against supplied facts or context and returns a decision — permit, deny, derive, trigger, or rewrite. It is an execution mechanism justified by modeled responsibility ([Modularity → Event, Rule, and Mechanism-First Design](./modularity.md#event-rule-and-mechanism-first-design)), not a reason to call every conditional a Rule.

In this repository:

- `modules/process/rules-engine/` and `modules/process/rule/` expose engine-shaped abstractions (`loadRules`, `assertFact`, `fireRules`, `Evaluate`, `GetDecision`) aligned with common business-rule-engine surfaces (facts, agenda, decision keys).
- [Modeling → Separating Structure (Code) from Policy (Rule)](./modeling.md#separating-structure-code-from-policy-rule) treats graph-stored Rule nodes as the model; the engine is the **interpreter** of those nodes, not part of the structural model.
- Production-rule systems (forward chaining, RETE-style agendas) are **implementation families** for rule engines — useful prior art, not Memar's definition. See [Rule Research 001 → Findings](./rule.research.001.md#findings).

A linter is **not** a rule engine in the general sense: it is a specialized analysis system that enforces governance-tier Rules on programs, usually by subscribing to compiler events rather than maintaining a separate fact base ([Linter → Analysis consumes compiler events](./protocols/computer/linter.md#analysis-consumes-compiler-events-not-library-names)). A rule engine may consume modeled Rules at runtime; a linter consumes authored Rules at analysis time. A toolchain may combine both.

### Relationship to Modularity and Modeling
At the modular boundary, a Rule often appears as an **optional Module** or attachable behavior: it constrains or extends a host Module without becoming part of that Module's essential identity ([Modularity → Rules as a Provisional Term](./modularity.md#rules-as-a-provisional-term)). Capability completeness requires that the Rules governing a relationship belong with the Module that owns that relationship ([Modularity → Capability Completeness](./modularity.md#capability-completeness)).

At the modeling boundary, [Type → Type and Rules](./type.md#type-and-rules) separates invariants, constraints, behavioral rules, and business rules by volatility and checking strategy. Those categories describe **what** is being ruled; this document describes **where and how** authored Rules are introduced and enforced. [Modeling → Constraints Belong to the Constraining Concern](./modeling.md#constraints-belong-to-the-constraining-concern) places constraint ownership on the constraining concern — consistent with Rule ownership by subject, not by every touched endpoint.

### What This Document Does Not Define
- The final notation for linter-checkable Rules (open in [Linter handoff](./protocols/computer/linter.handoff.md)).
- Whether the module-attachment framing or the graph-node framing is primary (open in [Modeling handoff](./modeling.handoff.md) and [Modularity handoff](./modularity.handoff.md#what-is-the-final-terminology-for-the-kind-of-optional-module-currently-discussed-provisionally-as-a-rule)).
- Per-subject Rule catalogs — those live in each Module's `rules/` folder and in the paired [handoff inventory](./rule.handoff.md#follow-up-work-relocate-document-level-rules).
