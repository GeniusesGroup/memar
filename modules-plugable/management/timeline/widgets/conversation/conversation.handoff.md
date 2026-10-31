# Conversation Handoff
Open work for [conversation.md](conversation.md). Entries are mutable current state, revised as each item moves and removed when it resolves or is dropped. See [handoff.md](../../../../../modules-plugable/knowledge/documentation/handoff/handoff.md) for what a handoff is.

## Topic & Purpose
What the conversation widget requires of the modules it composes and what is still tentative in it.

## Status
Active. Redesigned on the owner's ruling (2026-10-31) that a conversation is only a widget of the timeline domain. The first design, which declared an identity, a store, events, errors and two services of its own, was withdrawn as a second owner of what the timeline owns. Only `Share` is written and accepted by the analyzer (task `20261030-T163544Z-10624`).

## Decisions
- **Every task has a timeline of its own, and no timeline is shared.** The owner ruled (2026-10-31) that the identity of a task is also the identity of its group and its timeline. **Decided.**
- **A content may be placed in several timelines with a number in each,** and a parent can read the replies to a content it also holds. The number is per timeline ([Timeline Handoff](../../../../../modules/management/timeline/timeline.handoff.md), its open question on a number of a placement). **Decided** by the owner; the numbering is that question's.
- **The timeline's identity is a `ThingUUID`.** From the timeline decision that a thing, its timeline and its group share one id. **Tentative**; changing it costs the type of one argument.

## Required of the Composed Modules
Recorded as requirements; none is declared here. The parent task queues them.
- **Timeline.** The identity field of a timeline; a service that places a content in a timeline with the instant, and one that answers the placements in order.
- **Content.** Khayyam for a content: its identity, name, media type, the text it holds and the content a reply answers.
- **Text.** Services that make a text and read it by its id.

## Proposed Next Steps
1. The reading of a conversation: the contents of a task's timeline and the replies to its shared contents, once timeline and content declare their services.
2. The gap tasks of the owners; then the widget gains `Read` and `Say`, and `Share` composes the timeline's services.
3. The task domain imports the widget and drops its own conversation type.
