# Lexer Handoff

## Topic & Purpose
Open questions and anticipated work for the Lexer protocol concept document (`lexer.md`), relocated there when the documentation method retired the base document's `## Discussion` wrapper (the second migration wave).

## Status
Active

Open work for `lexer.md`. Entries are mutable current state — revised as each item moves, removed when it resolves or is dropped. See [documentation-handoff.md](../documentation-handoff.md) for what a handoff is.

## Open Questions

### What makes something a lexical unit?
- State: moved 2026-09-11 from the retired Unresolved questions (item 1). The minimal contract every consumer can rely on, which data is optional per consumer, and whether the contract splits into a core plus per-consumer profiles (compiler vs analysis vs model consumers). The body names this the design session's central task (see [What a Lexer is](./lexer.md#what-a-lexer-is)). Structure candidates now on the table also include the tagged-union payload pattern (a unit as kind-plus-payload variants) alongside the industry `{kind, text, position}` shape.
- Next: settle in the dedicated design session (see Anticipated Work).

### What information may a lexical model provide about a unit?
- State: moved 2026-09-11 from the retired Unresolved questions (item 2). Which model-provided information belongs to the lexical result versus later analysis, and where exactly the boundary between Lexical Unit and Syntax sits: does the Lexer ever see structure, or only the flat stream plus source relations?
- Next: settle alongside the Syntax-layer question (see Anticipated Work).

### What names does the protocol's terminology fix?
- State: moved 2026-09-11 from the retired Unresolved questions (item 3). Is the output concept closest to *lexeme* or *token*? Does a `Lexeme → Token` layering exist here? What is the type concept's name (`TokenType` vs `LexicalType` vs others)? A terminology section must fix the project's vocabulary before names stabilize.
- Next: draft the terminology section in the design session; it is the prerequisite for settling any name.

### How does the Lexical Model express context?
- State: moved 2026-09-11 from the retired Unresolved questions (item 4). The passive-versus-active direction is settled — context-carrying recognition is the rule, not the exception (see [The Lexical Model](./lexer.md#the-lexical-model)). The remaining question is the protocol shape: modes (stacked, bitmask), tracked model state, whole-source context requirements (CommonMark-style), and what each means for type design, competition, and incremental updates.
- Next: settle the shape in the design session.

### What accompanies a capsule replacement?
- State: moved 2026-09-11 from the retired Unresolved questions (item 5). The model-lifetime question is settled — a capsule is permanently bound to the model supplied at initialization, and a different model means a new capsule (see [Lifecycle](./lexer.md#lifecycle-the-lexical-capsule)); mutation of a capsule's model was examined and rejected. The residual question is about the transition only: when a consumer ends one capsule and initializes a new one over the same source under a different model, does anything accompany the switch — for example a diff-style report between the old and new capsule's lexical results — or is the switch silent, with consumers simply reading the new capsule's result?
- Next: settle in the design session's capsule work.

### What is the matching-behavior abstraction?
- State: moved 2026-09-11 from the retired Unresolved questions (item 6). What the protocol returns when multiple types match at a position (continuation, exclusive ownership, nested re-lexicalization, and behaviors not yet discovered), and how precedence, coexistence, nesting, and lexical scope are expressed across type-level behavior versus model-level relationships.
- Next: settle in the design session.

### Who determines the affected scope of a source change?
- State: moved 2026-09-11 from the retired Unresolved questions (item 7). When a source change arrives, who determines the affected region — the Lexer itself, or a higher abstraction that passes a change scope in?
- Next: settle with the change contract, together with the Source Change question below.

### Where does the Source Change abstraction live?
- State: moved 2026-09-11 from the retired Unresolved questions (item 8). Its own protocol document, defined jointly with the content domain, since editors, indexers, parsers, caches, and graph stores are equally legitimate consumers.
- Next: see A Source Change protocol document under Anticipated Work.

### Does the Source side stay character-based?
- State: moved 2026-09-11 from the retired Unresolved questions (item 9). Does the source side stay character-based (character/code point/byte) or generalize to non-character units (visual symbols/regions)? The answer decides whether graphic notations such as standard musical notation are in scope — to be decided by argument, not assumption.
- Next: settle in the design session; standard musical notation is the standing test case (see [Domain scope](./lexer.md#domain-scope)).

### Where do weight and frequency observations live?
- State: moved 2026-09-11 from the retired Unresolved questions (item 10). The direction is settled: outside the unit, in sibling concepts — and the research supplies the concrete candidate shapes: per-type registries holding corpus-level statistics (frequency, document frequency, IDF, Zipf rank — spaCy's Lexeme, Clang's `IdentifierInfo`, Rust's interning) and per-context analyses holding runtime-computed properties (embeddings, attention, logits — properties of a (model, input) pair, never of the unit; see also the five unrelated meanings of "weight" in LLMs). Open: which of these belong to *this* module versus text/NLP sibling modules, and where TF-style (unit, document) observations live.
- Next: see Sibling abstractions for frequency/significance observations under Anticipated Work.

### Do non-substring units need a derived-from relationship?
- State: moved 2026-09-11 from the retired Unresolved questions (item 11). If any model ever produces non-substring units, do they need an explicit relationship to the source? Currently not admitted at the core. The standing test case for non-substring output is Unicode grapheme clusters (combining marks, ZWJ sequences): one cluster grounds in multiple source extents at once.
- Next: revisit if a real model requires non-substring output.

### Does the end-of-input signal ride the delivery channel?
- State: moved 2026-09-11 from the retired Unresolved questions (item 12). Settled in principle: end-of-input is a signal, not a unit — the grounding principle excludes it, and the survey shows both resolutions in production (EOF-as-token in most compilers, EOF-as-side-channel in Tree-sitter and Rust proc-macros), so a protocol keeping it a signal is viable. Open: whether the signal rides the same delivery channel as units or a separate one. The waived Appendix-D async-streaming question lands here too: the delivery contract must also state the async/streaming interface shape — the intake-side half of the same case (chunked arrival) is already registered in [Lifecycle](./lexer.md#lifecycle-the-lexical-capsule).
- Next: settle with the delivery contract.

### What is the shape and ownership of the consumer feedback channel?
- State: moved 2026-09-11 from the retired Unresolved questions (item 13). The evidence for *some* consumer-to-lexer feedback is strong — the HTML5 tree builder switches tokenizer states, JSX parsers switch lexer modes, Clang's parser fills annotation tokens in the stream, Tree-sitter's parser drives the lexer per step — so the design question is the shape and ownership of that channel, not its existence: a general capability of the concept, or per-model technique; and if a capability, whether it rides the delivery channel or its own contract.
- Next: settle in the design session.

### How are lexical results modeled in the graph?
- State: moved 2026-09-11 from the retired Unresolved questions (item 14). The `tokens_by`/`tokenize` candidate, the tokenizer node's identity (Module vs dedicated tokenization concept), inverse-relationship questions, and whether an individual unit ever becomes a node. The per-type registry evidence (spaCy, Clang, Rust — see [Lexical Unit and naming](./lexer.md#lexical-unit-and-naming)) independently supports the shared-dictionary instinct.
- Next: settle with the general modeling discipline (see [Modeling](../modeling.md), in particular the attribute-or-edge test).

### What is the trust posture for client-side lexing of untrusted input?
- State: moved 2026-09-11 from the retired Unresolved questions (item 15). The security posture for lexing untrusted input in a client before submission — including input-expansion attacks (XML entity expansion, decompression bombs) that a lexing layer over untrusted bytes must not amplify.
- Next: deferred to the security discussion of the design session.

### Where does the trivia policy live?
- State: moved 2026-09-11 from the retired Unresolved questions (item 16). Which of the surveyed policies (filter, flag-on-next-unit, separate channel, first-class trivia, trivia-as-units, grammar-controlled) the protocol must permit, and whether the policy is a model-level choice or a per-consumption view — see [Trivia](./lexer.md#trivia). Two further cases sharpen it: folding whitespace — RFC 5322's folding is unfolded by the specification itself before interpretation, so at least one grammar-controlled handling is mandatory rather than optional — and adjacency flags (Rust's `Spacing::Joint`/`Alone`), another member of the flag family where whitespace is observed without becoming a unit.
- Next: settle in the design session.

### What shape does a lexical error take?
- State: moved 2026-09-11 from the retired Unresolved questions (item 17). Are recognition failures units (model-defined error kinds grounded in extents), separate diagnostics with their own spans, or both — and is the recovery posture (recover-and-continue versus strict-abort) a model decision or a capsule decision? Whatever the answer, alignment with Memar's [Error](./error.md) protocol must be checked.
- Next: settle in the design session, with the Error-protocol conformance check.

### Must the lexical result round-trip to the source?
- State: moved 2026-09-11 from the retired Unresolved questions (item 18). Must the lexical result be sufficient to reconstruct the source? Two independent convergences say some consumers need it (Roslyn's first-class trivia for formatters; SentencePiece's `decode(encode(text)) == text`), while compiler lexing is routinely lossy. Which consumers require it, and does it become a model property or a trivia-policy consequence?
- Next: settle in the design session.

### What do non-deterministic models do to the change contract?
- State: moved 2026-09-11 from the retired Unresolved questions (item 19). Sampling segmenters (Unigram sampling, BPE-Dropout) produce multiple valid decompositions of one source — what does that do to the change contract, to result identity, and to the phrase "the lexical result" itself?
- Next: settle with the change contract and result-identity assumptions.

### Where does input preprocessing live?
- State: moved 2026-09-11 from the retired Unresolved questions (item 20). Where do byte→character decoding, newline normalization, and malformed-sequence replacement live — in the Source abstraction, an explicit preprocessing step, or capsule initialization — and against which stream (raw or preprocessed) are positions defined? The lossless/lossy distinction that keeps this outside [Working positions](./lexer.md#working-positions) is recorded in [What the research established](./lexer.md#what-the-research-established). Two boundary cases from the waived findings: HTML character-reference decoding (`&amp;` → `&`) — the HTML5 tokenizer performs it inside recognition, testing whether text-transforms belong to preprocessing or to model rules; and the UTF-8/default-encoding question, which is this question's byte-decoding first item — the waived Unicode-support note is covered here rather than separately.
- Next: settle in the design session.

## Anticipated Work

### The dedicated design session
- State: from the retired Future possibilities. Turns this document into the protocol proper: the minimal contract, the capsule's method surface, the type abstraction, the change-report format, and the vocabulary section.
- Next: the Open Questions above are its agenda.

### A Source Change protocol document
- State: from the retired Future possibilities. General enough for consumers beyond the Lexer.
- Next: defined jointly with the content domain; see the Source Change open question above.

### An open-source landscape study
- State: from the retired Future possibilities. After the model is more settled — comparing candidate projects (rustc_lexer, Tree-sitter, Roslyn, ANTLR, html5ever/Blink, libyaml, llhttp, simdjson, plus less famous candidates) by a fixed criterion: compatibility with the ontology *this* document discovers, not fame or feature count. Per candidate, the founding research's five evaluation questions apply: what it detects from the source, what it delivers to consumers, what it stores in its representation, what it computes, and what it deliberately delegates to later stages. The founding sessions deliberately deferred this study until the model can serve as the yardstick; a possible outcome — a candidate whose representation matches the industry shapes exactly — would still need its justification to be independent of "they did it this way".
- Next: run after the design session settles the ontology that serves as the yardstick.

### Sibling abstractions for frequency/significance observations
- State: from the retired Future possibilities. For frequency/significance observations over a source, if the concept work justifies them.
- Next: see the weight-and-frequency open question above.

### A Syntax-layer document
- State: from the retired Future possibilities. If the candidate layering `Source → Lexical Unit → Syntax → Semantic Abstraction` survives examination — with the boundary between the first two layers as its central question.
- Next: see the Lexical-Unit/Syntax open question above.
