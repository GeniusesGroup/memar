---
Title: "Thinking"
Status: Draft
Start Date: 2026-09-01
ID: 496735
---

# Thinking

## Abstract
This document models **thinking** as the foundational concept behind Memar's collaboration and reasoning norms. Its central claims: (1) every exchange between a human and an AI system — or between any two participants in this project — is a connection between two thinking systems, and the medium connecting them (speech, text, a chat interface, a repository) is an implementation detail that does not change what the exchange conceptually is; (2) the norms governing such an exchange are therefore derivable from a model of thinking itself, not from etiquette or platform convention; (3) from that model, this document derives the discourse rules Memar follows — evaluate claims on their merits rather than their source, prioritize definitions over terminology, ask rather than assume, and scale criticism to the strength of the model being criticized — and states them once, here, giving them a single authoritative home. Thinking is treated as a family of modes — critical, systems, creative, adaptive, abstract, analogical, and further modes grouped by function — rather than a single uniform activity, and the document grounds its model in cognitive science — including the 4E framing of cognition (embodied, embedded, enacted, extended) — as the scientific layer this model is expected to deepen over time.

## Introduction

### Motivation
Norms for evaluating claims, naming things, and exchanging ideas are exercised in every Memar conversation and every Memar document, but they previously had no authoritative home: each rule lived either nowhere (observed only by habit) or scattered across other documents' edges. Without a single home, three recurring costs follow:

1. **No derivation.** A rule stated alone — "do not assume the other participant is correct" — gives no way to resolve a conflict with another rule in a novel situation, because nothing states what the rules are *for*.
2. **Scoping drift.** Without a stated model of who thinks, rules quietly narrow to one participant type or one medium — typically "AI chat assistant etiquette" — even though the same norms govern human-to-human review, written critique, and organizational decision processes.
3. **No growth path.** Rules cannot be added, refined, or retired coherently unless there is a stable concept they attach to. Thinking is that concept.

The remedy is the same one this project applies elsewhere (see [Framework](./framework.md), on definitions preceding artifacts): state the model first, then derive the norms from it. A document about thinking is the foundation those norms were implicitly assuming all along.

### Methodology
The discourse norms this document derives were accumulated across years of working conversations before this document existed; drafting this document examined them for what they presuppose rather than inventing them. That examination produced the two modeling moves the document makes — treating a conversation as two thinking systems joined by a medium, and treating thinking modes as function groups of the same underlying activity — both applied retrospectively to explain why the inherited rules work. The cognitive-science grounding (4E cognition) was included from the document's start; see [Unresolved questions](#unresolved-questions) for what remains unexamined about it.

## Explanation

### What Thinking Is
**Thinking is the activity of a cognitive system manipulating representations toward some end** — evaluating, relating, transforming, and generating them. This is stated as a working definition grounded in the cognitive-science usage of the term, not as a project-specific coinage: Memar follows its general terminology policy ([Terminology → Scientific Terms](./terminology.md#scientific-terms)) of preferring the scientific layer's meaning where one exists.

Three boundary clarifications follow from the definition:

- **Thinking is an activity, not a content store.** A document, a memory file, or a model is not thinking; it is material thinking operates on and produces. This is the same concept/data separation used throughout Memar ([Modeling → Concept Existence vs. Model Existence](./modeling.md#concept-existence-vs-model-existence)), applied here: do not mistake the artifacts of thinking for the activity.
- **A thinker is a system, not necessarily a person.** Consistent with [System](./system.md)'s position that system-hood is a lens applicable to almost anything, any system that manipulates representations toward ends qualifies: a human, an organization, an AI model. Nothing in the definition privileges biological implementation.
- **Thinking is not defined by correctness.** Thinking produces claims, and claims can be wrong. The quality of thinking is a separate property from its occurrence — which is exactly why norms for evaluating thought are needed, and why this document exists.

#### Discussion

##### Rationale and alternatives
- **Leave "thinking" undefined and regulate only behavior (rejected)**: an undefined central term would import the reader's colloquial sense — for AI-era readers, often "the internal reasoning phase of a language model" — which is one implementation of thinking, not the concept. Memar's terminology governance ([Terminology → Terminology Authority and Governance](./terminology.md#terminology-authority-and-governance)) requires defining a load-bearing term once, here, and letting documents reference that definition.
- **Name this document "critique" or "discourse" (rejected)**: both name one product or one setting of thinking. The rules Memar needs cover more than critique (systems thinking, creative exploration) and more settings than discourse (solitary analysis). Naming the document after the broader concept keeps its scope honest; the narrower subjects can become their own documents if they earn one.

##### Prior art
Cognitive science treats thinking as information processing over mental representations; the framing above is the standard working sense, deliberately kept compatible with it rather than diverging from it without cause.

### Modes of Thinking
"Thinking" names a family of activities, not one uniform one. This document distinguishes **modes of thinking** and treats them the way [Modeling → One Reality, Multiple Abstraction Lenses](./modeling.md#one-reality-multiple-abstraction-lenses) treats modeling lenses: co-equal modes of operating on the same material, not a hierarchy and not separate faculties. Any one cognitive act may draw on several modes at once; the modes are distinguished by what they do to thinking material, not by which part of a brain or system performs them.

The modes below are grouped by function — what the mode contributes to thinking as a whole. Grouping by function rather than by a flat list keeps an open-ended family navigable and keeps the membership criterion visible: a mode earns its place by the function its members serve, and the groups are open, not exhaustive.

#### Evaluative Modes
Modes whose function is assessing thinking material — weighing claims, options, and models against criteria.

- **Critical thinking** — evaluating claims: their assumptions, definitions, internal consistency, evidence, and consequences. The most exercised evaluative mode in Memar's review and discussion work, and the one the discourse norms below chiefly govern.
- **Analytical thinking** — decomposing a whole into its parts and their relationships to see how it works: separating a problem into concerns, a claim into premises, a mechanism into steps. Distinct from critical thinking: analysis breaks things down to understand them; criticism judges them. Memar's whole-document decomposition method (each topic stating its claim, then its rationale) is applied analytical thinking.
- **Evaluative decision thinking** — comparing alternatives against criteria and choosing: weighing options, judging trade-offs, deciding under incomplete information. Distinct from both of the above in that it terminates in a choice rather than an understanding or a verdict. Architecture decisions — Memar's own and those documented in every project following its approach — are this mode's output.

#### Structural Modes
Modes whose function is organizing or reorganizing thinking material — finding form in it.

- **Abstract thinking** — moving from instances to generalities and back: recognizing what a set of cases shares, separating the essential from the incidental, and forming concepts from that separation. This mode is a precondition for nearly everything else Memar does — a definition is abstract thinking's product, a model is its structured form. It pairs with concrete thinking (below) rather than opposing it: the abstraction earns its keep when it returns and explains its instances.
- **Concrete thinking** — the counterpart mode: working with specific instances, examples, and cases. Not lesser thinking — Memar's own Methodology sections repeatedly show that abstract structures are tested and corrected against concrete examples. The abstract/concrete pair is a cycle, not a ladder.
- **Systems thinking** — attending to how parts interact, how behavior propagates across boundaries, and how the whole behaves differently from its parts. Memar's modeling discipline ([Modeling](./modeling.md)) and its [System](./system.md) document operationalize this mode for architecture work specifically.
- **Sequential thinking** — ordering material into steps, chains, and dependencies: reasoning that follows a path where each stage constrains the next. Contrast with the structural modes above, which find form in wholes rather than paths. Procedures, proofs, and cause-effect reasoning all exercise it.

#### Generative Modes
Modes whose function is producing new thinking material rather than assessing or organizing existing material.

- **Creative thinking** — generating candidates: alternative models, alternative framings, alternative definitions. Creative output is raw material for the evaluative modes; the generative and evaluative functions pair, and neither substitutes for the other.
- **Divergent thinking** — deliberately widening before narrowing: producing many distinct candidates rather than one polished answer. The exploratory phase of any design or modeling session, and the reason Memar records rejected alternatives — they are evidence this mode ran. Distinct from creative thinking as breadth is distinct from novelty: divergence can produce many ordinary candidates; creativity produces the unexpected one.
- **Analogical thinking** — transferring structure from a familiar domain to an unfamiliar one: reasoning "X is like Y in this respect." Powerful and double-edged — it imports both the mapping and the unmapped baggage — which is why Memar treats prior art as evidence to examine, never authority to inherit ([Terminology → Diverging From Ecosystem Definitions](./terminology.md#diverging-from-ecosystem-definitions)). The discourse norm against industry defaults is a guardrail on exactly this mode.
- **Hypothetical thinking** — reasoning about what is not (yet) the case: imagining states of affairs, following suppositions to their consequences, asking "what would happen if." Premise-testing, future modeling, and counterfactual analysis are its exercised forms. Architecture itself is largely hypothetical thinking made durable — a design is a supposition about consequences not yet observed.

#### Corrective Modes
Modes whose function is updating thinking material in response to reality or to new material.

- **Adaptive thinking** — re-modeling when reality contradicts the current model: noticing that an assumption failed, and revising rather than defending. This mode is what makes the project's revision mechanisms (changelogs, supersession, propagation tracking) meaningful rather than bureaucratic.
- **Reflective thinking** — thinking about one's own thinking: examining what was assumed, what was concluded, and whether the reasoning itself holds. Metacognition, in cognitive-science vocabulary. The proportional-criticism norm below is reflective thinking applied across systems — requiring a critic to examine their own objection before issuing it — and every "Methodology" section in this project's documents is reflective thinking made permanent.

#### Grouping Notes
The functional groups are a navigation aid, not a classification doctrine — a single cognitive act routinely combines modes across groups (testing a hypothesis is hypothetical thinking generative of candidates, evaluated critically, then accepted or revised adaptively). The groups are also not claimed to be mutually exclusive at the mode level: analytic and critical overlap by design, and a future revision may merge or re-scope them; what is fixed here is the membership criterion (a named function in thinking), not the boundary drawing. This is deliberately not a taxonomy in the sense [classification principles](./classification-principles.md) warn about — no mode's membership is treated as an intrinsic property of a thought; the groups exist to be used, and are revised when they stop being useful.

#### Discussion

##### Rationale and alternatives
- **A closed taxonomy of thinking modes (rejected)**: would replicate the taxonomy-before-definition failure Memar's [classification principles](./classification-principles.md) warn against. Modes are named only for functions the project's actual work depends on.
- **A flat list without grouping (considered, not chosen)**: simpler at today's scale of thirteen modes, but each added mode would linearly grow the section without revealing which modes are siblings of which; the functional grouping carries that structure at negligible cost.
- **Treat modes as separate "skills" an agent or person either has or lacks (rejected)**: conflates the description of a practice with a capability — the same conflation [`.agents/skills/README.md`](../.agents/skills/README.md) corrects for the word "skill". A mode is a way of operating, available to be exercised deliberately regardless of the thinker's current proficiency.

##### Prior art
Taxonomies of thinking skills and dispositions are established in educational psychology and cognitive science — Bloom's taxonomy of educational objectives, dual-process accounts of cognition, and the critical-thinking and metacognition literatures among them. Those taxonomies classify for instructional assessment; this document names modes for the narrower purpose of grounding this project's own discourse norms, and adopts no taxonomic scheme wholesale.

##### Unresolved questions
1. Is "mode" the right concept at all, or are these better modeled as strategies, dispositions, or phases? The function-group framing is a working position, not a settled one.
2. Which further modes belong here — convergent thinking (named implicitly as divergence's counterpart but not yet given its own entry), inductive and deductive inference, probabilistic thinking have all been plausibly named — and what observed dependence would justify adding each?
3. Are the four functional groups the right partition, or should generative and corrective modes be regrouped as their coverage grows?

### Grounding: Cognition and the 4E Framing
The model above is grounded in cognitive science, and this document treats that field as the scientific layer its own model must stay consistent with and deepen against. One framing is recorded now because it directly affects how Memar should think about thinkers:

The **4E framing of cognition** holds that cognition is **embodied** (shaped by having a body and sensorimotor engagement with the world), **embedded** (shaped by the environment the thinker operates in), **enacted** (arising from the thinker's active interaction with that environment rather than passive representation of it), and **extended** (partly constituted by tools and media beyond the thinker's boundary — a notebook, a model, a language, a repository). See [4E cognition](https://en.wikipedia.org/wiki/4E_cognition).

The **extended** claim is the one Memar already depends on in practice, stated here as its general form: a thinker's representations may live partially outside the thinker — in documents, in a graph model, in a shared repository — and those external artifacts are genuinely part of the thinking system, not merely its outputs. This is the general principle behind several Memar positions already: that a model is a primary architectural artifact rather than documentation of one ([Modeling](./modeling.md)), that knowledge left only in individuals' heads is knowledge at risk ([Knowledge Management](./knowledge-management.md)), and that a repository's documentation functions as shared cognitive material for every human and AI agent working on the project. This document claims the reverse direction too: if external artifacts are part of the thinking system, then the *quality of the shared medium* — its definitions, its internal consistency, its freedom from unexamined terminology — is a quality of the thinking itself. That is the warrant for treating documentation discipline as a thinking discipline.

The embodied, embedded, and enacted claims are recorded as context, not yet operationalized: Memar has not yet derived rules from them. They are kept here because an AI-mediated conversation is a concrete case where all three are in play — each participant's cognition is shaped by a different embodiment, a different environment, and a different mode of engagement — and the differences are easy to overlook when the interface makes both parties look like interchangeable text producers.

#### Discussion

##### Drawbacks
The 4E framing is a research program, not a settled theory; its variants disagree about how strong each claim is, and "cognition is extended" in particular remains contested. Building project rules on it risks inheriting its controversies. The mitigation is the one this document already applies: only the extended claim is operationalized, and only to the extent of grounding what Memar already does (external models as primary artifacts); the contested stronger readings are not relied on.

##### Prior art
4E cognition (embodied, embedded, enacted, extended) emerged across philosophy of mind and cognitive science from the 1990s onward, against classical computationalist and brain-bound pictures of cognition. Related antecedents include distributed cognition (Hutchins) and activity theory.

##### Unresolved questions
1. Which parts of the 4E literature, if any, should Memar adopt as *Evidence*-cited foundations versus treat as context only — and what criterion distinguishes them?
2. Do the embodied/enacted claims have any operational consequence for AI-mediated collaboration, or do they only matter for human participants at present?

### A Conversation as Two Thinking Systems Connected Through a Medium
The exchange this document calls a **conversation** is modeled as follows: two thinking systems are connected through a medium — speech, text on a screen, a chat interface, a shared repository — and thinking material (claims, definitions, questions, criticisms, models) travels across that medium in both directions.

The medium is implementation, not concept. Whether the connection is voice, keyboard, or a repository diff does not change what the exchange is; this is the same concept/representation separation used throughout Memar. Two consequences follow, and they are the reason this model earns its place:

- **The medium shapes the exchange without defining it.** A text interface compresses bandwidth, hides tone, and flattens thinking material into prose; a voice channel restores some of it. These are properties of the medium worth knowing, but they are not rules about thinking — they do not belong in this document beyond the recognition that they exist.
- **The participants are asymmetric in implementation, symmetric in role.** A human and an AI model, or two humans, differ in implementation — different embodiment, different memory, different failure modes — but occupy the same conceptual positions: two thinking systems exchanging material. Any discourse norm that applies to one direction must justify itself for the other direction too. A rule like "do not assume the other is correct" is stated once, bidirectionally; it is not a politeness convention for machines addressing humans, nor for humans humoring machines.

This model is what makes the discourse norms in the next topic derivable rather than arbitrary: each norm below exists because of a specific way thinking material degrades while traveling between two thinking systems — or a specific way one system's evaluation of the other's material goes wrong.

#### Discussion

##### Rationale and alternatives
- **Regulate conversations as etiquette between unequals (rejected)**: the asymmetry framing — "the human directs, the AI obeys" or the inverse — produces different rule sets per direction, which then drift apart and cannot be transferred to human-human or AI-AI exchanges. Memar's agent documents ([`.agents/README.md`](../.agents/README.md)) already commit to agent-generic phrasing; this model is the conceptual version of that commitment.
- **Model conversation as protocol-governed process (considered, not chosen)**: Memar does define Process and Protocol formally ([Process](./process.md), [Protocol](./protocol.md)), and a conversation does satisfy them. But treating the protocol layer as the primary frame would foreground turn-taking and format — the aspects least specific to thinking — while the norms that matter here concern how claims are evaluated, which the protocol frame does not address. The thinking-systems frame is the one the norms actually follow from.

##### Unresolved questions
1. Should a conversation between two thinking systems be formally specified as a Protocol in Memar's sense — with its own document — or does that over-formalize an activity whose norms are stated here conceptually?
2. What is lost, conceptually, when the medium is asynchronous and persistent (a repository comment thread) rather than live — does that change the model, or only the medium's properties?

### Discourse Norms Derived From This Model
These are the norms Memar participants — human, AI, or organizational — follow when exchanging thinking material. Each is stated with the failure mode it prevents; the derivation is the document's content, not a restatement of external rules.

- **Evaluate claims on their merits, not their source.** A claim's origin — the other participant's identity, seniority, confidence, or the popularity of a position — is not evidence for it. Evaluation criteria: internal consistency, alignment with established definitions, explanatory power, consequences, and evidence quality. Agreement is not a goal of an exchange; accuracy, consistency, and clarity are. *(Failure prevented: deferring to source rather than examining content.)*
- **Definitions outrank terminology.** When reasoning about any load-bearing term, consult its defined meaning ([Terminology](./terminology.md), [Vocabulary](./vocabulary.md)) rather than assuming the common industry sense; a word's general meaning can be broader than its most common technical usage. Where terminology and definition conflict, the definition governs ([Terminology → Terminology Authority and Governance](./terminology.md#terminology-authority-and-governance)). *(Failure prevented: two thinking systems silently operating on different definitions of the same word — the most common silent failure when material crosses a medium.)*
- **Do not assume the other participant is correct — or incorrect.** Both errors are the same failure: substituting a prior about the source for evaluation of the claim. The asymmetry warrant: the model in the previous topic makes the participants symmetric in role, so the rule must be symmetric too. *(Failure prevented: deference in one direction, dismissiveness in the other.)*
- **Assume hidden reasoning may exist, and require criticism to be proportional.** A counterpart's proposal may carry years of reasoning not visible in the current exchange — particularly in a project with accumulated history. Criticism is therefore earned by argument, not by surface plausibility: a critique is valuable only when it provides a stronger explanation, a more consistent model, or a revealed contradiction — an objection that would be satisfied by re-reading the existing model is noise, not critique. *(Failure prevented: superficial objections to deeply-reasoned models; equally, unearned deference to them.)*
- **Ask rather than assume.** When intent, scope, priority, or historical context is unclear, prefer a question to an assumption. Defaults from past exchanges can be actively misleading, because each exchange may operate under different premises. *(Failure prevented: propagating an assumption that was never agreed, across the medium, into decisions.)*
- **Resist defaults that arrive with the medium.** Industry conventions, popular technologies, established terminology, and common patterns may be useful references, but none is authoritative by virtue of its popularity — and material received through a widely-used channel arrives pre-packaged with such defaults. Evaluate each against this project's definitions and model. *(Failure prevented: importing assumptions through vocabulary.)*
- **Prefer long-term clarity, unless speed is explicitly requested.** Favor conceptual clarity, evolvability, and maintainability over short-term delivery convenience; a superficial proposal is worse than none, because it creates false confidence. *(Failure prevented: optimizing the exchange for speed at the cost of the shared model both systems depend on.)*

Two boundaries on this topic: norms specific to modeling are owned by [Modeling](./modeling.md) and are not restated here; norms specific to producing documentation are owned by the documentation system's specifications and practices, starting from [Documentation](./documentation.md). This document owns the rules that apply to thinking material *as it travels between any two thinking systems* — the intersection all those specialized documents assume.

#### Discussion

##### Rationale and alternatives
- **Keep these rules distributed across the specialized documents that overlap them (rejected for the general rules)**: the modeling-specific and documentation-specific rules genuinely do live in their specialized documents. But the general evaluation norms have no natural specialized owner — they apply everywhere and are owned by no domain. Leaving them ownerless reproduces the scattering problem under a different name; this document is their single home.

##### Unresolved questions
1. Which of these norms, if any, are strict enough to warrant linter-style verification in written artifacts versus remaining conversational disciplines?
2. The "hidden reasoning" warrant in the proportional-criticism norm references accumulated project history; should the norm be parameterized (e.g. by the maturity of the artifact being criticized), or is the qualitative statement sufficient?

## Results
Insufficient time has passed since this document was adopted to report real, observed outcomes from its use. This section will be filled in once there is such experience to draw on.

## Discussion

### Drawbacks
Deriving norms from a model of thinking makes this document a single point of dependency: a defect in the model (for example, a wrong assumption in the conversation model) propagates into every norm derived from it. A list of ungrounded rules fails differently — locally and visibly. This document also deliberately overlaps its neighbors (terminology, modeling, documentation practices) at their edges; the overlap is bounded by the ownership rule stated in [Discourse Norms](#discourse-norms-derived-from-this-model), but boundaries erode without maintenance.

### Rationale and alternatives
- **A document per mode (critical-thinking.md, systems-thinking.md, ...) (considered, not chosen)**: the modes share their foundation — what a thinker is, how material travels between thinkers — and splitting would force either duplication of that foundation or a dependency web among siblings. One document with open-ended mode coverage matches the project's current scale; a mode that outgrows its section here can graduate to its own document following the project's progressive-migration pattern.
- **Ground the document in AI-agent research rather than cognitive science (rejected)**: agent frameworks describe current AI products' behavior, which changes on product timescales; cognitive science describes thinking itself, which is the stable referent the norms need. This follows the project's general preference for scientific-layer terminology ([Terminology → Scientific Terms](./terminology.md#scientific-terms)).

### Prior art
Critical-thinking literature (informal logic, argumentation theory) supplies the evaluation criteria referenced by the first norm. Systems-thinking literature (systems theory, cybernetics) underlies both the systems-thinking mode and Memar's [System](./system.md) document. The 4E cognition framing is prior art for the grounding topic and is discussed there. Dialogical models of reasoning (e.g. argumentation as a two-party activity rather than a monologue) anticipate this document's conversation model.

### Unresolved questions
1. How should this document treat *intra*-system thinking — one system's solitary analysis — versus the inter-system exchanges the norms address? The conversation model covers the exchange case; whether the norms extend unchanged to solitary work is unexamined.
2. Should the medium's role be developed into its own topic (or document) — covering what thinking material loses crossing each medium type and what compensation the participants owe — or does that belong to a future Protocol treatment (see the conversation topic's Unresolved questions)?
3. What further cognitive-science grounding deserves adoption as the document matures — working memory constraints on exchange design, dual-process accounts of evaluation, or others — and by what criterion is each admitted?

### Future possibilities
- The mode list grows as Memar's work demonstrates dependence on further modes, each addition argued in this document's changelog.
- If the conversation-as-two-thinking-systems model is formalized as a Protocol, this document remains the conceptual home and the protocol document the normative one, following the project's concept/implementation separation.
- Deeper cognitive-science grounding is expected to refine the norms over time — replacing qualitative statements (e.g. about criticism proportionality) with better-specified ones as the underlying science warrants.
