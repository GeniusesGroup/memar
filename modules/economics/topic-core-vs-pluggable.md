# Topic: Core vs Pluggable Boundary Criteria

Status: consolidated from the Account & Transaction modeling sessions (2026-08). These criteria decide what lives in `modules/` vs `modules-plugable/` and where a capability's files go.

## Core-by-necessity

A domain is core only if removing it would force the kernel to fabricate or distort another foundational concept. Importance, prevalence, or "every organization has it" are NOT criteria — payroll, VAT, and POS may be ubiquitous and still be pluggable. Current core of economics: `account`, `transaction`, `invoice`, `product`.

## A pluggable module owns its complete capability

If a relationship needs processing semantics to be meaningful, the edge and its processing live in the same module. Never split "edge here, behavior there". A module is independently installable, removable, and replaceable as a whole.

## Edge vs module

An edge becomes its own module when it carries independent domain semantics (identity, lifecycle, authorization, rules, processing). Purely structural or shortcut edges do not. Shortcut edges are owned and maintained by the capability module that gives them meaning (e.g. `cash_transaction` is maintained by the cash module), never as separate modules.

## No bare edges

An edge without identifiable semantics (who may create/remove it, what it triggers) must not exist. Apparent "simple" edges (`member_of`, `related_to`) are either real capabilities with rules or shortcuts over a deeper path.

## Placement by entry point

A pluggable module is filed under the domain through which it is instantiated (its primary integration point), even if it affects several domains. `cash` starts at an account; its transaction-side shortcut edges stay inside the same module.

## Pluggable must not mimic core namespaces

`modules-plugable/<category>/<core-domain-name>/...` is forbidden: it implies a pluggable "version" of a core domain that does not exist. Capability names, not domain names, label pluggable modules.

## Names are labels; UUIDs are identity

Two organizations may ship edges/modules with the same human name (`all_or_none`, `endorsement_in_favor_of`) but different UUIDs and different rule semantics. Never bind behavior to a name; bind it to the module/edge identity.

## Analytics is always pluggable

Analytics produces discovered/derived data (cache-able, removable) from acquired data; it is never core. A query with its own types, events, storage, and processing is itself a pluggable module. Domain-specific analytics may live inside their pluggable module (e.g. payroll analytics); cross-domain analytics live under the category's analytics namespace, named by the knowledge produced, not by the core domains traversed.

## Core never knows Rule

Core domains do not reference the rule domain directly; generic edges (e.g. `(transaction)-[:condition_is]->(rule)`) connect subjects to rule nodes, and the rules-engine decides semantics.

## Module skeleton

Every module follows one project-defined skeleton (manifest, edges, edges-loop, edges-shortcut, protocol, services, status — names under revision); modules must not invent private folder taxonomies.

## Related

- [topic-accounting-invariants.md](topic-accounting-invariants.md)
- [modules/computer/rule](../computer/rule/README.md)
