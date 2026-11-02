---
Title: "UI Rule — A Widget Aggregates, a Service Does One Thing"
Labels: Draft
Start Date: 2026-10-30
---
# UI Rule — A Widget Aggregates, a Service Does One Thing
A rule of this repository, held for [Widget](../../widget/widget.md). It states where aggregation lives, because the widget document is silent on it and agents have placed aggregation in services.

## The rule
- **Aggregation is done only in a widget.** Joining the answers of several services, calling them in an order, branching on one answer to choose the next call, and keeping what they return between calls are the widget's work, and nothing else's. A task's status shown beside its likeness, a request checked by many checks before anything is written, and a conversation read from a timeline, content and text are each a widget.
- **A service does one definite thing and never aggregates.** It takes what it needs and returns one answer; it calls no other service to join an answer. A service that gathers several sources is several services and a widget over them.
- **A widget is stateful, and its state is not a type.** What passes between the services a widget composes within one operation is the widget's own state, held by it; it is not declared as a type of the domain the widget is in, and a member of it is not written again where its owner already declares it ([A concept has one owner module](../../../../knowledge/modularity/rules/one-owner/one-owner.md)).
- **A widget does not cache what services return.** The cache is the SDK's alone ([A Service's SDK Is the Only Place Its Answers Are Cached](../../../../process/service/rules/sdk-caches-answers/sdk-caches-answers.md)).
- **A widget is composed of widgets and services of other modules, and is not bound to a screen** ([Widget](../../widget/widget.md)); a widget of a domain composes its own services with the abstractions its neighbours' modules give.
- **A widget states its operation as methods,** in Khayyam, so that its inputs, outputs and order can be read and tested; embedding its parts alone says what it is made of, and not what it does.
- **A widget is a pluggable module's, or a core module's when a core domain needs it.** A widget that composes a pluggable module's services is pluggable; the kernel calls it never.

## Why it exists
The design of the making of a task (task 20261030-T094103Z-28324) gave a service the ranking of tasks and another the replay of a gate, each joining several services, and the owner corrected both: aggregation is the widget's. The widget document says nothing of this, and a reader took the word to mean only what is drawn.

## Keep it or drop it
An organization may let services aggregate and remain conformant to Memar's concepts, at the cost that a service then has no single reason to change and no single test.

## What this rule does not claim
- It does not claim a widget draws anything: a widget is not bound to the screen.
- It does not claim where a widget's state is stored; storing and retrieving belong to the owner of what is stored.
- It is enforced by no check this repository runs today.
