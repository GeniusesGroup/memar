---
Title: "Lexer"
Status: Draft
Start Date: 2026-08-12
ID: 496248
---

# Lexer
This document records the concept work behind Memar's Lexer protocol — the working positions, boundaries, and open questions reached in the sessions that defined it. It is a Draft: a dedicated design session will turn these positions into the protocol's actual specification. See [Protocol](../protocol.md) for the general concept of a protocol.

## Abstract
The Lexer protocol defines a general abstraction for lexical processing: identifying lexical units in a source according to a lexical model, and delivering them to consumers under a stated contract. The abstraction is defined independently of any domain, any consumer, and any tokenization strategy — a compiler's parser, a search indexer, a syntax highlighter, a language-model tokenizer, and a URI or MIME-header parser are equally legitimate consumers, and a consumer that parses characters directly without a lexer remains a valid architectural alternative. The concept boundary reached so far: the Lexer's responsibility is lexical decomposition and nothing else (no normalization, weighting, ranking, counting, or grammatical/semantic interpretation); it must make no assumption about what constitutes a token boundary; every lexical unit it reports must be grounded in an observable extent of the source; the lexical model that drives it is immutable and identity-bearing; and the processing capsule is a protocol-level lifecycle object that reports how its output changed so consumers never re-derive changes from raw input. What remains open — the structure and naming of lexical units, the delivery shape, the model's possible active behavior, and the final type inventory — is registered under [Unresolved questions](./lexer.handoff.md#open-questions).

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
3. Being a phase before a parser is **not part of the Lexer's definition**. `Source → Lexer → Parser` is one architecture, not the architecture; `Source → Lexer → {Parser, Search, Highlighting, Indexer, Analyzer}` and `Source → Lexer → Lexical Analysis` (no parser at all) are equally valid, and a consumer may legitimately skip the Lexer entirely (scannerless parsing). A fourth architecture exists too: the consumer may invoke the Lexer on demand — parser-driven lexing, as in Tree-sitter, where the parser asks for the next unit at each step and can tell it what is recognizable in the current context — instead of the Lexer producing a stream.
4. **The Lexer must make no assumption about what constitutes a token boundary.** Boundaries are determined by the lexical model, not by the Lexer concept. The common compiler-vs-NLP framing ("compilers have explicit boundaries; natural language is ambiguous") is rejected as an architectural property: even a compiler may need context-dependent boundaries, and a deterministic algorithm like BPE produces fixed segmentation once its vocabulary is fixed.
5. **Every lexical unit must be grounded in an observable extent of the source.** The Lexer observes and segments; it does not invent meaning. Reporting an observed `TAB` is lexical processing; translating it into `INDENT` assigns new meaning to the observation and belongs to a later layer. Synthetic markers such as `EOF` are end-of-input signals, not necessarily lexical units.
6. The tokenization method — whitespace splitting, regular expressions, state machines, merge rules, probabilities, or opaque scanner code such as Tree-sitter's external scanners — belongs to the **lexical model**, not to the Lexer concept. A declarative abstraction must not hard-code any one recognition technique.
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

Whether a given domain *uses* a Lexer is the consumer's architectural choice, and the founding research gave it a decision rule rather than a verdict: a separate lexical layer earns its keep when the grammar is large, when multiple consumers share the lexical surface, when streaming matters, when the specification mandates it, or when positions are needed downstream; otherwise a single-pass parser is the dominant architecture. HTML is the standing test case — its specification itself mandates the split — while URI, CSV, and TOML show the fused alternative is fully legitimate. The protocol's obligation is only that the abstraction be good enough that a domain *could* define its lexical model on it.

### Boundary principles
Two principles bound what the Lexer may report.

**No boundary assumptions.** The Lexer must not assume units are separated by whitespace or punctuation, that recognition is deterministic, or that any particular algorithm defines boundaries. Boundary determination is the lexical model's property. The compiler/NLP "explicit vs ambiguous" split fails as an architectural property from both directions: compilers can need contextual boundaries (state, lookahead, mode switching), and subword algorithms like BPE are fully deterministic once their vocabulary and merge rules are fixed — SentencePiece even operates on raw bytes without whitespace pre-tokenization.

**Grounding in observable extents.** Every lexical unit must be grounded in an observable extent of the source. The founding example: for source `\tfoo()`, reporting `TAB` followed by `IDENTIFIER(foo)` is reporting observations; reporting `INDENT` is assigning an interpretation the source does not contain — that belongs to a later layer (the parser may label the `TAB` based on surrounding units). The same reasoning excludes synthetic tokens such as `EOF` from the core: end-of-input is a signal about the stream, not a unit observed in the source. One edge is deliberately left open: if a lexical model explicitly defines "this source sequence is one unit with label X", it must still be determined with real examples whether such labels remain *classification* or become *semantic interpretation* — the grounding principle is accepted, and the classification/interpretation boundary is not yet drawn.

A unit grounded in an extent need not be a *substring*: a vocabulary model splitting `playing` into `play` + `ing` still grounds both units in source extents. Whether non-substring outputs (if any model ever requires them) need an explicit derived-from relationship is an open question; the founding position is that the protocol does not admit them at the core.

One boundary case deserves its own registration because the founding research surfaced it: the **C lexer-hack problem** (`A * B;` — declaration or multiplication). The established industry lesson matches this document's grounding principle exactly: the Lexer reports the maximum observable information without performing interpretation — the identifier is reported as an identifier, and type resolution belongs to the parser. Clang's annotation tokens (placeholder units later filled by the semantic layer) show the complementary pattern: a unit may later *acquire* richer interpretation, but the interpretation is injected by a later layer, not invented at lexing time. Both confirm: recognition without interpretation.

### The Lexical Model
The Lexical Model is the concept that determines *what* is recognizable in a source and *how*. It is not mere configuration: it gives the Lexer the set of lexical types plus the rules governing their interactions — precedence, coexistence, nesting, conflict resolution — and it determines the structure of the units it produces. Whether the model is a passive set of types and rules or a more active abstraction that carries context and state (recognition depending on what has already been seen) was left deliberately open — and the commissioned research has since settled its direction: context-carrying models are the rule, not the exception. Python's INDENT/DEDENT track an indentation stack, YAML's indentation is grammatical, HTML5's tokenizer is driven between 84 states by the tree builder, JSX switches lexer modes parser-side, CommonMark's link references require whole-document context (so a Markdown model cannot even stream), and C's lexer-hack was the historical warning. The remaining design question is therefore not *whether* models may carry context but *how* the protocol expresses it — modes, tracked state, whole-source requirements — and what each means for type design, competition, and incremental updates.

Two properties are settled:

- **Identity.** The model is an identity-bearing concept, not a temporary object: two models differing in a single rule are different models, and that difference is meaningful to the system. This matters for caching, for sharing one model across several processing capsules, for versioning, and for graph modeling — and it must be fixed in the model before an implementation is forced to invent it.
- **Immutability.** The model — and each lexical rule within it — is immutable. A rule change produces a new model identity; a model change produces a new processing capsule. This is not merely a performance stance (though it is what makes compile-once rule processing economical): a capsule exists to hold *one specific interpretation* of its source under *one specific model*; with a different model it is a different capsule, not a new version of the old one. Specification evolution is represented by versioned identities, not mutation — `HTML Lexical Model v1` and `v2` are two models, and a healthy system can route old documents to v1 and new documents to v2. A legitimate spec release is therefore not modeled as "the rules changed mid-work"; conversely, if a system genuinely needs its rules to change mid-stream, that is a design alarm to investigate.

Because rules are immutable, they can be compiled once — into an automaton, a table, or any other representation — and reused for the capsule's whole lifetime without re-parsing or re-interpreting rule text. The abstraction must preserve this possibility without tying itself to any one representation (regex is a candidate input format, not the abstraction) — and if regex is chosen as the rule format, the implementation-stage condition is explicit: rules are compiled once at preparation, never interpreted per match — and regex-form rules must additionally be chosen or constrained so that no model rule can trigger catastrophic backtracking ([ReDoS](https://en.wikipedia.org/wiki/ReDoS)): a model whose matching can grow exponentially on adversarial input is unfit for the client-side untrusted-input case this protocol registers under [Domain and consumers](#domain-and-consumers).

One further model property is registered now: some models are legitimately **non-deterministic** — sampling segmenters (Unigram sampling, BPE-Dropout) produce multiple valid decompositions of the same source, and training-time regularization depends on that. This does not break any position above (boundaries remain model-determined; determinism was never assumed), but it must shape the change contract and any result-identity assumptions: the protocol cannot silently assume "one source, one canonical result".

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

Naming is unsettled and consciously so. The word **token** is overloaded across the literature and across this project's consumers; the sessions decided that abstraction and capsule names must avoid it (at most appearing as a compound such as "lexical token", and always in prose rather than in names). The [lexical-analysis](https://en.wikipedia.org/wiki/Lexical_analysis) literature distinguishes **lexeme** (the source character sequence matching a lexical rule), **token** (a representation/classification of that lexeme for later stages), **token type/kind** (the classification), and **pattern** (the rule defining the lexeme) — and these definitions differ between sources, so they are used as evidence, not authority. The trap repeats inside the founding research itself: its reports use **Lexeme** for something else again — a per-type *registry entry* (spaCy's `Vocab`/`Lexeme`, Clang's `IdentifierInfo`, Rust's interned `Symbol`) holding the shared string once for all occurrences plus corpus-level statistics (frequency, IDF, rank). That concept is real and valuable, and it independently converges with this protocol's graph-modeling instinct — units registered in a shared dictionary rather than duplicated per occurrence — but it must not silently inherit the literature's word. Whether the output concept is closest to the literature's *lexeme* or *token*, whether the classic `Lexeme → Token` layering exists in this model at all, and what name the per-type registry takes are all derived from the concept work — and a terminology section fixing the project's vocabulary is a prerequisite for settling any name.

Classification is deliberately kept out of the unit's core. A classification can form in two different places: when a unit is registered as an entity in the system (its lexical identity), and when an occurrence is classified *in a context* — the same word `run` is a verb in one sentence and a noun in another, but tokenization is identical in both. Classifications also layer (lexical → syntactic → semantic) and must not collapse into a single `kind` field on the unit.

### Trivia
Whitespace, comments, and formatting-only content expose a genuine design dimension the founding sessions had not named: what the survey counts as **six distinct policies** — filtered out entirely (Go, Clang), flagged onto the following unit (`StartOfLine`, `LeadingSpace`), routed to a separate channel (ANTLR's `HIDDEN`), first-class trivia attached to every unit (Roslyn's leading/trailing trivia, the formatter-enabling gold standard), reported as units like any other (rustc_lexer, HTML5, CSS), or grammar-controlled (Tree-sitter's `extras`). There is no single right answer: formatters and round-tripping consumers need full trivia, analyzers want it gone, markup languages tokenize it visibly, and NLP has no concept of it at all. The protocol question is therefore not *which* policy wins but *where the policy lives* — model-level, capsule-level, or per-consumption — and whether a consumer may request a different trivia view than the one the model produced.

### Errors
What happens when recognition fails is part of the contract, not an afterthought: the survey splits into two philosophies — recover-and-continue (HTML5, Clang, Go, Tree-sitter; world-facing inputs) versus strict-abort (XML, JSON, YAML; machine-to-machine inputs) — with both fully viable and llhttp exposing the choice as a per-flag toggle. The open shape question: is a failed recognition reported as a *unit* (a model-defined error kind, grounded in the extent that could not be recognized — `tok::unknown`-style), as a separate diagnostic with its own span, or both? The grounding principle permits either, since the unrecognized extent is observable. What the protocol must settle: error output is first-class (never a silent skip or an abort-by-exception in the default path), carries positions, and its recovery posture is a stated model or capsule decision — see [Unresolved questions](./lexer.handoff.md#open-questions).

### Delivery and memory
How units reach consumers is a contract question, not only an implementation detail. Three questions are kept strictly separate:

```text
What is a lexical unit?      (concept)
How is one represented?      (representation)
How are many units managed?  (collection/delivery strategy)
```

Candidate delivery forms: a materialized sequence, an incremental stream (`next()`, with consumed representations reusable), views on the source (the unit's text is never copied; it is read from the source through its extent), and the **push/callback sink** (SAX-style; llhttp and html5ever run entire production systems this way). Two shared requirements cut across the forms: limited **lookahead** (`peek`, bounded ahead-of-consumer reads — V8 keeps a four-slot ring buffer for exactly this), which stream-shaped deliveries must support without materializing everything; and the survey's own resolution worth keeping — one focused scanning core, exposed through pull, push, and eager adapters, so that delivery remains a consumer contract rather than a Lexer property. `TokenSequence` and `TokenStream` are promising distinct candidates — sequence as materialized collection, stream as gradual consumption — but their exact semantics must be established from real consumer cases, not from the names. The finer distinctions behind these names are the design session's to separate: the unit, its occurrence(s) in a source, the collection of occurrences, their ordering, traversal over them, and their production are different concerns that industry shapes tend to merge into one type.

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

Two source-side obligations attach to the capsule and were confirmed by the founding research. First, the source is **referenced, not owned**: the capsule holds access to the source, which lives outside it — ownership would prevent several consumers from sharing one source and would force copies. Second, the change contract extends to the *streaming* case: sources that arrive in chunks (network streams, HTTP bodies) must be lexable without the whole source being materialized, which the HTML5 tokenizer's design assumes throughout and HTTP proxies require — the change contract above describes *edits to an existing source*, while chunked arrival is a distinct intake shape the design session must decide whether to express in the same protocol or a sibling one.

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
| Lexical Model | Drives recognition; immutable, identity-bearing; owns inter-type rules; may carry context |
| Lexical Type | Defines a lexical kind and its recognition behavior; name unsettled |
| Lexical Unit / occurrence | An observed unit in a source; structure model-defined; grounded in an extent |
| Per-type registry | Shared string + corpus statistics held once for all occurrences (spaCy's Lexeme, Clang's `IdentifierInfo`, Rust's interning); name unsettled — the word *lexeme* is itself overloaded |
| `Lexical` capsule | The lifecycle object holding source access, model, compiled rules, result, change subscription |
| Lexical Change | The report of how the lexical result changed after a source change |
| Source Change | A separate general abstraction (not owned by this protocol) |
| Trivia policy | How whitespace/comments are handled: filter, flag, channel, first-class, as-units, grammar-controlled |
| Lexical error | The report of failed recognition; unit-grounded and/or separate diagnostic |
| Sequence / Stream / Sink / View | Candidate delivery forms; possibly several concepts, possibly fewer concepts plus delivery mechanisms |

### Examples the abstraction must express
The design session validates the abstraction against deliberately diverse, textually-described examples (not code): a programming language (identifier/literal/operator recognition without any syntax or semantics knowledge); HTML (nested lexical scopes, content re-lexicalized under different rules — SVG/MathML foreign content is the concrete case where a single document switches lexical handling mid-parse — without concluding HTML *must* use this Lexer); URI (lexical decomposition as an independent concern even when the consumer is a parser/validator); MIME headers (textual protocol decomposition); natural language (unit detection with grammatical classification strictly in a later layer); and mathematical or musical notation (as far as their source representation admits units). Each example must be expressible in the model's vocabulary — types, boundaries, matching behavior, inter-type rules — or the abstraction is wrong. The founding research adds three examples worth adopting into the exercise because each stresses a different position: CommonMark (a model that *cannot* stream — the whole-source link-reference case stresses the streaming assumption); a BPE model (stresses grounding with vocabulary units, offsets, and non-whitespace boundaries); and a YAML or Python-indented model (stresses context-carrying recognition and the INDENT-belonging-above boundary at once).

### What the research established
Two commissioned reports — a DeepSeek survey and a z.ai survey-plus-synthesis across 36+ systems in four families (compiler lexers: LLVM, Clang, Go, Rust, ANTLR, Roslyn, Tree-sitter, V8, Python; markup: HTML, XML, CSS, Markdown, JSX; structured text: URI, MIME, HTTP/email headers, JSON, CSV, YAML, TOML, Protobuf, logs; NLP/LLM: BPE, WordPiece, SentencePiece, Unigram, spaCy, ICU, vocabularies, offsets) — served as evidence. Findings **adopted** into the positions above: the Lexer is not necessarily a pre-parser phase and not even necessarily a producer (parser-driven lexing exists); valid architectures differ within a single domain; units can be small and zero-copy; span/offset is a first-class relationship, best stored opaquely with line/column computed on demand; delivery splits into pull, push, and eager forms over one scanning core; HTML is the strongest test case against a simple `Lexer → Parser` assumption; memory representation is separable from the concept, with every high-performance system refusing per-unit allocation; context-carrying recognition is the rule rather than the exception; trivia handling is a genuine configurable dimension with six distinct policies; lexical-error philosophy splits into recover-and-continue versus strict-abort with both viable; input preprocessing (decoding, newline normalization, malformed-sequence replacement) is a distinct *lossless* layer that HTML5 and CSS specification-mandate before recognition; per-type registries separate shared strings and statistics from occurrences (spaCy's Lexeme, Clang's `IdentifierInfo`, Rust's symbol interning); and a separate lexical layer earns its keep only under specific conditions (large grammar, multiple consumers, streaming, spec mandate, downstream positions). Findings **examined and rejected**: the universal four-part token core (`kind/id, lexeme/source, span/extent, metadata`) — an observation about implementations, not an ontology, with `metadata` an open bucket incompatible with Memar's modeling discipline; the four-stage NLP pipeline as core architecture — one family's implementation pattern (the reports argue any model can be expressed in it with identity stages; that is a testable assertion for the examples exercise, not a reason to adopt it as the core); the compiler-explicit/NLP-ambiguous boundary framing — see [Boundary principles](#boundary-principles); a lexer back-channel as a first-class trait — deferred until it is clear whether that is a capability of the concept or an implementation technique of some models. Set aside outright as premature planning: the research reports' adoption roadmaps and reference-language suggestions (a phased 9–13 month plan, Rust as the reference implementation) — implementation planning before the concept settles is exactly what this protocol's discipline defers.
