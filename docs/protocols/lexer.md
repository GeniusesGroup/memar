---
Title: "Lexer"
Status: Draft
Start Date: 2026-08-12
ID: 496248
---

# Lexer
This document records the concept work behind Memar's Lexer protocol — the working positions, boundaries, and open questions reached in the sessions that defined it. It is a Draft: a dedicated design session will turn these positions into the protocol's actual specification. See [Protocol](../protocol.md) for the general concept of a protocol.

## Abstract
The Lexer protocol defines a general abstraction for lexical processing: identifying lexical units in a source according to a lexical model, and delivering them to consumers under a stated contract. The abstraction is defined independently of any domain, any consumer, and any tokenization strategy — a compiler's parser, a search indexer, a syntax highlighter, a language-model tokenizer, and a URI or MIME-header parser are equally legitimate consumers, and a consumer that parses characters directly without a lexer remains a valid architectural alternative. The concept boundary reached so far: the Lexer's responsibility is lexical decomposition and nothing else (no normalization, weighting, ranking, counting, or grammatical/semantic interpretation); it must make no assumption about what constitutes a token boundary; every lexical unit it reports must be grounded in an observable extent of the source; the lexical model that drives it is immutable and identity-bearing; and the processing capsule is a protocol-level lifecycle object that reports how its output changed so consumers never re-derive changes from raw input. What remains open — the structure and naming of lexical units, the delivery shape, the model's possible active behavior, and the final type inventory — is registered under [Unresolved questions](#unresolved-questions).

## Introduction

### Motivation
The trigger was the Khayyam compiler's need for [lexical analysis](https://en.wikipedia.org/wiki/Lexical_analysis) — but the same reasoning that separates other protocols from their consumers applies here: a tokenizer serves **many consumers, of which a compiler is only one**. Text-analysis systems, search and indexing, syntax highlighting, and language-model tokenization are equally legitimate consumers, and some of their needs (occurrence positions, frequency, significance) are already load-bearing in AI systems today. The abstraction is therefore defined by the general question — *what does a Lexer extract from a source, and what contract does it offer its consumers?* — not by what any one consumer wants.

Two further observations forced the concept open beyond the classic compiler shape. First, real systems disagree about whether a lexer exists at all: some domains (HTML, URI) are routinely parsed directly from characters, while others (email per RFC 5322) have an explicit lexical analyzer — so "phase before the parser" cannot be part of the definition. Second, lexical processing has become a load-bearing part of AI systems (subword tokenization, vocabularies, offsets), which shows the concept is broader than compilers and must not be shaped by compiler history alone.

### Methodology
This document's content was arrived at across four working sessions (2026-08-12 through 2026-08-15) that split the topic out of the Khayyam compiler discussion and developed it concept-first, per Memar's protocol-before-implementation discipline. Two external research reports were commissioned as evidence — a survey-oriented report (DeepSeek) and a survey-plus-synthesis report over 36+ systems (z.ai), summarized in [What the research established](#what-the-research-established) — and were deliberately treated as evidence rather than authority: every architecture proposal they contained (a universal four-part token core, a four-stage NLP-style pipeline, a lexer back-channel) was examined and rejected or deferred rather than adopted by default. Each position below was argued for and against across the sessions; the full provenance, including the session transcripts and both research reports, is recorded in [lexer.changelog.md](./lexer.changelog.md).

## Explanation

### Working positions
The sessions converged on the following statements. They are the settled core of the concept; each is elaborated in its own topic below.

1. The module is named **Lexer**, not Tokenizer: tokenization is one capability of a Lexer, not the whole concept. If the Lexer later performs other lexical operations, the narrower name would be wrong.
2. The Lexer is **domain-independent** and **consumer-independent**. Programming languages, markup, structured textual formats (URI, MIME, HTTP and email headers, JSON, CSV), natural language, and machine-oriented tokenization are all in scope; a compiler is one consumer among many.
3. Being a phase before a parser is **not part of the Lexer's definition**. `Source → Lexer → Parser` is one architecture, not the architecture; `Source → Lexer → {Parser, Search, Highlighting, Indexer, Analyzer}` and `Source → Lexer → Lexical Analysis` (no parser at all) are equally valid, and a consumer may legitimately skip the Lexer entirely (scannerless parsing).
4. **The Lexer must make no assumption about what constitutes a token boundary.** Boundaries are determined by the lexical model, not by the Lexer concept. The common compiler-vs-NLP framing ("compilers have explicit boundaries; natural language is ambiguous") is rejected as an architectural property: even a compiler may need context-dependent boundaries, and a deterministic algorithm like BPE produces fixed segmentation once its vocabulary is fixed.
5. **Every lexical unit must be grounded in an observable extent of the source.** The Lexer observes and segments; it does not invent meaning. Reporting an observed `TAB` is lexical processing; translating it into `INDENT` assigns new meaning to the observation and belongs to a later layer. Synthetic markers such as `EOF` are end-of-input signals, not necessarily lexical units.
6. The tokenization method — whitespace splitting, regular expressions, state machines, merge rules, probabilities — belongs to the **lexical model**, not to the Lexer concept. A declarative abstraction must not hard-code any one recognition technique.
7. The structure of a lexical unit is **determined by the lexical model**, not by the Lexer: one model may produce `{kind, extent}`, another `{vocabulary_id, extent}`, another `{category, normalized_value}`. There is no universal token shape; in particular, an open-ended `metadata` field is rejected as a junk drawer, and `kind` is not intrinsic to the unit.
8. **Position/span is a relationship between a unit and its source, not an intrinsic property of the unit.**
9. The Lexer's responsibility is lexical decomposition and nothing else: not normalization, weighting, ranking, counting, interpreting, or understanding. What a consumer may still want to know about a unit — occurrence count, relative frequency, significance, the unit's relations to other units, or properties computable only over the whole input about it — are observations *in a context*, not intrinsic unit properties; they belong to later layers or separate abstractions, and naming any of them `weight` everywhere is not itself an abstraction (in NLP/IR/embeddings/attention the word means unrelated things).
10. The Lexer is deliberately **not restricted by algorithm** (e.g. regular languages). Restricting the algorithm while keeping the responsibility would force exception after exception (HTML, indentation-sensitive languages, stateful protocols) until the abstraction becomes an incomplete parser. The distinction is: keep *what it does* precise; keep *how it determines lexical units* open.
11. `TokenSequence`, `TokenStream`, and views-on-source are **candidate concepts**, not settled types; delivery may be lazy or eager, pull or push. Memory representation is kept out of the conceptual ontology (see [Delivery and memory](#delivery-and-memory)).
12. All domains named above — and the research behind them — are **test cases** for the abstraction, not its definition.
13. A consumer-side pipeline such as `Normalizer → PreTokenizer → Model → PostProcessor` is one implementation pattern of some lexical models, **not** the core architecture of the Lexer.

### What a Lexer is
A Lexer is the abstraction that applies a lexical model to a source and produces lexical units. Its subject matter is the process the literature calls [lexical analysis](https://en.wikipedia.org/wiki/Lexical_analysis) — deriving a structure of meaningful units from a flat source — but the protocol's contribution is the general abstraction over that process, not any one implementation of it:

```text
                 ┌─────────────────────┐
                 │       Source        │
                 └──────────┬──────────┘
                            │  lexical processing
                            │  (applies a Lexical Model)
                 ┌──────────▼──────────┐
                 │    Lexical Units    │
                 └──────────┬──────────┘
                            │  delivery / collection
              ┌─────────────┴─────────────┐
              ▼                           ▼
     Sequence / materialized       Stream / incremental
              │                           │
              └─────────────┬─────────────┘
                            ▼
     Parser · Search · Highlighting · Indexer · Analyzer · Models
```

The general question the protocol answers is not "what should the compiler's lexer look like?" but: **what does a Lexer extract from a source, and what contract does it offer its consumers?** Each consumer then becomes one realization of that contract. The consumer's view of the contract is deliberately two-sided: the Lexer must expose the *decisions* it makes (what was recognized, where, as what) without prescribing the *representations* behind those decisions.

A deliberate guard against two opposite failure modes shapes this definition. If the Lexer's definition is too rich — a universal `Token {kind, span, value, metadata}` — the abstraction collapses into a bag of representations that fit no consumer exactly. If it is too vague — "the Lexer produces things" — it loses all meaning relative to a parser. The working resolution is the responsibility statement in [Working positions](#working-positions) (decomposition only) plus the boundary principles below; the remaining freedom in unit structure is bounded by the question *what makes something a lexical unit at all*, which is the design session's central task.

### Domain and consumers
The Lexer is not limited to any language or any consumer. Candidate consumers identified across the sessions:

- **Compilers, linters, and analysis tools** — the classic consumer; needs units, extents, and change tracking.
- **Search, indexing, and text analysis** — needs units and positions, often without any parser downstream.
- **Syntax highlighting and editors** — need incremental updates over changing documents.
- **Language models and NLP** — need vocabulary-based units, offsets, and per-source frequency/significance observations.
- **Structured-format consumers** — URI, MIME, HTTP and email headers, JSON, CSV: domains whose textual decomposition is a concern independent of the final parse.
- **Client-side preprocessing** — e.g. lexing text in the user's client before submission. This use is in scope, with a registered concern: the output of lexing untrusted input may not be trustworthy; how the protocol addresses that is deferred to the security discussion of the design session.

Whether a given domain *uses* a Lexer is the consumer's architectural choice. HTML is the standing test case: production HTML parsers consume characters directly, which does not prove the abstraction unnecessary — it proves that adopting the Lexer must pay for itself per consumer. The protocol's obligation is only that the abstraction be good enough that a domain *could* define its lexical model on it.

### Boundary principles
Two principles bound what the Lexer may report.

**No boundary assumptions.** The Lexer must not assume units are separated by whitespace or punctuation, that recognition is deterministic, or that any particular algorithm defines boundaries. Boundary determination is the lexical model's property. The compiler/NLP "explicit vs ambiguous" split fails as an architectural property from both directions: compilers can need contextual boundaries (state, lookahead, mode switching), and subword algorithms like BPE are fully deterministic once their vocabulary and merge rules are fixed — SentencePiece even operates on raw bytes without whitespace pre-tokenization.

**Grounding in observable extents.** Every lexical unit must be grounded in an observable extent of the source. The founding example: for source `\tfoo()`, reporting `TAB` followed by `IDENTIFIER(foo)` is reporting observations; reporting `INDENT` is assigning an interpretation the source does not contain — that belongs to a later layer (the parser may label the `TAB` based on surrounding units). The same reasoning excludes synthetic tokens such as `EOF` from the core: end-of-input is a signal about the stream, not a unit observed in the source. One edge is deliberately left open: if a lexical model explicitly defines "this source sequence is one unit with label X", it must still be determined with real examples whether such labels remain *classification* or become *semantic interpretation* — the grounding principle is accepted, and the classification/interpretation boundary is not yet drawn.

A unit grounded in an extent need not be a *substring*: a vocabulary model splitting `playing` into `play` + `ing` still grounds both units in source extents. Whether non-substring outputs (if any model ever requires them) need an explicit derived-from relationship is an open question; the founding position is that the protocol does not admit them at the core.

### The Lexical Model
The Lexical Model is the concept that determines *what* is recognizable in a source and *how*. It is not mere configuration: it gives the Lexer the set of lexical types plus the rules governing their interactions — precedence, coexistence, nesting, conflict resolution — and it determines the structure of the units it produces. Whether the model is a passive set of types and rules or a more active abstraction that carries context and state (recognition depending on what has already been seen, as in HTML or indentation-sensitive languages) is deliberately open; the answer shapes the type design, nesting, competition, and incremental updates, and must be settled before type names are finalized.

Two properties are settled:

- **Identity.** The model is an identity-bearing concept, not a temporary object: two models differing in a single rule are different models, and that difference is meaningful to the system. This matters for caching, for sharing one model across several processing capsules, for versioning, and for graph modeling — and it must be fixed in the model before an implementation is forced to invent it.
- **Immutability.** The model — and each lexical rule within it — is immutable. A rule change produces a new model identity; a model change produces a new processing capsule. This is not merely a performance stance (though it is what makes compile-once rule processing economical): a capsule exists to hold *one specific interpretation* of its source under *one specific model*; with a different model it is a different capsule, not a new version of the old one. Specification evolution is represented by versioned identities, not mutation — `HTML Lexical Model v1` and `v2` are two models, and a healthy system can route old documents to v1 and new documents to v2. A legitimate spec release is therefore not modeled as "the rules changed mid-work"; conversely, if a system genuinely needs its rules to change mid-stream, that is a design alarm to investigate.

Because rules are immutable, they can be compiled once — into an automaton, a table, or any other representation — and reused for the capsule's whole lifetime without re-parsing or re-interpreting rule text. The abstraction must preserve this possibility without tying itself to any one representation (regex is a candidate input format, not the abstraction) — and if regex is chosen as the rule format, the implementation-stage condition is explicit: rules are compiled once at preparation, never interpreted per match.

### Lexical Type
The model's central component is the concept provisionally called **TokenType** — a name the sessions flagged as misleading (too close to the output unit's name) and left open, with candidates: `LexicalType`, `LexicalKind`, `LexicalDefinition`, `LexicalRule`, `LexicalUnitType`, `TokenDefinition`, `LexicalPattern`. Its working definition: a lexical type **identifies a lexical kind and defines the recognition behavior for occurrences of that kind** — what it is, and how to recognize it. Whether it is a category, a rule, or identity-plus-rule (the most likely shape) is open.

Its recognition behavior goes beyond a single-character start/end pair. Boundary conditions may be single characters, sequences, patterns, contextual conditions, or explicit events (e.g. end-of-input); the paragraph case — two consecutive newlines, the first opening the unit and the second closing it — shows single-character start/end is insufficient. Start/end may not even be direct methods but one capability group under a broader recognition definition.

Two distinct questions attach to the type:

- **Matching behavior.** When several types can match at a position, part of the resolution belongs to the matched type itself: after recognizing an occurrence of this type, does the Lexer keep recognizing other candidates within its extent, own the region exclusively, or re-lexicalize it under another model? The protocol must expose this decision — but must not prescribe its representation. It is not necessarily an enum (`ALLOW|DENY|NEST`); an implementation may legitimately return a general abstraction that maps to an enum, a state machine, a flag set, or anything else. A single boolean such as `allow_other_tokens_until_end` is explicitly rejected as too narrow: ownership, nested re-lexicalization, and scope termination are different behaviors.
- **Inter-type relationships.** The rest of the resolution — precedence (`A > B`), containment (`A can contain B`), coexistence, lexical scope — belongs to the relationships between types inside the Lexical Model, not to any single type. The two layers must not be conflated.

The type inherits the project's general Type machinery (identity, naming) rather than redefining it — it is a type in the existing sense, extended with lexical recognition capabilities. Terminology must not drive this decision: inheritance from `DataType` (or similar) holds only insofar as that abstraction's own definition fits, not because the name contains "Type". The founding session's consumer-side sketch, recorded for history and immediately critiqued (misleading single-character method names; Start/End premature as intrinsic definition):

```khayyam
tp TokenType ab {
    DataType
    Field_MediaType
    Charecter_Start() ()
    Charecter_End() ()
}
```

The recognition rules — boundary conditions, matching behavior — belong to the Lexer's own conceptual domain. The founding sessions found no evidence for moving them out: any abstraction elsewhere that defines "with what pattern or conditions a lexical unit starts and ends" would, in practice, be performing lexical processing and re-deriving this module. This is a statement about the domain boundary, not about code layout — an implementation is free to place these pieces in separate packages; the protocol claim is only that they are concepts of this module.

### Lexical Unit and naming
The output of lexical processing is a **lexical unit occurrence**: an observed instance in the source, identifiable by its extent and by which lexical type identified it. The occurrence/type relation (`identified_as`) is part of the concept; whether it is realized as a field or a relationship is a representation choice, not a design fork. The founding sessions deliberately kept "occurrence" (occurrence-in-a-source) distinct from the type that defines the kind.

Naming is unsettled and consciously so. The word **token** is overloaded across the literature and across this project's consumers; the sessions decided that abstraction and capsule names must avoid it (at most appearing as a compound such as "lexical token", and always in prose rather than in names). The [lexical-analysis](https://en.wikipedia.org/wiki/Lexical_analysis) literature distinguishes **lexeme** (the source character sequence matching a lexical rule), **token** (a representation/classification of that lexeme for later stages), **token type/kind** (the classification), and **pattern** (the rule defining the lexeme) — and these definitions differ between sources, so they are used as evidence, not authority. Whether the output concept is closest to *lexeme* or to *token*, and whether the classic `Lexeme → Token` layering exists in this model at all, must be derived from the concept work, and a terminology section fixing the project's vocabulary is a prerequisite for settling any name.

Classification is deliberately kept out of the unit's core. A classification can form in two different places: when a unit is registered as an entity in the system (its lexical identity), and when an occurrence is classified *in a context* — the same word `run` is a verb in one sentence and a noun in another, but tokenization is identical in both. Classifications also layer (lexical → syntactic → semantic) and must not collapse into a single `kind` field on the unit.

### Delivery and memory
How units reach consumers is a contract question, not only an implementation detail. Three questions are kept strictly separate:

```text
What is a lexical unit?      (concept)
How is one represented?      (representation)
How are many units managed?  (collection/delivery strategy)
```

Candidate delivery forms: a materialized sequence, an incremental stream (`next()`, with consumed representations reusable), and views on the source (the unit's text is never copied; it is read from the source through its extent). `TokenSequence` and `TokenStream` are promising distinct candidates — sequence as materialized collection, stream as gradual consumption — but their exact semantics must be established from real consumer cases, not from the names. The finer distinctions behind these names are the design session's to separate: the unit, its occurrence(s) in a source, the collection of occurrences, their ordering, traversal over them, and their production are different concerns that industry shapes tend to merge into one type.

The founding sessions registered a hard memory concern — a lexer over a large source that materializes one runtime object per unit can spend more on representation than on content, in allocation pressure, ownership complexity, and string copies — and then made a scoping decision: **the conceptual model, the runtime representation, and the memory strategy are three different concerns**, and only the first belongs to this protocol's ontology. Zero-copy extents, contiguous collections, pools, and tapes are implementation research; the contract must merely not *forbid* them (e.g. by requiring materialized strings). The part of the memory cost that comes from string handling is deferred to the string abstraction's own discussion.

### Change contract
Incremental behavior is a contract, not a type: there is no `IncrementalLexer` concept. The contract has three positions:

```text
Source Change  →  Lexer (capsule)  →  Lexical Change
```

- The capsule learns of a source change either by **pull** (a caller invokes a re-read/update method, preferably passing the change's location) or by **push** (the capsule listens to source-change events while it lives). The Lexer never mutates the source.
- The Lexer reports **changes in its own output, not raw source changes**: which occurrences were removed, added, or changed, which extent of the output was invalidated, and which regions are unchanged. Because every occurrence carries its position, a listener can act on the change without re-searching the source.
- The consumer decides what to do with the report; re-lexicalization strategies (full re-check, range re-check, caches, dependency graphs) are implementation concerns the contract deliberately stays independent of.

One subtlety is registered now: a one-character change does not necessarily change one unit. Longest-match rules and stateful models can propagate a change across several boundaries, so the change report must describe *propagation* (affected and unchanged extents), not just "the changed unit". Who determines the affected scope — the Lexer itself, or a higher abstraction that passes a change scope in — is open.

The **Source Change** abstraction itself is intentionally out of this protocol's ownership: editors, indexers, parsers, caches, and graph stores are equally legitimate consumers of "this content changed, here is where". It must be defined as a general abstraction — jointly with the content domain — with its own document; the Lexer protocol will define only its side of the exchange.

### Lifecycle: the Lexical capsule
The unit of work is a **capsule named `Lexical`** (not "Lexical Context" — the plain name suffices), created by an initialization call taking the source access and the Lexical Model, and alive until the consumer disposes it. While it lives, it is the protocol-level holder of: source access, the lexical model, the compiled rule representations, the lexical result, and — if requested — the change subscription that keeps the result updated and announces lexical changes. This is an obligation of the module protocol, not an implementation freedom: a capsule that dropped its change subscription, or required the caller to re-drive updates, would violate the contract. "Capsule" here is deliberately not "cache": the cache question (what to keep, why, for how long) stays an implementation concern, and the sessions explicitly retired the word *state* from the protocol vocabulary until it can be defined concretely — what is kept, why, and for how long.

The capsule's two dependencies are fixed for its lifetime:

```text
Lexical.source = fixed dependency   (source changes arrive; the source is never mutated)
Lexical.model  = fixed dependency   (a different model means a different capsule)
```

Model changes therefore do not mutate a capsule: the old capsule ends and a new one is initialized for the same source under the new model.

### Modeling the results
How lexical results appear in Memar's graph modeling is a candidate, not a decision. The founding discussion rejected one edge per token (an explosion of connections) in favor of the shape the user proposed: tokens registered in a shared dictionary/node, with the content-to-tokens relationship carried as a set on a single relationship rather than as per-token edges:

```text
(text)-[:tokens_by]->(module)
(module)-[:tokenize]->(text)
```

Registered open points, to be settled with the general modeling discipline (see [Modeling](../modeling.md), in particular the attribute-or-edge test): whether `Module` is the right node for the tokenizer role or a dedicated tokenization node is needed (`Source -tokenized_by-> Tokenization -produces-> [units]`); whether `tokens_by`/`tokenize` are independent relationships or inverses of one; and whether an individual unit ever becomes a node at all. The underlying principle already settled: **tokenization is an observation/process performed on a source**, not a per-unit graph of ownership edges.

### Domain scope
The Lexer is not finalized for "human language text" or "programming languages" — both are just domains admitting lexical models. The scope condition is deliberately domain-neutral: **a source that admits a lexical model capable of identifying lexical units.** Arithmetic expressions admit one; textual music notation admits one. Graphic notations raise a genuinely open question: standard musical notation lives on a five-line staff, and its natural source units are visual symbols and regions, not characters. If the protocol's Source side stays character-based (character/code point/byte), such domains are excluded — but by argument, not by assumption: whether the Source abstraction generalizes to non-character units is an open question, and no claim is made either way for standard notation.

Structures above the unit — sentences, paragraphs, sections — are **domain structures, not lexical concepts**. A lexical model may legitimately include rules that detect sentence or paragraph boundaries (a boundary is a boundary), and the Lexer then reports units at those extents; but the Lexer does not own the concepts `Sentence` or `Paragraph`, does not answer "which sentence is this word in" as a lexer question, and is by default not responsible for meaning, syntax, semantics, normalization, weight, ranking, or interpretation. Whether those structures can live inside a lexical model without the Lexer owning the concepts is accepted as *possible* (a corpus model may produce units that the consumer names "sentences"), with the standing guard: the unit concept must not be stretched until everything becomes a token.

### Candidate concept inventory
The concepts on the table after the founding sessions — candidates for the design session to confirm, merge, or drop:

| Candidate | Working meaning |
| --- | --- |
| Source | The input side; its unit granularity (character vs other) is itself open |
| Lexical Model | Drives recognition; immutable, identity-bearing; owns inter-type rules |
| Lexical Type | Defines a lexical kind and its recognition behavior; name unsettled |
| Lexical Unit / occurrence | An observed unit in a source; structure model-defined; grounded in an extent |
| `Lexical` capsule | The lifecycle object holding source access, model, compiled rules, result, change subscription |
| Lexical Change | The report of how the lexical result changed after a source change |
| Source Change | A separate general abstraction (not owned by this protocol) |
| Sequence / Stream / View | Candidate delivery forms; possibly two concepts, possibly one concept plus a delivery mechanism |

### Examples the abstraction must express
The design session validates the abstraction against deliberately diverse, textually-described examples (not code): a programming language (identifier/literal/operator recognition without any syntax or semantics knowledge); HTML (nested lexical scopes, content re-lexicalized under different rules — without concluding HTML *must* use this Lexer); URI (lexical decomposition as an independent concern even when the consumer is a parser/validator); MIME headers (textual protocol decomposition); natural language (unit detection with grammatical classification strictly in a later layer); and mathematical or musical notation (as far as their source representation admits units). Each example must be expressible in the model's vocabulary — types, boundaries, matching behavior, inter-type rules — or the abstraction is wrong.

### What the research established
Two commissioned reports — a DeepSeek survey and a z.ai survey-plus-synthesis across 36+ systems in four families (compiler lexers: LLVM, Clang, Go, Rust, ANTLR; markup: HTML, XML; structured text: URI, MIME, HTTP/email headers, JSON, CSV; NLP/LLM: BPE, WordPiece, SentencePiece, vocabularies, offsets) — served as evidence. Findings **adopted** into the positions above: the Lexer is not necessarily a pre-parser phase; valid architectures differ within a single domain; units can be small and zero-copy; span/offset is a first-class relationship; delivery can be lazy/eager/pull/push; HTML is the strongest test case against a simple `Lexer → Parser` assumption; memory representation is separable from the concept. Findings **examined and rejected**: the universal four-part token core (`kind/id, lexeme/source, span/extent, metadata`) — an observation about implementations, not an ontology, with `metadata` an open bucket incompatible with Memar's modeling discipline; the four-stage NLP pipeline as core architecture — one family's implementation pattern; the compiler-explicit/NLP-ambiguous boundary framing — see [Boundary principles](#boundary-principles); a lexer back-channel (consumer mutation of lexer state) as a general capability — deferred until it is clear whether that is a capability of the concept or an implementation technique of some models. Set aside outright as premature planning: the research reports' adoption roadmaps and reference-language suggestions (a phased 9–13 month plan, Rust as the reference implementation) — implementation planning before the concept settles is exactly what this protocol's discipline defers.

## Results
Insufficient time has passed since these positions were adopted to report real, observed outcomes from implementing against them. This section will be filled in once there is such experience to draw on.

## Discussion

### Drawbacks
- **Under-determination risk.** The abstraction deliberately leaves unit structure, recognition strategy, and delivery open. That is the point, but it means the document alone does not yet enable an implementation; the design session must convert these positions into a checkable protocol, and until then two implementers could build incompatible things both claiming conformance.
- **Naming instability.** Every core name (the output unit, the type, the capsule's parts) is provisional until the terminology section lands; documents written against these names may need repointing.
- **Grounding-principle cost.** Excluding invented units means designs that want `INDENT`-style or `EOF` tokens must build them above the Lexer. Some compiler consumers will find that less convenient than the industry norm, and the protocol should be honest that this is a deliberate cost.
- **Immutability cost.** A consumer holding long-lived capsules across a specification upgrade must manage an identity swap (old capsule ends, new capsule begins) rather than mutate in place.

### Rationale and alternatives
- **Name the module Tokenizer (rejected)**: tokenization is one capability; other lexical operations would make the name wrong in retrospect.
- **Start from the industry token shape — `kind + text + location` (rejected)**: it is one representation, not the concept. Whether it survives as a model-specific unit shape is decided per model, from the consumer contract.
- **Start from one type per keyword (rejected)**: a keyword is a linguistic sign, not necessarily an independent concept; several keywords may share one abstraction, and a keyword may have no semantic type of its own. If the final model happens to yield one type per keyword, that is an outcome, not a starting assumption.
- **One general Lexer that every domain must plug into (rejected as an assumption)** and **one lexer per domain (rejected as an assumption)**: the settled position is stronger and more precise — Memar needs *an abstraction for lexical processing* defined independently of domain, consumer, and strategy; whether a domain then writes a lexical model on it, a dedicated lexer above it, or skips it entirely is decided per consumer with evidence.
- **Adopt the four-stage pipeline (Normalizer → PreTokenizer → Model → PostProcessor) as core (rejected)**: it is a known, useful pattern in one family; importing it would silently convert that family's architecture into the ontology.
- **Allow an open `metadata` field on units (rejected)**: an open bucket is where undecided information goes to die; the model determines unit structure explicitly.
- **Mutable lexical model / mutable rules (rejected)**: a capsule holds one interpretation under one model; mutation would make "the same capsule" mean two interpretations over its lifetime, break compile-once rule economics, and conflate natural source changes with changes in the definition of interpretation. Specification versioning is represented by new model identities.
- **Matching behavior as an enum in the protocol (rejected)**: the protocol must expose the decision, not prescribe its representation.
- **One edge per token in graph modeling (rejected)**: connection explosion with no ownership semantics; the observation/process framing with a set-on-relationship is the working candidate.
- **Keep frequency/weight inside the unit (rejected)**: they are observations about a unit in a context, not intrinsic properties; "weight relative to what, for what decision" must be answered by whichever abstraction owns them.

### Prior art
- **The lexical-analysis literature**: the lexeme/token/pattern/token-type vocabulary (see the [Wikipedia treatment](https://en.wikipedia.org/wiki/Lexical_analysis)) — used as terminology evidence, with the caveat that definitions differ across sources.
- **Compiler implementations**: Go's token (`kind`, text, position) as the common industry shape under critique; Rust's deliberately layered design (a minimal `kind + len` token low-level, spans added at a higher layer) as evidence that representation layering is real; rustc_lexer as evidence for a lexical layer cleanly separated from the compiler; ANTLR for grammar-driven lexical models and channels; Roslyn for trivia modeling.
- **Incremental and hybrid consumers**: Tree-sitter for incremental re-lexing over edits; the HTML5 tokenizer as the standing example of a stateful tokenizer whose state interacts with tree construction (the back-channel evidence).
- **Non-materializing designs**: libyaml's public token API; llhttp and simdjson, which deliberately present lexical-level results without materializing per-unit objects — evidence that the contract and the memory strategy can be decoupled.
- **NLP/LLM tokenization**: BPE, WordPiece, SentencePiece, vocabulary IDs, offsets — evidence that deterministic segmentation needs no whitespace assumptions and that frequency/significance observations are consumer-relevant.
- **Commissioned research**: the z.ai and DeepSeek reports (see [lexer.changelog.md](./lexer.changelog.md)) — the survey layer beneath the rejections recorded in [What the research established](#what-the-research-established).

### Unresolved questions
1. **What makes something a lexical unit?** The minimal contract every consumer can rely on, which data is optional per consumer, and whether the contract splits into a core plus per-consumer profiles (compiler vs analysis vs model consumers).
2. **What information may a lexical model provide about a unit** — and which of it belongs to the lexical result versus later analysis? Where exactly is the boundary between Lexical Unit and Syntax: does the Lexer ever see structure, or only the flat stream plus source relations?
3. **Vocabulary and naming.** Is the output concept closest to *lexeme* or *token*? Does a `Lexeme → Token` layering exist here? What is the type concept's name (`TokenType` vs `LexicalType` vs others)? A terminology section must fix the project's vocabulary before names stabilize.
4. **Is the Lexical Model passive or active?** A set of types and rules, or an abstraction carrying context/state (recognition depending on previously seen source)? This shapes type design, nesting, competition, and incremental updates.
5. **Capsule-replacement reporting.** The model-lifetime question itself is settled — a capsule is permanently bound to the model supplied at initialization, and a different model means a new capsule (see [Lifecycle](#lifecycle-the-lexical-capsule)); mutation of a capsule's model was examined and rejected. The residual question is about the transition only: when a consumer ends one capsule and initializes a new one over the same source under a different model, does anything accompany the switch — for example a diff-style report between the old and new capsule's lexical results — or is the switch silent, with consumers simply reading the new capsule's result?
6. **The matching-behavior abstraction.** What the protocol returns when multiple types match at a position (continuation, exclusive ownership, nested re-lexicalization, and behaviors not yet discovered), and how precedence, coexistence, nesting, and lexical scope are expressed across type-level behavior versus model-level relationships.
7. **Affected-scope determination.** When a source change arrives, who determines the affected region — the Lexer itself, or a higher abstraction that passes a change scope in?
8. **The Source Change abstraction's home.** Its own protocol document, defined jointly with the content domain, since editors, indexers, parsers, caches, and graph stores are equally legitimate consumers.
9. **The Source-unit abstraction.** Does the source side stay character-based (character/code point/byte) or generalize to non-character units (visual symbols/regions)? The answer decides whether graphic notations such as standard musical notation are in scope — to be decided by argument, not assumption.
10. **Weight and frequency.** Do they get sibling abstractions of their own, and where do they live — in the unit, in a per-source profile, or computed by the consumer? The founding position: outside the unit, owned by whatever abstraction answers "weight relative to what, for what decision".
11. **The derived-from relationship.** If any model ever produces non-substring units, do they need an explicit relationship to the source? Currently not admitted at the core.
12. **Synthetic markers.** Do signals such as end-of-input belong anywhere in the protocol, and as what — a signal type, a unit, or nothing?
13. **Consumer feedback on lexer state** (the HTML back-channel case): a general capability of the concept, or an implementation technique of some models? Examine before generalizing.
14. **Graph representation of results.** The `tokens_by`/`tokenize` candidate, the tokenizer node's identity (Module vs dedicated tokenization concept), inverse-relationship questions, and whether an individual unit ever becomes a node.
15. **Client-side trust.** The security posture for lexing untrusted input in a client before submission.

### Future possibilities
- **The dedicated design session** that turns this document into the protocol proper: the minimal contract, the capsule's method surface, the type abstraction, the change-report format, and the vocabulary section.
- **A Source Change protocol document**, general enough for consumers beyond the Lexer.
- **An open-source landscape study** — after the model is more settled — comparing candidate projects (rustc_lexer, Tree-sitter, Roslyn, ANTLR, html5ever/Blink, libyaml, llhttp, simdjson, plus less famous candidates) by a fixed criterion: compatibility with the ontology *this* document discovers, not fame or feature count. Per candidate, the founding research's five evaluation questions apply: what it detects from the source, what it delivers to consumers, what it stores in its representation, what it computes, and what it deliberately delegates to later stages. The founding sessions deliberately deferred this study until the model can serve as the yardstick; a possible outcome — a candidate whose representation matches the industry shapes exactly — would still need its justification to be independent of "they did it this way".
- **Sibling abstractions** for frequency/significance observations over a source, if the concept work justifies them.
- **A Syntax-layer document** if the candidate layering `Source → Lexical Unit → Syntax → Semantic Abstraction` survives examination — with the boundary between the first two layers as its central question.
