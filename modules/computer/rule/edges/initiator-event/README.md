# Rule initiator - event
EntryPoint (EventBase) of the rule to execute. Rule engine Will execute rule when this event(data-type) event will dispatched.

## Graph
- `(rule)-[:initiator_by_event]->(event)`
- `(event)-[:event_initiator_for]->(rule)`

## Policy (rule)
- Trigger when desire `Event` dispatched
- The event initiator the process of rule
- Whenever the event dispatched, the rule will be executed.
- e.g. `RegisterNewInvoice`, ... dispatched

## Fields
- Like event dispatcher we need to let rule select when called e.g. before, async or after service logic execute.
