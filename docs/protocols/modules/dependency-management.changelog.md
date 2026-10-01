# Dependency and Version Management Changelog

## Changelog

### Initial draft — the repository as the dependency mechanism
- Time: 2026-09-06T00:00:00Z
- Type: Added
- Contributors:
  - [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) — claimed, argued
  - [Super Z](../../../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — reviewed, rewrote

#### What changed
- Initial Draft positioning the version-control repository as the dependency mechanism — repository references, explicit pinning, local relative addressing — with the package-manager layer (registries, resolution, lockfiles) recorded as an unnecessary default and the strongest practical objections kept open.
- The position was stated as "the VCS is the mechanism", with the boundary rule (a dependency's internal structure is its own encapsulation) as the second load-bearing claim (Super Z).
- Registry-as-catalog (accepted) was separated from registry-as-infrastructure (rejected) so the position is not misread as rejecting discovery (Super Z).
- Semver was recorded as a claim rather than a guarantee (Super Z).
- The tooling gap (reference-refresh automation) was kept honest in the unresolved questions (Super Z).

#### Deliberation
- The position was brought from an extended public debate on package management: remote import paths break reproducibility and self-containment; transitive-resolution algorithms make every consumer responsible for conflicts in code it never calls; the VCS already provides pinning (submodule-style references, local relative addressing) and the package-manager layer re-solves that worse (Omid Hekayati).
- The position was defended through the debate's strongest counter-arguments (transitive pinning ergonomics, fork workflows, download cost) (Omid Hekayati).
- The genuinely open counter-arguments were accepted as open (Omid Hekayati).

---

### Documentation-method migration: rejected alternatives and anticipated work relocated
- Time: 2026-09-06T00:00:00Z
- Type: refactor
- Propagates to:
  - dependency-management.handoff.md: Done - anticipated work recorded there under `Anticipated Work`.
- Contributors:
  - [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) - claimed, decided
  - [Super Z](../../../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) - moved

#### What changed
- The body's `Discussion` wrappers dissolved entirely, per the finalized documentation method (documentation-explanation.changelog.md, same date) (Omid Hekayati - decided; Super Z - applied).
- The topic-level `Discussion`'s evidence paragraph (vendoring and monorepo one-version policies as evidence that explicit pinning and graph resolution are alternatives) folded into its topic as inline evidence (Super Z).
- The document-level `Drawbacks` removed from the body; its content preserved below without loss (Super Z).
- Rejected-alternative reasoning moved from the body's `Rationale and alternatives` sections into this entry's `Considered and not done`, without loss (Super Z).
- Anticipated work moved from the body's `Future possibilities` into the paired handoff's `Anticipated Work` (Super Z).

#### Considered and not done
- **Adopt the package-manager default (rejected)**: the costs above; the framework's posture - many small repositories, source-distributed, built with its own tooling - makes registry-centered resolution an ill fit by construction. (Omid Hekayati)
- **A hybrid of VCS references plus a resolution layer for transitive conflicts (rejected)**: re-introduces the second source of truth while keeping the VCS mechanism, inheriting both layers' costs. (Omid Hekayati)
- **Central registries for discovery (accepted as orthogonal)**: finding projects is a real need; a search index serves it without owning addressing, pinning, or resolution - the rejection is of registry-as-infrastructure, not registry-as-catalog. (Omid Hekayati)

#### Considered and not done (from the removed document-level Drawbacks section)
- **The position trades ecosystem compatibility for self-containment: a team whose other projects use package managers must maintain two dependency vocabularies** — the accepted trade. (Omid Hekayati)
- **The position inherits the VCS's ergonomics problems as its own** — this document treats that as honesty (the mechanism is what it is) while acknowledging that a purpose-built tool could smooth it without becoming a resolver. (Omid Hekayati)

---

### The manifest's identity and reachability, added to a document that names the VCS as the mechanism
- Time: 2026-09-30T00:00:00Z
- Type: Changed
- Ruling: owner, 2026-09-29
- Contributors:
  - opencode (space-bunny-free) - applied

#### What changed
- The 2026-09-29 rulings that bear on this document were recorded in its [handoff](./dependency-management.handoff.md) rather than in its body: the base an address is resolved from is the manifest of the module that wrote it; a manifest says everything about its own module in four obligations and is complete; a fault in one is a fault in the whole module; and its name is `memar.manifest.{format}`. They are in the handoff because they **collide with this document's stated position** — its Abstract names the version-control repository as the dependency mechanism and a manifest as machinery Memar's default does not require — and a reader of the body would meet a settled design and no sign of the conflict. The possible reconciliation, a manifest declaring identity and reachability while the VCS pins revisions, is recorded there as a question and is not adopted.
- A module claims an address by a pattern rather than by a row per declaration, and either a whole framework or each of its parts may be a module. The precedence question this raises, what answers when a whole's claim and a part's claim both cover one address, is recorded as open, along with the receiver's reading that a claim should be a path-shaped pattern rather than a regular expression — offered for the owner to accept or overrule, and not adopted.
- No sentence of this document's body changed, and nothing here supersedes its position.

#### Considered and not done
- **Writing the four obligations and the manifest's name into this document's body.** Considered and not done, because the rulings have not been reconciled with the position the body states, and stating them as current design would hide that. The alternative was to revise the position in place, which is a change to a protocol document and the owner's to make.
- **Creating a new document for the manifest.** Considered and not done: this document is already the subject, at ID 496870 since 2026-09-06. A second dependency document would have split one subject across two files and left a later session choosing between them.
