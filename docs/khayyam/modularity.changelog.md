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
  - [Qwen](../../CONTRIBUTORS.md#qwen) (qwen3.8-flash via [OpenCode](../../CONTRIBUTORS.md#opencode)) - moved

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
  - [Linter](../protocols/computer/linter.md) — Consumed contract: the check is governance; this document owns the modularity claim.
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — decided (rule home is the subject's document)
  - [Grok](../../CONTRIBUTORS.md#grok) (Grok 4.6 via [Cursor](../../CONTRIBUTORS.md#cursor)) — applied

#### What changed
- Inclusion Is Not Module Definition now states that attaching a method to a type imported from an external library or a different domain directory is syntax-legal and a governance failure (monkey-patching); the reference linter configuration warns or errors, and the repair is composition — content relocated from the retired Khayyam-shelf linter document.

---

### The `in` value is a URI: the language fixes no scheme for it, and the corpus is re-rooted
- Time: 2026-09-26T13:27:17Z
- Type: Changed
- Cited:
  - [Khayyam — Import Mechanism (`in`)](./khayyam.md#import-mechanism-in) — Depends_on: what this document's boundary is, in the language document's own words — the `in` value is a URI, and the scheme it is written in and the means of resolving it are the resolver's and its manifest's business.
  - [Khayyam — File Extension](./khayyam.md#file-extension) — Evidence: ".kh for files that have Khayyam language code" is a statement about what this project calls its files, which is a naming convention of the realization, not a rule about what a URI may contain.
  - [Khayyam — Separation of Syntax and Governance: A Principle](./khayyam.md#separation-of-syntax-and-governance-a-principle) — Evidence: the principle that fixes how much enters the grammar. Requiring a suffix is not separable from how a resolver finds things; a suffix is one of the things a resolver keys on.
  - [Modularity in Khayyam → Dependency Resolution and Companion Manifest](./modularity.md#dependency-resolution-and-companion-manifest) — Evidence: this document's own resolution boundary, which states the address/scheme/manifest separation the decision rests on.
- Propagates to:
  - docs/khayyam/khayyam.md: Done — the *Path shape* paragraph is replaced by *The path is a URI*, which states that the language fixes no scheme, points here for the manifest side, and points at *Minimal Legislation* for where a tool's own spelling rule lives.
  - docs/khayyam/khayyam.md: Done — the third `in` example in that list was re-rooted from `memar/` to `modules/`; the two examples beside it keep the `.kh` spelling, which is one well-formed URI among the ones a manifest may serve.
  - docs/khayyam/khayyam.changelog.md: Done — the *Minimal Legislation* entry of the same day carries the decision and this entry's position among its Considered and not done.
  - docs/khayyam/khayyam.handoff.md: Done — its mutual-`in` cycle question is untouched by this change, and its next step names the Import Mechanism itself rather than a revision of it.
  - docs/khayyam/modularity.handoff.md: Done — its "What is the exact `in` path shape?" entry states the ruling and carries what the manifest work leaves open.
  - modules/khayyam/core/src/frontend.ts: Done — the `import-path-shape` refusal and the exported `KHAYYAM_FILE_EXTENSION` constant it keyed on are removed, along with the `"import-path-shape"` member of `RefusalReason`. The frontend resolves the address it is given.
  - modules/khayyam/core/test/matrix.test.ts: Done — the two tests that asserted the extension refusal now assert acceptance of the same addresses, and the unresolvable-import fixture's address is re-rooted. No test was deleted.
  - modules/khayyam/execution.handoff.md: Done — its `in` failure-semantics entry states the rule the toolchain already matches (a URI carrying no extension and one carrying a foreign extension are accepted; only a URI with no file behind it is refused) and claims no `import-path-shape` check.
  - modules/**/*.kh: Done — 665 `in` URIs across 203 files re-rooted from `memar/` to `modules/`; see *What changed*.
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — decided (resolution belongs to the manifest; the language says the value is a URI)
  - [Space Bunny Alpha](../../CONTRIBUTORS.md#space-bunny-alpha) (space-bunny via [OpenCode](../../CONTRIBUTORS.md#opencode)) — argued, applied

#### What changed
- **The decision.** The value an `in` declaration carries is a *URI*, and the language says that much and no more: it fixes no scheme for it. Several URI schemes serve — a path relative to the repository root, an opaque identifier the manifest maps — and which one a project uses is dependency management's decision, not the language's. The scheme and the means of resolution are declared by the module manifest, which is itself a requirement and must therefore provide dependency management rather than leave it implicit. This repository writes its URIs as repository-root-relative paths, because they are readable and deterministic.
- **The corpus.** 665 `in` URIs in 203 `.kh` files were re-rooted from `memar/` to `modules/` — `memar/codec/string/protocol/string.kh` became `modules/codec/string/protocol/string.kh`, and so on for every URI whose first segment was `memar/`. The single URI already rooted at `modules/` (`modules/computer/datatype/protocol/detail.kh`) was left alone. No other content in those files changed: the rewrite was scripted, and the script reverted its own substitution and compared the result to the original before writing, failing the run on any other difference.
- **This document.** The address paragraph in *Dependency Resolution and Companion Manifest* states the URI/scheme/manifest boundary, names where the scheme this repository uses is recorded, and says why a spelling rule would not have kept the grammar small — a rule about what a URI must look like is only ever a rule about which URIs a particular resolver can serve. The two `in` examples under *Inclusion Is Not Module Definition* are written extensionless, and the manifest example's root follows the corpus to `modules/`. A closing paragraph states the consequence of the boundary: the same declaration may be written with a different scheme in a different project with no source change.
- **The toolchain.** `modules/khayyam/core/src/frontend.ts` resolves the address it is given and does not grade its shape. The three removed pieces were the `import-path-shape` member of `RefusalReason`, the `KHAYYAM_FILE_EXTENSION` export, and the `endsWith` check in `analyzeImports`. The suite still passes at 65 tests.
- **The tests that asserted a shape check, and why each changed.** `refuses("an import path without the .kh extension …")` and `refuses("an import path carrying a foreign extension")` asserted exactly the removed check, on addresses (`"memar/math/boolean"`, `"lib/boolean.go"`) their fixtures made resolvable, so with the check gone both now accept. They were rewritten as `accepts` cases, not deleted, and their names were changed to state the reason they now hold: the manifest resolves the address, and the grammar does not grade it. The third affected test, `refuses("an unresolvable import path …")`, refuses for `unresolved-import`, which is what the address's resolution turns on, so only its address and name were re-rooted.
- **Verification.** The M1 frontend was run over all 300 `.kh` files with addresses resolved against the repository root, which is the reading the corpus and the pre-existing `detail.kh` address both use: 292 accept, 8 refuse. Six of the eight are pre-final-syntax or scratch files in another dialect (`life_cycle.kh` carries Go's `type … interface {`; `blocking.kh` and `concurrency.kh` omit `mt`; `mutable.kh` writes its import without `in`; `weak.kh` puts the subtype before the name; `mem.kh` carries C++ template syntax) and `main.kh` is an untracked scratch file. The eighth is `process/control-flow/protocol/if.kh`, whose address `modules/process/error/error.kh` does not exist — the real file is `modules/process/error/protocol/error.kh`. That address is equally unresolvable under its `memar/` root, so the rewrite neither caused nor fixed it; it is recorded rather than corrected, since correcting it is a decision about which of the two paths is right.

#### Considered and not done
- **A `.kh` extension mandatory in the grammar, with the address stated as a file name the language names**: `.kh` is this repository's naming convention for its own files, and an address need not be a repository file path at all, so the rule belongs to whoever owns the files. What the toolchain accepts and what an address may look like are the [Import Address → The rule](../../modules/khayyam/rules/import-address/import-address.md#the-rule) rule's; this document states the boundary and links the rest.
- **Rewriting the manifest discussion around a bare stem, on the theory that a shorter address is what a resolver wants**: the address a source file carries and the name a resolver maps are the same string here, so shortening the former to suit the latter would have put the resolver's convenience into the grammar — the coupling this document's *Ecosystem Coupling* section exists to avoid, and the one its C/C++ row names.
- **Rewriting the `memar/` references in the non-Khayyam files that carry them**: `modules/khayyam/targets/go/abstraction_bridge.py`, several `modules/**/*.go` files, and the `//memar:impl` annotations in about twenty `.kh` files carry `memar/`-rooted references. None is an `in` URI, so none is in the corpus this change governs, and each needs its own decision about what it means — an annotation naming a symbolic `memar:impl` target is not a URI at all. Reported, not touched.
- **Fixing the `modules/process/error/error.kh` address in `if.kh`**: the rewrite carried the address across faithfully, and choosing the correct target is a fact about the corpus that this change does not establish.
- **Naming the resolution base in the grammar**: a resolver whose base is the repository's `modules/` directory and a URI rooted at `modules/` collide — the same string means two things. The collision is a real argument for the manifest to name its base rather than the grammar to imply it, which is why the handoff records it as load-bearing manifest work; the base this repository's toolchain resolves from is recorded as a property of the rule in [Import Address → The rule](../../modules/khayyam/rules/import-address/import-address.md#the-rule).
- **Restating the address's spelling rule in this document**: the rule is recorded once, in [Import Address → The rule](../../modules/khayyam/rules/import-address/import-address.md#the-rule). This document states the boundary and links the rest, per [Documentation → Content Rule: No Fabricated or Redundant Provenance](../documentation.md#content-rule-no-fabricated-or-redundant-provenance).

#### Deliberation
- `.kh` is this repository's naming convention for its own files, and the address in an `in` declaration is not required to be a repository file path — it is a URI whose scheme the manifest declares. Once the manifest is the thing that says how an address resolves, a rule about suffixes in the grammar is a rule about one resolver's key (OpenCode, argued; Omid Hekayati, decided).
- A related point decided the corpus root rather than taste: the owner accepted a git-root-relative path for this repository because it is readable and deterministic, and stated that a UUID scheme would be equally acceptable in a project that preferred one. That is why the rewrite re-roots to `modules/` rather than to a UUID, and why the grammar gains no rule either way (Omid Hekayati, decided).
- The base collision named above is the consequence the rewrite surfaced: the verification harness specified for this session resolved addresses against `modules/`, which turns every re-rooted address into `modules/modules/…` and refuses 207 of 300 files. Resolving against the repository root — which is what the rewritten corpus and the one pre-existing `modules/`-rooted address both assume — accepts 292. Both tallies are reported rather than one being chosen silently, because the base is manifest work (OpenCode, found and reported).

---

### Naming and URI spelling conventions relocated to rules catalog
- Time: 2026-09-29T16:00:00Z
- Type: Changed
- Propagates to:
  - [identifier naming](../../modules/khayyam/rules/identifier-naming/identifier-naming.md): Done
  - [import address](../../modules/khayyam/rules/import-address/import-address.md): Done
- Contributors:
  - Auto (model not recorded) via [Cursor](../../CONTRIBUTORS.md#cursor) - applied

#### What changed
- [Naming Without Package Context](./modularity.md#naming-without-package-context): organizational naming discipline links to rules; illustrative paragraphs removed.
- [Dependency Resolution and Companion Manifest](./modularity.md#dependency-resolution-and-companion-manifest): repository URI spelling defers to [import address](../../modules/khayyam/rules/import-address/import-address.md).

---

### Orphan-extension governance relocated from Inclusion section
- Time: 2026-09-29T20:30:00Z
- Type: Changed
- Propagates to:
  - [orphan extension](../../modules/khayyam/rules/orphan-extension/orphan-extension.md): Done
- Contributors:
  - Auto (model not recorded) via [Cursor](../../CONTRIBUTORS.md#cursor) - applied

#### What changed
- [Inclusion Is Not Module Definition](./modularity.md#inclusion-is-not-module-definition): monkey-patching governance text replaced with a link to [orphan extension](../../modules/khayyam/rules/orphan-extension/orphan-extension.md); local-directory file-splitting syntax retained.
