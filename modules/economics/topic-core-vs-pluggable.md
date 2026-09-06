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

## Parameters vs semantics

A difference in parameters → configuration/rule inside one module. A difference in processing semantics → potentially a distinct module. Example: VAT differs across jurisdictions mostly in products and rates (one VAT module + per-organization configuration), but if one jurisdiction requires a VAT line inside the invoice and another requires a separate invoice, that is a semantic difference — one module whose rule decides the output shape, or two modules.

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

## Discussion

### Drawbacks

- Core-by-necessity is argued, not measured; two modelers can disagree (invoice and product were both contested in the source sessions before settling as core).
- Entry-point placement is ambiguous for capabilities instantiated from two domains at once; the taxonomy can force a false primary.
- "Edge = module when it carries semantics" still needs a judgement per edge; without recorded rationale the repo drifts toward "everything is a module".

### Rationale and alternatives

- Importance/prevalence was rejected as the core test: payroll, VAT, POS are ubiquitous yet removable; making them core forces every organization to carry them.
- Filing pluggable edges under the core domain folder (`transaction/edges/endorsement`) was rejected: readers infer the core processor must know that behavior, and the core processor accretes organization-specific workflows one edge at a time.
- Splitting an edge and its processing across modules was rejected: it creates half-modules that cannot be installed/removed as a unit.
- A `cross-domain` bucket was rejected: it becomes the home of things nobody understands; such capabilities need their own identity instead.

### Prior art

- DDD bounded contexts and plugin architectures — this model goes further: relationships (edges) are first-class module candidates, not just services.
- Labeled property graphs: edges carrying state (the bookkeeping edge holding Balance) is native practice.

### Unresolved questions

- Final module skeleton folder names (manifest, edges, edges-loop, edges-shortcut, protocol, services, status) — under revision in a separate session; `edges-loop`/`edges-shortcut` need precise structural definitions, not topical ones.
- Where does a capability instantiated from two entry points go?
- Does `analytics` get one namespace per category or one global analytics category?

### Future possibilities

- A "Module Contract" spec: manifest fields, allowed folders, machine-checkable placement rules.
