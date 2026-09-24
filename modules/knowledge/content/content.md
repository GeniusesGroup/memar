# Content

## Idea backlog

Review discipline per modules/management/vocabulary-discipline.handoff.md. Nothing below is ratified.

- **Idea**: GUI widget limit forms `[comment, ---, forward_off] >>` and `[group, ---, forward_off] >>` — all comments in that group can't forward; policy text recorded: "No `comment` can made a relation to this `comment` with `forward` label."
- **Review questions**: widget = GUI-side surface, not a core edge — who enforces `forward_off`: a rule on the existing [forward](edges/forward/forward.md) edge (core never knows rule; the group list is a parameter ⇒ one rules module + configuration) with the widget only surfacing it in the pluggable GUI, or is all of this presentation configuration with nothing to model?
- **Idea**: GUI widget limit forms `[comment, ---, quote_off] >>` and `[group, ---, quote_off] >>` — all comments in that group can't quote; policy text recorded: "No `comment` can made a relation to this `comment` with `quote` label."
- **Review questions**: widget = GUI-side surface, not a core edge — does `quote_off` ride as a rule on the existing [quote](edges/quote/quote.md) edge (core never knows rule; group lists are parameters), surfaced by the GUI widget? Any semantics beyond presentation?
- **Idea**: GUI widget limit forms `[comment, reply_off, ---] >>` and `[group, reply_off, ---] >>` — all comments in that group can't get reply. The `Policy (rule):::` statement was left empty in the source — the `reply_off` policy text still needs authoring (forward and quote have theirs).
- **Review questions**: same placement question as forward/quote — a rule on the existing [reply](edges/reply/reply.md) edge, not a core widget edge; what should the `reply_off` policy say once authored — mirror the forward/quote wording, or does reply's standalone-thread rule demand something different?
- **Idea**: if a comment wants `text`, it MUST use the same UUID for the `text` domain (shared identity, not a copy); if a comment's text contains only emojis, show them larger than normal text.
- **Review questions**: same-UUID requirement = the comment node taking the text identity simultaneously (content multi-typing / reference-not-embed — the precedent recorded in [product.md](../../../modules/economics/product/product.md): a node can take Product and Content identities at once) vs a stored edge to a text node — which is it, and does it converge with the text-only ownership decision in [text.handoff.md](../text/text.handoff.md)? Emoji sizing is presentation → pluggable GUI only — confirm nothing to model?
- **Idea**: three reads of content — by type, by time, and by user plus type — returning content ids with offset and limit.
- **Review questions**: these reads are content's own lookup, not a GUI page. Does each read earn a module (analytics is always pluggable; a query with its own storage is a module), or are they one content read with parameters?
