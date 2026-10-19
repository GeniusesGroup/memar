# Storage
Memar provide local storage engine in many abstraction as low level as `Page` to many indexing packages. Organization provide upper layer to have distributed storage functionality.

Read more about storage on [Memar storage package]

## Idea backlog from service code comments

Nothing below is ratified. Prefer existing homes over inventing new modules.

### Async analytic query
- **Idea**: an async query that runs beside the normal query from the existing database and gets the long-time answer ready.
- **Review questions**: analytics is always pluggable - does this async query live in a pluggable analytics capability with core storage serving only the normal query path, and who owns the pre-computed long-time answers (derived data is removable cache, never core)?
