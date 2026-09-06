# Rules protocols
Use `rule` domain to save protocols to call them in 
- When desire `Event` dispatched
- When any service(usually called by user e.g. voucher) ask to run
- in repeatable manner e.g. every one minute, everyday, ...

## Rule as a first-class graph node
The general principle — why a domain splits into **Code** (fixed structure: node types, edge types, mandatory relationships) and **Rule** (conditional, context-dependent policy), and why a Rule is modeled as a graph node rather than a hardcoded `if` branch or an external config file — lives in Memar: [Separating Structure (Code) from Policy (Rule)](https://github.com/GeniusesGroup/memar/blob/main/docs/modeling.md#separating-structure-code-from-policy-rule). Do not restate it here.

This module is the concrete home of that principle in the graph: a Rule is a node connected by an edge to the Code element (node type, edge type, or specific instance) it governs, so "which entities are subject to Rule X" is answerable by traversing the graph. Evaluating whether a Rule's condition holds at runtime is the job of a separate rule-engine component that reads Rule nodes from the graph — the interpreter, not the data.

## How Rules react (mechanics agreed with consumers)

- Events need no new types: service request/response pairs are themselves suitable events; a Rule may condition on a specific request (e.g. "a transaction request on account 235689").
- A Rule is an extension point, not the default processing path: the simplest transactions are processed by the kernel's foundational behavior; only edges like `condition_is` route a transaction through a Rule.
- A Rule may act before processing, after processing (post-booking), on a status change, on a request, or in reaction to another transaction — it is not limited to being a pre-condition.
- A Rule may ask the processor to re-invoke it, attach an additional transaction to the triggering one (processed after the main transaction), or produce transactions of its own (fee, legal block, release). It never modifies or rolls back the triggering transaction.

## Discussion

### Drawbacks

- Rule sprawl: making Rule a first-class node tempts modelers into turning genuinely universal constraints (which should stay Code) into Rule nodes, inflating the graph without benefit. The Code/Rule boundary test (below) is the guard and is still open.
- A Rule reachable by many edges can become a de-facto global event listener; without scope/trigger/ownership limits, the rules-engine can end up entangled with the whole architecture (raised during economics modeling of `condition_is`/restriction).

### Rationale and alternatives

- Rule-as-graph-node over a hardcoded `if` or an external config file: keeps "what is governed by Rule X" answerable by graph traversal and lets organizations install/remove policies without touching Code.
- Engine kept separate from data (interpreter vs data): this module stores Rule nodes only; evaluation is another component's job.

### Prior art

- Production-rule systems (e.g. RETE engines) and policy-as-code; the Memar Code/Rule split is the governing principle (linked above).

### Unresolved questions (not settled by this module; carried in Memar)

These are carried as unresolved in the Memar document; this module must not silently pick an answer:
- Internal representation of a Rule node's condition (declarative expression, external function reference, decision table, …).
- Conflict resolution when multiple Rules govern the same Code element (precedence, specificity, explicit override edge).
- Temporal validity of a Rule (effective date, amendment, repeal) and its interaction with historical edges created under a now-superseded Rule — the auditability concern that matters most for tax and dispute-resolution domains.
- The precise Code/Rule boundary test (when a condition is "conditional enough" to warrant a Rule vs. an inherent constraint that stays Code).
- Whether a Rule may attach to multiple independent events/triggers, or needs scope/ownership limits to prevent global-listener sprawl.
- Idempotency and race handling when multiple Rules react to the same event (double-fire prevention, reaction ordering).
- Authority and priority between competing Rules on the same trigger (who wins, who may override).

### Future possibilities

- A rule-scoping convention (which events a Rule may bind, who owns it) informed by the economics consumers (`transaction/condition_is`, `restriction/restricted_rule`, fee rules).
