# Status

## What a status is
A status is a [label](../label/label.md) combined with a [rule](../../process/rule/rule.md). A label may carry a rule or none; a status almost always carries one, and when it attaches to a node it makes an [Event](../../process/event/event.md) spread and work start: a Task made Queued is taken by an agent in the order of its priority. A label that starts nothing is a label, not a status. A status is not a [Role](../../management/role/role.md), which is authorization.

Attachment is not this module's. Every status value is a label that takes the label `Status` on its definition ([Label → A name is one label](../label/label.md#a-name-is-one-label)), and a record takes that value only through Label's edge: `(thing)-[:label]->(queued)` with `(queued)-[:label]->(Status)`. This module does not introduce `:draft`, `:complete`, `:status`, or any other relation for the same fact. A second attach path is a duplicate and is refused ([A Fact in Code Is Written Once](../../../modules-plugable/knowledge/documentation/documentation.md#a-fact-in-code-is-written-once)). Intrinsic / Neo4j-style labels on a vertex with no edge are the same refusal.

What this module owns is the kind, the rule that may run on attach or on a move, and the event of a move. The move from one status to another is an event. A rule may allow or block that event. The rule lives with the event.

### Where a status is defined
This module holds the account of what a status is. Shared Status-kind words are declared as code under this module's `labels/` (see `labels/status_values.py`, `labels/shared_markers.py`). A domain declares the Status-kind labels that belong to it in that domain's `labels/` — never in a parallel `status/` vocabulary tree ([Label → Where labels are declared](../label/label.md#where-labels-are-declared)). Prose beside a word may stay in a subfolder of `labels/`; its Model cites Label's attachment and does not restate a relation. The domain's main document states the record. It does not repeat the status list.

### Asking which records carry a status
All laws that carry draft are the laws that took the draft label:

`(law)-[:label]->(draft)` where `(draft)-[:label]->(Status)`

The identity of draft is the label's identifier. A scan that must not walk that path every time is an [edges-shortcut](../../modules.md#edge-buckets) recomputed from those Label edges; the shortcut is never the source of truth.

## Policies (rules)
- A word used as a status takes the label `Status` on its definition, never beside every record that carries the word.
- Attachment of a status value uses only Label's `(thing)-[:label]->(label)`. No Status-owned edge type.
- Who set a status, when, and the chain of changes, if recorded, ride the event of the move — not a second attach mechanism.
