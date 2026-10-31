# Widget
A widget is the aggregator of services and of other domains' widgets: a named, stateful element that a piece of software hosts, and the only place where aggregation is done. Core domains need it, so it is a core part of `computer/ui` and not pluggable (owner, 2026-10-22). Home: `modules/computer/ui/widget`.

## What a widget is
- **Named, with application-wide identity.** One instance of a widget exists in an application; it is not a template instantiated per use with data passed in from above (that is a component, which the [GUI](../../../../modules-plugable/computer/ui/gui/gui.md#position-on-gui-architecture) position does not take).
- **Stateful.** A widget holds the state of its own operation between the calls it makes: where it is in its sequence, what the person has entered or chosen, and the values one call returned that the next call needs. This state is its own and is not declared as a type of the domain the widget is in ([A Widget Aggregates, a Service Does One Thing](../rules/widget-aggregates/widget-aggregates.md)). It is not a store of services' data: a widget acquires the data it needs from the services when it needs it, and the one place such data is cached is the SDK of the service ([State and the SDK cache](#state-and-the-sdk-cache)).
- **Not bound to a screen.** A widget need not draw anything. A voice, a command line and a program meet services through widgets as a screen does, composing them differently; how a widget is drawn is a realization's, and the realization is pluggable ([UI](../ui.md)).
- **Hosted by software.** A widget lives in an application ([app relation](../../software/edges/widget/widget.md)) and reaches services only through their generated SDK functions ([SDK](../../../process/service/rules/sdk/sdk.md)), so no widget knows a network exists.

## State and the SDK cache
The state of a widget is what its own operation is in: its position in the sequence, the input it was given, and the values it has carried from one call to the next within that operation. It is not a retention of services' answers: a cache belongs to the service's SDK alone, and a widget never caches, as the rule [A Service's SDK Is the Only Place Its Answers Are Cached](../../../process/service/rules/sdk-caches-answers/sdk-caches-answers.md) states.

## Aggregation
Aggregation is the widget's work and nothing else's: joining the answers of several services, calling them in an order, branching on one answer to choose the next call, and keeping what they return between calls. A task's status shown beside its likeness is a widget over two services; a request checked by many checks before anything is written is a widget; a conversation is a widget composed of widgets (its timeline, its content, its text). A service does one definite thing and never aggregates (owner, 2026-10-30). The rule, with its cost and what it does not claim, is [A Widget Aggregates, a Service Does One Thing](../rules/widget-aggregates/widget-aggregates.md).

## Composition
A widget is composed of the widgets and the services of other modules. A widget of a domain composes that domain's own services with the abstractions its neighbours' modules give, and it imports a concept from the module that owns it instead of declaring a copy ([A Concept Has One Owner Module](../../../knowledge/modularity/rules/one-owner/one-owner.md)). A domain does not know another domain's work; the composition is the widget's, and a page composes widgets only through their contracts ([Page](../page/page.md)). Whether a widget is core or pluggable is stated in [A Widget Aggregates, a Service Does One Thing](../rules/widget-aggregates/widget-aggregates.md).

## Operation
Embedding its parts says what a widget is made of and not what it does. A widget states its operation as methods in Khayyam, so that its inputs, outputs and order can be read and tested.

## Model
- `(software)-[:---]->(software_gui_widget)`
