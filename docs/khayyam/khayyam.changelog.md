# Khayyam - Programming Language Changelog

## Changelog

### Initial specification
- Time: 2020-02-02T00:00:00Z
- Type: Added
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — claimed

#### What changed
- Established the canonical Khayyam syntax specification: file extension `.kh`; the two top-level keywords (`tp`, `vr`); the five subtypes (`in`, `cp`, `mt`, `ab`, `sc`); pass-by-reference-only semantics with no assignment operator and no implicit copying; no generic syntax; capsules with fully hidden fields; methods with mandatory three-part signatures and body-less forms for abstraction contracts and FFI; abstractions as pure, generic-free contracts satisfied structurally; and scope blocks for library-defined control flow.
- The Separation of Syntax and Governance philosophy was part of this original language design.
- This document predates the project's current documentation-explanation template and paired-changelog convention; no front-matter Citations or Contributors existed prior to this entry, since none were ever recorded for it.

---

### Migration to the current documentation methodology, plus a researched Naming section
- Time: 2026-08-17T00:00:00Z
- Type: refactor
- Cited:
  - [khayyam-design_philosophy.md] — Depends_on: the one-sentence "Why Choose Khayyam for naming this language" note is migrated from that document's Reference-level explanation and substantially expanded here, as part of that document's planned retirement.
- Propagates to:
  - khayyam-design_philosophy.md: Done — the migrated Naming content is removed from there in the same session; see that document's own changelog.
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — requested
  - [Claude](../../CONTRIBUTORS.md#claude) — rewrote

#### What changed
- The document was restructured from an untemplated `Summary/Core Philosophy/[sections]/CRITICAL INSTRUCTION` layout into the current template (`Abstract → Introduction → Explanation → Results → Discussion`), per `documentation-explanation.md`.
- No construct-level content was shortened or removed in this pass: all original construct-level content (Keywords, Import, Type/Capsule/Method/Abstraction/Scope, Variable) was preserved verbatim, reorganized under Explanation rather than summarized — the migration lesson from this same review's `khayyam-abstraction.md` correction (do not summarize foundational documents while restructuring them) was applied here from the start.
- The Naming section grows from one factual sentence to a researched explanation connecting three specific, factual aspects of Omar Khayyam's own work — his geometric, first-principles treatment of cubic equations; the precision of his calendar reform relative to its era; and his poetry's skepticism of inherited certainty — to three already-documented design habits of the language itself (Grammar Atomicity/Zero-Magic Core, willingness to accept upfront modeling cost for long-term integrity, and skepticism of "other languages do it this way" as a justification), with an explicit disclaimer that this is an observed fit rather than a claim of deliberate point-for-point engineering.
- The old in-body "CRITICAL INSTRUCTION for any Readers" AI-prompting block is preserved but flagged as possibly redundant with the newer `khayyam-syntax` skill, rather than unilaterally removed: it was moved into a Discussion Unresolved question.

#### Deliberation
- The migration of this document to the current template was requested (Omid Hekayati — requested).
- The naming explanation was specifically requested to be rewritten with a fuller, better-researched connection between Omar Khayyam and the language's design philosophy, given the reviewer's now-deeper familiarity with both, rather than carrying forward the single-sentence biographical note that existed before (Omid Hekayati — requested).

#### Considered and not done
Considered removing the "CRITICAL INSTRUCTION for any Readers" block outright, since `khayyam.practice.md` (the `khayyam-syntax` skill) now states equivalent guidance for AI assistants specifically. Rejected: that block also addresses human readers ("Architects"), which the skill file does not, and removing content neither requested nor clearly fully superseded risks the same kind of unilateral loss this review corrected elsewhere. Recorded as an open question instead.

---

### Removed the in-body AI-prompting warning block, added Methodology, added inline links to companion documents
- Time: 2026-08-17T00:00:00Z
- Type: Fixed
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — approved, argued
  - [Claude](../../CONTRIBUTORS.md#claude) — rewrote

#### What changed
- The "CRITICAL INSTRUCTION for any Readers" block and its corresponding Unresolved question were removed; the document no longer tells readers, in an alarmed tone, to go read other documents before trusting this one.
- A Methodology subsection was added under Introduction stating the overview-only, link-outward approach — plainly and once, near the top, that this is an overview and where the fuller reasoning lives — and pointing to companion documents' own Prior art sections (e.g. [Abstraction in Khayyam](./abstraction.md)'s comparison against Go, Rust, Java, TypeScript, Zig, and Haskell) as where the comparative, computer-science-grounded critique actually lives, rather than repeating it here.
- Inline links were added from Capsule to `khayyam-encapsulation.md`, from Pass-by-Reference to `khayyam-memory_model.md`, from the FFI bullet to `Khayyam-compiler.md`, from the No Generic Syntax bullet to `khayyam-polymorphism.md`, and opening-sentence links for Scope (to `khayyam-control_flow.md`) and Variable (to `khayyam-variable.md`), matching the pattern the Method and Abstraction sections already used — the body now links to the fuller reasoning inline, at the specific construct each companion document actually concerns: Capsule, Method, Abstraction, Scope, and Variable all point to their own document at the point of first mention, rather than leaving the reader to discover the companion set from a single block at the end.

#### Deliberation
- The removal of the "CRITICAL INSTRUCTION for any Readers" block was approved (Omid Hekayati — approved).
- Inline links to companion documents can do the same job less alarmingly, wherever a term already has its own document (Omid Hekayati — argued).
- The same guidance belongs earlier and calmer, in a Methodology subsection, stating plainly that this document is an overview and that the project's approach has deliberately been not to write one very long document (Omid Hekayati — argued).
- The document's methodology should also note that construct decisions are grounded in deliberate comparison against other languages and, where possible, the wider computer-science literature, rather than informal preference (Omid Hekayati — argued).

---

### Inspired of list reviewed and moved out of khayyam-design_philosophy.md
- Time: 2026-08-17T00:00:00Z
- Type: Removed
- Propagates to:
  - khayyam-abstraction.md: Reference — that document's own Prior art section already carries out this kind of critical, per-language comparison (Go, Rust, Java, TypeScript, Zig, Haskell) for the abstraction model specifically; this entry does not add new content there, it records that the comparison exists and was checked against this list.
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — requested, clarified
  - [Claude](../../CONTRIBUTORS.md#claude) — reviewed, rewrote

#### What changed
- The "Inspired of" section (Lessoned Languages: C, D, Go, Rust, Spiral, flat assembler; three articles on Go/Rust comparison and compiler design) was removed from `khayyam-design_philosophy.md`'s body and recorded here instead of in a changelog of its own.
- The list was checked against this session's own work: nothing in it was used as direct inspiration for a specific Khayyam construct — no direct borrowing from this list was found anywhere in Khayyam's current design.
- The list's actual function — a harsh, critical comparison against prior languages — is the same function [Abstraction in Khayyam](./abstraction.md)'s own Prior art section already performs for the abstraction model specifically; that section is the closest existing embodiment of what this list was for.
- An earlier, mistaken `khayyam-design_philosophy.changelog.md`, created for this same entry in a previous pass before this document's planned retirement was accounted for, was deleted.

#### Deliberation
- Moving "Inspired of" (a list in `khayyam-design_philosophy.md`) to a changelog was requested, now that a Changelog facet exists (Omid Hekayati — requested).
- This entry was clarified to belong here rather than in a `khayyam-design_philosophy.changelog.md`, since `khayyam-design_philosophy.md` itself is being retired entirely — its existence is misleading once every `khayyam-*.md` document is, in effect, a design-philosophy document for its own construct — so a changelog paired to it would have no base document to remain paired to; that document will not exist much longer (Omid Hekayati — clarified).
- The list was clarified to have never been a record of features borrowed directly from these languages — the "Lessoned Languages" framing already in the list's own text says so explicitly ("these languages inspirations don't mean just about get good idea but mean drop bad idea from these"); it was a checklist for critical review, not a source of adopted ideas — material to critically weigh Khayyam's choices against, what to reject rather than what to copy (Omid Hekayati — clarified).

#### Considered and not done
Considered redistributing each named language/article into whichever topic document its critique most applies to. Rejected: the list itself does not say which specific Khayyam decision each entry informed, and guessing at that mapping risks manufacturing a connection that was not actually there — the same mistake corrected earlier in this review's `khayyam-agency.md` work.

---

### System-Modeling Language Philosophy and Domain Modeling Principles migrated in from khayyam-design_philosophy.md
- Time: 2026-08-17T00:00:00Z
- Type: Added
- Cited:
  - [khayyam-design_philosophy.md] — Depends_on: both topics are migrated verbatim from that document's Reference-level explanation, as part of that document's planned retirement.
- Propagates to:
  - framework.md: Rejected — considered as a destination for System-Modeling Language Philosophy, since it discusses architectural-principles-over-feature-collection in terms close to Framework's own Constraint Space language. Rejected: Omid specifically does not want Khayyam's own voice or framing entering `framework.md` or `modeling.md`, which are meant to stay independent of any one language's perspective; this document is the correct, deliberately Khayyam-specific home instead.
  - modeling.md: Rejected — considered as a destination for Domain Modeling Principles for the same reason (its Primitive Obsession / Utility-Oriented Architecture resistance echoes modeling.md's own domain-decomposition arguments), and rejected for the same reason.
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — requested, argued
  - [Claude](../../CONTRIBUTORS.md#claude) — rewrote

#### What changed
- "System-Modeling Language Philosophy" — the framing of Khayyam as a system-modeling language deriving constructs from architectural principles rather than collecting features (with the Long-Term Architectural Potential trade-off) — was added to Introduction, between Motivation and Naming, with its "Long-Term Architectural Potential" subsection and full Discussion (Drawbacks, Prior art, Unresolved questions).
- "Domain Modeling Principles" — the domain-modeling stance against primitive obsession and utility-oriented architecture — was added to Explanation, after Variable, with its "Resistance to Primitive Obsession" and "Resistance to Utility-Oriented Architecture" subsections and full Discussion (Drawbacks, Rationale and alternatives, Prior art).
- Both topics moved from `khayyam-design_philosophy.md` into this document intact: both were removed from `khayyam-design_philosophy.md` in the same pass, preserving all original prose, examples, and Discussion content without summarizing.

#### Deliberation
- The two sections (and potentially others) were requested to move here rather than to `framework.md` or `modeling.md`, specifically because they are written with a direct Khayyam-language viewpoint, and introducing that viewpoint into documents meant to stay language-independent — independent of any single language's own framing — would compromise their independence; this document is where a Khayyam-specific perspective belongs, and both topics were deliberately kept here on that basis (Omid Hekayati — requested, argued).

#### Considered and not done
Considered splitting each topic's general principle (which could read as domain-agnostic) from its Khayyam-specific illustration, sending the general half to `framework.md`/`modeling.md` and keeping only the illustration here. Rejected per Omid's explicit direction: even a general-sounding principle, once phrased through Khayyam's own examples and voice, carries Khayyam's perspective into a document meant to stay independent of it; keeping both topics whole and Khayyam-specific here avoids that leakage entirely rather than trying to draw a clean line mid-topic.

---

### Self-Documenting Code and Naming, and Syntactic Atomicity, migrated in — no coding-style.md destination
- Time: 2026-08-17T00:00:00Z
- Type: Added
- Cited:
  - [khayyam-design_philosophy.md] — Depends_on: both topics are migrated verbatim from that document's Reference-level explanation, as part of that document's planned retirement.
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — argued
  - [Claude](../../CONTRIBUTORS.md#claude) — rewrote

#### What changed
- "Self-Documenting Code and Naming" and "Syntactic Atomicity and Semantic Clarity" were added to Introduction, immediately after System-Modeling Language Philosophy, preserving their full text, examples, and Unresolved questions; both were removed from `khayyam-design_philosophy.md`.
- No `coding-style.md` was created or referenced as a destination for either, nor assumed as a future destination for this or related content.

#### Deliberation
- Both sections' own text was pointed out to already make the placement decision explicit: "Self-Documenting Code and Naming" opens by saying naming is a style preference in most languages but is enforced by the language itself in Khayyam, and both sections state directly that they are not one-time decisions to file elsewhere but recurring tensions applied every time a new construct is considered — a description of this document, not of a peripheral style guide; on the strength of that own stated reasoning, each already argued against being extracted into a separate topic document, since each names an ongoing tension re-applied every time a new Khayyam construct is proposed — which describes this document, now that it is the living document `khayyam-design_philosophy.md` used to be (Omid Hekayati — argued).
- Memar probably should not have a generic `coding-style.md` at all, since a document with that shape tends to become exactly what `khayyam-design_philosophy.md` became — a place where anything not-yet-placed accumulates until it needs its own later redistribution effort (Omid Hekayati — argued).

#### Considered and not done
Considered a generic `coding-style.md` as the eventual home for style-adjacent content across the Khayyam document set. Rejected per the argument above: a general-purpose style document is structurally the same shape as `khayyam-design_philosophy.md` — a container with no natural boundary on what belongs in it — and would likely reproduce the same eventual need for redistribution this session has spent considerable effort resolving. Content that is genuinely about how Khayyam itself works, including its enforced naming and syntactic-atomicity properties, belongs in this document; content that turns out to be genuinely independent of Khayyam specifically should find its own, more precisely scoped document when that need actually arises, not a shared catch-all created in advance of any specific need.

---

### khayyam-design_philosophy.md fully retired — remaining Summary/Motivation content merged in, front matter migrated
- Time: 2026-08-17T00:00:00Z
- Type: refactor
- Cited:
  - [khayyam-design_philosophy.md] — Depends_on: this entry absorbs everything that remained in that document — its Summary and Motivation content, and its front-matter Citations and Contributors — completing its retirement. That document should now be deleted from the repository; nothing in it is not already reflected here or in khayyam-abstraction.md.
  - [Terminology](../terminology.md) — Depends_on: governs how capsule/abstraction/behavior are defined across Memar, carried forward from `khayyam-design_philosophy.md`'s own Citations.
  - [Protocol](../protocol.md) — Depends_on: per Protocol's definition, Khayyam's method/abstraction model is itself an instance of a protocol; this framing is inherited even though "Protocol" is not named verbatim in this document's body, carried forward from `khayyam-design_philosophy.md`'s own Citations.
  - [Framework](../framework.md) — Depends_on: the separation of encapsulation syntax from governance enforcement follows the framework/language/OS separation defined there, carried forward from `khayyam-design_philosophy.md`'s own Citations.
  - [Modeling](../modeling.md) — Depends_on: modeling is a recurring concept throughout this document's philosophy-derived content — system-modeling language, domain modeling — as a direct application of Modeling's definitions to language design, carried forward from `khayyam-design_philosophy.md`'s own Citations.
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — requested, reviewed
  - [Claude](../../CONTRIBUTORS.md#claude) — rewrote

#### What changed
- `khayyam-design_philosophy.md` is now fully retired: everything it held has either moved to this document, moved to `khayyam-abstraction.md`, or — for the two items with no forward destination — is recorded in this entry.
- Its front-matter Citations (Terminology, Protocol, Framework, Modeling — all `Depends_on`) are carried forward above, since this document now stands in that document's place.
- Most of `khayyam-design_philosophy.md`'s remaining Reference-level content was manually merged into this document directly, leaving only front matter, Summary, Motivation, and Guide-level explanation in the source (Omid Hekayati).
- A sentence was added to Motivation recording that behavior-over-type-identity, domain modeling, and syntax/governance separation were principles that converged independently across many separate design discussions before ever being written down together — the reason `khayyam-design_philosophy.md` was created in the first place (Claude).
- The remaining Guide-level explanation text ("Khayyam is evolving away from being a traditional programming language...") was not migrated into this document's body, since it duplicates System-Modeling Language Philosophy nearly verbatim and is already present here (Claude).
- `khayyam-design_philosophy.md`'s meta-commentary about its own scope and structure (why it excluded resolved technical mechanisms, why it stayed at the level of philosophy) was not migrated, since that commentary describes a document that will no longer exist; the one substantive lesson buried in that commentary is recorded in this section below, where a future reader can still learn from it (Claude).
- A concrete historical lesson from the document's own drafting is preserved even though the document holding it is gone: an earlier draft of `khayyam-design_philosophy.md` restated an error-propagation question that had already been substantially addressed elsewhere, creating drift between the philosophy layer and the actual decided mechanism — the concrete failure mode this whole document-consolidation effort has been guarding against throughout this session, kept as a citable instance of it happening once already, not only as an abstract risk.
- A separate duplication was found in the same pass and is now resolved here rather than in a new entry: this document's "Behavior Over Type Identity" and "Reassessment of Parametric Polymorphism" sections (added directly by Omid's own manual edit) were the earlier, less-refined versions of content a prior pass in this same session had already migrated — in expanded, better cross-referenced form — into [Abstraction in Khayyam](./abstraction.md)'s own "Behavior Over Type Identity" and "A Note on Parametric Polymorphism" sections. The more developed version in `khayyam-abstraction.md` was kept as authoritative; this document's own section was shortened to state the principle in brief (tying it explicitly to the No Generic Syntax rule under Abstraction, above) and point to `khayyam-abstraction.md` for the full treatment, rather than carrying two versions of the same reasoning forward.
- The original contributions to `khayyam-design_philosophy.md`'s Reference-level content, now living in this document and in `khayyam-abstraction.md`, are recorded here: [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — original idea, reflections, and design leadership behind every principle now merged in; [ChatGPT](../../CONTRIBUTORS.md#chatgpt) (GPT-5.5, medium effort) — drafted the initial text; [Super Z](../../CONTRIBUTORS.md#super-z) (GLM 5.2, medium effort) — restructured the original unstructured reflections into document-template form; [Claude](../../CONTRIBUTORS.md#claude) (claude-sonnet-5, high effort with thinking) — separated the narrative/philosophy layer from the technical/decision layer in an earlier pass.

#### Deliberation
- The remainder of `khayyam-design_philosophy.md` — front matter, Summary, Motivation, and Guide-level explanation — was asked to be merged in as well, and its front-matter Citations and Contributors, which have nowhere else to go since the base document is being deleted, to move to this changelog (Omid Hekayati — requested).

#### Considered and not done
Considered migrating the remaining Guide-level explanation paragraph verbatim regardless of its overlap with System-Modeling Language Philosophy, on the grounds that completeness favors keeping source wording rather than judging it redundant. Rejected: the two passages say the same thing in nearly the same words (compare "Khayyam follows a fundamentally different path: instead of asking 'What features should a language provide?'..." against System-Modeling Language Philosophy's own "Instead of asking 'What features should a language provide?'...") — carrying both forward would be the first real duplication introduced into this document by this consolidation effort, which the effort exists to prevent.

---

### Full re-review: fixed self-referential Discussion section and other leftovers from the manual merge
- Time: 2026-08-17T00:00:00Z
- Type: Fixed
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — requested, corrected
  - [Claude](../../CONTRIBUTORS.md#claude) — reviewed, rewrote, corrected

#### What changed
- The document-level Discussion section (Drawbacks/Rationale and alternatives/Prior art/Unresolved questions/Future possibilities) was found to be still, word for word, the deleted design-philosophy document's own self-referential Discussion — describing "this document" as a philosophy-only layer kept deliberately separate from technical specification, which directly contradicts this document's actual current state now that the two are merged: it previously described a document that no longer exists in that form rather than this document's actual, now-merged state.
- The whole Discussion section was rewritten to describe this document's real situation: it now combines both, the prior separation was tried and reversed after a concrete drift incident, and the ongoing risk is managed by stating each topic once and linking rather than restating — the section is now accurate.
- A dropped word and missing punctuation in *Khayyam Is Not Its Own Compiler or Runtime* were fixed ("...principle\nKhayyam exists to protect..." → "...principle that Khayyam exists to protect — protection that has to come from the inside...").
- That same section's inline "(This is a draft note for further discussion...)" parenthetical was moved out of Explanation into a proper Unresolved question, matching how every other open item in this document is recorded.
- An empty "### Naming Conventions" Discussion subsection that said only "Not applicable at the document-wide level," which is not part of this template and stated nothing, was removed.
- "file URI system" was restored — wrongly flattened to "file system" on a first pass — with a parenthetical added distinguishing it from a general filesystem dependency.
- The two remaining in-body mentions of `khayyam-design_philosophy.md`'s specific former filename were removed from Discussion, rephrasing to describe what happened without naming the now-nonexistent file, since this changelog is where that provenance belongs.

#### Deliberation
- The duplication fix was asked to edit the existing entry rather than add a new one (done — see the entry above), and a fresh full review of the whole document was asked for, for anything else needing correction or added explanation (Omid Hekayati — requested).
- A mistake in that review was corrected: "file URI system" was deliberate, not a typo — Khayyam's import mechanism addresses source by file URI specifically, not by depending on a filesystem's broader feature set (permissions, watches, and other OS-level semantics), and the wording should say so explicitly rather than being flattened to "file system" (Omid Hekayati — corrected).
- It was separately asked that this document's body stop naming `khayyam-design_philosophy.md` by its former filename in the Discussion section, since that document is deleted and the name adds nothing a reader can act on — the full provenance already lives in this changelog (Omid Hekayati — requested).

#### Considered and not done
Considered leaving the Discussion section's philosophical framing intact on the theory that it still describes real, useful tradeoffs even if some phrasing is stale. Rejected: the section did not just have stale phrasing, its central claims were actively false about this document as it now stands (e.g. claiming this document "differs by keeping the philosophical/ongoing-tension layer separate from decidable technical specification entirely" when the document's whole recent history is the opposite of that) — accurate self-description is not optional in a document other people and AI assistants will rely on to understand what this document is.

---

### Add Separation of Syntax and Governance principle; correct static/instance enforcement; document import-collision and fix `=` examples
- Time: 2026-08-27T00:00:00Z
- Type: Changed
- Cited:
  - [Variable in Khayyam](./variable.md) — Reference: magic-number example for the “lint can be disabled” argument
  - [Memory Model](./memory_model.md) — Reference: linter-enforced safety as the contrasting flow-policy example
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — requested, clarified
  - [Super Z](../../CONTRIBUTORS.md#super-z) — rewrote

#### What changed
- Added `Separation of Syntax and Governance: A Principle` — *Syntax defines what exists* (types/values/relationships, compiler-enforced) vs. *Governance defines how instances flow* (lifecycle, error routing, architectural constraints, linter/framework-enforced).
- The test was documented: “does this rule decide whether a program *may mention* something?” → syntax; “which flows are preferred?” → governance.
- Consequences documented: magic-number ban stays syntax (denies existence of unmodeled values) while memory-safety stays governance (polices flow of already-typed instances).
- Corrects `Method Invocation Rules` to state that static-vs-instance dispatch is enforced by the compiler (previously misworded as linter) and is a compile-time error.
- Documents `Import Mechanism` name collision as an architecture error (no `as` alias; fix at root cause, temporary wrapper via composition, versioning is a build/tooling concern).
- Replaces the `err = ErrServiceNotFound` example snippet that used `=` (which does not exist in Khayyam) with the statement-form `CopyFrom` equivalent.

#### Deliberation
- The principle that the language need not restrict which types may be passed as type-arguments was requested (Omid Hekayati — requested).
- The compiler's event role was clarified (Omid Hekayati — clarified).

---

### Restore Execution Semantics Philosophy — silently lost in the f73c633 restructure
- Time: 2026-09-06T10:30:00Z
- Type: Fixed
- Cited:
  - [Khayyam Runtime Specification](./runtime.md) — Reference: the runtime-side realization of the execution-semantics alignment, now linked from the restored topic so the principle and its one concrete realization stay distinct.
  - commit `091333a` (2026-07-13, `RFCs/khayyam.md`) — Evidence: this topic was added to the language document on 2026-07-13, directly after the session that drafted it, and was removed on 2026-07-18 during the Encapsulation/Variable restructure (`f73c633`) without being migrated anywhere.
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — directed, decided
  - [Super Z](../../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash, via the OpenCode agent) — reviewed, restored

#### What changed
- The *Execution Semantics Philosophy* topic — explicit, predictable, architecturally visible execution behavior; the three explicit-over-implicit preferences; unikernel-style computing as a natural alignment rather than a deployment requirement — is restored to this document, after *Separation of Syntax and Governance*, with its full text, Drawbacks, Unresolved questions, and Future possibilities preserved.
- The addition and silent removal were traced through git history: the topic had been added on 2026-07-13 and then silently dropped by the 2026-07-18 restructure, with no migration record; this entry is that missing record.
- One link sentence was added to the runtime reference architecture and one "recurring tension" placement paragraph, mirroring how *Self-Documenting Code and Naming* and *Syntactic Atomicity* justify their placement here.

#### Deliberation
- While migrating two design-chat transcripts into the documentation, the topic was noticed missing from the current document, and a history check was asked for before deciding its home (Omid Hekayati — directed).
- On the evidence it was confirmed that the topic once lived here, was lost in transit, and belongs here rather than in a tooling document (Omid Hekayati — decided).
- The placement decision was checked and confirmed: the principle is a language-design principle applied at every construct-vs-execution decision (language-level, like Separation of Syntax and Governance), while `khayyam-runtime.md` is the Memar Framework's one concrete runtime realization of it (implementation-side) — so the principle lives here, with a link outward, not in the runtime document, which deliberately binds implementers rather than the language (Omid Hekayati — decided).

#### Considered and not done
Considered placing the topic in `khayyam-runtime.md` instead, since Unikernel is named only in the tooling documents today. Rejected: the runtime document is addressed to the runtime's developers and imposes nothing on the language — a language-design philosophy placed there would invert its own direction of constraint; the correct shape is the principle here, linked from the runtime side whenever needed. Also considered rewriting the topic against the current document's voice before restoring. Rejected: the text was already session-approved in this exact form; only a placement paragraph and the runtime link were added.

---

### Hypothesis-voice corrections and the modeling boundary link
- Time: 2026-09-06T11:00:00Z
- Type: Fixed
- Cited:
  - [Modeling](../modeling.md) — Reference: modeling methodology, including Concept Existence vs. Model Existence and the limits of modeling, now linked from Domain Modeling Principles instead of being implied.
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — directed
  - [Super Z](../../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash, via the OpenCode agent) — applied

#### What changed
- Three claim-voice corrections aligning assertions with the design-review discipline established in the chat that produced them: "Khayyam optimizes for architectural integrity over time" now reads "is designed to optimize for"; "the grammar makes the architect's intent visible at every call site" now reads "the grammar is designed to make"; "ensures that business meaning is never lost to primitive types" now reads "is designed to keep business meaning from being lost". Each is a design hypothesis pending empirical validation, not a demonstrated result.
- Domain Modeling Principles now states explicitly that modeling methodology and the limits of modeling belong to the Modeling document, with a direct link to Concept Existence vs. Model Existence - closing the chat's decision that khayyam.md should relate to modeling.md on that question instead of leaving the boundary implicit.

#### Deliberation
- While auditing the design-chat transcript for untransferred points before deleting it, the un-applied design-review corrections from that same chat were identified: the document's claims about long-term benefits should read as design intent (hypotheses) rather than established results, and the limits-of-modeling question should relate to the Modeling document rather than stay implicit in this one (Omid Hekayati — directed).

---

### Second migration wave: `## Discussion` retired per the finalized method
- Time: 2026-09-08T00:00:00Z
- Type: refactor
- Propagates to:
  - khayyam.handoff.md: Created - open questions and anticipated work moved there.
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) - requested
  - [OpenCode](../../CONTRIBUTORS.md#opencode) (qwen3.8-flash) - moved

#### What changed
- The body retains only the fixed top-level sections (`Abstract`, `Introduction`, `Explanation`, `Results`): the document-level `## Discussion` and all five topic-level `#### Discussion` wrappers (under *Execution Semantics Philosophy*, *System-Modeling Language Philosophy*, *Self-Documenting Code and Naming*, *Syntactic Atomicity and Semantic Clarity*, and *Domain Modeling Principles*) are removed.
- Twelve open questions and one anticipated-work item (the **Target Platform Implications** document seed) moved to the newly created paired handoff.
- Rejected alternatives and audit-record drawback positions moved to this entry's `Considered and not done`; the three prior-art surveys moved to this entry's `Related work`.
- Three drawback claims proved to be current-state claims about the design's cost and were folded inline instead: the unikernel-alignment adoption limit into *Execution Semantics Philosophy*, the upfront-investment cost into *System-Modeling Language Philosophy*'s Long-Term Architectural Potential, and the naming-before-behavior workflow-inversion cost into *Domain Modeling Principles*.
- The document-level Drawbacks' risk-management method needs no copy: it is already carried by the Introduction's Methodology (state each topic once, link outward rather than restate); the surrounding consolidation-risk record moved to this entry.
- The plain-text pointer "see Unresolved questions" in *Khayyam Is Not Its Own Compiler or Runtime* is now a real hyperlink to the paired handoff's Open Questions.
- Final audit fix: the Introduction's pointer to a companion document's "own Prior art section" was retargeted to that companion's paired changelog (its Related work), the section having been retired from the companions by this wave.

#### Considered and not done
- **Keep a separate philosophy document (original approach, reversed; migrated from the removed document-level Rationale and alternatives)**: the split created the same duplication risk it was meant to avoid — technical claims in the philosophy document could drift out of sync with the dedicated documents where those mechanisms were actually decided, which happened concretely once, when an earlier draft of that document restated an error-propagation question already substantially addressed elsewhere. The document was retired and its content merged back here and into each construct's own dedicated document, rather than trying to patch the split further.
- **Keep philosophy and syntax reference as two documents indefinitely, accepting the drift risk (rejected; migrated from the same section)**: rejected once a second, independent failure of the same kind confirmed the risk was recurring, not a one-time accident — this document's own then-superseded "Behavior Over Type Identity"/"Reassessment of Parametric Polymorphism" sections had drifted out of sync with the more developed version already migrated to `khayyam-abstraction.md`.
- **Allow generic containers alongside domain-specific capsules (rejected; migrated from the Domain Modeling Principles topic's retired Rationale and alternatives)**: this would immediately re-open the door to the primitive-obsession and utility-dumping patterns that Khayyam's design explicitly aims to prevent.
- **Provide a lint rule rather than a language-level constraint (considered, not chosen; migrated from the same topic's wrapper)**: lint rules can be disabled or ignored at the organizational level, weakening the architectural safeguard.
- **Consolidating philosophy and syntax reference into one document carries a duplication risk (drawback record; migrated from the removed document-level Drawbacks)**: this document now combines finalized syntax and semantics with the philosophical and architectural reasoning behind them, after absorbing what previously lived in a separate design-philosophy document, and a construct's rationale, once stated here, must not also be restated — and risk drifting out of sync — in that construct's own dedicated document (e.g. [Abstraction in Khayyam](./abstraction.md), [Method in Khayyam](./method.md)). The risk is managed the same way those documents manage their own overlaps: state a topic once, in the place closest to where a reader would look for it, and link to it from everywhere else rather than restating it.

#### Related work
- Rust's design philosophy documents and Go's "Go Proverbs" serve a similar purpose of capturing design intent alongside technical specification, generally as separate documents from the language reference itself. Khayyam's own experience with that split — the drift recorded under Considered and not done above — is a data point specific to this project, not a general argument against the pattern; other projects may find the split works well for them. (Migrated from the removed document-level Prior art.)
- A language derived from architectural principles rather than feature collections has precedents in restricted domains — for example, Erlang's design from telecommunications reliability requirements, or Verilog's design from hardware modeling needs; Khayyam's ambition is to apply this principle more broadly to general-purpose system software. (Migrated from the System-Modeling Language Philosophy topic's retired Prior art.)
- Domain-Driven Design as formulated by Eric Evans advocates for rich domain models, but leaves enforcement to developer discipline; Khayyam encodes this discipline into the language grammar itself, making it structurally difficult to violate. (Migrated from the Domain Modeling Principles topic's retired Prior art.)

---

### The Grammar Refuses Protocol Semantics
- Time: 2026-09-10T00:00:00Z
- Type: Added
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — requested, decided the criterion
  - [Super Z](../../CONTRIBUTORS.md#super-z) — stated, applied

#### What changed
- Added the *The Grammar Refuses Protocol Semantics* principle to the Explanation, between *Separation of Syntax and Governance* and *Execution Semantics Philosophy*: a construct enters the grammar only when its semantics can be stated without adopting any protocol's definitions; where a construct's meaning would require protocol-owned definitions, the grammar refuses the construct, and the need is met through the language's generic mechanisms (ordinary values and explicit outputs, explicit imports, library-provided methods, the `ab` construct for authoring contracts).
- The principle states as a rule what the per-construct documents already enacted individually (no error-handling syntax, no memory primitives, no concurrency keywords, no standard-library shapes in the grammar) and fixes the boundary as protocol-level, not concept-level: base-layer modeling concepts (`tp` for Type, `sc` for Scope) remain expressible, because the grammar supplies the declaration mechanism, not a specific contract.
- Names the framework-independence consequence: protocols are owned by the governance framework above the language (Memar today, another framework tomorrow); baking one in would reduce the language to that framework's syntax extension.
- Trigger: the language–protocol relationship had been stated per construct but never as a general rule, and a documentation-set review misread [Control Flow in Khayyam](./control_flow.md)'s citation of [The Error](../protocols/error.md) as a grammar-level dependency. The general statement closes that misreading path; the folder role statement ([README.md](./README.md)) carries the citation-layer version of the same statement.

---

### The Grammar Refuses Protocol Semantics revised; the Control Flow document retired
- Time: 2026-09-10T00:00:00Z
- Type: Changed
- Cited:
  - [Control Flow](../protocols/control-flow.md) — Depends_on: the design of library-defined control flow and the negative reasoning about grammar absences are owned there after the absorption.
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — decided (the negatives-to-changelog doctrine: bodies carry current positive state only, per the same reasoning that retired the Discussion section)
  - [Super Z](../../CONTRIBUTORS.md#super-z) — applied

#### What changed
- The principle section keeps the positive criterion (what enters the grammar) and the protocol-level boundary; its negative-illustration paragraph (the `try`/`catch` enumeration, the baked-error critique, the worked-case pointer) migrated to the Control Flow protocol document's changelog.
- The Scope topic now states the grammar facts positively and retargets its pointer: a code scope is inert until a library-provided method drives it, the grammar ships no control-flow keywords or logical operators of its own, and the design of flow constructs lives in the Control Flow protocol document.
- `control_flow.md` and its paired changelog and handoff are retired and deleted; their content is fully redistributed (the migration map is the protocol document's changelog entry). The prior entry below remains as history; its links describe the document as it then was.

#### Considered and not done
- **Keeping a stub pointer file in place of the retired document (rejected)**: a near-empty body would need permanent maintenance while carrying no state of its own; every consumer pointer was retargeted instead.

---

### Toolchain documents leave this layer; grammar facts stay
- Time: 2026-09-15T09:00:00Z
- Type: Changed
- Cited:
  - [Memory](../protocols/memory.md) — Consumed contract: copy, teardown, and safety as protocol, not a Khayyam memory model.
  - [Linter](../protocols/linter.md) — Consumed contract: compiler/linter split this document already named as syntax/governance.
  - [Compiler](../protocols/compiler.md) — Consumed contract: primitives versus library names; this document keeps the `sc` lowering as realization.
  - [Runtime](../protocols/runtime.md) — Consumed contract: execution environment, not a Khayyam-owned VM.
- Propagates to:
  - README.md: Done — membership criterion no longer houses compiler, linter, or runtime.
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — decided
  - [Grok](../../CONTRIBUTORS.md#grok) (Grok 4.6 via Cursor) — applied

#### What changed
- Pass-by-reference, FFI, syntax/governance, and execution-semantics pointers retarget to the protocol documents; `memory_model.md` is no longer cited.
- Scope states command-newline and `sc` lowering without a `goto` keyword; type-as-argument grammar lives in [Method](./method.md), with a pointer from Scope.
- Folder README: a document belongs here for grammar and construct design, not for toolchain protocols this layer consumes.
- Import mechanism states contracts-first reading; companion folding is the Linter protocol's assist, not a practice-file note.

---

### How Khayyam realizes Memory — notes from the retired shelf
- Time: 2026-09-15T13:00:00Z
- Type: Changed
- Cited:
  - [Memory](../protocols/memory.md) — Consumed contract: the requirements these notes realize.
- Propagates to:
  - variable.md: Done — Resource Lifecycle points here and to Memory; deferred wording removed.
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — decided
  - [Cursor](../../CONTRIBUTORS.md#cursor) (Composer) — applied

#### What changed
- Variable bullets state no raw machine pointers and no `nil`/`null` keyword; absence uses a type method, conventionally `IsNull()`.
- A new topic, [How Khayyam realizes Memory](./khayyam.md#how-khayyam-realizes-memory), carries the retired shelf's Khayyam-specific mechanisms: no lifetime annotations and why, `Deinit()`/`Free()` as teardown conventions, static escape analysis plus PGO-as-library (including the unikernel worker-stack motivation), and the generated-companion naming pointer to Memory's handoff.

#### Deliberation
- These notes were deliberately kept out of the Memory protocol so that protocol stays language-independent; deleting the shelf without placing them would have lost realization content (Omid Hekayati — decided).


---

### migration_guide.md removed from the language document set
- Time: 2026-09-23T04:38:49Z
- Type: Removed
- Propagates to:
  - khayyam.handoff.md: Done — the stdlib-bootstrap entry's pointer to the migration guide was reworded to a plain-text note that an earlier promotional migration note (removed) covered ecosystem onboarding, not first-capsule ordering.
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — decided
  - [Mimo](../../CONTRIBUTORS.md#mimo) (mimo-v2.6-flash via OpenCode) — applied

#### What changed
- `docs/khayyam/migration_guide.md` was deleted. It was an old, promotional, agent-authored document (porting difficulty matrix, transpiler strategy, cross-language comparison matrix) that did not meet this folder's membership criterion — it did not specify a construct or concern of the Khayyam language itself — and its presence contradicted the language documents' own tone and scope.
- The sole inbound reference (khayyam.handoff.md's stdlib-bootstrap entry) was fixed before deletion; no other tracked document cited it.

#### Deliberation
- Ruled to delete rather than rewrite: the document is promotional and not language documentation; fixing the bootstrap-ordering contradiction by rewriting it was considered, then superseded by removal from the language docs (Omid Hekayati — decided).

#### Considered and not done
- **Rewrite in place to fix the contradiction with the no-hidden-primitive ruling (considered, rejected)**: even a corrected migration guide would remain ecosystem-marketing content outside this folder's criterion; removal is the cleaner boundary.

---

### Abstraction wording aligned with Protocol vs Contract
- Time: 2026-09-23T05:38:39Z
- Type: Fixed
- Cited:
  - [Protocol](../protocol.md) — Depends_on: Protocol vs Contract defines a contract as parties, obligations, and commitments; an abstraction names required behavior only.
  - [Abstraction in Khayyam](./abstraction.md) — Reference: the document-level conflation was corrected there first; this entry extends that correction to this document.
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — decided
  - [Mimo](../../CONTRIBUTORS.md#mimo) (mimo-v2.6-flash via OpenCode) — applied

#### What changed
- The Abstraction paragraph now says abstractions are pure *behavioral specifications*, not pure contracts; the methods that fulfill this specification are defined outside it.
- The composition-example comment says sub-typing/behavioral dependency, not contractual dependency.
- Both Grammar Refuses Protocol Semantics mentions say the `ab` construct authors *specifications*, not contracts.
- Companion practice/handoff/polymorphism/metaprogramming/inheritance/type wording was aligned in the same pass; changelog narratives were left as history.

#### Deliberation
- Contract remains a distinct architecture concept (parties commit to each other); abstraction only declares behavior (Omid Hekayati — decided).

---

### Type Principles Realized received from type.md; folder citation rule tightened
- Time: 2026-09-23T07:07:01Z
- Type: Added
- Cited:
  - [Type](../type.md) — Depends_on: the base-layer principles these realizations instantiate (Type as semantic entity, nominal identity, four categories of Type, owned rules).
  - [Type vs Implementation Type](../type.md#type-vs-implementation-type) — Reference: the ascent problem the no-primitive-types rule eliminates at the language level.
- Propagates to:
  - khayyam/README.md: Done — the Citation direction paragraph no longer allows a base instance-pointer hyperlink; upward mentions of Khayyam from base are plain-text only.
  - docs/README.md: Done — the `khayyam/` section's citation clause now says plain-text name only, never via hyperlink, and its folder pointer is an inline-code path.
  - khayyam.handoff.md: Done — the stdlib-bootstrap entry's `type.md#manifestation-in-khayyam` link retargeted here to Type Principles Realized (handoff: no entry of its own).
  - type.handoff.md: Done — upward links replaced with plain-text path references (handoff: no entry of its own).
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — decided
  - [Mimo](../../CONTRIBUTORS.md#mimo) (mimo-v2.6-flash via OpenCode) — applied

#### What changed
- khayyam.md gains "Type Principles Realized": the seven-item realization account transferred from type.md's former Manifestation in Khayyam section, with the duplicate Sovereign Encapsulation bullet merged and each item linking to its companion document or the relevant base section.
- khayyam/README.md's citation rule now forbids upward hyperlinks entirely — the former instance-pointer exception is removed; a base document may name Khayyam in prose only.
- docs/README.md's `khayyam/` entry describes base citation as plain-text-only, and its `khayyam/README.md` pointer is an inline-code path rather than a hyperlink.

#### Deliberation
- Transfer, not delete; citation direction runs down (Omid Hekayati — decided).

#### Considered and not done
- **Creating `docs/khayyam/type.md` as the transfer destination (considered, rejected)**: every Manifestation bullet already has a dedicated companion (encapsulation, method, abstraction, inheritance, polymorphism) or belongs in khayyam.md's own philosophy sections (no primitive types, the `tp` keyword); a new document would either duplicate that material — the drift failure mode this document set has already retired documents to escape — or exist as a thin link stub. Recorded here so the question does not reopen without new material to justify a separate document (Omid Hekayati — decided).

---

### Transferred inheritance bullet aligned off "contract layer"
- Time: 2026-09-23T08:28:49Z
- Type: Fixed
- Cited:
  - [Type](../type.md) — Depends_on: inheritance between Abstractions is requirement extension, not a separate contract plane.
  - [Abstraction in Khayyam](./abstraction.md) — Reference: an abstraction is a behavioral specification, not a contract.
- Contributors:
  - [Grok](../../CONTRIBUTORS.md#grok) (Grok 4.7 via Cursor) — reviewed, applied
  - [Gemini](../../CONTRIBUTORS.md#gemini) (Gemini 3.8 flash via Cursor) — reviewed

#### What changed
- The Inheritance bullet under Type Principles Realized now places inheritance in the specification layer — requirement extension between Abstractions — rather than in a "contract layer" opposed to the state layer of Capsules.

#### Deliberation
- Both reviews of the staged transfer found the same residue: Type's defined-contract vocabulary names a Type's guarantees, not an inheritance plane, and Protocol vs Contract reserves *contract* for parties, obligations, and commitments (Grok — reviewed; Gemini — reviewed).

---

### Retired the swapped efficacy labels; pointed at two open grammar questions
- Time: 2026-09-23T08:43:30Z
- Type: Fixed
- Cited:
  - [Method in Khayyam](./method.md) — Depends_on: influencing and influenced are the signature groups this document's pattern already names.
- Propagates to:
  - type.md: Done — the opposite efficacy/impressible gloss is withdrawn there.
- Contributors:
  - [Grok](../../CONTRIBUTORS.md#grok) (Grok 4.7 via [Cursor](../../CONTRIBUTORS.md#cursor)) — reviewed, applied
  - [Meta AI](../../CONTRIBUTORS.md#meta-ai) (muse-spark-1.3 via [Cursor](../../CONTRIBUTORS.md#cursor)) — reviewed

#### What changed
- The method bullet names the owner, the influencing variables, and the influenced variables. The labels `efficacy` and `impressible` are recorded only here: this document had glossed them as arguments and returns, and Type had glossed them as outputs and inputs (Grok — applied).
- `Sum` is `tp Sum mt (self W32) (a W32, b W32) (total W32, err Error)`, called `W32.Sum(a, b)(total, err)`. `Set` is called `k.Set(value)(err)`. The parent type stays in `self` (Omid Hekayati — decided).
- Human-facing text is a value a method writes into an influenced variable. The method's signature is an open question in the handoff (Omid Hekayati — decided the placement; the signature remains open).
- When `self`'s owner is a method, the receiver is that method. The method implements an abstraction by defining methods on itself (Omid Hekayati — decided).
- A one-token line in a capsule body is a bare abstraction name the capsule composes (Grok — applied).
- The practice cheat sheet's calls use the same two groups after the receiver (Grok — applied).
