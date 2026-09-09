# Service

## Idea backlog from edge code comments

Raw proposals from comment notes inside edge .go files (comments remain in code as source). Review discipline per modules/management/vocabulary-discipline.handoff.md. Nothing below is ratified.

### Service relations - edges/service-relation-module.go, edges/service-relation-service.go
- **Idea**: service-to-module relations PartOf, DependOn; service-to-service DependOn.
- **Review questions**: do these duplicate module-level dependency semantics (see the reference-by-UUID rule in modules/economics/account/edges/bookkeeping/README.md - no embedded types across domains)?