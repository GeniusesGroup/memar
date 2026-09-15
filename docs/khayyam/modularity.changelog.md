# Modularity in Khayyam Changelog

## Changelog

### Initial language-and-ecosystem modularity design
- Time: 2026-07-29T00:00:00Z
- Type: Added
- Cited:
  - [Khayyam — Programming Language](./khayyam.md) — Reference: defines the `in` inclusion mechanism whose modularity consequences this document explains.
  - [Encapsulation in Khayyam](./encapsulation.md) — Depends_on: provides the encapsulation context for keeping behavior and representation boundaries explicit.
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — claimed
  - [ChatGPT](../../CONTRIBUTORS.md#chatgpt) (GPT-5.5) — argued

#### What changed
- Created the Khayyam-specific modularity document, covering the separation of language inclusion syntax from storage and distribution concerns, package-elimination through explicit naming, and the proposed companion-manifest direction for dependency resolution.

#### Deliberation
- The original design decisions for Khayyam's modular-programming direction were claimed (Omid Hekayati).
- Alternatives were developed and revisions incorporated (ChatGPT).

---

### Aligned with the general Modularity document and current documentation structure
- Time: 2026-08-19T00:00:00Z
- Type: refactor
- Cited:
  - [Modularity](../modularity.md) — Depends_on: the authoritative definition of Module and Modularity; this document now retains only Khayyam-specific language and ecosystem consequences.
  - [Documentation — Explanation](../documentation-explanation.md) — Depends_on: defines the current Explanation-facet structure.
  - [Documentation — Changelog](../documentation-changelog.md) — Depends_on: defines this companion changelog as the home for provenance and revision history.
  - [How to make a new explanation document](../documentation-explanation.practice.md) — Reference: supplies the migration procedure.
- Propagates to:
  - [Modularity](../modularity.md): Done — the general document links to this document for the Khayyam language and ecosystem realization.
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — requested
  - [ChatGPT](../../CONTRIBUTORS.md#chatgpt) (GPT-5.6) — rewrote

#### What changed
- Reframed the document as the Khayyam language and ecosystem application of the general modularity model.
- Duplicated conceptual Module definitions — content that only redefined Module or modularity — were removed in favor of an explicit link to the authoritative Modularity document.
- The language-specific inclusion, naming, and manifest/resolution material was retained and clarified: the remaining content specifies the `in` boundary, naming without package context, and companion-manifest direction.
- Provenance was migrated out of front matter.
- This changelog was created.
- All obsolete internal numbered-document terminology was removed, with obsolete internal references replaced by `document` terminology.

#### Deliberation
- The migration to the current documentation methodology, a review against the general Modularity document, and the removal of obsolete internal numbered-document terminology were requested (Omid Hekayati).

---

### Restored the Manifest contract and ecosystem-coupling material
- Time: 2026-08-19T00:00:00Z
- Type: Fixed
- Cited:
  - [Modularity](../modularity.md) — Depends_on: distinguishes a Module's conceptual identity from its framework-level manifest representation.
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — reviewed
  - [ChatGPT](../../CONTRIBUTORS.md#chatgpt) (GPT-5.6) — rewrote

#### What changed
- The prior migration removed more than conceptual duplication: it also removed the substantive manifest content model and the comparative explanation of why Khayyam separates language grammar from ecosystem resolution.
- Both, being specific to Khayyam's language and framework boundary, are restored here: the full Manifest-as-Module-Contract model and the ecosystem-coupling comparison.
- The manifest was clarified as a formal external contract and representation of a Module, not the conceptual definition of Module itself; the document now preserves the distinction that Modularity defines what a Module is, while the manifest defines the external contract through which tools discover, validate, resolve, and consume it.

#### Deliberation
- The previous migration had removed valuable Khayyam-specific content while reducing general duplication (Omid Hekayati).
- The removed material was audited (ChatGPT).

---

### Completed a second loss audit after restoring the Manifest model
- Time: 2026-08-19T00:00:00Z
- Type: Fixed
- Cited:
  - [Modularity](../modularity.md) — Reference: supplies the shared conceptual methodology and the authoritative Module definition to which this document refers.
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — reviewed
  - [ChatGPT](../../CONTRIBUTORS.md#chatgpt) (GPT-5.6) — audited, rewrote

#### What changed
- The second audit distinguishes content that may be referenced from Modularity — the general definition of Module and the claim that physical representations do not define it — from content that remains necessary in this document.
- The latter content was restored: the Khayyam-specific Methodology section (the methodology for evaluating Khayyam language constructs), the explicit naming rationale (the naming consequence of having no package context), and the concrete motivation for a framework-level dependency resolver (the operational motivation for manifest-based resolution).
- No other original section was removed solely to shorten the document.

#### Deliberation
- The Methodology section and supporting rationale had still been lost in the first restoration (Omid Hekayati).

---

### Second migration wave: `## Discussion` retired per the finalized method
- Time: 2026-09-08T00:00:00Z
- Type: refactor
- Propagates to:
  - khayyam-modularity.handoff.md: Created - open questions and anticipated work moved there.
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) - requested
  - [OpenCode](../../CONTRIBUTORS.md#opencode) (qwen3.8-flash) - moved

#### What changed
- The body's fixed top-level sections are now Abstract, Introduction, Explanation, Results only; the document-level Discussion, the Naming Without Package Context topic's Discussion wrapper, and the Manifest as the Module Contract topic's Discussion wrapper were dissolved.
- Rejected-alternative records were relocated to this entry's Considered and not done, and comparative prior-art surveys to its Related work, each with the retired subsection it came from named.
- Open questions and anticipated work moved to the newly created paired handoff; the topic-level and document-level whole-file-inclusion questions were recorded there as a single question because they are one question.
- Premise and current-state-cost content folded inline: the practical concern that package context can be absent in review, search results, generated documentation, or an AI-assisted analysis, plus the naming-discipline and migration-verbosity cost, into the Naming Without Package Context topic; the manifest-and-resolver gap (unanswered operational cases) and the two-layer reading cost (postponed tooling ergonomics) into the Dependency Resolution and Companion Manifest topic; the accidental-second-language risk and the requirement that the eventual schema preserve the stated boundary into the Manifest as the Module Contract topic.
- Graduated content dropped rather than copied: the Drawbacks acceptance-reason clause (combining the layers would make distribution-policy changes language changes — already stated in Ecosystem Coupling); the document-level Rationale and alternatives (already carried by Relationship to Modularity, the Motivation's concern-layering statement, and the Inclusion Is Not Module Definition topic); and the document-level Prior art framing (already carried by Ecosystem Coupling).

#### Considered and not done
- **Conventional package and namespace systems as the language's primary source of semantic context (rejected; migrated from the Naming Without Package Context topic's retired Rationale and alternatives)**: they encourage prefix-reliant naming and couple a logical grouping mechanism to source organization. Khayyam instead requires meaningful entity names and uses `in` only to make the source dependency explicit.
- **Encoding source location or version information directly in an `in` address (rejected; migrated from the Manifest as the Module Contract topic's retired Rationale and alternatives)**: it makes an ecosystem convention a permanent part of the language grammar. A companion manifest keeps that policy external, allowing different build systems, package managers, deployment environments, and organizations to interpret or replace it without changing Khayyam syntax.
- **Treating a manifest as only a dependency lock file (rejected; migrated from the same retired subsection)**: consumers need more than a resolved source location — a stable way to discover a Module's identity, entry points, published contracts, capabilities, compatibility conditions, and integrity information.
- **Treating a manifest as the Module itself (rejected; migrated from the same retired subsection)**: the conceptual Module exists independently of whichever representation a particular toolchain uses.

#### Related work
- Go and Java rely on packages for organization and disambiguation. ES-module imports demonstrate one useful part of the alternative: an explicit import identifies where a dependency comes from without making a global package hierarchy the sole carrier of meaning. Khayyam applies the stronger requirement that the included entity's own name must remain meaningful without depending on such a prefix. (Migrated from the Naming Without Package Context topic's retired Prior art)
- Go's `go.mod`, Node's `package.json` and lock files, and Rust's `Cargo.toml` and `Cargo.lock` all place significant dependency-resolution data beside source code rather than inside their languages' import grammar. Khayyam follows the companion-manifest direction while avoiding source-level import strings that encode a distribution location or version. (Migrated from the Manifest as the Module Contract topic's retired Prior art)

---

### Orphan-rule realization: attaching methods to imported types
- Time: 2026-09-15T09:00:00Z
- Type: Changed
- Cited:
  - [Linter](../protocols/linter.md) — Consumed contract: the check is governance; this document owns the modularity claim.
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — decided (rule home is the subject's document)
  - [Grok](../../CONTRIBUTORS.md#grok) (Grok 4.6 via Cursor) — applied

#### What changed
- Inclusion Is Not Module Definition now states that attaching a method to a type imported from an external library or a different domain directory is syntax-legal and a governance failure (monkey-patching); the reference linter configuration warns or errors, and the repair is composition — content relocated from the retired Khayyam-shelf linter document.

