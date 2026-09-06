# Rules protocols
Use `rule` domain to save protocols to call them in 
- When desire `Event` dispatched
- When any service(usually called by user e.g. voucher) ask to run
- in repeatable manner e.g. every one minute, everyday, ...

## Rule as a first-class graph node
The general principle — why a domain splits into **Code** (fixed structure: node types, edge types, mandatory relationships) and **Rule** (conditional, context-dependent policy), and why a Rule is modeled as a graph node rather than a hardcoded `if` branch or an external config file — lives in Memar: [Separating Structure (Code) from Policy (Rule)](https://github.com/GeniusesGroup/memar/blob/main/docs/modeling.md#separating-structure-code-from-policy-rule). Do not restate it here.

This module is the concrete home of that principle in the graph: a Rule is a node connected by an edge to the Code element (node type, edge type, or specific instance) it governs, so "which entities are subject to Rule X" is answerable by traversing the graph. Evaluating whether a Rule's condition holds at runtime is the job of a separate rule-engine component that reads Rule nodes from the graph — the interpreter, not the data.

### Open questions (not settled by this module)
These are carried as unresolved in the Memar document; this module must not silently pick an answer:
- Internal representation of a Rule node's condition (declarative expression, external function reference, decision table, …).
- Conflict resolution when multiple Rules govern the same Code element (precedence, specificity, explicit override edge).
- Temporal validity of a Rule (effective date, amendment, repeal) and its interaction with historical edges created under a now-superseded Rule — the auditability concern that matters most for tax and dispute-resolution domains.
- The precise Code/Rule boundary test (when a condition is "conditional enough" to warrant a Rule vs. an inherent constraint that stays Code).
