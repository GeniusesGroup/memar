# Knowledge Management

**Status: composition bundle — deliberately NOT a module.** This bundle owns no kernel schema of its own (no node type, no edge type, no rule identity that only exists here). It is a named composition of capabilities that live in other modules, for the upstream organizational need: creating, converting, preserving, discovering, and revising knowledge across people and time.

## Why a bundle (not core, not a single pluggable)

Three layers in this repository:

| Layer | Location | What it is |
|---|---|---|
| **Core / kernel** | `modules/` | Domains that are core-by-necessity: removing one would force fabricating or distorting another foundational concept. |
| **Pluggable** | `modules-plugable/` | Independently modeled capabilities that attach to core (or to each other) through explicit relationships; installable/removable as a whole. |
| **Bundle** | `bundles/` | A named composition of several modules toward a higher-level requirement (e.g. bank, leadership, knowledge-management). The umbrella word lives here; the semantics live in the real modules. |

**Knowledge management** fails core-by-necessity: Content, Text, Task, Timeline, Status, Group, and related domains already hold the graph. KM does not introduce a new foundational quantity or holding type. It also fails as a *single* pluggable module: the practice spans creation workflows, tacit↔explicit conversion, sector adoption, change management, channel import, task-centric history, and multi-GUI projections — many capabilities, not one edge+processor. Like **bank** (compose account, transaction, settlement, …) or **leadership** (compose delegate, role, group, …), KM is the upstream composition that answers "how does this organization manage knowledge?" without reifying the umbrella as a fake kernel entity.

Memar owns the *concept* of knowledge and its modeling principles (`docs/knowledge.md`, resolve via Memar skill / local checkout). This bundle owns the *organizational practice* that consumes those principles against this repository's real modules.

## Composed modules (index — grow as design sessions land)

Structural / holding:

- [`modules/knowledge/content`](../../modules/knowledge/content/README.md) (+ [content.handoff.md](../../modules/knowledge/content/content.handoff.md)) — Content units, timelines attachment, document-model blocks, knowledge-capture decisions
- [`modules/knowledge/text`](../../modules/knowledge/text/README.md) (+ [text.handoff.md](../../modules/knowledge/text/text.handoff.md)) — human-readable tokens; other domains relate, do not own text bodies
- [`modules/knowledge/status`](../../modules/knowledge/status/README.md) — shared status machinery (including review/RFC-as-phase)
- [`modules/management/task`](../../modules/management/task/) (+ [task.handoff.md](../../modules/management/task/task.handoff.md)) — Task as work/knowledge unit; Discussion/Decision/Change association
- [`modules/management/timeline`](../../modules/management/timeline/) (+ [timeline.handoff.md](../../modules/management/timeline/timeline.handoff.md))
- [`modules/management/group`](../../modules/management/group/README.md) — membership; Task is additive over Group

Pluggable / temporary add-ons that the practice may install:

- [`modules-plugable/knowledge/channel-comms`](../../modules-plugable/knowledge/channel-comms/README.md) — temporary home for geniuses.group editorial framework until a permanent comms placement is chosen

GUI / projection (consumers of the same graph):

- [`modules-plugable/gui`](../../modules-plugable/gui/) (+ [gui.handoff.md](../../modules-plugable/gui/gui.handoff.md))

Also composed / related (seed mapping — grow as sessions land):

- `modules/knowledge/` siblings the practice may speak: knowledge_unit, question, answer, skill, label (alongside content, text, status already listed)
- `modules-plugable/management/meeting`; `modules/management/staff`, `department` — conversation→Task and personnel-transition preservation workflows
- `modules/identity/organization` — where the framing claim is argued against real org models

## Active design state

See [knowledge-management.handoff.md](knowledge-management.handoff.md) — migrated seed + brainstorm material awaiting dedicated design sessions. Design dialectic lives in that handoff's Discussion sections. Nothing in that handoff is fully ratified as a finished Explanation-facet document yet.
