---
Title: "Software"
Status: Draft
Start Date: 2026-09-10
ID: 510422
---

# Software

## Abstract
This document establishes Software as a Memar concept: **the objective manifestation of a system of aggregated processes** — a system whose core is a composition of processes, given a durable, operable form. The positions recorded here as settled: software is not limited to the computer world — the computer is one execution substrate for software, the dominant one today, not the defining one — and "software ecosystem" is read through the [ecosystem](./system.md#ecosystem) definition the System document establishes, not through the industry's marketing sense. The document also anchors the software life cycle's concern space, using the IEEE software documentation family as its prior-art taxonomy, and maps what the framework already owns against what dedicated sessions still owe.

## Introduction

### Motivation
The word "software" carries heavy ecosystem ambiguity: industry usage oscillates between code, product, running system, documentation, and the whole lifecycle's output — and even the most experienced practitioners give inconsistent, vague answers when asked what software *is*. Every Memar document that touches deployment, lifecycle, tooling, or quality inherits whatever "software" means; without a concept-first definition, each inherits the ambiguity. This document records the definition Memar refines against, so the ambiguity stops propagating into downstream decisions.

### Methodology
The document was founded during the Immutable Infrastructure layering session: resolving where deployment governance belongs surfaced how much weight the words "software" and "ecosystem" silently carried, and the session's findings were recorded here so the dedicated session does not restart from zero. The settled positions were directed by Omid Hekayati; the IEEE software documentation family was adopted as the prior-art taxonomy; full definition refinement and lifecycle treatment are owed to dedicated sessions (see the paired [handoff](./software.handoff.md)).

## Explanation

### Software in Memar's sense
**Software is the objective manifestation of a system of aggregated processes.** [Process](./process.md) treats processes as composable; a software system's core is a composition of processes, and software is what gives that process system a durable, operable, transferable form — the form in which the process system's [Structure](./system.md#structure) (its capabilities and constraints) is stated, and from which its instances execute.

Two boundary positions follow, and are recorded as settled here. First, **software is not limited to the computer world**: the computer is one — today dominant — substrate for carrying and executing software, not the defining one; a defined organizational procedure encoded so that it can be operated, transferred, and executed by others is software in this sense as well. Second, **software is not its code alone**: for computer-carried software, code is one definitional artifact; the definition/execution boundary ([Type → Structure Is Fixed by Definition](./type.md#structure-is-fixed-by-definition)) applies to the software system whole — its definition (source, configuration, and the definition-time artifacts) and its execution (running instances) are distinct, and Structure enters execution only through the definition.

### The software life cycle, as prior-art taxonomy
The IEEE software documentation family is the mature taxonomy of the lifecycle concern space; it is prior art to examine, not authority to inherit. Each area will eventually receive Memar's concept-first treatment; the table records where the framework already owns each concern and where the home is still owed.

| Lifecycle concern | IEEE standard | Memar home today |
| --- | --- | --- |
| [Software requirements specification](https://en.wikipedia.org/wiki/Software_project_management) | IEEE Std 830 | [Modeling](./modeling.md) owns which concepts exist; a requirements body is largely modeled concepts and constraints ([System → Structure](./system.md#structure)). Full treatment owed. |
| [Software design description](https://en.wikipedia.org/wiki/Software_design_description) | IEEE Std 1016 | Design lands as Type decisions ([Type](./type.md), [Modularity](./modularity.md), the Khayyam documents). |
| [Software configuration management](https://en.wikipedia.org/wiki/Software_configuration_management) | [IEEE Std 828](https://ieeexplore.ieee.org/document/6170935/) | The framework's Immutable Infrastructure protocol document owns the deployment immutability rule; the lifecycle working-out is owed (see its handoff). |
| [Software test documentation](https://en.wikipedia.org/wiki/Software_test_documentation) | IEEE Std 829 | No home yet; owed. |
| [Software verification and validation](https://en.wikipedia.org/wiki/Software_verification_and_validation) | IEEE Std 1012 | Partially anchored: abstraction conformance ([Abstraction in Khayyam](./khayyam/abstraction.md)) is the compile-time verification face; the rest owed. |
| [Software quality assurance](https://en.wikipedia.org/wiki/Software_quality_assurance) | IEEE Std 730 | No home yet; owed. |
| [Software project management](https://en.wikipedia.org/wiki/Software_project_management) | IEEE Std 1058 | No home yet; owed. |
| [Software user documentation](https://en.wikipedia.org/wiki/Software_user_documentation) | IEEE Std 1063 | Partially owned: [Type Practice → Carrying Type metadata](./type.practice.md#carrying-type-metadata) covers human-facing companion artifacts per Type. |
| [Software review and audit](https://en.wikipedia.org/wiki/Software_audit_review) | IEEE Std 1028 | The documentation system's audit trail ([Changelog facet](./documentation-changelog.md)) is the artifact-history face; the review process owed. |

### "Software ecosystem"
As applied to software, "ecosystem" names the [ecosystem](./system.md#ecosystem) formed around software practice — the languages, tools, products, conventions, organizations, and communities interacting within the practice's shared environment — not a property of any single software system: a software system is a constituent such an ecosystem can form around, never the ecosystem itself. The marketing sense ("join our ecosystem") names a vendor's governed offering set, which is precisely not an ecosystem ([System → Ecosystem](./system.md#ecosystem), Colloquial usage); it is a Business Term and carries no weight here — where it is meant, the concrete relationships are named instead: the base document set, the framework's protocol documents, and the implementation repositories.
