# Conversation Changelog

## Changelog

---

### The conversation is a widget of the timeline domain
- Time: 2026-10-31T12:00:00Z
- Type: added
- Cited:
  - [UI Rule — A Widget Aggregates, a Service Does One Thing](../../../../../modules/computer/ui/rules/widget-aggregates/widget-aggregates.md) - Reference: aggregation is the widget's, and a conversation is a widget
  - [A concept has one owner module](../../../../../modules/knowledge/modularity/rules/one-owner/one-owner.md) - Reference: the module declares nothing the timeline owns
- Tasks:
  - main:.agents/tasks/20261030-T163544Z-10624/: Partial - one method written; reading and saying wait for timeline and content
- Contributors:
  - [Omid Hekayati](../../../../../CONTRIBUTORS.md#omid-hekayati) — ruled that a conversation is only a widget of the timeline domain (2026-10-31)
  - An AI agent (Claude, model claude-sonnet-5-5 as reported by the runtime; no CONTRIBUTORS.md entry) — redesigned

#### What changed
- The first design, with its own identity, store, events, errors and two services under `modules-plugable/knowledge/conversation`, is removed. The widget with `TimelineOf`, later `Share`, is placed under `modules-plugable/management/timeline/widgets/conversation`.

#### Considered and not done
- The widget's reading and saying are not declared, because timeline and content hold no Khayyam to compose.

---

### Each task keeps its own timeline and the widget shares contents between timelines
- Time: 2026-10-31T13:00:00Z
- Type: changed
- Cited:
  - [Timeline Handoff](../../../../../modules/management/timeline/timeline.handoff.md) - Reference: a content is attachable to one or more timelines
- Tasks:
  - main:.agents/tasks/20261030-T163544Z-10624/: Complete - the owner's ruling applied
- Contributors:
  - [Omid Hekayati](../../../../../CONTRIBUTORS.md#omid-hekayati) — ruled that a task has a timeline of its own and a content may be placed in several (2026-10-31)
  - An AI agent (Claude, model claude-sonnet-5-5 as reported by the runtime; no CONTRIBUTORS.md entry) — applied

#### What changed
- `TimelineOf` is replaced by `Share`, which places a content in one more timeline and answers its number there. The open question on a shared timeline is resolved.
