# Rule UML
[The Unified Modeling Language (UML)](https://en.wikipedia.org/wiki/Unified_Modeling_Language) is a general-purpose, object-oriented, visual modeling language that
provides a way to visualize the architecture and design of a system, similar to the function of a blueprint.

## Graph
- `(rule)-[:uml_is]->(object)`
- `(object)-[:is_uml_for]->(rule)`

## Policy (rule)
- The service called in the process of rule
- or action service
- e.g.
  - then call NotifyUser(UserID, InvoiceID)
  - then call UserEarnCoin(UserID, invoice.TotalPayment/1000)

## TODO
- 

## Fields
- 
