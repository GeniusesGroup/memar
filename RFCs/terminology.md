---
Title: "Terminology"
Status: Proposed
Start Date: 2026-07-11
RFC Number: 495495
Applied to: ["*"]
Related RFCs: []
Contributor(s):
  - Name: "Omid Hekayati"
    URI: "mailto:omid@geniuses.group"
    Contribution: "Core concepts, terminology philosophy, architectural rationale, three-tier classification, critique of AI-drafted material, worked examples (heat pump, container/docker, cloud), position on independent AI review as interim external scrutiny."
    Tasks: []
  - Name: "ChatGPT"
    URI: "https://openai.com"
    Contribution: "Initial drafting, critique, synthesis"
    Tasks: []
  - Name: "Claude"
    URI: "https://claude.ai"
    Model: "Claude Sonnet 5"
    Effort: ""
    Contribution: "Critical review pass: flagged internal inconsistency in the Scientific-terms tier (conflation of mathematical, empirical, and philosophical epistemic categories), proposed explicit tier-assignment criteria for Technology and Scientific terms, identified inconsistency between an earlier draft's simplified Protocol example and the finalized Protocol RFC's ontology, grounded the concept-vs-representation pattern in genericized-trademark theory and prototype theory, reframed 'independent verification' to account for AI-assisted review as an interim mechanism for an open-source project without yet-active external human reviewers, and expanded the document from an outline into full explanatory prose."
    Tasks: ["critical-review", "clarification", "grounding-citations", "expansion"]
---

# Terminology

## Summary

This RFC establishes Memar's terminology philosophy: the position that the words used to name a concept are not a cosmetic layer sitting on top of architecture, but one of the forces that produces architecture in the first place.

Memar treats terminology as a first-class architectural concern rather than a communication detail. The terminology used to describe a problem directly influences the mental model used to understand it. That mental model subsequently influences architecture, implementation, optimization, decomposition, governance, and long-term maintainability. A team that names a problem badly will, on average and over time, build a worse system than a team that names the same problem well — not because the first team is less skilled, but because it is reasoning about a distorted object.

The purpose of this RFC is not to classify words for their own sake. The purpose is to improve reasoning quality by encouraging deliberate movement toward more fundamental concepts before selecting technologies, tools, products, standards, frameworks, implementation strategies, or vendors. Classification is a means to that end, not the end itself: a term's tier tells a reader how much architectural weight it should be allowed to carry, not merely which bucket it belongs in.

Memar distinguishes between three layers of terminology — Scientific Terms, Technology Terms, and Business Terms — and recommends that learning, modeling, and architectural reasoning begin from the most fundamental layer available. This three-layer model is a deliberate simplification. A more granular model is possible and is discussed later in this RFC (see "Why Three Layers, and Not More"); Memar adopts the simpler model because a workable, memorable classification that developers will actually use during real reviews is worth more, in practice, than a taxonomically perfect one that nobody applies.

### Core Principle

> Architectural quality is bounded by mental-model quality.

> Mental-model quality is bounded by terminology quality.

Therefore:

> Terminology is not merely a communication tool.

> Terminology is an architectural dependency.

Consequently, terminology decisions should be reviewed with the same seriousness as architectural decisions — the same scrutiny that would be applied to a choice of data model or a service boundary should be applied to the choice of the word used to describe that data model or that boundary.


## Motivation

Many software discussions begin with questions such as:

- Which language should we use?
- Which database should we use?
- Which framework should we use?
- Which cloud provider should we use?
- Which message broker should we use?
- Which orchestration platform should we use?
- Which AI model should we use?

These questions are frequently asked before the problem itself has been clearly understood. Memar considers this inversion one of the most common sources of architectural failure, because a developer who begins from tools inevitably inherits the assumptions, abstractions, limitations, terminology, and worldview of those tools before understanding the actual problem the tools are meant to serve.

As a result:

- The problem model becomes distorted, shaped to fit the tool rather than the reverse.
- Artificial constraints appear that have nothing to do with the original problem, only with the tool's implementation choices.
- Hidden assumptions become accepted as facts, simply because the tool's documentation stated them as if they were self-evident.
- Solution spaces become unnecessarily limited to whatever the tool's vocabulary can express.
- Optimization efforts target representations instead of problems — teams tune the tool rather than reconsider the model.
- Technology selection begins to drive architecture, instead of architecture driving technology selection.
- Products begin to redefine concepts, until the concept can no longer be described without describing the product.

Many failures that appear, on the surface, to be implementation failures are actually terminology failures that occurred much earlier, during model formation — long before a single line of code was written.

Representative examples of this substitution:

- Relation becomes synonymous with Table.
- Identity becomes synonymous with Primary Key.
- Service becomes synonymous with Microservice.
- Protocol becomes synonymous with API Specification.
- Graph ([Graph Theory](https://en.wikipedia.org/wiki/Graph_theory), [Graph Rewriting](https://en.wikipedia.org/wiki/Graph_rewriting)) becomes synonymous with Graph Database.
- Heat Pump becomes synonymous with Air Conditioner.
- Abstraction becomes synonymous with OOP.
- Container becomes synonymous with Docker.
- Cloud becomes synonymous with a vaguely defined collection of unrelated technologies.

Once these substitutions occur, architectural reasoning becomes constrained by implementations rather than guided by concepts. The remainder of this RFC exists to give Memar contributors a working vocabulary and a working discipline for noticing when this has happened, and for reversing it before it hardens into architecture.


### Terminology Debt

Terminology Debt occurs when a system, document, team, organization, or ecosystem accumulates ambiguous, overloaded, implementation-centric, product-centric, or commercially-driven terminology that obscures the underlying concepts those terms were originally meant to name.

Symptoms include:

- Persistent misunderstanding between contributors who believe they are discussing the same thing.
- Endless debates around definitions that never resolve, because the disagreement is actually about which concept the word refers to, not about the concept itself.
- Architecture driven by products rather than by requirements.
- Technology-first decision making, where the tool is chosen before the problem is fully stated.
- Conflicting interpretations of the same term across teams, documents, or even within a single document.
- Difficulty onboarding new contributors, who must absorb a private vocabulary before they can absorb the actual system.
- Growing dependence on tribal knowledge — understanding that lives in the heads of a few long-tenured people rather than in the words on the page.
- Repeated architectural disagreements caused by vocabulary rather than by engineering trade-offs.

Memar considers Terminology Debt a precursor to many forms of Technical Debt, not a parallel or unrelated category of debt.

> Technical Debt often originates from Terminology Debt.

This is not a metaphorical claim. A system cannot be consistently understood if its terminology cannot be consistently understood; and a system that is inconsistently understood by the people building it will, over time, accumulate structural inconsistency as a direct consequence — different contributors, working from different mental models of the same word, will make locally reasonable but globally incompatible decisions. By the time that incompatibility becomes visible as a technical problem (a data model that cannot represent a case someone assumed it already handled, an API boundary that leaks an assumption another team didn't share), the terminology failure that caused it may be months or years in the past and easy to miss entirely.


## Guide-Level Explanation

### Terminology Shapes Mental Models

Terminology is not neutral. It is not a label applied after the thinking is done; it participates in the thinking itself.

The words used to describe a problem influence:

- What questions are asked, because a question can usually only be phrased in terms of the vocabulary already available.
- Which assumptions remain hidden, because a word can smuggle in an assumption (for example, that a "cache" is inherently ephemeral, or that a "queue" is inherently ordered) without ever stating it explicitly.
- Which solutions appear possible, because a solution that has no name in the current vocabulary is much harder to notice, let alone propose.
- Which solutions become difficult to imagine, for the same reason in reverse.
- Which architectural patterns appear reasonable, because a pattern that matches the vocabulary's assumptions will look natural, and one that conflicts with them will look strange even if it is objectively superior.
- Which trade-offs become visible, because a trade-off can only be weighed once both sides of it have names.

Terminology is therefore an active participant in system design, not a passive record of decisions already made elsewhere. Two teams solving the identical problem, but describing it with different vocabularies, will frequently arrive at meaningfully different architectures — not because one team is wrong, but because the vocabulary each team used made different parts of the solution space visible.


### Concept-First Thinking

Memar promotes Concept-First Thinking: the discipline of understanding a problem at increasing levels of concreteness, in a fixed order, rather than jumping directly to the most concrete level available.

The preferred reasoning flow is:

**Problem → Concept → Scientific Principle → Technology → Tool → Product**

A short clarification on the first two steps, since they can look redundant at first glance: a **Concept** is the informal, working understanding of what is actually being dealt with — the rough shape of the idea before it has been made precise. A **Scientific Principle** is that same idea after it has been made precise enough to be stated, examined, and criticized independently of any particular problem instance. "I need to model things that point to other things" is a Concept; "this is a directed graph" is the same idea promoted to a Scientific Principle, because it now carries a formal definition, known properties, and a body of established results that can be consulted rather than reinvented.

Each layer should be understood before moving to the next. The goal is not to avoid technologies — Memar is, after all, a software framework that will eventually run on real technologies. The goal is to prevent technologies from defining the problem.

A concept should remain valid even if all current technologies implementing it disappeared tomorrow. A technology should be replaceable without invalidating the concept it implements. The more fundamental a concept is, the longer its expected lifespan tends to be — a relational join has outlived, and will likely continue to outlive, any particular database engine's implementation of it.

For this reason, Memar encourages investing learning effort into concepts before investing effort into technologies. This is not a claim that technology-specific knowledge is worthless; it is a claim about sequencing and about which knowledge is more durable and therefore merits earlier investment.


### Tool-First Thinking

Tool-First Thinking reverses the preferred sequence:

**Tool → Technology Assumptions → Artificial Constraints → Problem Definition**

Memar considers this an anti-pattern: a developer encounters a tool before understanding the underlying concept, absorbs that tool's specific assumptions as if they were properties of the concept itself, and then unconsciously lets those assumptions constrain how the actual problem gets defined.

Representative examples of this ordering error:

- SQL before Relation.
- OOP before Abstraction.
- Kubernetes before Distributed Systems.
- Air Conditioner before Heat Pump.
- Docker before Container.
- Container before Process Isolation.
- Microservice before Service.
- Cloud before Infrastructure Design.

In each pair, the item on the left is what most developers encounter first in practice, and the item on the right is the more fundamental concept it implements or specializes. The implementation must be derived from the concept; the concept must never be derived from the implementation.

A useful heuristic:

> If a technology disappears tomorrow, the concept should still make sense.

If the concept disappears together with the technology — if a developer genuinely cannot describe what they were trying to achieve without referring to the specific tool — the concept was likely never understood independently of that tool in the first place. This heuristic is a fast, practical test a contributor can apply to their own understanding before relying on it architecturally.


## Reference-Level Explanation

### Terminology Layers

Memar sorts terms into three layers. Each layer is defined below by what distinguishes it, not only by example, so that the classification can be applied to a term this RFC has not already listed.

#### Scientific Terms

**Definition:** A term qualifies as a Scientific Term when its meaning has been established, or is deliberately intended to be established, through a methodology characterized by explicit and falsifiable definitions, clearly stated boundaries and edge cases, openness to criticism and revision, and — where available — independent verification by parties outside the term's original author or authoring organization. Scientific Terms are not, by this definition, restricted to terms that already belong to an established academic discipline; a term Memar itself defines can qualify as Scientific if it is produced and defended through this methodology, rather than asserted by convenience.

Examples:

- Graph ([Graph Theory](https://en.wikipedia.org/wiki/Graph_theory), [Graph Rewriting](https://en.wikipedia.org/wiki/Graph_rewriting))
- Relation ([Mathematics](https://en.wikipedia.org/wiki/Relation_(mathematics)))
- Identity ([Identity Over Time — Stanford Encyclopedia of Philosophy](https://plato.stanford.edu/entries/identity-time/))
- State
- Information ([Information Theory](https://en.wikipedia.org/wiki/Information_theory))
- Constraint ([Constraint Satisfaction Problem](https://en.wikipedia.org/wiki/Constraint_satisfaction_problem))
- Classification
- Modularity ([Modular Design](https://en.wikipedia.org/wiki/Modular_design))
- Thermodynamics ([Thermodynamics](https://en.wikipedia.org/wiki/Thermodynamics))
- Aerodynamics ([Aerodynamics](https://en.wikipedia.org/wiki/Aerodynamics))
- Protocol — see the Protocol RFC, which established Protocol's definition precisely through this kind of methodology: competing candidate definitions were proposed, tested against counterexamples, and narrowed to one that survives them.

This list mixes concepts with quite different epistemic character — some are mathematical constructs with formal proofs (Graph, Relation), some are results of empirical, falsifiable science (Thermodynamics, Aerodynamics, Information Theory), and some are foundational or philosophical concepts (Identity, State, Classification) that have been examined rigorously for a very long time without ever converging on a single settled academic consensus, the way a mathematical theorem converges on a proof. Memar is aware that grouping these together as one "Scientific" layer is itself a simplification of exactly the kind this RFC warns against elsewhere — a full accounting would likely separate formal/mathematical terms, empirical/scientific terms, and philosophical/foundational terms into distinct sub-tiers, since a mathematical proof, a reproducible experiment, and a centuries-old philosophical argument are validated in different ways and offer different strengths of guarantee. Memar accepts this simplification deliberately, for the reasons given in the Summary and revisited in "Why Three Layers, and Not More" below, and flags the finer-grained alternative as an open question rather than pretending the single Scientific layer is internally uniform.

Scientific terminology is not considered infallible. Scientific models evolve and are regularly challenged; scientific communities regularly replace, refine, merge, split, and invalidate models that were once considered settled. Memar does not treat science as a source of absolute truth. However, scientific terminology is generally subjected to explicit definitions, reproducibility requirements, continuous criticism, clearer boundaries, stronger validation processes, independent verification, public scrutiny, and cross-disciplinary review — mechanisms that technology and business terminology are usually not subjected to with the same rigor or consistency. Memar therefore treats scientific terminology as the preferred foundation for learning, modeling, and architectural reasoning. This preference is pragmatic rather than ideological: the objective is not to be scientific for its own sake, but to maximize reasoning quality, and science currently offers the strongest known set of mechanisms for that purpose.

#### On Independent Verification, Today

The ideal Memar holds for a Scientific Term is the same ideal science holds generally: a definition that has survived scrutiny by parties with no stake in its author being right. In an established academic field, that scrutiny typically comes from peer reviewers, competing research groups, replication attempts, and years or decades of citation and critique by people the original author has never met.

Memar and the wider Memar/Khayyam ecosystem are, at the time of this RFC, a young, largely single-author body of work. Geniuses Group has published its RFCs and source code openly, and has publicly invited outside review; as of this writing, that invitation has not yet produced sustained external human review at the depth this RFC's own standard calls for. Waiting indefinitely for that review before treating any RFC's terminology as sufficiently scrutinized would stall a project that already has real, current dependencies, including startups building directly on top of Memar.

Given this, Memar currently treats structured critical review by independent AI systems — systems trained on broad, cross-disciplinary public knowledge, and with no organizational stake in Geniuses Group or in any particular RFC being accepted — as a working, interim form of independent scrutiny. This is explicitly not treated as equivalent to institutional peer review. AI-assisted review can surface internal inconsistency, missing counterexamples, unexamined assumptions, and relevant existing terminology or research the author was not aware of; it does not provide the sociological functions that give peer review much of its force — independent replication, competing incentives, professional accountability within a field, or scrutiny from someone who might actually be motivated to find the definition wrong. AI-assisted review is therefore a provisional mechanism, to be supplemented, and eventually superseded, by sustained human external review as and when the Memar community grows enough to provide it. An RFC that has only undergone AI-assisted review should be understood as having met a real but lower bar of "public scrutiny" than one that has also survived critique from humans outside Geniuses Group, and this RFC does not claim otherwise.


#### Technology Terms

**Definition:** Technology, for the purposes of this RFC, is **the application of knowledge — techniques, skills, methods, and processes — to develop (create or modify) systems, whether those systems are tools, artifacts, or bodies of engineering knowledge, in order to achieve a specific goal**. A Technology Term is, correspondingly, a term that names such an applied system, technique, or engineering approach, rather than the underlying concept that system was built to realize.

Examples:

- SQL
- REST
- Kubernetes
- Thread
- ORM
- Event Store
- Operating System
- Message Queue

By this definition, a term belongs to the Technology layer not because it lacks rigor — many Technology Terms have quite formal specifications, and some (REST, TCP) are backed by careful, well-argued documents — but because the term is defined relative to achieving a goal within an engineering context, and its meaning is bound up with implementation choices that are not forced by the underlying concept. An Operating System, for instance, is built from a large number of individually well-defined scientific and mathematical concepts (scheduling, virtual memory, process isolation), but "Operating System" itself names a particular bundling and engineering realization of those concepts for a particular goal (managing a computer's resources on behalf of programs), not a freestanding scientific concept in its own right. Two operating systems can make substantially different design choices about that bundling while both legitimately being called operating systems — which is not true of a mathematical relation, whose defining properties are not negotiable.

Many technology terms represent decades of accumulated practical experience, and they are usually closer to the implementation than to the underlying concept. Technology terminology should be used to implement concepts rather than to replace them: technology should explain *how* a concept is realized, not redefine *what* the concept means.

For example: a relation is not defined by SQL. A graph is not defined by a graph database. A process is not defined by an operating system. A protocol is not defined by a specific implementation framework. Technology can provide useful, even excellent, implementations of a concept; it should not become the source of conceptual truth for that concept.


### Business Terms

**Definition:** Business terminology includes commercial labels, industry narratives, consulting vocabulary, ecosystem movements, product families, and marketing-oriented abstractions. Business terminology is frequently optimized for adoption, market expansion, ecosystem growth, branding, communication efficiency, or product positioning, rather than for conceptual precision.

Examples:

- Agile
- DevOps
- NoOps
- Cloud
- OOP
- DDD
- UX
- Digital Transformation

Memar does not claim these terms are wrong or useless; many contain valuable ideas and hard-won historical lessons. However, because business terminology is optimized for adoption rather than precision, it frequently accumulates multiple meanings over time and should be treated with caution when used as a foundation for learning, modeling, or architectural reasoning.

Memar does not assume malicious intent on the part of anyone who coins or popularizes a business term. However, conceptual precision is often simply not the primary optimization target of business terminology, and a business term may become successful precisely *because* multiple groups can interpret it differently — ambiguity can widen a term's appeal even as it narrows its usefulness for precise reasoning. The result is often an illusion of shared understanding: multiple participants use the same word while silently referring to different concepts, and the mismatch only surfaces later, once it has already shaped incompatible decisions.


### OOP Warning

Object-Oriented Programming (OOP) deserves special attention as a worked case of Business/Technology terminology collapse, because it is one of the most consequential examples in software history.

Different languages, frameworks, books, vendors, and communities use OOP to mean substantially different things: classes, objects, encapsulation, inheritance, polymorphism, interfaces, message passing, design patterns, SOLID, and a long tail of language-specific conventions have all, at various points and in various communities, been treated as *the* defining property of OOP. As a result, OOP is no longer a precise conceptual term; it has become an ecosystem term, closer in kind to Agile or DevOps than to a scientific concept. Two developers may both sincerely claim to be discussing OOP while referring to substantially different ideas, and a disagreement between them about whether some design "is" or "is not" OOP is frequently a disagreement about vocabulary rather than about the design itself.

For this reason, Memar discourages using OOP as a starting point for learning concepts such as Abstraction, Identity, Classification, Modularity, or Composition. Those concepts should be studied directly, at the Scientific layer, before evaluating how any particular technology or ecosystem — OOP included — has chosen to interpret them. The concept is more fundamental than the ecosystem that references it; learning should begin with the concept, and only afterward should technology-specific interpretations be evaluated against it.


### Concept vs. Representation: Conceptual Leakage

A pattern recurs across this RFC's examples — Graph vs. Graph Database, Relation vs. Table, Container vs. Docker, Heat Pump vs. Air Conditioner: a broad, durable concept gets replaced, in everyday practice, by one narrow, popular representation of it. Memar calls this pattern **conceptual leakage**: the boundary between a concept and one of its implementations or representations erodes, until practitioners can no longer describe the concept without describing the representation, and properties that are specific to the representation get silently attributed to the concept as a whole.

It is tempting to describe this as the concept gradually "evolving" or "migrating" toward the representation, as though Container slowly became Docker over time, or as though a term's tier could shift as its most common usage shifts. Memar rejects this framing. The underlying concept does not change; a habit of speech changes, while the concept itself sits exactly where it always did, waiting to be reconstructed by anyone willing to look past the popular representation.

This is the same phenomenon familiar from everyday language, where a brand name displaces the generic word for an entire product category — a well-documented phenomenon in trademark law and linguistics known as a **genericized trademark**, or *genericide* (https://en.wikipedia.org/wiki/Generic_trademark). Aspirin, Kleenex, Thermos, and Escalator were originally specific brand names that the public now uses for an entire class of products, without the underlying products, or the identity of their original manufacturers, actually merging into one thing. In Persian, dish soap is very commonly called "Pak" or "Rika" regardless of the actual brand on the bottle, after two early market-leading products; the generic concept ("dish soap") and the brand names never actually merged — usage merely collapsed them in casual speech, and nobody seriously believes that a competing brand's dish soap has stopped being dish soap because it is not called Pak.

Container and Docker follow the same shape, in the opposite direction of specificity: Docker is the specific brand — one company's particular implementation of container tooling — and Container is the general concept it implements. The practical effect, though, is identical to genericization: practitioners reach for Docker's specific internals and guarantees when asked to reason about containers in general, rather than studying process isolation, namespaces, and control groups as concepts in their own right, independent of any single vendor's implementation of them.

This particular direction of leakage — a general concept being understood only through its single most familiar exemplar — also has a name in cognitive science: **prototype theory** (Eleanor Rosch, 1970s; https://en.wikipedia.org/wiki/Prototype_theory), a theory of categorization holding that human beings tend to organize a conceptual category not around that category's full formal definition, but around a graded sense of typicality centered on the category's most familiar, most representative member. Under prototype theory, once Docker becomes the most familiar exemplar of "container" for an entire generation of developers, Docker's specific properties — including properties that are implementation choices rather than guarantees of the underlying concept — get silently attributed to the category itself, simply because Docker is the example that comes to mind first.

Memar's response to conceptual leakage is not to wait for a term's usage to "settle," and not to track the term's "lifecycle" as though the concept itself were unstable — the leakage exists entirely in usage, not in the concept, and the concept was never actually in motion. The correct response is the same one this RFC applies throughout its worked examples: whenever a familiar, product-associated term is encountered, deliberately reconstruct its underlying concept from first principles — as this RFC does with Heat Pump, Graph, and Relation below — before relying on the term to reason architecturally.


### Architectural Rule

When learning, modeling, or making architectural decisions, Memar contributors should follow this order:

1. Identify the problem.
2. Identify the underlying concepts.
3. Identify relevant scientific principles.
4. Evaluate technologies.
5. Evaluate tools.
6. Evaluate products.

Reversing this order should require explicit justification — it is not forbidden, since real projects sometimes have real constraints (an existing technology commitment, a hard deadline) that legitimately force the order to be reversed, but the reversal should be a visible, acknowledged decision rather than an invisible default.

This rule does not prohibit the use of products, technologies, frameworks, or tools; Memar itself will eventually run on all of these. Instead, it defines the preferred *direction* of reasoning. The objective is to ensure that solutions emerge from the problem space rather than forcing the problem to fit a preselected solution.


### Examples

#### Heat Pump vs. Air Conditioner

The phrase "Air Conditioner" encourages product-centric thinking: it names a category of consumer appliance, not a physical process. The phrase "Heat Pump" encourages functional thinking: it names what the device actually does, which is move heat from one place to another using a refrigeration cycle, rather than "create cold," which is not physically what happens.

This difference in framing is not merely semantic; it exposes architectural opportunities that the product-centric framing tends to hide. Viewed as a heat-transfer system rather than a cooling product, additional possibilities become visible: heat recovery, thermal reuse, energy balancing, waste-heat utilization, and integration with larger environmental systems (for instance, routing recovered heat into a building's hot water system rather than simply venting it outside). None of these possibilities require new physics; they were always latent in the underlying concept. They become invisible, however, to a designer whose only available vocabulary is "air conditioner," because that vocabulary was never built to express them.

The product-oriented term narrows the solution space. The concept-oriented term expands it.


#### Graph vs. Graph Database

A graph is not a graph database. Graph concepts — vertices, edges, paths, cycles, connectivity, traversal, rewriting — exist independently of any storage engine, and predate every graph database currently on the market by decades. Graphs can be used for modeling, analysis, reasoning, transformation, and simulation, in contexts that have nothing to do with persistent storage at all.

Reasoning should begin with graph theory and graph transformation concepts before evaluating storage technologies. When "Graph" becomes synonymous with "Graph Database," architectural discussions become constrained by storage concerns — indexing strategy, query language, transactional guarantees — instead of by the conceptual structure of the actual problem. The concept becomes subordinate to one particular implementation of it. Memar considers this inversion undesirable, for the same reasons discussed in "Concept vs. Representation" above.


#### Container vs. Docker

Containers and process-isolation concepts exist independently of Docker, and existed as research and production ideas (chroot, jails, namespaces, control groups) well before Docker packaged them into a widely adopted product. Products frequently become substitutes for the concepts they implement; once this occurs, architectural reasoning becomes constrained by the product's specific ecosystem rather than by the underlying problem the product was built to solve.

This case is a useful reminder that even the underlying concept, once reconstructed, should not be treated as offering guarantees stronger than it actually offers. Container technologies are often assumed to provide guarantees they cannot fully deliver:

- Isolation may be partial rather than complete.
- Resources may still be shared at the kernel level even when they appear logically separated.
- Kernel-level interactions may remain coupled between containers that are otherwise treated as independent — for example, shared kernel-space buffers (such as those involved in the TCP stack) mean that genuinely clean separation is not always achievable, regardless of which container runtime is used.
- "Noisy neighbor" effects may persist even under nominal isolation, because the isolation is enforced by the same shared kernel that all containers on a host depend on.

A number of Linux kernel features aimed at stronger container-level isolation have historically been simplified or removed specifically because a fully correct, low-overhead implementation of the stronger guarantee turned out not to be achievable at acceptable cost. Therefore, even the reconstructed concept of a container should not be treated as an absolute abstraction boundary; architectural reasoning should remain grounded in the actual mechanisms involved (namespaces, cgroups, the shared kernel), not in the marketing-level promise of "isolation" that either Docker or the general term "container" might seem to offer at first glance.


#### Cloud

Cloud is a representative example of a highly adopted term with weak conceptual precision. The term may refer to infrastructure, virtualization, distributed systems, network services, utility billing models, managed services, or platform services — or, most commonly, some unstated combination of these, decided differently by whoever happens to be using the word at the time.

Popularity should not be mistaken for conceptual clarity. The widespread use of a term does not guarantee that all participants attach the same meaning to it; two people can agree enthusiastically that a system "should be cloud-native" while picturing entirely different architectures. Cloud is therefore a useful reminder that adoption and precision are not the same axis, and that a term can score highly on one while scoring poorly on the other. The "as-a-Service" family of terms that has grown up around Cloud (IaaS, PaaS, SaaS, and an ever-expanding list of others) tends to make this worse rather than better, since each new "-aaS" label further fragments an already imprecise term into an even larger set of loosely bounded sub-labels, with no widely agreed boundary between adjacent ones.


### Science as Methodology

Memar does not claim that science is always correct. Memar claims that science is currently the strongest known methodology for constructing reliable knowledge — a pragmatic claim, not an ideological one.

Science is preferred because it provides mechanisms for error detection, criticism, reproducibility, validation, revision, and knowledge accumulation that no competing methodology currently matches across all of those dimensions simultaneously. If an alternative methodology claims superiority, it should demonstrate stronger capabilities in knowledge generation, validation, error detection, reproducibility, and long-term reliability than science currently offers. Until such a methodology exists, scientific terminology remains the preferred starting point for learning and architectural reasoning within Memar.

This preference should not be interpreted as a claim that every scientific model is correct, nor that everything Memar labels a "Scientific Term" has been validated to the standard of a mature academic field (see "On Independent Verification, Today," above, for Memar's current, honestly limited, position on that question). It is a claim that the scientific process currently provides the strongest available framework for evaluating correctness, and that Memar's own terminology work should be held to that framework's standard as closely as the project's current resources allow.


### AI Implications

AI systems, including this RFC's own AI contributors, learn from text in proportion to how much of that text exists, not in proportion to how precise or well-validated that text is. This creates a plausible hypothesis: popular terminology may receive disproportionate weight in an AI system's responses compared to precise, less-frequently-discussed terminology, simply because the volume of marketing material, blog posts, and casual technical writing produced about a popular product term (Docker, Cloud) vastly exceeds the volume of rigorous material produced about the underlying concept (process isolation, distributed infrastructure) that the product term has come to stand in for.

Memar treats this as a working hypothesis about AI training dynamics, not as a settled or independently measured fact. No contributor to this RFC, human or AI, has direct, reliable introspective access to an AI system's internal weighting mechanisms sufficient to confirm this mechanism with certainty; it is inferred, plausibly but not conclusively, from known properties of how language models are trained on large, frequency-skewed public corpora.

Consequently AI systems, absent deliberate correction, often favor product-centric interpretations, technology-centric interpretations, industry-default assumptions, and common ecosystem narratives over concept-centric interpretations, scientific terminology, explicit definitions, and first-principles reasoning. This effect is expected to be strongest when terminology has accumulated multiple meanings over time — Cloud, OOP, Service, Protocol, Architecture, and Platform are all plausible candidates for this effect, precisely because each has a very large volume of loosely-defined, popularity-driven text written about it.

Whether or not the underlying mechanism is exactly as described above, the practical guidance for AI systems working within Memar does not depend on resolving that uncertainty: when evaluating a claim, an AI system should weight a source by its independent credibility and rigor — academic critique, formal specification, reproducible measurement — rather than by the source's popularity or by how many times a similar claim appears across the training corpus. A widely repeated marketing claim about a container runtime's isolation guarantees should carry less architectural weight than a smaller number of careful, technically grounded critiques of that runtime's actual kernel-level isolation properties, even though the marketing claim is, by volume, far more common. Popularity is evidence of adoption; it is not evidence of correctness. This is the same distinction this RFC applies to terminology generally (see Business Terms, above) applied specifically to how an AI system should weigh its own sources.

When ambiguity exists, AI systems operating within the Memar ecosystem should prefer the most fundamental interpretation available unless the surrounding context explicitly requires otherwise. Memar therefore encourages explicit terminology governance whenever AI systems participate in modeling, documentation, architecture, analysis, or design activities — including, recursively, the drafting and critique of this RFC itself.


### Architectural Review Guidance

During reviews, contributors should ask:

- Is this term fundamental or implementation-specific?
- Is this term overloaded — does it carry more than one distinct meaning depending on who is using it?
- Is this term hiding multiple concepts behind a single label?
- Is this term a product label masquerading as a concept?
- Can a more fundamental term improve understanding of what is actually being discussed?
- Are we reasoning from the problem, or from a tool we have already implicitly committed to?
- Does this term introduce hidden assumptions that nobody in the discussion has actually agreed to?
- Would the concept remain meaningful if the current technology naming it disappeared tomorrow?
- Is the evidence behind this term's usage weighted by how credible the evidence is, or simply by how often the term is repeated?

Terminology review should occur before architectural review whenever possible, because poor terminology often produces poor architecture, and correcting terminology after an architecture has already been built around it is significantly more expensive than correcting it before.


## Drawbacks

This approach increases documentation effort, learning effort, review effort, terminology analysis effort, and concept clarification effort. Discussions may initially become slower, because participants are encouraged to clarify concepts before proposing technologies, rather than jumping straight to a familiar tool. Some widely accepted industry terminology may require decomposition into more fundamental concepts before it can be used safely within Memar, which itself takes time and can feel, to a newcomer, like unnecessary ceremony around a word everyone already understands well enough for ordinary purposes.

Some participants may view this process as unnecessary complexity, particularly under deadline pressure, when a familiar but imprecise term would let a conversation move faster in the short term. However, Memar considers these costs significantly lower than the long-term costs of reasoning from distorted mental models, which tend to surface much later, much more expensively, and in a form that is far harder to trace back to its terminological origin. The objective of this RFC is not speed of discussion; it is quality of understanding.


## Rationale and Alternatives

### Why not simply use popular terminology?

Popularity does not imply precision. Many popular terms accumulate conflicting meanings over time precisely because their popularity is driven by broad appeal rather than by narrow, precise applicability. Popularity is therefore insufficient, on its own, as a foundation for architectural reasoning, even though it remains useful for other purposes (discoverability, communication with newcomers, marketing).

### Why not eliminate technology terminology?

Technology terminology remains necessary; implementation eventually requires technologies, and no system can be built entirely out of scientific principles without ever naming an actual technique or tool. This RFC only rejects allowing technology terminology to redefine foundational concepts. Technology is a consumer of concepts; it should not become the source of concepts.

### Why not eliminate business terminology?

Business terminology often carries valuable historical, organizational, operational, and commercial knowledge — Agile and DevOps, whatever their definitional instability, both encode real, hard-won lessons about how software gets built by actual teams under actual constraints. The problem is not the existence of business terminology; the problem is its misuse as a conceptual foundation. Business terminology can remain useful provided it does not replace more fundamental concepts in architectural reasoning.

### Why prefer scientific terminology?

Because scientific terminology is generally associated with stronger validation processes and clearer definitions than technology and business terminology. This does not make scientific terminology perfect; it makes it the strongest available starting point currently known, for the reasons discussed in "Science as Methodology" above.

### Why classify terminology at all?

Because terminology influences mental models, mental models influence architecture, and architecture influences system outcomes. Therefore terminology is an architectural concern, not merely a stylistic one. Classification provides a mechanism for evaluating terminology quality before it affects architectural decisions, rather than discovering the problem only after the architecture built on top of it has already calcified.

### Why Three Layers, and Not More

A more granular classification is defensible, and this RFC does not claim the three-layer model is the only correct one. The Scientific layer in particular could reasonably be split into mathematical/formal terms, empirical/scientific terms, and philosophical/foundational terms, since these are validated by different mechanisms and offer different strengths of guarantee (see the discussion under "Scientific Terms," above). Memar has deliberately chosen the coarser three-layer model — Scientific, Technology, Business — because a classification that developers will actually apply during a real review, under real time pressure, is more valuable in practice than a taxonomically complete one that is too elaborate to use consistently. This is a stated trade-off, not an oversight, and it is revisited in "Unresolved Questions" below.


## Prior Art

Most mature engineering disciplines naturally move from Scientific Principles, to Engineering Models, to Technologies, to Tools, before making implementation decisions. Structural engineering does not begin with CAD software selection. Aeronautical engineering does not begin with simulation tool selection. Thermal engineering does not begin with product selection. Software development frequently reverses this order and begins with tools — arguably because software's tooling is cheap and immediate to acquire in a way that a wind tunnel or a structural test rig is not, which removes much of the friction that would otherwise force earlier disciplines back toward first principles.

This RFC attempts to restore, within Memar, the direction of reasoning commonly found in mature engineering disciplines, while acknowledging that software's low barrier to tool acquisition makes this discipline harder to sustain than it is in fields where reaching for a tool prematurely is simply not an option.


## Unresolved Questions

- Should the Scientific layer eventually be split into mathematical/formal, empirical/scientific, and philosophical/foundational sub-tiers, or does the coarser single layer remain the right trade-off as Memar's documentation grows?
- Should terminology classification become part of RFC review checklists across all of Memar, not only as guidance within this RFC?
- Should Memar maintain a formal terminology registry?
- Can terminology analysis be partially automated — for example, by detecting when a general concept's mentions in a document correlate almost entirely with mentions of a single specific vendor or tool (a possible automated signal for conceptual leakage)?
- How should AI systems implement terminology weighting in practice, beyond the qualitative guidance given in "AI Implications"?
- Should future RFCs explicitly identify which terminology layer each of their key terms belongs to, as this RFC's own Protocol RFC arguably should have done and did not?
- Can terminology debt be measured, even approximately?
- Can terminology quality be objectively evaluated, or is evaluation of terminology quality itself inescapably a matter of expert judgment?
- At what point, if any, should AI-assisted review (see "On Independent Verification, Today") be considered to have been superseded by sustained human external review, and how would Memar recognize that point when it arrives?
- Should this RFC's Related RFCs field eventually reference a stable Framework/Language/OS relationship document, once that document has a settled RFC number and URI? At the time of this RFC's drafting, that document exists only as informal working material.


## Future Possibilities

- Framework-wide terminology registry.
- Automated terminology conflict detection.
- Automated conceptual-leakage detection, flagging documentation where a general concept is discussed almost exclusively in terms of one specific vendor or tool.
- AI-assisted concept tracing.
- Concept-to-technology mapping tools.
- Terminology linting as part of RFC review tooling.
- Auto-generated Memar glossary, tagged by terminology layer.
- Terminology debt assessment tooling.
- Architectural terminology review workflows.
- A documented convention, once RFC contributor governance is finalized, for distinguishing AI-assisted internal critique from sustained human external review in a contributor's listed effort — so that a reader can tell, at a glance, how much of "public scrutiny" a given RFC has actually received.


## Change Rationale

### Initial Version

Introduces Memar's terminology philosophy, terminology layers, terminology debt, concept-first reasoning, tool-first anti-patterns, scientific methodology rationale, terminology governance principles, and AI interpretation guidance.

Establishes terminology as a first-class architectural concern within the Memar ecosystem. Defines the relationship between terminology quality, mental-model quality, and architectural quality. Provides a foundation for future terminology governance, concept tracing, AI-assisted reasoning, and architectural review processes.

### Review Cycle with ChatGPT

Strengthened the Graph example to explicitly cite Graph Theory and Graph Rewriting rather than naming only the anti-pattern. Strengthened the Business Terms definition to describe business terminology as optimized for adoption and communication efficiency rather than precision, avoiding an unprovable claim about intent. Added Cloud and Container/Docker as worked examples. Established the dependency direction that other Memar RFCs should depend on this Terminology RFC, and not the reverse — including the explicit decision that the Protocol RFC should not be listed in this RFC's Related RFCs, since Protocol is a specific application of the principles established here, not a peer or a prerequisite.

### Critical Review Cycle with Claude

- Flagged that the Scientific-terms layer, as originally written, silently conflated mathematical/formal concepts, empirical/scientific concepts, and philosophical/foundational concepts under a single label, and added an explicit acknowledgment of this simplification along with a pointer to the finer-grained alternative, rather than presenting the layer as internally uniform.
- Added explicit, criterion-based definitions for the Scientific and Technology layers (rather than relying on examples alone), including a formal definition of Technology grounded in knowledge-applied-to-system-development-toward-a-goal.
- Resolved an open question about whether Protocol belongs in the Scientific layer despite not being part of established academic science, by clarifying that the Scientific layer is defined by methodology (explicit, falsifiable, criticized, revised) rather than by prior membership in an academic discipline — and added an explicit note on what "independent verification" and "public scrutiny" currently mean for Memar in practice, given that the project is open-source and publicly announced but has not yet attracted sustained external human review, and that AI-assisted review is being used as a provisional, explicitly non-equivalent substitute in the interim.
- Removed a deep "Protocol vs. API Specification" section that had begun restating and simplifying the Protocol RFC's own ontology within this document, consistent with the decision, above, that this RFC should not depend on or import content from other RFCs; a short one-line reference to Protocol/API-Specification confusion remains in the Motivation examples, without restating Protocol's definition.
- Reframed the "term migrates between layers" idea — raised and rejected during this review — into a named pattern, **conceptual leakage**, grounded in two established, citable frameworks: genericized trademark theory (for the general phenomenon of usage collapsing a broad and a narrow term into one) and prototype theory (for the specific case where a general concept is understood only through its most familiar exemplar, as with Container and Docker). This replaces any notion that the underlying concept itself changes over time.
- Marked the AI Implications section's core claim (that AI systems overweight popular terminology) as an explicit working hypothesis rather than a stated fact, consistent with Memar's general position that unvalidated claims should not be presented with more confidence than their evidence supports — including when the claim concerns an AI system's own behavior.
- Expanded the document throughout from an outline into full explanatory prose, per explicit request, without shortening or summarizing any previously agreed content.
