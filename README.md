# Memar 
**Memar** is a computer software development **structure** document that gives you a [structuralism](https://en.wikipedia.org/wiki/Structuralism) mental model to understand the development model. The implementation version of Memar is used as the software development **framework**.

Memar is not an authority that decides reality. Memar is a framework for constructing, examining, and refining mental models about systems. The goal is not to eliminate ambiguity, but to make ambiguity visible, explicit, and subject to independent evaluation.

It will provide ZeroOps(zero operations), edge computing, ... that let you develop both server and client applications in any programming language without need to think more about any fundamental requirements, Just develop business services and user interfaces, build apps as OS images or OS applications and easily just run first server node and let it distributes by many factors with inside logics not need external decision makers (automating software deployment) like Kubernetes(K8s) but with some improvements.

## Why Memar Exists
Memar did not begin with the goal of creating a new programming language, framework, architecture methodology, or software platform. It began with a different question:

> How many of the concepts commonly accepted in software engineering are actually well-defined?

Throughout the history of computing, many concepts have become deeply embedded in industry practice. Terms such as architecture, framework, technology, relation, encapsulation, leadership, abstraction, and many others are widely used and often treated as self-evident. Memar started from the observation that widespread usage does not necessarily imply conceptual clarity. Many software projects operate within existing assumptions. Memar takes a different approach. Instead of starting from established terminology, it starts from definitions. Instead of accepting classifications, it asks how those classifications are justified. Instead of optimizing implementation details, it attempts to understand the underlying structure of the problem space.

This approach naturally requires crossing traditional disciplinary boundaries. Modeling, systems thinking, architecture, language design, knowledge organization, management, and software engineering cannot always be treated as isolated domains. Many of the patterns, ambiguities, and contradictions observed in one domain reappear in others. As a result, Memar is not primarily an exercise in specialization. It is an attempt to discover deeper structures that remain consistent across multiple domains.

The project assumes that meaningful progress often requires stepping outside existing conceptual systems and examining their assumptions from an external perspective. This process is difficult because it challenges ideas that are frequently treated as foundational, yet it is often the only way to expose hidden contradictions and create more coherent models. Memar therefore treats definitions as more fundamental than terminology, models as more important than implementations, and understanding as more important than convention.

## Goals
- Improves the quality of reasoning about systems.
- 
- Provide complete framework to develop any purpose distributed application with **low||no code**.
- No(minimum) dependency on any other repositories.
- Compile an application as **Unikernel** instead of regular OSs or containers binaries.
- Develop high available and distributed software without any admin in any infrastructure layers (DevOps culture goal).
- Let service developers act Lean and Agile in their organization.
- [Reinvent the wheel](https://en.wikipedia.org/wiki/Reinventing_the_wheel)

## Not Goals
- Not respect ecosystem word definitions

## Why Memar Insists on Precise Definitions
Memar does not assume that common industry meanings are correct. Terms are defined from first principles and may intentionally differ from conventional usage when conventional usage is ambiguous, inconsistent, or misleading.

Memar does not begin by asking how to build a system. It begins by asking whether the concepts used to describe that system are themselves well-defined.

Words like "system," "architecture," and "protocol" feel obvious — until two people, or two AI models, discover mid-conversation that they have been using the same word to mean different things. This is not a rare accident. It happens routinely, even among careful, experienced contributors, and even among AI systems trained on the same language. An ambiguous term does not just create confusion; it silently shapes the reasoning built on top of it, and that reasoning compounds as more decisions are layered above it.

Memar treats this as a structural risk, not a stylistic preference. Before any architectural guidance is given, the foundational vocabulary is defined as precisely as the current understanding allows — grounded, where possible, in established scientific and engineering traditions, and stated clearly enough to be challenged and revised.

This precision is deliberately domain-agnostic. Memar's core vocabulary is meant to serve anyone reasoning about systems — whether they are building software, designing a physical structure, or organizing a process — because the underlying concepts (system, structure, process, architecture) are not specific to any one domain. The goal is not to eliminate ambiguity entirely — that is not realistic — but to keep it as small and as visible as possible, so that development proceeds on a
shared, examined foundation rather than on assumptions no one stated out loud.

## How to Navigate This Documentation
Memar's documentation is intentionally decentralized: each concern is documented in exactly one authoritative place, and content is not duplicated across files to describe the same decision twice. This keeps every topic maintainable from a single source of truth, but it means no single file — including this README — gives a complete picture on its own.

If you encounter an open question, an ambiguity, or a topic that doesn't seem to be addressed in the file you're reading, do not assume it's unresolved:

1. **Search full-text across the documents, not by filename.** File names are descriptive slugs, not a topic taxonomy — a concept can live under a name you wouldn't guess. For example, questions about generics are addressed under *Polymorphism*, not under a file named "generics." Judging relevance by filename alone will cause you to miss existing answers.
2. **If a thorough search still doesn't resolve the ambiguity, open an issue.** Describe the specific ambiguity so it can be addressed — either by extending an existing document or by creating a new one.

This applies to human readers and AI assistants alike: don't infer the absence of a decision from the absence of a mention in the current file.

## Transition period
Since the Memar introduces all tools needed in software development and operation as a programming language([Khayyam](./Khayyam.md)) and OS([PersiaOS](./PersiaOS.md)) and network protocols like [Chapar](./chapar.md) or [GP](./networking-osi_3-Giti-Network.md), If any organization want to move to the Memar, we provide some exiting programming language implementation to smooth this period and use existing infrastructure like Golang and Linux and IP.

**But remember we don't suggest using this method in starting new projects.**

## Enterprise
Contact us by [this](mailto:ict@geniuses.group) or [this](mailto:omid@geniuses.group) or [this](mailto:omidhekayati@gmail.com) if you need enterprise support for developing high available and distributed software. See features available in enterprise package:
- Develop exclusive features in very short time
- Bug fixing quickly
- 

## Related Projects
- [Clive is an operating system designed to work in distributed and cloud computing environments.](https://github.com/fjballest/clive)
- [SQLc](sqlc.dev)
- [EntGo](https://entgo.io/)
- [go-zero](https://github.com/zeromicro/go-zero) as bad idea because of (microservice system), (fully compatible with net/http), (middlewares are supported), ...
or [really relativetime?? Why not monotonic time??](https://github.com/zeromicro/go-zero/blob/master/core/timex/relativetime.go)

## Word
Memar is the Persian word means [architect](https://en.wikipedia.org/wiki/Architect), That is a person who plans, designs and oversees the construction of buildings. To practice architecture means to provide services in connection with the design of buildings and the space within the site surrounding the buildings that have human occupancy or use as their principal purpose. Etymologically, the term architect derives from the Latin architectus, which derives from the Greek (arkhi-, chief + tekton, builder), i.e., chief builder.
