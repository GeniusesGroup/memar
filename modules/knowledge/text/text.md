# Text
The word text has its origins in [Quintilian](https://en.wikipedia.org/wiki/Quintilian)'s [Institutio Oratoria](https://en.wikipedia.org/wiki/Institutio_Oratoria), with the statement that "after you have chosen your words, they must be weaved together into a fine and delicate fabric", with the Latin for fabric being [textum](https://en.wiktionary.org/wiki/textus#Participle).

Within the field of [literary criticism](https://en.wikipedia.org/wiki/Literary_criticism), "text" also refers to the original information content of a particular piece of writing; that is, the "text" of a work is that primal symbolic arrangement of letters as originally composed, apart from later alterations, deterioration, commentary, translations, paratext, etc.

## Text (literary theory)

In [literary theory, a text](https://en.wikipedia.org/wiki/Text_(literary_theory)) is any object that can be read, literally or figuratively, whether this object is a work of literature, a street sign, an arrangement of buildings on a city block, or styles of clothing. It is a set of signs that is available to be reconstructed by a reader (or observer) if sufficient interpretants are available.[citation needed] This set of signs is considered in terms of the informative message's content, rather than in terms of its physical form or the medium in which it is represented.

## Text Search

As [describe in the wikipedia](https://en.wikipedia.org/wiki/Full-text_search) in text retrieval, full-text search refers to techniques for searching a single computer-stored document or a collection in a full-text database. Full-text search is distinguished from searches based on metadata or on parts of the original texts represented in databases (such as titles, abstracts, selected sections, or bibliographical references).

### Index vs [Concordance](https://en.wikipedia.org/wiki/Concordance_(publishing))

## accuracy(accurate) vs. precision vs. recall

The best quality scientific observations are both accurate and precise.

## Topics

- query caching? how?
- features supported by commercial search engines like boolean operators, negation, stemming, relevance feedback and clustering
- support user context like the user’s location
- result summarization
- proximity information
- use of link structure. Simple experiments indicate PageRank can be personalized by increasing the weight of a user’s home page or bookmarks.
- Use of link text, we are experimenting with using text surrounding links in addition to the link text itself.

## Articles

- https://static.googleusercontent.com/media/research.google.com/en//pubs/archive/334.pdf
- https://www.elastic.co/search-labs/blog/articles/lexical-and-semantic-search-with-elasticsearch
- https://en.wikipedia.org/wiki/Bag-of-words_model
- https://en.wikipedia.org/wiki/Okapi_BM25
- https://en.wikipedia.org/wiki/Linguistics
- https://en.wikipedia.org/wiki/Lexicology
- https://en.wikipedia.org/wiki/Word
- https://en.wikipedia.org/wiki/Lexeme
- https://en.wikipedia.org/wiki/Lexicon
- https://en.wikipedia.org/wiki/Lexical_semantics

## Idea backlog from edge code comments

Raw proposals from comment notes inside edge .go files (comments remain in code as source). Review discipline per modules/management/vocabulary-discipline.handoff.md. Nothing below is ratified.

### Token index - edges/tokens/protocol/dt-token.go
- **Idea**: token detail for indexing (Google calls it a "Hit List"): TextUUID, token offset in sentence/text, first-character offsets, Weight (tokens in larger/bolder font weighted higher), ScoreInSentence/ScoreInText/RankingScore, commented-out BackLinksNumbers (citations). TODO: removing stop words?
- **Review questions**: is stop-word removal an analyzer concern (dt-analyzer) rather than storage? Do weights/scores belong to analytics (pluggable)?

### Text types - edges-loop/types.go

The full original file is restored verbatim at `edges-loop/types.go` (Localization proposal, PERSON/GPE entity notes, and the complete POS tag list). Do not summarize it - review it in place.

- **Review questions**: is Localization a text type or a query-time behavior? Does the POS tag list become a uri/label vocabulary?
### Query - edges-loop/query/protocol/data_model.go, dt-precision.go
- **Idea**: query model storing the user, raw text (comment: keyword order is just one factor; location, history, and page quality also matter), with open TODOs: is a query a text edge or a comment edge? Is ModuleID a filter? Is pagination a filter? Precision tuning as uint8 following the Elastic App Search precision values.
- **Review questions**: query-as-edge vs query-as-service-request; filter semantics.