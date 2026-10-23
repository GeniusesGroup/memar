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

Rule is described in two places, once as a node in a model ([Modeling → Separating Structure (Code) from Policy (Rule)](../../../docs/modeling.md#separating-structure-code-from-policy-rule)) and once as a Module attached to another Module ([Modularity → Rules as a Provisional Term](../../knowledge/modularity/modularity.md#rules-as-a-provisional-term)), and each of those documents needs a definition that will not collapse under the other's lens. This document supplies one: [One Concept, Two Lenses](#one-concept-two-lenses) states that the two are one concept seen through two lenses, that neither lens is primary, and what each lens owes a Rule that claims it. Placement, ownership, and enforcement follow from that; the two subject documents keep only their own consequence and link here.

### Methodology
The definition is derived from practice already exercised in this repository: Khayyam's rules catalog (`bundles/khayyam/rules/README.md`), the [Linter](../../computer/linter/linter.md) protocol's compiler-versus-governance split and authorship members, `modules/process/rule/` and `modules/process/rules-engine/` as evaluation abstractions, and the owner's position that any Module may carry a `rules/` folder the way every Module carries `protocol/`. Terminology was checked against external prior art in [Rule Research 001](./rule.research.001.md) (SBVR, the Business Rules Group, production-rule literature).

## Explanation

### What a Rule Is
A Rule is a **stated condition** whose truth or satisfaction can be checked, evaluated, or enforced against some input — source text, a graph of modeled entities, a wire frame, a process state. It answers a question of the form "given this subject, must / may / must not this hold?"

A Rule is distinguished from neighboring terms as follows:

- **Constraint** — a condition that must hold for a subject to be valid. In Memar, a constraint is often one *kind* of Rule (structural, invariant, relational). Not every Rule is a constraint: a Rule may also prescribe preferred form, trigger an action, or rewrite source without stating a validity boundary.
- **Policy** — high-level guidance that may be discretionary and need not be directly checkable ([Protocol → Protocol vs Policy](../../../docs/protocol.md#protocol-vs-policy)). Policy may *motivate* Rules; a Rule is the practicable, checkable statement derived from or aligned with policy.
- **Convention** — a practice an owner adopts without claiming it is the only legitimate practice. Conventions are often governance-tier Rules an organization may keep or drop ([Explanation → Conventions](../../knowledge/documentation/explanation/explanation.md#conventions)); disabling them does not change what programs or artifacts *may exist*, only how well they are kept.
- **Protocol** — declarative rules governing one or more Processes within a System ([Protocol → What is a Protocol?](../../../docs/protocol.md#what-is-a-protocol)). A protocol document may *contain* Rules at document level until they are relocated; the protocol's identity is the contract for a process, not the folder layout of its Rules.

Two Rule *roles* appear repeatedly in Memar and must not be conflated:

1. **Ontology rules** — decide whether something may exist at all (existence, resolution, well-formedness). Disabling an ontology rule changes what artifacts are admitted. These are enforced by compilers, parsers, resolvers, and validators at the "compiler gate" tier.
2. **Governance rules** — decide how already-admitted instances must flow, name, relate, or present ([Linter → Linter versus compiler](../../computer/linter/linter.md#linter-versus-compiler)). Disabling a governance rule changes posture, not existence. These are enforced by linters, formatters, tidy tools, and organizational configuration.

A single authored Rule declares which tier it belongs to. The [Linter](../../computer/linter/linter.md) protocol's test applies: if turning the check off would admit something the owning specification says cannot exist, the Rule is ontology wearing a governance label.

### One Concept, Two Lenses
A Rule is one thing seen through two lenses, and each lens carries obligations of its own. The lenses are not two descriptions of a Rule from which a session picks one, and they do not compete for primacy: there is one concept ([Modularity → One Term, One Identity](../../knowledge/modularity/modularity.md#one-term-one-identity)), so whichever lens a session works in, the obligations of the other still stand for the same object.

Through the **graph lens** ([Modeling → Separating Structure (Code) from Policy (Rule)](../../../docs/modeling.md#separating-structure-code-from-policy-rule)) a Rule is a node in the model. What this lens owes: the node carries an identity of its own, addressable and nameable apart from the Code element it governs, and it reaches the nodes it concerns through named edges ([Modeling → Edge Types and Their Traditional Counterparts](../../../docs/modeling.md#edge-types-and-their-traditional-counterparts)) rather than through a position in a file, an entry in a configuration, or an attachment only its host knows of. A Rule that the model cannot traverse to and from is not a node in it: it is a setting, and what it governs cannot be asked about it.

Through the **module lens** ([Modularity → Rules as a Provisional Term](../../knowledge/modularity/modularity.md#rules-as-a-provisional-term)) a Rule is a Module developed on its own, carrying a stated boundary, its own identity and lifecycle, and reached across an explicit relationship by whatever it constrains or extends — never through uncontrolled knowledge of what is inside it ([Modularity → Module Identity and Responsibility](../../knowledge/modularity/modularity.md#module-identity-and-responsibility)). Attaching a Rule to a host does not fold it into the host's essential identity ([Modularity → Core Structure and Optional Modules](../../knowledge/modularity/modularity.md#core-structure-and-optional-modules)): the host states where behavior may attach and does not change shape to fit what attaches.

Neither lens settles the other. A Rule placed in the graph and traversable there is still owed a boundary of its own, because behavior whose extent is fixed by whatever reads it cannot be developed independently. A Rule developed as a Module is still owed a place in the model, because behavior a model cannot reach cannot be asked what it governs — and a subject governed by a condition nothing in the model points at is a subject nobody can enumerate the conditions of. Each lens's obligations are requirements on the same Rule, so both are stated here, and no document is asked to answer for the other's.

### Rules, Code, and Services
A Rule states a **condition** — what must, may, or must not hold for a subject. It is not a substitute for the code, modules, and services that realize work in a repository.

Generating, scaffolding, or rewriting source is a **capability of a service** — for example a Memar server endpoint an agent or tool invokes — not a Rule. Producing an abstraction such as `Observer_X` from a naming pattern is mechanical work a service performs when it receives a request; it is not manual application of Rule text.

A Rule may be **enforced** by a service: the service evaluates the condition and returns diagnostics, permits compilation, or triggers a rewrite. The service's behavior — how it parses, generates, or applies a transformation — lives in **code**; the Rule text states only the condition being checked.

Rule-making must not take the place of everything else. Each repository's modules, protocols, and services remain the primary home for what the system does; `rules/` holds the checkable conditions an owner attaches to those subjects.

### Who Owns and Introduces Rules
A Rule is **introduced by an owner** — typically an organization (for example Geniuses.Group for this repository's Khayyam rules) or a Module maintainer — and is **not** part of the language, protocol, or concept itself unless the owner explicitly elevates it to that status through the normal documentation process.

Consequences:

- Another organization may define a different Rule set for the same language, protocol, or codebase. That is a supported outcome, not a fork of the subject (Khayyam rules → This set is a floor, not a ceiling (`bundles/khayyam/rules/README.md#this-set-is-a-floor-not-a-ceiling`)).
- A Rule's normative claim states *what* is required and *why*; the owner's identity is recorded in the Rule artifact and its changelog, not inferred from toolchain behavior.
- Concept and protocol documents own **definitions** of their subjects. When they also state Rules at document level, those Rules are **candidates for relocation** to a Module `rules/` folder (see [Handoff → Follow-up work](./rule.handoff.md#follow-up-work-relocate-document-level-rules)).

A grammar's well-formedness condition is a Rule, and its being part of the language does not stop it being one. A condition is outside a language, protocol, or concept until an owner elevates it by stating it in that subject's own document, and a well-formedness condition is elevated exactly there by the owner of the language it constrains.

### Retiring a Rule
Retiring a Rule removes a Module and a node in one act, so its normative claim and its executable form leave together or are re-owned together: a requirement nothing checks and a condition nothing requires are the drift [Normative Claim and Executable Form](#normative-claim-and-executable-form) exists to prevent. Where what the Rule held was part of the subject's own identity, removing it gives the same source a second meaning rather than retiring a Rule, and the document that owns the subject changes with it; a Rule that held only posture is a replaceable claim and leaves without the subject document changing.

### Where Rules Live: `rules/` Beside `protocol/`
Modularity is not defined by directories, but Modules in this repository are **represented** with a consistent layout: implementation and contracts under `modules/<path>/`, with `protocol/` holding the Module's protocol surface. **Any Module may carry a `rules/` folder beside `protocol/`**, holding that owner's executable Rules for the Module's subject.

Each Rule in `rules/` is a folder (or equivalent unit) containing at minimum:

- a main document naming the Rule and stating what it is, why it exists, what it does not claim, and its enforcement class;
- a citation to the document that owns the Rule's **normative claim** (the concept doc, protocol doc, or type doc where the subject is defined);
- the enforcement class: compiler gate, governance report, source rewrite, resolver behavior, or rule-engine evaluation — as appropriate to the subject;
- scope: unit, repository, organization, or runtime graph — as appropriate.

The `rules/` folder is an **index of executable conditions**, not a second protocol folder. `protocol/` states what the Module exposes; `rules/` states what an owner requires when checking or evaluating work against that Module.

`bundles/khayyam/rules/` is the reference catalog for Khayyam-shaped Rules in this repository. `modules/process/rule/` and `modules/process/rules-engine/` declare evaluation abstractions for process-domain rule engines; they are mechanisms, not the definition of Rule itself.

### Which Module a Rule Belongs To
**A Rule belongs to the module that owns its subject — the module that would have to change if its subject changed.** Ask which document states the normative claim the Rule cites ([Normative Claim and Executable Form](#normative-claim-and-executable-form)), and the Rule's home is that subject's module: a language's toolchain for a Rule about the language, the concept's own module for a Rule about a concept, and the owner's own place for a Rule about an organization, a codebase, or a tool. This extends to the `rules/` folder the [Linter → A rule's home is its subject's document](../../computer/linter/linter.md#a-rules-home-is-its-subjects-document) principle already fixes for the claim, and it is what [Modeling → Constraints Belongs to the Constraining Concern](../../../docs/modeling.md#constraints-belong-to-the-constraining-concern) requires of a constraint's bookkeeping: a condition owned by the concern that originates it is not duplicated onto each place it reaches. A catalog is not a place everything goes; it is one module's rules, and a Rule filed outside its subject's module is a Rule whose reader must already know which subject it governs before reading it.

**A Rule belongs to a language exactly when no program satisfies every Rule of that language's catalog and still violates this one** — when turning the condition off would change what a program means rather than how well a codebase is kept. That is the language's own test: Khayyam → Minimal Legislation (`docs/khayyam/khayyam.md#minimal-legislation-a-principle`) asks it of every proposed condition, and an organization that turns a language's Rule off has not relaxed a Rule but written a second meaning for the same source. Where such a program does exist, the subject is a tool's, an organization's, or a concept's, and a language's catalog gains nothing by legislating it: the language states what a program's meaning requires, and a condition whose handling may differ between one realization and the next is stated by the tool that applies it.

**Enforcement does not decide this.** A Rule may be enforced by a compiler, a resolver, a linter, or a rewrite, and the tool that runs the check is not the module that owns the claim — the tool owns the check, not the Rule. `bundles/khayyam/rules/comment-forms/` is read by a scanner and `bundles/khayyam/rules/file-layout/` is applied by a rewrite, and both are about this repository's Khayyam; a Rule about a concept's contract may equally be enforced by this repository's tooling and belong to that concept's module. Only the subject decides the home.

Two cases the subject test does not decide, and neither is settled here. A Rule whose subject a language and a concept both claim belongs to whichever document states the normative claim, and where both decline it the Rule has no home until one accepts it. A Rule about a codebase's own sources in a language has a subject that is neither the language nor a concept, and its home is the owner of that codebase rather than any module inside it.

### Normative Claim and Executable Form
A Rule has two parts that must stay linked:

1. **Normative claim** — the subject-matter statement in the document that owns the concept, type, or protocol (what must hold and why).
2. **Executable form** — the check, gate, rewrite, or engine binding in `rules/`, citing that claim.

The [Linter → A rule's home is its subject's document](../../computer/linter/linter.md#a-rules-home-is-its-subjects-document) principle applies to the **normative claim**. The linter (or other tool) owns the **check**, not the claim. As Rules migrate into `rules/` folders, the claim may remain in the subject document with a pointer to the executable Rule, or move with the Rule while the subject document links back — but the two must not drift apart.

Until a shared notation exists ([Linter handoff → rule-authorship notation](../../computer/linter/linter.handoff.md#the-rule-authorship-notation)), governance Rules authored for linter consumption should carry the members stated in [Linter → How a governance rule is authored](../../computer/linter/linter.md#how-a-governance-rule-is-authored): Subject, Tier, Default, Override. Those members describe the authoring form a Rule takes; the claim itself is a Type on the subject it governs ([Type](../../../docs/type.md)), and a notation is one rendering of that statement rather than its carrier.

### Rule Engines
A **rule engine** is a system that **evaluates** Rule artifacts against supplied facts or context and returns a decision — permit, deny, derive, trigger, or rewrite. It is an execution mechanism justified by modeled responsibility ([Modularity → Event, Rule, and Mechanism-First Design](../../knowledge/modularity/modularity.md#event-rule-and-mechanism-first-design)), not a reason to call every conditional a Rule.

In this repository:

- `modules/process/rules-engine/` and `modules/process/rule/` expose engine-shaped abstractions (`loadRules`, `assertFact`, `fireRules`, `Evaluate`, `GetDecision`) aligned with common business-rule-engine surfaces (facts, agenda, decision keys).
- [Modeling → Separating Structure (Code) from Policy (Rule)](../../../docs/modeling.md#separating-structure-code-from-policy-rule) treats graph-stored Rule nodes as the model; the engine is the **interpreter** of those nodes, not part of the structural model.
- Production-rule systems (forward chaining, RETE-style agendas) are **implementation families** for rule engines — useful prior art, not Memar's definition. See [Rule Research 001 → Findings](./rule.research.001.md#findings).

A linter is **not** a rule engine in the general sense: it is a specialized analysis system that enforces governance-tier Rules on programs, usually by subscribing to compiler events rather than maintaining a separate fact base ([Linter → Analysis consumes compiler events](../../computer/linter/linter.md#analysis-consumes-compiler-events-not-library-names)). A rule engine may consume modeled Rules at runtime; a linter consumes authored Rules at analysis time. A toolchain may combine both.

### Relationship to Modularity and Modeling
At the modular boundary, a Rule is a Module developed on its own, related to the Module whose subject it governs: it constrains or extends a host Module without becoming part of that Module's essential identity ([Modularity → Rules as a Provisional Term](../../knowledge/modularity/modularity.md#rules-as-a-provisional-term), and [One Concept, Two Lenses](#one-concept-two-lenses) for what the module lens owes it). Capability completeness requires that the Rules governing a relationship belong with the Module that owns that relationship ([Modularity → Capability Completeness](../../knowledge/modularity/modularity.md#capability-completeness)).

At the modeling boundary, [Type → Type and Rules](../../../docs/type.md#type-and-rules) separates invariants, constraints, behavioral rules, and business rules by volatility and checking strategy. Those categories describe **what** is being ruled; this document describes **where and how** authored Rules are introduced and enforced. [Modeling → Constraints Belong to the Constraining Concern](../../../docs/modeling.md#constraints-belong-to-the-constraining-concern) places constraint ownership on the constraining concern — consistent with Rule ownership by subject, not by every touched endpoint.

### What This Document Does Not Define
- The final notation for linter-checkable Rules (open in [Linter handoff](../../computer/linter/linter.handoff.md)).
- Per-subject Rule catalogs — those live in each Module's `rules/` folder and in the paired [handoff inventory](./rule.handoff.md#follow-up-work-relocate-document-level-rules).
