---
Title: "Conversation"
Status: Draft
Start Date: 2026-10-31
---

# Conversation

## Abstract
A conversation is a widget of the [timeline](../../../../../modules/management/timeline/timeline.md) domain, not a concept of its own ([Widget](../../../../../modules/computer/ui/widget/widget.md)). It aggregates the services of timeline, of [content](../../../../../modules/knowledge/content/content.md) and, through them, of [text](../../../../../modules/knowledge/text/text.md), so that what is said about a task is placed, read and said across the timelines of the task and of its parent. It is pluggable, since it composes pluggable services and no core domain needs it ([A Widget Aggregates, a Service Does One Thing](../../../../../modules/computer/ui/rules/widget-aggregates/widget-aggregates.md)).

## Model
- The module declares no identity, field, store, event or error. The timeline's identity, storage and refusals are the timeline domain's, and the content and text it shows are theirs ([A concept has one owner module](../../../../../modules/knowledge/modularity/rules/one-owner/one-owner.md)).
- Every task has a timeline of its own, because the identity of a task is also the identity of its group and of its timeline (owner, 2026-10-31). No timeline is shared between tasks.
- A content may be placed in more than one timeline, and has its own number in each: the content that is number 128 in the timeline of a parent can be number 1 in the timeline of a child. A reply to it can be read by the parent, since the parent sees the contents replied to.
- What is called joining a conversation is therefore the placing of a content in the timeline of a task and in the timeline of its parent. [`Share`](conversation.kh) places a content in one more timeline and answers its number there.

## Saying and Reading
`Post` says a text into a timeline: it checks the text, creates its content and places it, and answers the placement's number; `Latest` reads the latest content of a kind. They are the verbs `memar conversation post` and `memar conversation latest`, whose helps say their words. The widget owns no check of a template: the check of a kind that has one is composed by name, and a general check by kind is owed by the [content domain](../../../../../modules/knowledge/content/content.handoff.md).
