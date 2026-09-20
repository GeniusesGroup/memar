# Group
`Group` sits under the `management` domain (persons, other groups, or even whole organizations can be members). The conceptual `Organization` vs. `Group` distinction is settled and documented in [`modules/identity/organization`](../../identity/organization/README.md#organization-vs-group-conceptual-level); this file carries only the structural questions still open after source inspection.

## Decisions from Organization ideas backlog (2026-09-16)

- Task is not primitive: modeled as an additive entity over **Group** — participant/member management belongs to Group, not Task; Task itself is also a Content (needs human text, images, audio). *(decided — Group is the org repo's own concept; no Memar-side owner)*


## Resolved via source inspection
- **Department ↔ Group typing link**: `department_p.Model` embeds both `thing_p.Model` and `group_p.Model` (Go interface embedding) — Department is a Group (and a Thing) at the compile-time type level, not just conceptually. `label.go` additionally defines `department` as an edge label from Group, documented (in a comment marked "Policy (rule)") for organizational-chart display and staff-join purposes.
- **Containment membership vs. oversight membership — resolved direction**: proper modeling decomposes relationships into several small, single-purpose edges (e.g., membership + role as separate edges) rather than overloading one generic edge. A combined/derived-lookup edge ("edges-shortcut") may exist purely as a traversal optimization, but must never become the primary source of truth or influence core design.

## Discussion

### Drawbacks

- Decomposing membership into several small single-purpose edges (the resolved direction above) makes common questions ("who's in this group and in what role?") cost multiple traversals instead of one edge read; a shortcut edge mitigates this but must stay non-authoritative.
- Allowing org-as-member and group→parent hierarchy makes cycles structurally possible (see unresolved #4); any authority/access inheritance must guard against them explicitly.

### Rationale and alternatives

- Small, single-purpose edges over one overloaded generic edge: keeps each relationship's authorization and lifecycle independent and matches the graph-modeling principle that a bare generic edge (`member_of`, `related_to`) hides real semantics.
- Compile-time interface embedding (Department-is-a-Group) vs runtime type-upgrade via `edges-loop` is an unresolved mechanism choice, not a preference-free one (see #1).

### Prior art

- Organizational-chart and RBAC membership models; DAO/treasury and informal-group cases (below) are the stress tests that break registration-based assumptions.
- Spotify Model (Squads, Tribes, Chapters, Guilds) — cross-cutting group kinds over one generic group, explicitly not a tree; supports the "generic Group + distinguishing label" reading over separate entity types per group kind (from the 2026-08-04 Task Management discussion: groups are recognized by the labels they carry, and a Department is a Group that some authorized role has distinguished as such).

### Unresolved questions

1. **Static embedding vs. runtime type upgrade**: Department uses compile-time interface embedding, while the `task` module implements type-upgrade via a runtime graph `edges-loop` (a Thing dynamically acquiring a type via a graph edge). The general criterion for choosing one mechanism over the other is recorded as an open question in Memar ([modeling.md → Edge Types and Their Traditional Counterparts](https://github.com/GeniusesGroup/memar/blob/main/docs/modeling.md#edge-types-and-their-traditional-counterparts)); the working hypothesis (embedding when the type is definitionally always the parent; edge-loop when it may be acquired dynamically) is not yet confirmed.
2. **Oversight membership shape**: for an external organization acting as a committee's oversight member, does it get (a) a dedicated, standalone edge type (e.g., `oversees`) with no accompanying generic membership edge at all, or (b) both a generic `member_of` edge and an additional `oversees` edge in parallel? Not yet confirmed.
3. **Organization-to-organization business relationships** (franchise, sales agent, repair agent, etc.): should each business-relationship kind get its own dedicated edge type (a new kind requires a Code change), or one shared base edge (e.g., `business_relation`) plus a separate node/edge specifying the relationship's nature (a new kind is only a data addition, consistent with the Code/Rule boundary discussion)? Open, and in tension with the decomposition principle above.
4. **Cycle potential**: with org-to-org relation edges coexisting with `group→parent` hierarchies and org-as-external-member-of-group relations, cycles are structurally possible (e.g., Org A's committee has Org B as oversight member, and Org B's structure eventually relates back to Org A). Not necessarily a modeling flaw, but any algorithm that assumes membership implies inherited authority/access must explicitly guard against cycles. Is cycle handling already addressed elsewhere in the codebase, or must it become an explicit design consideration?
5. **Label-granting authority**: the structural reading above says a Department *is* a Group (type level); the discussion reading says a Department is a Group that an authorized role has *labeled* as one. Who may grant that label — which role/edge carries the permission — and is it the same mechanism that would distinguish other group kinds (squad, tribe, chapter, guild)?

### Future possibilities

- A cycle-detection/authority-resolution utility once the membership-edge set is fixed.
- Reconciling these membership edges with `rights/delegate` so oversight/authority is not re-derived per domain.

## Test cases any resolved criterion must pass
- A registered NGO
- A sole proprietorship (one person acting as an "organization")
- An unregistered street vendor collective
- A DAO (decentralized, pseudonymous, no legal registration, but persistent identity/treasury)
- An informal friend group chat / travel planning group
- A family unit
- A government agency
- A university committee with an external organization as an oversight member
