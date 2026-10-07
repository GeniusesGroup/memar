# Memar 
**Memar** is a system development **framework** as **structure** document that gives you a [structuralism](https://en.wikipedia.org/wiki/Structuralism) mental model to understand the development model.

Memar is not an authority that decides reality. Memar is a framework for constructing, examining, and refining mental models about systems. The goal is not to eliminate ambiguity, but to make ambiguity visible, explicit, and subject to independent evaluation.

## Why Memar Exists
Memar did not begin with the goal of creating a new programming language, framework, architecture methodology, or software platform. It began with a different question:

> How many of the concepts commonly accepted in engineering (building, software, ...) are actually well-defined?

Throughout the history of computing, many concepts have become deeply embedded in industry practice. Terms such as architecture, framework, technology, relation, encapsulation, leadership, abstraction, and many others are widely used and often treated as self-evident. Memar started from the observation that widespread usage does not necessarily imply conceptual clarity. Many software projects operate within existing assumptions. Memar takes a different approach. Instead of starting from established terminology, it starts from definitions. Instead of accepting classifications, it asks how those classifications are justified. Instead of optimizing implementation details, it attempts to understand the underlying structure of the problem space.

This approach naturally requires crossing traditional disciplinary boundaries. Modeling, systems thinking, architecture, language design, knowledge organization, management, and software engineering cannot always be treated as isolated domains. Many of the patterns, ambiguities, and contradictions observed in one domain reappear in others. As a result, Memar is not primarily an exercise in specialization. It is an attempt to discover deeper structures that remain consistent across multiple domains.

The project assumes that meaningful progress often requires stepping outside existing conceptual systems and examining their assumptions from an external perspective. This process is difficult because it challenges ideas that are frequently treated as foundational, yet it is often the only way to expose hidden contradictions and create more coherent models. Memar therefore treats definitions as more fundamental than terminology, models as more important than implementations, and understanding as more important than convention.

## Goals
Memar's purpose is a chain: reliable **knowledge** of reality, built and revised through **thinking**, at a quality that constitutes **intelligence**, exercised as **agency** toward goals beyond itself — ultimately the outcomes those agents pursue, such as quality of life. The goal is stated in full, with its rationale, in [Framework → Memar's Purpose Space](./docs/framework.md#memars-purpose-space-from-knowledge-to-agency); the concept homes are [Knowledge](./docs/knowledge.md), [Cognition](./docs/cognition.md), and [Agency](./docs/agency.md).

The engineering goals below are means to that end:
- Improves the quality of reasoning about systems.
- Almost no (minimum) dependency on any other repositories (frameworks).
- Let developers act Lean and Agile (not [agile-manifesto](https://agilemanifesto.org/)) in their organization.
- [Reinvent the wheel](https://en.wikipedia.org/wiki/Reinventing_the_wheel)

## Where Memar Stops, and Where Work Continues
Memar states the path; it does not hand over the finished work. Those are different deliveries, and the difference is one of cost rather than of coverage. A framework that carries a concept can show every project the shape that concept requires. It cannot hand that project a built system, a generated organization, or a running deployment without that becoming a product — and [Enterprise](#enterprise) is where that difference is settled. The components named there are developed under Geniuses Group, and the identity and structural core they are made from is developed in the [Organization](https://github.com/GeniusesGroup/organization) project, which is where an answer to the questions below is being built rather than described.

- **Every change, whatever its size.** No threshold below which the practice is skipped. A change's size is judged by the participant about to make it, from inside the exchange in which the change is proposed — and that judgment is one of the things least likely to be examined, because the exchange feels too small to hold one. A one-line edit to a definition is a large-scope change: [confirm before large-scope changes](./docs/cognition.md#confirm-before-large-scope-changes) turns on whether a change reaches beyond the instance, never on how many lines it takes. The cost of loading the practice is a few reads; the cost of a concept quietly redefined is carried by every document that cites it, and it is carried silently.
- **The finished delivery of a structure Memar names.** Memar states what a group's responsibilities are, what a model's boundaries are, what a protocol obliges a participant to do, and how far a development's expectations must be written before the work. Turning those statements into the organization itself, its generated modules, and its deployment is Enterprise work, and a project that wants it sooner pays for it rather than asking the framework again. Nothing here withholds the path; a project that follows the documentation arrives at the structure the generated system would have had. Knowledge work is the concrete case: the performed service over a live corpus — orientation, extraction, retrieval — is built in the Organization project and delivered under Enterprise, not specified here.
- **Subjects no Memar document governs.** Silence is not a claim in either direction: not that a decision is available, and not that it is unavailable. Report the absence ([report absence rather than supplying it](./docs/cognition.md#report-absence-rather-than-supplying-it)) and it becomes a question with an owner, which is the only form in which it can be answered.

This section is kept because a framework's own consistency claim is checkable only where it names its limits. A project that reaches a boundary here should be able to say which of the three it has reached, and should be told plainly rather than discovering the answer by finding nothing. Its counterpart — a maintained record of where Memar's own development has applied its stated goals and where it has not, including disciplines tried and abandoned — is anticipated work; see [Framework → Goal-Oriented Frameworks and Purpose Space](./docs/framework.md#memars-purpose-space-from-knowledge-to-agency).

## Not Goals
- Not respect ecosystem word definitions

## Why Memar Insists on Precise Definitions
Memar does not assume that common industry meanings are correct. Terms are defined from first principles and may intentionally differ from conventional usage when conventional usage is ambiguous, inconsistent, or misleading.

Memar does not begin by asking how to build a system. It begins by asking whether the concepts used to describe that system are themselves well-defined.

Words like "system," "architecture," and "protocol" feel obvious — until two people, or two AI models, discover mid-conversation that they have been using the same word to mean different things. This is not a rare accident. It happens routinely, even among careful, experienced contributors, and even among AI systems trained on the same language. An ambiguous term does not just create confusion; it silently shapes the reasoning built on top of it, and that reasoning compounds as more decisions are layered above it.

Memar treats this as a structural risk, not a stylistic preference. Before any architectural guidance is given, the foundational vocabulary is defined as precisely as the current understanding allows — grounded, where possible, in established scientific and engineering traditions, and stated clearly enough to be challenged and revised.

This precision is deliberately domain-agnostic. Memar's core vocabulary is meant to serve anyone reasoning about systems — whether they are building software, designing a physical structure, or organizing a process — because the underlying concepts (system, structure, process, architecture) are not specific to any one domain. The goal is not to eliminate ambiguity entirely — that is not realistic — but to keep it as small and as visible as possible, so that development proceeds on a
shared, examined foundation rather than on assumptions no one stated out loud.

## How to navigate Memar's content
Memar's written content is intentionally decentralized: each concern lives in one authoritative place, so no single file — including this README — is a complete picture. "Content" here is everything this repository has written, not only prose: the model definitions, the rule catalog, the protocol implementations and their sources, and the configuration a session is driven by are content too, and a reader who understood "documentation" as the Markdown under `docs/` would look in one place and conclude the rest was not written.

1. **Ask `memar`.** Memar installs one command, and it answers questions about its own content. Run `memar --help` for the list, or `memar <verb> --help` for one verb's own interface. Nothing needs to be fetched or configured first: the command is part of the checkout it answers for, so it works the moment Memar is on the machine.
2. **Search full-text across the content, not by filename.** File names are descriptive slugs, not a topic taxonomy — a concept can live under a name you would not guess, and under a folder you would not think to look in. Judging relevance by name or by folder alone will miss existing answers.
3. **If a thorough search still does not resolve the ambiguity, open an issue.** Describe the specific ambiguity so it can be addressed.

Agents working the Memar way follow [`.agents/skills/memar/SKILL.md`](.agents/skills/memar/SKILL.md), which routes into the live content of the repository through the same command rather than through memorized paths. Using Memar outside this repository is [Using Memar in another project](#using-memar-in-another-project).

Fair, public comparisons with projects often treated as substitutes for Memar live under [`docs/comparisons/`](./docs/comparisons/) — the method is [docs/documentation-comparison.md](./docs/documentation-comparison.md).

## Using Memar in another project
Memar is a development framework, not a host-tool plugin. There is one skill: it routes into this repository's live content; it does not carry a copy of it.

What someone needs in order to use it — getting Memar into a project or an agent app, what the executable helpers in [`.agents/scripts/`](./.agents/scripts/) are for, and the one environment variable that says where Memar lives on a machine — is the subject of [`.agents/scripts/README.md`](./.agents/scripts/README.md). Each of those scripts declares its own interface, and those declarations, not prose anywhere else, are the authority.

## System Categories

### Computer
The computer software implementation version of Memar is used as the software development **framework**.

It will provide ZeroOps(zero operations), edge computing, ... that let you develop both server and client applications in any programming language without need to think more about any fundamental requirements, Just develop business services and user interfaces, build apps as OS images or OS applications and easily just run first server node and let it distributes by many factors with inside logics not need external decision makers (automating software deployment) like Kubernetes(K8s) but with some improvements.
- Compile an application as **Unikernel** instead of regular OSs or containers binaries.
- Develop high available and distributed software without any admin in any infrastructure layers (DevOps culture goal).
- Provide complete framework to develop any purpose distributed application with **low||no code**.

#### Transition period
Since Memar introduces technologies needed in software development and operation, including the [Khayyam](./docs/khayyam/khayyam.md) language, an [OS](./docs/protocols/computer/os.md), and protocols such as [Chapar](./docs/protocols/net/chapar.md) and [Giti-Protocol](./docs/protocols/net/giti.md), an organization adopting Memar may choose the language and runtime that fit its existing stack and migration plan. Memar's concepts and protocols remain independent of any one programming language; Khayyam is one realization hosted in this repository.

**But remember we don't suggest using this method in starting new projects.**

## Enterprise
Some components named throughout Memar's documentation — **ChaparKhane** (the router / network-coordinator role) and **Achaemenid** (the application auto-generation mechanism) among them — are intended to be offered as commercial software by Geniuses Group. Wherever such names appear without further explanation, this is why: they are products in their own right, not merely documentation subjects.

This restricts no one. Organizations remain free to develop whatever implementations these open protocols require for their own needs. But part of this project is commercial by design, because Memar's continuous development depends on the support of the organizations using it: if you find the introduced protocols good, the way forward is not to implement them yourselves — it is to support us, so that Memar moves faster.

Contact us by [this](mailto:ict@geniuses.group) or [this](mailto:omid@geniuses.group) or [this](mailto:omidhekayati@gmail.com) if you need enterprise support for developing high available and distributed software. See features available in enterprise package:
- Develop exclusive features in very short time
- Bug fixing quickly

## Word
Memar is the Persian word means [architect](https://en.wikipedia.org/wiki/Architect) ([معمار](https://fa.wikipedia.org/wiki/%D9%85%D8%B9%D9%85%D8%A7%D8%B1)), That is a person who plans, designs and oversees the construction of buildings. To practice architecture means to provide services in connection with the design of buildings and the space within the site surrounding the buildings that have human occupancy or use as their principal purpose. Etymologically, the term architect derives from the Latin architectus, which derives from the Greek (arkhi-, chief + tekton, builder), i.e., chief builder — where *arkhe* (from the verb *arkhin*) carries the sense of "guiding" and "governing".

We chose this name for the framework because of the strong resemblance between the architect's role and the process that takes place in the world of computing.
