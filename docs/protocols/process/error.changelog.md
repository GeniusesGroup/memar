# The Error Changelog

## Changelog

The entries below consolidate the document's former front-matter provenance (`Applied to`, `Citations`, `Contributors`) and its former `## Change Rationale` section. The source records did not carry per-phase timestamps; all three historical phases predate the document's first commit (2026-07-24), so each carries `Time: unknown`. Contributor attribution follows the former `Contributors` field, whose Works lists were not pinned to phases; each contributor is listed under the phase their recorded contribution belongs to.

### Initial draft — the Error Abstraction document (495440)
- Time: unknown (historical import)
- Type: Added
- Cited:
  - [Khayyam](../khayyam/khayyam.md) — Reference: source of truth for the syntax of every code example in this document (`tp`/`mt`/`vr`/`cp`/`ab`/`sc` keywords, capsule composition, abstraction composition, body-less methods as contracts).
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — claimed, argued
  - [Gemini](../../CONTRIBUTORS.md#gemini) (3.1 Pro, extended thinking) — drafted, argued
  - [Super Z](../../CONTRIBUTORS.md#super-z) (GLM-5.2) — drafted, argued
  - [Claude](../../CONTRIBUTORS.md#claude) (claude-sonnet-5, extended thinking) — reviewed.

#### What changed
- Defined `Error`'s composition (`DataType`, `Field_MediaType`, `ADT`, `ImplementsError`) and its method composition and boundary-crossing discipline, identity by `DataTypeID()` alone, the rejection of `Equivalence` and of sealed-interface markers, the optional capability-interface pattern (`Internal`/`Temporary`/`Timeout`), the `ImplementsError` naming rationale, and the multi-cause return convention (Omid Hekayati — authored the core design decisions).
- Tracked `ADT`'s `IsNull`/`IsEmpty` semantics, the `IsEqual`/`MediaType` redundancy question, and the open Khayyam capsule-composition model.
- Initial draft (Gemini).
- Drafted and revised the interface across several rounds (Super Z).

#### Deliberation
- The core design decisions were authored across an extended multi-session discussion (Omid Hekayati).
- An intermediate marker-method design was drafted, in which two Go package-visibility bugs were identified and corrected (Super Z).
- A sealed-interface marker pattern was argued for, then against, as evidence developed (Super Z).
- Sealed-interface markers were rejected (Omid Hekayati).

---

### Boundary-translation rule (originally the separate Error vs. Log document, 000010)
- Time: unknown (historical import)
- Type: Added
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — claimed

#### What changed
- Authored in parallel as a standalone document, since absorbed into this one, defining the boundary-translation discipline — the Capture → Persist → Re-express discipline; the two-audience distinction between `Error` (caller-facing contract) and Log (operator-facing forensic event); the corollary that user-domain outcomes must not be modeled as log events; and the worked financial-transaction example demonstrating the rule.
- Noted explicitly that the rule cannot be reduced to a structural or syntactic check and is better suited to AI-assisted static analysis than to a linter.

---

### Consolidation of the two documents into one
- Time: unknown (historical import — first committed together on 2026-07-24)
- Type: refactor
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — directed
  - [Super Z](../../CONTRIBUTORS.md#super-z) (GLM-5.2) — rewrote

#### What changed
- Merged the *Error vs. Log* boundary-translation rules into the *Error Abstraction* document, on the recognition that they answer two halves of one question — what an `Error` *is*, and what it is allowed to do when it leaves its origin layer — and that forcing readers to load two documents produced the same scattering problem the documentation specification was written to eliminate (Omid Hekayati — decided the merge once both halves were recognized as one question).
- Decided, informed by document 495420 developed in a parallel session, that each Error concept is its own concrete type (Omid Hekayati).
- Consolidated the two discussions into this single canonical document; restructured the merged content to follow then-current body-section specification; verified all Khayyam code examples against khayyam.md's syntax rules (Super Z).
- Every load-bearing claim, alternative rejection, and unresolved question from both sources was preserved without summarizing; a Composition overview topic was added; a Boundary discipline topic now separates the two boundary rules explicitly (process/network crossing vs. diagnostic-to-actionable layer translation); an Enforcement topic states that "each Error is its own type" is load-bearing for everything else (Super Z).

---

### References repointed to the Type document
- Time: 2026-08-25T00:00:00Z
- Type: refactor
- Propagates to:
  - type.md: Done — the principle this document depends on now lives there as "Stateless Types"; see type.changelog.md for its dissolution record.
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — directed
  - [Super Z](../../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — rewrote.

#### What changed
- Error was the motivating case of the dissolved *Static Concepts Must Be Types* document (495421); that document's principle now lives in [Type](../type.md).
- Nine references were repointed with no content change: the front-matter `Citations` entry, the Abstract's assumption statement, Multi-cause returns, both code-generator Future-possibilities notes, Enforcement (including the `Err` naming-convention pointer, which now targets type.practice.md), Drawback 1, the generic-`Init` rejection rationale, and Prior art (which now names only the memar-go companion analysis directly, since the base document it used to cite alongside that companion is gone) (Omid Hekayati — directed dissolving pre-facet micro-documents so citations point at Type and Modeling generally; Super Z — rewrote).
- Recorded for a future pass, so the outstanding work is searchable: this document still carries legacy `Applied to`/`Citations`/`Contributors` front matter and a `## Change Rationale` section from before the Facet split, and is due for its own Explanation-facet migration like the rest of the set.

---

### Migration to the Explanation-facet template
- Time: 2026-08-25T00:00:00Z
- Type: refactor
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — requested
  - [Super Z](../../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — rewrote.

#### What changed
- Continuing the documentation-correction pass onto this document itself, the body already conformed to `documentation-explanation.md` (Abstract; Introduction with Motivation and Methodology; topic-first Explanation with per-topic Discussion bundles; Results; document-wide Discussion); the remaining work was provenance and identity.
- The former `Applied to`, `Citations`, and `Contributors` front-matter fields and the trailing Change Rationale section moved into this file (entries above, in phase order).
- Citation dispositions: the Type dependency is now linked directly in the body (see the repointing entry); the Khayyam syntax-source citation became an ordinary body link at its one reader-needed mention (Unresolved questions, capsule-composition model); the abstraction_p.Implements dependency had never had a resolvable URI and remains tracked through the Implements-pattern follow-up under Unresolved questions; the Documentation structure-compliance citation became obsolete under the facet split.
- H1 aligned to the Title ("The Error"), dropping the subtitle descriptor the Abstract already carries; this changelog retitled accordingly.

---

### Relocated to `docs/protocols/`
- Time: 2026-09-03T00:00:00Z
- Type: refactor
- Propagates to:
  - khayyam-control_flow.md: Done — both `error.md` links repointed to `./protocols/error.md`.
  - khayyam-control_flow.changelog.md: Done — both historical `error.md` references repointed to the new path, content unchanged.
  - khayyam-metaprogramming.md: Done — both `abstraction-implements.md` links repointed to `./protocols/abstraction-implements.md` (that document's relocation was registered in its own changelog).
  - type.practice.md: Done — the `error.md` link repointed to `./protocols/error.md`.
  - chapar.changelog.md: Done — the historical `error.md` reference repointed to the new path, content unchanged.
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — directed, decided
  - [Super Z](../../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — moved, rewrote

#### What changed
- This document and its changelog moved from `docs/` into the framework-contracts subdirectory (`docs/abstractions/`, since renamed `docs/protocols/`) — a subdirectory whose membership criterion (recorded in its README) is: documents specifying Memar's own framework-level contracts, as distinct from the conceptual foundation documents at `docs/` root. These documents are the source of truth for their protocols, not executable code; implementations live in the `memar-{language}` repositories. No content change; no new dependency or citation introduced (Omid Hekayati — decided that documents defining a Memar framework-level abstraction or contract get their own subdirectory under `docs/`, so that base documents referencing the abstraction layer do so deliberately rather than by accident; the subdirectory was later renamed `docs/protocols/` when its membership widened to Memar's protocol specifications — see the renaming entry below; Super Z — relocated this document and its changelog, adjusted internal relative links for the new depth, repointed the inbound references listed above).

---

### Boundary discipline expanded: Bug/Error/Log distinction, wire-format rationale, immutability position
- Time: 2026-09-06T00:00:00Z
- Type: Expanded
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — claimed, argued
  - [Super Z](../../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — reviewed, rewrote

#### What changed
- Boundary discipline gained three additions: an explicit Bug/Error/Log-Event three-entity distinction grounding why the error contract must not absorb forensic bookkeeping; a stated rationale for the numeric-identifier wire format (stability, dispatch, locale-independence, per-audience text resolution at the ends); and a new Immutability topic stating the protocol's deliberate break from the ecosystem's wrap-and-enrich convention, with the rejected convention's strongest argument (trace preservation) answered by pointing at the Capture → Persist → Re-express steps as the place diagnostic data actually lives.
- The additions were verified against the document's existing claims before writing — immutability was found to be already implied by the identity model ("no per-instance dynamic field meaningful to compare", each error its own type) but never stated as a discipline, and the wire-format rationale was found consistent with `DataTypeID`-only crossing but never articulated, so both additions extend rather than contradict existing content. The three additions were written into Boundary discipline (the Bug paragraph, the wire-format paragraph, the immutability topic) in the document's established prose style, the immutability argument linked to the identity model and the capture/persist/re-express steps so the rejection of wrap-enrichment does not read as information loss (Super Z).

#### Deliberation
- Three positions were brought from years of public developer-community discussions (gopherconf.ir, Go Engineers, Gommunity) (Omid Hekayati).
- (1) the three-entity distinction — a bug is a defect in human reasoning discoverable by human investigation, an error is an informational entity the system holds and reports, a log event records what the system experienced — with the corollary that per-layer diagnostic attachment (wrap/enrich) confuses the error contract with the log's forensic role (Omid Hekayati).
- (2) an `Error` must be immutable, never created dynamically to carry per-request particulars like a failing filename — if the caller needs those, the operation's design is wrong or the data belongs to the caller's own inputs (Omid Hekayati).
- (3) what crosses the wire is a numeric identifier, not a single-locale text string, since strings cannot be dispatched on reliably and bind the contract to one rendering (Omid Hekayati).
- Counter-positions from the discussions (wrap-as-trace-preservation: "without enrichment at each layer you lose the trace") were explicitly weighed in the text rather than ignored (Omid Hekayati).
- Position (2) was accepted into the document as stated; positions (1) and (3) were recorded with their ecosystem-contrary framing intact (Omid Hekayati).

---

### Documentation-method migration completed: Discussion wrappers, Drawbacks, Rationale, Prior art dissolved per the finalized method
- Time: 2026-09-07T00:00:00Z
- Type: refactor
- Propagates to:
  - error.handoff.md: Done - all open questions and future-possibilities content moved there.
- Contributors:
  - [Super Z](../../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — moved

#### What changed
- The body's fixed top-level sections are now `Abstract`, `Introduction`, `Explanation`, `Results` only (Super Z - applied the finalized documentation method).
- Topic-level drawback statements (identity's cross-organization consequence; the non-lintability of translation; the ADT conservative-answer mitigation) folded into their topics as inline content (Super Z).
- In-body `[Unresolved questions]` pointers retargeted to the paired handoff (Super Z).
- The not-yet-designed logging-capsule companion document named inline as anticipated work and tracked in the handoff (Super Z).

Dissolved every `#### Discussion` wrapper (Identity and equality, Boundary translation, Detail and Quiddity fields, ADT composition, ImplementsError) and the document-level `## Discussion`; drawback statements folded into their topics as inline content; rejected-alternative reasoning, comparative prior art, document-level Drawbacks, open questions, and future possibilities relocated below without loss. (Super Z)

#### Considered and not done
- **`Equivalence[Error]` method (rejected; migrated from the Identity-and-equality topic's retired `Rationale and alternatives`)**: redundant with `DataTypeID()` comparison once it was established that `Error` carries no comparison-meaningful per-instance data. Maintaining it would have required every concrete error to implement a method whose body always degenerates to the same `DataTypeID` comparison.
- **`ExpireInFavorOf` as implicit equivalence (rejected; migrated from the Identity-and-equality topic's retired `Rationale and alternatives`)**: conflates type-lifecycle phasing with value equality. A deprecated type and its replacement are not "the same value" — they are two distinct types, one of which is being phased out in favor of the other.
- **Identity by `Name` or `Aliases` (rejected; migrated from the Identity-and-equality topic's retired `Rationale and alternatives`)**: human-readable names are not guaranteed unique across files, are locale-dependent, and may change as a type's vocabulary evolves. `DataTypeID` is stable, programmatically safe, and locale-independent.
- **A single free-text `Description` field (rejected; migrated from the Detail-and-Quiddity topic's retired `Rationale and alternatives`)**: collapses two genuinely different jobs (describing the type in general versus advising the occurrence-facing reader on what to do) into one blob of text, with no machine-readable signal of which audience a given sentence serves.
- **Locale-independent `Domain` as a classification signal (rejected; migrated from the Detail-and-Quiddity topic's retired `Rationale and alternatives`)**: would couple a business-domain taxonomy to `Error`'s dispatch model, freezing a particular taxonomy into the type system when capability interfaces already provide a more flexible, type-safe alternative.
- **Narrow to `Nil` alone at the canonical level (an earlier draft; rejected; migrated from the ADT-composition topic's retired `Rationale and alternatives`)**: generalized a Go-specific realization fact into the abstraction. Khayyam's reference semantics are different enough from Go's pointer semantics that the same narrowing does not necessarily make sense in other backends.
- **Drop `ADT` from `Error`'s composition entirely (rejected; migrated from the ADT-composition topic's retired `Rationale and alternatives`)**: would remove the only contract-level way to ask "is there actually an error here at all" without a separate side-channel boolean. The `OnPresent`/`OnAbsent` dispatch used in the worked example under Boundary translation depends on this.
- **Sealed-interface marker method (rejected; migrated from the ImplementsError topic's retired `Rationale and alternatives`)**: examined in detail and found to provide no guarantee beyond a plain exported method. The marker added ceremony (one extra embedded struct per concrete type, in a specific package) without adding any real protection — a determined bad actor can embed the marker just as trivially as they can write the plain method.
- **The fully generic `Implements()` name, with no domain suffix (rejected; migrated from the ImplementsError topic's retired `Rationale and alternatives`)**: a capsule declaring intent for more than one abstraction at once would have no way to indicate *which* declaration was for which abstraction. The `ImplError` name resolves that ambiguity at zero cost.
- **No tooling-facing declaration at all (rejected; migrated from the ImplementsError topic's retired `Rationale and alternatives`)**: a code generator scaffolding a large capsule from a `.kh` definition would have no signal that an incomplete capsule is *meant* to become an `Error`, and would be forced to wait until every required method is hand-written before it could recognize the capsule as conforming. The declaration shifts intent-discovery to the earliest possible moment.
- **Single generic `Error` capsule with an `Init` method (rejected; migrated from the document-level retired `Rationale and alternatives`)**: the central rejected alternative of the [Type](../type.md) identity principle, applied here to `Error` specifically — the concept motivating case for that principle in the first place. Demotes identity from the type system to runtime data; incompatible with covariant returns and with the optional capability-interface pattern (both depend on distinct concrete types).
- **A single `Category()` enum for classification (rejected in favor of optional capability interfaces; migrated from the document-level retired `Rationale and alternatives`)**: a closed enum forces every error into one bucket along one axis; `Internal`/`Temporary`/`Timeout` capture genuinely orthogonal dimensions (an error can be any combination) more accurately than a single tag could, and remain fully optional per concrete error rather than mandatory.
- **Keeping the Error composition rules and the boundary-translation rules in separate documents (rejected; migrated from the document-level retired `Rationale and alternatives`)**: the two are halves of the same question — what an `Error` *is* and what an `Error` is *allowed to do* when it leaves its origin layer. Forcing a reader to load two documents to assemble a single mental model produced the same scattering problem this project's documentation specification was written to eliminate.

#### Considered and not done (topic-level drawbacks and rejected narration relocated per owner ruling)
- **Equality by `DataTypeID` alone means two structurally identical errors defined in different files (or different organizations) are *not* equal**, even if a human would call them the same concept. This is intentional — identity is anchored to the file URI the type was declared in, exactly as Khayyam's import mechanism anchors everything else — but it does mean the framework has no built-in notion of "synonymous errors across organizations." Cross-organization error mapping, when it is needed, is an application concern handled at a translation boundary (see Boundary translation), not a property of `Error` itself. (Migrated from the Identity-and-equality topic)
- **The boundary-translation rule cannot be reduced to a structural or syntactic check,** unlike most other rules in this document set (for example definite assignment, or `Deinit`-path coverage). Determining whether a given error *should* have been translated at a given boundary requires understanding the semantic role of that boundary — a judgment about domain architecture, not about code shape. A structural linter can verify that a logging capsule was called somewhere along a path, or that a return type is `Error`-compatible; it cannot determine whether the *specific* error returned still leaks internal vocabulary inappropriate to its caller, or whether a low-level error was forwarded unchanged when it should have been re-expressed. This class of review is better suited to AI-assisted static analysis trained on the distinction, operating as a complementary check alongside (not a replacement for) the structural linter rules defined elsewhere. (Migrated from the Boundary-translation topic)
- **Requiring three `ADT` methods whose semantics are not yet settled is an uncomfortable position:** implementers writing concrete errors today are asked to provide `IsNull`/`IsEmpty` implementations whose contracts are not yet fully defined. The mitigation: a concrete error can return a fixed, conservative answer (`false` for both, since an `Error` value that exists is by definition not null) until the dedicated ADT document resolves the deeper question. (Migrated from the ADT-composition topic)
- **The rejected alternative to boundary translation:** letting errors propagate verbatim through every layer, with logging treated as an afterthought, was rejected as the direct cause of both failure modes described in Boundary discipline. It is the prevailing pattern in most codebases precisely because no language or framework makes translation the path of least resistance; this document makes it explicit that the Memar framework does. (Migrated from the Boundary-translation topic)
- **The sealed-interface realization history:** the ImplementsError method provides no safety or "sealed interface" guarantee — an earlier design (now Rejected) attempted to harden the Go realization into a compiler-enforced sealed interface using an unexported method and a required embedded marker struct. On review, this was found to add real ceremony (the marker had to live in a specific package, one extra embedded field per concrete type) without buying a real guarantee: deliberately embedding a shared marker struct and deliberately writing the same plain method independently are equally trivial for anyone acting in bad faith, so neither realization is actually harder to fake than the other. Accidental (non-deliberate) collision was separately judged implausible on its own, given `Error`'s real, fully-expanded method count (~15-20 methods once `DataType` is expanded). (Migrated from the ImplementsError topic; the body now states the claim without the design history)
- **`ExpireInFavorOf` as an implicit equivalence relation** — a related, briefly considered design, using `ExpireInFavorOf() DataType` (from `datatype_p.Details`) so a deprecated error could be treated as "equal to" its replacement — was rejected as misleading: conflating "this type is being phased out in favor of that one" with "these two values are the same" is a category error. (Already recorded above; the body now keeps only the live question pointer.)

#### Considered and not done (from the removed document-level Drawbacks section)
- **Type proliferation** — a system with many distinct error concepts will contain many distinct type definitions; the general trade-off is recorded with the identity principle itself in [Type](../type.md). Mitigated by code generation (the `abstraction_p.Implements` pattern); the framework's position is that this is an intended, correct consequence, not a flaw.
- **Two design threads remain genuinely open** (now in the paired handoff) — this document should not be read as completely closing the `Error` abstraction's design, only as the current, consolidated, best understanding.
- **`ADT`'s `IsNull`/`IsEmpty` semantics for `Error` are not yet defined** — the methods are required (canonically, in Khayyam), but what they should actually return for a value like `Error` is deferred to the dedicated ADT session. Go's realization sidesteps this by using only `Nil`, which is a legitimate, narrower backend-specific choice, not a resolution of the underlying question.
- **Boundary translation cannot be linted structurally** — stated inline under the Boundary-translation topic. This shifts the burden of verifying the rule onto semantic review or AI-assisted static analysis, neither of which is yet built.

#### Related work
- Go's `error` interface (single method, value-oriented, identity via `errors.Is`/`errors.As` chain-walking) and Rust's `Error` trait with enum-based error families are both discussed in depth in the Go-focused companion analysis kept in the memar-go repository ([memar_type-vs-go_philosophy.md](https://github.com/GeniusesGroup/memar-go/blob/main/.agents/docs/memar_type-vs-go_philosophy.md)), which this document defers to rather than repeating. (Migrated from the document-level retired `Prior art`)
- The Detail/Quiddity split (type documentation vs. occurrence guidance) has no direct precedent identified in mainstream error-handling literature; it was arrived at independently during this discussion. Most prior art (Go's `error`, Rust's `Error` trait, Java's `Throwable`) carries a single free-text message or a context-display string with no built-in audience distinction. (Migrated from the Detail-and-Quiddity topic's retired `Prior art`)
- The boundary-translation pattern echoes the general "fault boundary translation" practice recommended in DDD and clean-architecture literature (translating infrastructure exceptions into domain exceptions at a repository boundary), but is stated here as an explicit, named, framework-wide rule rather than an implicit convention. The specific enrichment-before-logging step (attaching `ServerInstanceID`, `ConnectionID`, correlated IDs to the log record at the point of maximum available context) draws on observability engineering practices (structured logging, distributed tracing correlation) that exist in the ecosystem as best practices but are rarely enforced architecturally. (Migrated from the Boundary-translation topic's retired `Prior art`)
