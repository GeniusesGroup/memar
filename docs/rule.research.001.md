# Rule Research 001 — Terminology: Rule, Policy, Constraint, Convention

## Table of Contents
- [Status](#status)
- [Question and Goals](#question-and-goals)
- [Participants](#participants)
- [Methodology](#methodology)
- [Findings](#findings)
- [Conclusion](#conclusion)

## Status
Complete

## Question and Goals
- **Questions**
  - How do rule, policy, constraint, and convention differ in established business-rules and standards literature? — `Answered`
  - How do production-rule systems and business-rule engines relate to the business-level notion of a rule? — `Answered`
  - What should Memar adopt, reject, or remain neutral on when defining its own Rule concept? — `Answered`
- **Goals**
  - Inform `docs/rule.md` with cited external vocabulary without importing foreign definitions wholesale — `Met`
  - Record negative space: terms Memar deliberately does not equate — `Met`
- **Scope**
  - External terminology (SBVR, Business Rules Group, production-rule literature, Ross). Memar's existing internal usage in modularity, modeling, linter, and Khayyam rules. Excludes implementation survey of specific products (Drools, OPA) beyond illustrative mention.

## Participants
- [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — `Questioner`, `Goal-setter`
- Cursor agent — `Researcher` — `Not yet reviewed`

## Methodology
Sources consulted, and what they may carry: the definitional content of SBVR and of the Business Rules Group's vocabulary was read from industry-community articles and from a tertiary compilation, consulted as orientation alongside the general production-rule and forward-chaining references cited in [Modeling → Separating Structure (Code) from Policy (Rule)](./modeling.md#separating-structure-code-from-policy-rule). None of these holds standing under [Documentation → Citations → Source standing](./documentation.md#citations) — an industry-community article belongs to the vendor class of source, and a tertiary compilation is a pointer toward primary sources rather than a support for a claim — so none is cited as `Evidence`, no URL is recorded, and every claim drawn from them below is this research's own reading of material found in internet research rather than a finding those sources establish. **Known limitation.** The OMG specification that defines this vocabulary was not consulted, so a finding below that states what the vocabulary says is provisional against that specification, and resolving it is an open question in [Rule Handoff](./rule.handoff.md). No product documentation was treated as normative for Memar.

## Findings
- **Element of guidance (SBVR).** In SBVR, the umbrella term for business-side direction is *element of guidance*: a proposition that guides, defines, or constrains some aspect of an enterprise, formulated under enterprise control by an authorized party (internet research — `Reference`). Memar's "owner introduces a Rule" aligns with authorized-party formulation; Memar does not adopt SBVR's full metamodel.
- **Policy versus rule (SBVR).** A *business policy* is an element of guidance that is **not practicable** — less structured, less atomic, not directly enforceable. A *business rule* is **practicable**: a proposition under business jurisdiction, typically a claim of obligation or necessity, formulated using verb concepts from the business vocabulary (same source — `Reference`). Memar's distinction: policy motivates; Rule is checkable. [Protocol → Protocol vs Policy](./protocol.md#protocol-vs-policy) already states a similar hierarchy for organizational versus process-level precision.
- **Definitional versus behavioral rules (SBVR / BRG).** *Definitional* (structural) rules state necessities — "true by definition," alethic; they cannot be violated without changing the model. *Behavioral* (operative) rules state obligations — deontic; they can be violated and carry an enforcement level (internet research — `Reference`). Memar's ontology-versus-governance split maps loosely: ontology rules behave like definitional necessities for existence; governance rules behave like behavioral obligations with configurable enforcement ([Linter → Linter versus compiler](./modules/computer/linter.md#linter-versus-compiler)).
- **Constraint (SBVR / engineering usage).** SBVR uses *static constraint* and *dynamic constraint* for restrictions on fact populations and transitions (internet research — `Reference`). Engineering literature often treats constraints as propositions that must always hold; BRCommunity maps structural business rules to derivation rules and operative rules to process rules or constraints (internet research — `Reference`). Memar treats **constraint** as a kind of Rule tied to validity ([Type → Type and Rules](./type.md#type-and-rules)), not as a synonym for Rule.
- **Convention.** Standards literature rarely elevates "convention" to a formal BRG category; it appears as organizational practice or structural agreement. Memar already uses *convention* for non-binding, owner-specific practice ([documentation-explanation → Conventions](./documentation-explanation.md#conventions)) — consistent with "practicable but overrideable governance."
- **Production rules (mechanism, not definition).** Production-rule systems implement forward-chaining over a fact base and agenda — an **execution strategy** for rules, not the business definition of a rule (internet research — `Reference`). Memar's `modules/process/rules-engine/` follows this family (`loadRules`, `assertFact`, `fireRules`) as mechanism; `docs/rule.md` keeps engine and Rule concept separate ([Modularity → Event, Rule, and Mechanism-First Design](./modularity.md#event-rule-and-mechanism-first-design)).
- **Ross and the Business Rules Group.** Ronald Ross and the Business Rules Group popularized "business rule" as guidance about conduct within an activity, with motivation and enforceability as first-class concerns (internet research — `Reference`). Memar adopts the **owner and enforceability** emphasis; it does not adopt BRG's full definitional apparatus or Zachman row placement.
- **What Memar rejects from the literature.** Treating "rule engine" as the definition of Rule; collapsing policy into rule; importing ecosystem product taxonomies (entity/value object/service) as Rule kinds; requiring a RETE engine for every Rule.

## Conclusion
Memar's Rule concept is **compatible with** SBVR's practicable-rule notion and BRG's owner/enforceability emphasis, but **not identical**: Memar Rules live in Module `rules/` folders, serve software and non-software systems, and split ontology from governance along the compiler/linter line already stated in this repository. Policy remains higher-level and optionally non-checkable; constraint names a validity-focused Rule kind; convention names overrideable governance; production-rule engines are one execution family. Findings graduate into [rule.md](./rule.md); this research remains as audit trail. What [rule.md](./rule.md) adopted was independently supplied by this repository's own practice ([Rule → What a Rule Is](./rule.md#what-a-rule-is)), so the standing of the sources read here bears on how far the vocabulary findings above may be relied upon, and not on the Rule definition itself.
