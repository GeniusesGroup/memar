# Lexer Changelog

## Changelog

### Seed — split out of the Khayyam compiler discussion
- Time: 2026-08-12T11:30:00Z
- Type: Added
- Cited:
  - [Khayyam Compiler Directives](../khayyam-compiler.md) — Depends_on: the compiler-side Future-possibilities note that called for this abstraction to be specified as an independent protocol before any compiler consumes it; this document is the realization of that note.
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — directed, claimed: decided to split the topic out of the Khayyam compiler implementation discussion into its own session and protocol; framed the general question (what does a Tokenizer extract from a Source, and what contract does it offer consumers?); registered the initial consumer-relevant scope (frequency, weight, position, source relations); named the module `Lexer` rather than `Tokenizer`; raised the memory-management concern (per-unit allocation cost over large sources) and the HTML/URI/MIME domain question; asked whether one general Lexer serves all domains or each domain needs its own.

#### Summary
Initial seed document. Recorded the decision boundary from the session that split the topic out: the abstraction serves many consumers (compiler only one), must not start from the industry token shape (`kind + text + location`) nor from "one type per keyword"; candidate layering `Source → Lexical Unit → Syntax → Semantic Abstraction` named for examination; consumer-relevant metadata (frequency, weight, span, source relations) declared first-class protocol questions. Open questions registered: the minimal per-consumer contract, where weight lives, whether frequency is an output or a consumer-side computation, the Lexical-Unit/Syntax boundary, and whether non-compiler needs split the contract into core + profiles.

---

### Commissioned research as evidence
- Time: 2026-08-13T08:16:00Z
- Type: Added
- Cited:
  - [researchs/lexer - deepseek.md](../../researchs/lexer%20-%20deepseek.md) — Evidence: the survey report commissioned for this topic.
  - [researchs/Lexer - z.ai.eng.md](../../researchs/Lexer%20-%20z.ai.eng.md) — Evidence: the survey-plus-synthesis report (36+ systems, four families) commissioned for this topic.
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — requested, reviewed: commissioned two research reports (DeepSeek survey; z.ai survey-plus-synthesis) and reviewed both, judging the DeepSeek report closer to a research note and the z.ai report stronger on synthesis but premature on design.

#### Summary
Two external reports entered the record as evidence, deliberately subordinate to the concept work: the z.ai report surveyed 36+ systems across compiler/markup/structured-text/NLP families and proposed (a) a universal four-part conceptual token core (`kind/id, lexeme/source, span/extent, metadata`), (b) a four-stage pipeline (Normalizer → PreTokenizer → Model → PostProcessor), (c) memory strategies (pointer-pair, bump allocator, tape), and (d) an incremental-lexer shape; the DeepSeek report surveyed the same families and framed compiler vs NLP boundaries as explicit-vs-ambiguous. Neither report was adopted by default: every proposal was queued for examination against the concept being developed, with the boundary framing flagged immediately as the first candidate for rejection.

---

### Concept sessions — working positions established
- Time: 2026-08-15T05:43:00Z
- Type: Added
- Cited:
  - [researchs/Lexer - z.ai.eng.md](../../researchs/Lexer%20-%20z.ai.eng.md) — Evidence: source of the rejected universal-token-core and four-stage-pipeline proposals examined in these sessions.
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — claimed, argued: authored the founding positions across four sessions — module named `Lexer` not `Tokenizer`; no token-boundary assumptions (rejected the compiler-explicit/NLP-ambiguous framing); grounding of every unit in an observable source extent (the `TAB` vs `INDENT` and `EOF` arguments); the lexical model as immutable and identity-bearing (model change = new capsule; rule change = new model; versioned spec evolution, not mutation); structure of units determined by the model (rejected the universal `kind` and the open `metadata` bucket); position/span as a unit–source relationship; responsibility limited to decomposition (normalization, weight, frequency excluded); incremental behavior as change-reporting contract (`Source Change → Lexical Change`), no `IncrementalLexer` type; the `Lexical` capsule as a protocol-level lifecycle object (not "cache", not "context"); matching behavior exposed without prescribing representation; memory kept out of the ontology (concept ≠ representation ≠ strategy); the graph-modeling candidate (`tokens_by`/`tokenize` with tokens as a set on one relationship, not per-token edges); client-side lexing in scope with a registered trust concern; domain scope stated as "a source that admits a lexical model" (music/math not excluded by assumption); suggested naming start from the lexical-analysis vocabulary (lexeme/token/pattern); requested open-source landscape study be deferred until the model can serve as the comparison yardstick.
  - [ChatGPT](../../CONTRIBUTORS.md#chatgpt) — reviewed, argued: counter-posed each position, derived the rejects recorded in the base document (universal token core, four-stage pipeline, boolean matching behavior, enum representation, scannerless phase assumption), supplied the HTML/URI/MIME test-case framing, the play/ing non-substring example, and the SentencePiece counter-example against the ambiguity framing; flagged `TokenType` as a misleading name; proposed the candidate-name list.
  - [Super Z](../../CONTRIBUTORS.md#super-z) (GLM, research producer) — Reference: the z.ai research report's synthesis was the evidence base examined and partly rejected in these sessions; DeepSeek's survey report likewise (no contributor entry exists for it — recorded here as the report's producer).

#### Summary
The document's whole conceptual core was established and the base document rewritten to record it: thirteen working positions; the definition of the Lexer and the consumer contract; boundary principles (no boundary assumptions; grounding in observable extents); the Lexical Model with identity and immutability; the Lexical Type with matching behavior and inter-type relationships; unit/naming separation with classification kept out of the unit core; the delivery/memory split; the change contract; the `Lexical` capsule lifecycle; graph-modeling candidates; domain scope; the candidate concept inventory; the research-evidence disposition (adopted findings vs examined-and-rejected proposals). The document also migrated to the current Explanation-facet structure (Abstract / Introduction / Explanation / Results / Discussion) with a paired changelog, per [documentation-explanation.md](../documentation-explanation.md).

---

### Terminology link to lexical analysis formalized
- Time: 2026-09-06T10:30:00Z
- Type: Fixed
- Cited:
  - [Lexical analysis (Wikipedia)](https://en.wikipedia.org/wiki/Lexical_analysis) — Reference: the terminology entry point for the lexeme/token/pattern/token-type vocabulary this document already uses as evidence.
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — requested: link the Lexical Analysis concept explicitly in the base document.
  - [Super Z](../../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash, via the OpenCode agent) — edited: added the link at the two reader-facing points — the *What a Lexer is* topic (naming the process the protocol abstracts over) and the *Lexical Unit and naming* topic (the lexeme/token/pattern vocabulary, where the link had existed only in Prior art).

#### Summary
The Wikipedia Lexical Analysis reference, previously present only as a Prior-art bullet, is now linked inline where a reader first needs it: once in *What a Lexer is* (identifying the subject-matter process), once in *Lexical Unit and naming* (the terminology vocabulary under critique). No content change beyond the two link sentences.

---

### Audit pass — untransferred details from the founding sessions
- Time: 2026-09-06T11:10:00Z
- Type: Fixed
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — requested: before deleting the source chat transcripts, audit the transfer line by line rather than from memory; suspected summarization losses.
  - [Super Z](../../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash, via the OpenCode agent) — audited, applied: compared both transcripts against the document claim by claim and closed the gaps below.

#### Summary
Five gaps closed. (1) The model-lifetime open question wrongly stayed fully open: the sessions had settled that a capsule is permanently bound to its model (mutation examined and rejected, with the new-capsule-not-new-version identity argument); the question is narrowed to the residual transition-reporting case only. (2) The weight critique restored in full: naming any such quantity `weight` everywhere is not itself an abstraction — the word means unrelated things across NLP/IR/embeddings/attention — plus the general enumeration of consumer-side observations (relations to other units, properties computable only over the whole input). (3) The industry-shape critique restored: Token/TokenSequence/TokenStream/TokenCollection each carry different semantics, and the unit/occurrences/collection/ordering/traversal/production distinctions are the design session's to separate rather than merge into one type. (4) The Lexical Type topic now carries two session arguments previously dropped: recognition rules stay in the Lexer's conceptual domain because any other abstraction defining unit start/end conditions would itself be performing lexical processing (a domain-boundary statement, explicitly not a code-layout one), and the implementation-stage condition that regex-form rules are compiled once, never interpreted per match. (5) The research disposition now records that the reports' implementation roadmaps (9–13 month plan, Rust reference implementation) were set aside as premature planning, and the open-source landscape study carries the five evaluation questions from the founding research plus the independence-of-precedent condition on any industry-matching result.
