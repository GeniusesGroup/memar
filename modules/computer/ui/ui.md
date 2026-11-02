---
Title: "UI - User Interface"
Labels: Draft
Start Date: 2021-05-25
ID: 450528
---
# UI - User Interface
UI is how any agent (a person, a screen, a voice, a command line, a program) meets services. It is the concept; the GUI, the VUI, the command and the CLI are its realizations, each a module of its own, and this document is the concept's, not any one realization's. The concept has two core parts, [Widget](./widget/widget.md) and [Page](./page/page.md), which core domains build on and which are bound to no screen; the rest of a realization is pluggable. The position of the graphical realization is in [GUI](../../../modules-plugable/computer/ui/gui/gui.md).

## Widget
A widget is the aggregator of services and of other domains' widgets: it is named and stateful, and it is where aggregation happens. Joining the answers of several services, such as a task's status beside its likeness, is done only in a widget; a service does one definite thing and never aggregates (owner, 2026-10-30). A widget reaches services only through their generated SDK functions ([SDK](../../process/service/rules/sdk/sdk.md)), and it is not bound to a screen, since a voice or a command line composes the same services differently. What a widget is, how it is composed and how it states its operation are in [Widget](./widget/widget.md); where aggregation lives is the rule [A Widget Aggregates, a Service Does One Thing](./rules/widget-aggregates/widget-aggregates.md).

## Page
A page is an addressable composition of widgets with state and history ([Page](./page/page.md)). It belongs to the one domain whose subject it is, and it composes the widgets of other domains only through their widget contracts.

## Realizations
- [GUI](../../../modules-plugable/computer/ui/gui/gui.md) — the graphical realization, for a person at a screen.
- `command`, in `modules-plugable/computer/ui/command` — how a service is called from a command line.
