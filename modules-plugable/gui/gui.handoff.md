# GUI Handoff

## Topic & Purpose
Org product GUI / projection requirements and second-pass Semantic UI bullets: GUIs as consumers of a semantic content contract, catalog hygiene, AI-era discovery discipline, upper-document principles, and the org's place relative to Memar. Migrated from the Organization ideas backlog (2026-09-16) and second-pass audit.

## Status
Active — multi-GUI / logical-snapshot decided; Semantic UI catalog ownership and org-vs-Memar UI placement remain open/direction.

## Decisions

### GUI / projection requirements for the org product

- Multiple simultaneous GUIs (GitHub-, Reddit-, Twitter-, Jira-like, forum, wiki, graph, timeline, kanban, file-explorer for legacy users) must be buildable over the same data; if they can't, the team is modeling UI, not domain. *(decided)*
- Repository-wide physical snapshots are replaced by logical snapshots: "show me all content states related to Task-42". *(decided)*

### Second-pass — Semantic UI / content-modeling (from `content - chat context.md`)

- **The org's GUIs are consumers of a semantic content contract, not owners of one.** The catalog
  work (discovering the small set of primitives under HTML/ARIA/DOM conventions — Reference+Locator+
  Affordance for links, State vs Role vs Capability, Addressability as the shared primitive of text
  fragments and widgets) must finish discovery before any org GUI locks in a projection. The org's
  multiple GUIs (GitHub-, Twitter-, Jira-like views) should render from the *same* discovered
  primitives, not from per-GUI vocabularies. *(direction; the catalog itself stays a Memar-side effort)*
- **Working catalog hygiene rule — keep the `Raw Name | Source | Candidate Primitive | Overlaps With |
  Status` columns.** When the org extracts any domain vocabulary (not just UI), record each candidate
  concept with its overlap-with field and status; the sessions rejected the premature six-way
  Type/Role/Capability/State/Relation/Rule matrix as final taxonomy, but the matrix survives as a *working
  lens* with recorded overlaps. *(accepted method from the session)*
- **AI-era discovery discipline: hypothesis-rejection rate is the real metric, not hypothesis-production
  rate.** A chatbot accelerates generating candidates as much as generating wrong candidates; a fixed
  rubric + stop criteria must gate batch classification regardless of speed. Applies directly to how
  the org runs AI-assisted requirement extraction and domain-modeling sessions. *(decided method)*
- **Upper document states principles, never instantiations.** Whatever top-level document governs a
  domain (UI, bookkeeping, tasks) must introduce the general principles and refuse positive per-case
  rules ("disabled is a State" never belongs there) — instances are discovered in the domain's own
  sessions. Also left explicitly open: whether a *new* upper document is warranted at all versus the
  domain being a plain instance of memar's `modeling.md` — decide per domain by what it genuinely adds.
  *(open; owner leaned "a document that only restates modeling.md must not exist")*
- **The org product's own place relative to Memar is undecided** — UI modeling could be a Memar layer
  (a UI concern in the main architecture) or an independent project on Memar like `organization`
  itself. Recording early prevented renumbering later; the same early-registration question applies to
  every future org sub-project. *(open for the org; the UI one specifically stays with its own repo)*

## Open Questions
- Whether a *new* upper document is warranted at all versus the domain being a plain instance of memar's `modeling.md` — decide per domain by what it genuinely adds. *(open; owner leaned "a document that only restates modeling.md must not exist")*
- **The org product's own place relative to Memar is undecided** — recorded above. *(open for the org; the UI one specifically stays with its own repo)*

## Related Artifacts
- [`../knowledge/content/content.handoff.md`](../knowledge/content/content.handoff.md)
- Memar Semantic UI / content-modeling work (catalog stays Memar-side)

## Notes
- Provenance: Organization ideas backlog → GUI / projection requirements + second-pass Semantic UI bullets (2026-09-16 migration).
- Multi-GUI / logical-snapshot dialectic expanded in KM bundle handoff Discussion sections: [`../../bundles/knowledge-management/knowledge-management.handoff.md`](../../bundles/knowledge-management/knowledge-management.handoff.md).
