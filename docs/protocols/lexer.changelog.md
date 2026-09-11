# Lexer Changelog

## Changelog

### Seed — split out of the Khayyam compiler discussion
- Time: 2026-08-12T11:30:00Z
- Type: Added
- Cited:
  - [Khayyam Compiler Directives](../khayyam/compiler.md) — Depends_on: the compiler-side Future-possibilities note that called for this abstraction to be specified as an independent protocol before any compiler consumes it; this document is the realization of that note.
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — directed, claimed

#### What changed
- Created as the initial seed document.
- The initial consumer-relevant scope was registered: frequency, weight, position, source relations.
- The seed document recorded the decision boundary from the session that split the topic out: the abstraction serves many consumers (compiler only one), and must not start from the industry token shape (`kind + text + location`) nor from "one type per keyword".
- The candidate layering `Source → Lexical Unit → Syntax → Semantic Abstraction` was named for examination.
- Consumer-relevant metadata (frequency, weight, span, source relations) was declared a first-class protocol question.
- Open questions registered: the minimal per-consumer contract, where weight lives, whether frequency is an output or a consumer-side computation, the Lexical-Unit/Syntax boundary, and whether non-compiler needs split the contract into core + profiles.

#### Deliberation
- The topic was split out of the Khayyam compiler implementation discussion into its own session and protocol.
- The general question was framed: what does a Tokenizer extract from a Source, and what contract does it offer consumers?
- The module was named `Lexer` rather than `Tokenizer`.
- The memory-management concern (per-unit allocation cost over large sources) and the HTML/URI/MIME domain question were raised.
- It was asked whether one general Lexer serves all domains or each domain needs its own.

---

### Commissioned research as evidence
- Time: 2026-08-13T08:16:00Z
- Type: Added
- Cited:
  - [researchs/lexer - deepseek.md](../../researchs/lexer%20-%20deepseek.md) — Evidence: the survey report commissioned for this topic.
  - [researchs/Lexer - z.ai.eng.md](../../researchs/Lexer%20-%20z.ai.eng.md) — Evidence: the survey-plus-synthesis report (36+ systems, four families) commissioned for this topic.
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — requested, reviewed

#### What changed
- Two external reports entered the record as evidence, deliberately subordinate to the concept work.
- The z.ai report surveyed 36+ systems across compiler/markup/structured-text/NLP families and proposed (a) a universal four-part conceptual token core (`kind/id, lexeme/source, span/extent, metadata`), (b) a four-stage pipeline (Normalizer → PreTokenizer → Model → PostProcessor), (c) memory strategies (pointer-pair, bump allocator, tape), and (d) an incremental-lexer shape.
- The DeepSeek report surveyed the same families and framed compiler vs NLP boundaries as explicit-vs-ambiguous.
- Neither report was adopted by default: every proposal was queued for examination against the concept being developed.

#### Deliberation
- The commissioned reports were reviewed: the DeepSeek report judged closer to a research note, the z.ai report stronger on synthesis but premature on design.
- The boundary framing was flagged immediately as the first candidate for rejection.

---

### Concept sessions — working positions established
- Time: 2026-08-15T05:43:00Z
- Type: Added
- Cited:
  - [researchs/Lexer - z.ai.eng.md](../../researchs/Lexer%20-%20z.ai.eng.md) — Evidence: source of the rejected universal-token-core and four-stage-pipeline proposals examined in these sessions.
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — claimed, argued
  - [ChatGPT](../../CONTRIBUTORS.md#chatgpt) — reviewed, argued
  - [Super Z](../../CONTRIBUTORS.md#super-z) (GLM, research producer — also produced the DeepSeek survey report, for which no contributor entry exists) — Reference

#### What changed
- The document's whole conceptual core was established and the base document rewritten to record it: thirteen working positions; the definition of the Lexer and the consumer contract; boundary principles (no boundary assumptions; grounding in observable extents); the Lexical Model with identity and immutability; the Lexical Type with matching behavior and inter-type relationships; unit/naming separation with classification kept out of the unit core; the delivery/memory split; the change contract; the `Lexical` capsule lifecycle; graph-modeling candidates; domain scope; the candidate concept inventory; the research-evidence disposition (adopted findings vs examined-and-rejected proposals).
- The z.ai research report's synthesis was the evidence base examined and partly rejected in these sessions; the DeepSeek survey report likewise.
- The document also migrated to the current Explanation-facet structure (Abstract / Introduction / Explanation / Results / Discussion) with a paired changelog, per [documentation-explanation.md](../documentation-explanation.md).

#### Deliberation
- The founding positions were authored across four sessions (Omid Hekayati — claimed):
  - The module is named `Lexer`, not `Tokenizer`.
  - No token-boundary assumptions: the compiler-explicit/NLP-ambiguous framing was rejected.
  - Every unit is grounded in an observable source extent (the `TAB` vs `INDENT` and `EOF` arguments).
  - The lexical model is immutable and identity-bearing (model change = new capsule; rule change = new model; versioned spec evolution, not mutation).
  - The structure of units is determined by the model (the universal `kind` and the open `metadata` bucket were rejected).
  - Position/span is a unit–source relationship.
  - Responsibility is limited to decomposition (normalization, weight, frequency excluded).
  - Incremental behavior is a change-reporting contract (`Source Change → Lexical Change`), with no `IncrementalLexer` type.
  - The `Lexical` capsule is a protocol-level lifecycle object (not "cache", not "context").
  - Matching behavior is exposed without prescribing representation.
  - Memory is kept out of the ontology (concept ≠ representation ≠ strategy).
  - The graph-modeling candidate: `tokens_by`/`tokenize` with tokens as a set on one relationship, not per-token edges.
  - Client-side lexing is in scope, with a registered trust concern.
  - Domain scope is stated as "a source that admits a lexical model" (music/math not excluded by assumption).
  - Naming should start from the lexical-analysis vocabulary (lexeme/token/pattern).
- The open-source landscape study was to be deferred until the model can serve as the comparison yardstick (Omid Hekayati — claimed).
- Each position was counter-posed (ChatGPT — argued).
- The rejects recorded in the base document were derived: universal token core, four-stage pipeline, boolean matching behavior, enum representation, scannerless phase assumption (ChatGPT — argued).
- The HTML/URI/MIME test-case framing, the play/ing non-substring example, and the SentencePiece counter-example against the ambiguity framing were supplied (ChatGPT — argued).
- `TokenType` was flagged as a misleading name (ChatGPT — argued).
- The candidate-name list was proposed (ChatGPT — argued).

---

### Terminology link to lexical analysis formalized
- Time: 2026-09-06T10:30:00Z
- Type: Fixed
- Cited:
  - [Lexical analysis (Wikipedia)](https://en.wikipedia.org/wiki/Lexical_analysis) — Reference: the terminology entry point for the lexeme/token/pattern/token-type vocabulary this document already uses as evidence.
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — requested
  - [Super Z](../../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash, via the OpenCode agent) — edited

#### What changed
- The Wikipedia Lexical Analysis reference, previously present only as a Prior-art bullet, is now linked inline at the two reader-facing points where a reader first needs it: once in *What a Lexer is* (naming the subject-matter process the protocol abstracts over), once in *Lexical Unit and naming* (the lexeme/token/pattern vocabulary under critique) (Super Z — edited).
- No content change beyond the two link sentences.

#### Deliberation
- Linking the Lexical Analysis concept explicitly in the base document was requested (Omid Hekayati — requested).

---

### Audit pass — untransferred details from the founding sessions
- Time: 2026-09-06T11:10:00Z
- Type: Fixed
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — requested
  - [Super Z](../../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash, via the OpenCode agent) — audited, applied

#### What changed
- Both transcripts were compared against the document claim by claim, and five gaps were closed:
  - The model-lifetime open question wrongly stayed fully open: the sessions had settled that a capsule is permanently bound to its model (mutation examined and rejected, with the new-capsule-not-new-version identity argument); the question is narrowed to the residual transition-reporting case only.
  - The weight critique restored in full: naming any such quantity `weight` everywhere is not itself an abstraction — the word means unrelated things across NLP/IR/embeddings/attention — plus the general enumeration of consumer-side observations (relations to other units, properties computable only over the whole input).
  - The industry-shape critique restored: Token/TokenSequence/TokenStream/TokenCollection each carry different semantics, and the unit/occurrences/collection/ordering/traversal/production distinctions are the design session's to separate rather than merge into one type.
  - The Lexical Type topic now carries two session arguments previously dropped: recognition rules stay in the Lexer's conceptual domain because any other abstraction defining unit start/end conditions would itself be performing lexical processing (a domain-boundary statement, explicitly not a code-layout one), and the implementation-stage condition that regex-form rules are compiled once, never interpreted per match.
  - The research disposition now records that the reports' implementation roadmaps (9–13 month plan, Rust reference implementation) were set aside as premature planning, and the open-source landscape study carries the five evaluation questions from the founding research plus the independence-of-precedent condition on any industry-matching result.

#### Deliberation
- Before deleting the source chat transcripts, the transfer was to be audited line by line rather than from memory; summarization losses were suspected (Omid Hekayati — requested).

---

### Research integration pass — the three commissioned reports audited against the document
- Time: 2026-09-06T11:40:00Z
- Type: Added
- Cited:
  - [researchs/Lexer - z.ai.eng.md](../../researchs/Lexer%20-%20z.ai.eng.md) — Evidence: the 36+-system synthesis behind the new positions (trivia, errors, preprocessing, context-carrying models, per-type registries, delivery forms, lexer-earning-its-keep conditions).
  - [researchs/lexer - deepseek.md](../../researchs/lexer%20-%20deepseek.md) — Evidence: the survey behind the C lexer-hack lesson, the source-ownership recommendation, and the Unicode support note.
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — directed
  - [Super Z](../../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash, via the OpenCode agent) — audited, applied.

#### What changed
- The three research reports were compared against the document finding by finding.
- Adopted into the body:
  - parser-driven lexing as a fourth architecture (position 3)
  - the lossless-preprocessing versus lossy-normalization distinction in position 9 (decoding, newline normalization, and malformed-sequence replacement are Source-side and specification-mandated in HTML5/CSS - not the normalization the position excludes)
  - the lexer-earning-its-keep decision rule in Domain and consumers
  - the C lexer-hack and Clang annotation-token evidence in Boundary principles
  - the context-carrying-models verdict in The Lexical Model (Python INDENT/DEDENT, YAML, HTML5 modes, JSX, CommonMark whole-document references) with the passive/active question converted to a settled direction
  - the non-determinism registration (sampling segmenters)
  - two new topics - Trivia (six policies; placement open) and Errors (two philosophies; unit-grounded versus separate diagnostics open, with a required conformance check against the Error protocol)
  - source reference-not-ownership and the chunked-stream intake question in Lifecycle
  - push-sink as a first-class delivery form plus lookahead in Delivery
  - the per-type registry concept and the lexeme-word trap in Lexical Unit and naming
  - three stress examples (CommonMark, BPE, indented models) in Examples
  - prior-art extensions
- Unresolved questions updated: Q4 converted to settled-direction-plus-open-shape; Q10 converted to settled-direction-plus-open-allocation (the research's weight/frequency taxonomy); Q12 converted to settled-signal-plus-open-channel; Q13 strengthened with the four feedback evidence patterns; Q15 extended with input-expansion attacks; Q16-Q20 added (trivia policy placement, lexical error shape, round-tripping, non-deterministic models, preprocessing placement).
- Candidate inventory extended with the per-type registry, trivia policy, lexical error, and the Sink delivery form.
- Document-wide Drawbacks gained an absent-topics self-audit item and an evidence-traceability item (the survey's per-family source files are not in this repository).

#### Deliberation
- A full audit of the three research files against this document was asked for before their companion chat transcripts are deleted (Omid Hekayati — directed).
- It was confirmed that where research conclusions conflict with the sessions' positions, the sessions' positions remain authoritative — back-channel deferral, pipeline rejection, open Khayyam-rule-set question (Omid Hekayati — directed).

---

### Second migration wave: Discussion retired; routed to changelog and handoff
- Time: 2026-09-11T08:29:10Z
- Type: Changed
- Cited:
  - [Documentation — Explanation](../documentation-explanation.md) — Depends_on: the three-section skeleton and the Relevance-discipline routing this migration applies are defined by the Explanation facet's governing specification.
  - [Documentation — Handoff](../documentation-handoff.md) — Depends_on: any open work created by this migration follows the Handoff facet's specification.
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) - directed
  - [Super Z](../../CONTRIBUTORS.md#super-z) (GLM 5.3) - applied

#### What changed
- The base document's `## Discussion` section was retired and its five subsections routed per the Relevance-discipline routing.
- Its twenty Unresolved questions moved to the newly created [lexer.handoff.md](./lexer.handoff.md) (handoff created, not extended) as Open Questions, each State line carrying the original item number for traceability to this changelog's earlier entries that reference questions by number.
- Its five Future-possibilities items became the handoff's Anticipated Work.
- Its six Drawbacks are preserved in this entry below.
- Of its ten Rationale-and-alternatives items, one — the one-type-per-keyword starting point — is preserved in this entry below; the other nine were dropped rather than migrated because the body already records each rejection with its argument: the Tokenizer naming (position 1), the industry token shape as a starting point (position 7 with the too-rich/too-vague guard in What a Lexer is, and the research disposition), the one-general-Lexer and one-lexer-per-domain assumptions (position 2 with Domain and consumers), the four-stage pipeline as core (position 13 and What the research established), the open `metadata` field (position 7), the mutable model/rules (the Immutability paragraph of The Lexical Model), matching behavior as an enum (Lexical Type), one edge per token (Modeling the results), and frequency/weight inside the unit (position 9).
- Of its seven Prior-art bullets, four are preserved in this entry below (compiler implementations; incremental and hybrid consumers; non-materializing designs; NLP/LLM tokenization); the lexical-analysis-literature bullet was dropped as already graduated into [Lexical Unit and naming](./lexer.md#lexical-unit-and-naming); the "Prior-art bullets" editorial note was dropped as duplicated by the preserved bullets and by this changelog's research-integration entry ("prior-art extensions"); and the commissioned-research pointer was dropped as already recorded by this changelog's "Commissioned research as evidence" entry.
- The two inline pointers to the retired section (in the Abstract and in Errors, both linking `#unresolved-questions`) were repointed in this same pass to [Open Questions](./lexer.handoff.md#open-questions); nothing else in the base document was touched beyond the Discussion removal.

#### Considered and not done (migrated from the retired Rationale and alternatives)
- **Start from one type per keyword (rejected)**: a keyword is a linguistic sign, not necessarily an independent concept; several keywords may share one abstraction, and a keyword may have no semantic type of its own. If the final model happens to yield one type per keyword, that is an outcome, not a starting assumption.

#### Related work (from the retired Prior art)
- **Compiler implementations**: Go's token (`kind`, text, position) as the common industry shape under critique; Rust's deliberately layered design (a minimal `kind + len` token low-level, spans added at a higher layer) as evidence that representation layering is real; rustc_lexer as evidence for a lexical layer cleanly separated from the compiler; ANTLR for grammar-driven lexical models and channels; Roslyn for first-class trivia and green/red incremental trees; Zig for the minimal `tag + start/end` shape.
- **Incremental and hybrid consumers**: Tree-sitter for incremental re-lexing over edits and for the parser-driven `TSLexer` pattern (no token stream at all); the HTML5 tokenizer as the standing example of a stateful tokenizer whose state interacts with tree construction (the back-channel evidence); V8 for ring-buffer lookahead and lazy pre-parsing.
- **Non-materializing designs**: libyaml's public token API (both token and event views over one scanner); llhttp and simdjson, which deliberately present lexical-level results without materializing per-unit objects — evidence that the contract and the memory strategy can be decoupled; uriparser's zero-allocation pointer-pair tokens; protobuf's `io::Tokenizer`; RFC 5322 as the specification that itself mandates a lexical layer.
- **NLP/LLM tokenization**: BPE, WordPiece, SentencePiece, Unigram, vocabulary IDs, offsets — evidence that deterministic segmentation needs no whitespace assumptions and that frequency/significance observations are consumer-relevant; spaCy's Token/Lexeme separation as the registry pattern; ICU BreakIterator and UAX #29 as Unicode segmentation standards; PTBTokenizer's invertibility and SentencePiece's reversibility as the round-trip evidence.

#### Drawbacks (from the retired body Discussion)
- **Under-determination risk.** The abstraction deliberately leaves unit structure, recognition strategy, and delivery open. That is the point, but it means the document alone does not yet enable an implementation; the design session must convert these positions into a checkable protocol, and until then two implementers could build incompatible things both claiming conformance.
- **Naming instability.** Every core name (the output unit, the type, the capsule's parts) is provisional until the terminology section lands; documents written against these names may need repointing.
- **Grounding-principle cost.** Excluding invented units means designs that want `INDENT`-style or `EOF` tokens must build them above the Lexer. Some compiler consumers will find that less convenient than the industry norm, and the protocol should be honest that this is a deliberate cost.
- **Immutability cost.** A consumer holding long-lived capsules across a specification upgrade must manage an identity swap (old capsule ends, new capsule begins) rather than mutate in place.
- **Absent topics (self-audit).** Three dimensions the founding sessions never named and this document only registered after the commissioned research — trivia, lexical errors, and input preprocessing — are present as open questions but lack settled positions. If any of them turns out to load-bearing for the minimal contract (they plausibly are: errors especially), the design session's scope grows accordingly.
- **Evidence asymmetry.** The commissioned research's per-family detail lives in external reports (and the four per-family source files behind them are referenced by paths that no longer exist in this repository — `/home/z/my-project/research/...`). A reader auditing a claim adopted from the survey must trust the summary here or the two reports in `researchs/`; the primary-source traceability the survey itself advertises is not preserved in this repository.
