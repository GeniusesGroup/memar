# Text
The word text has its origins in [Quintilian](https://en.wikipedia.org/wiki/Quintilian)'s [Institutio Oratoria](https://en.wikipedia.org/wiki/Institutio_Oratoria), with the statement that "after you have chosen your words, they must be weaved together into a fine and delicate fabric", with the Latin for fabric being [textum](https://en.wiktionary.org/wiki/textus#Participle).

Within the field of [literary criticism](https://en.wikipedia.org/wiki/Literary_criticism), "text" also refers to the original information content of a particular piece of writing; that is, the "text" of a work is that primal symbolic arrangement of letters as originally composed, apart from later alterations, deterioration, commentary, translations, paratext, etc.

## Text (literary theory)

In [literary theory, a text](https://en.wikipedia.org/wiki/Text_(literary_theory)) is any object that can be read, literally or figuratively, whether this object is a work of literature, a street sign, an arrangement of buildings on a city block, or styles of clothing. It is a set of signs that is available to be reconstructed by a reader (or observer) if sufficient interpretants are available.[citation needed] This set of signs is considered in terms of the informative message's content, rather than in terms of its physical form or the medium in which it is represented.

## Model

- `Text` — the value a human reads. It is the one kind of value human-readable
  text is written as; every other domain holds a relation to it (a `username`,
  an `email`, a title, a comment body) rather than a copy. `Text` is a `String`,
  and it is the text domain's own value rather than a bare `String` because the
  text is text *for a human in a locale*, not a byte sequence.
- `Field_Text` / `GetText` — the surface a holder of text answers to. The body
  comes from the generator (an `Implements` intent), never hand-written.
- `Field_TextID` / `TextID` — a text's identity. A text is a thing, so its
  identity is a `ThingUUID` from the thing domain; the text domain does not
  declare a competing identifier. A text's identity is unique across all
  domains, and therefore unique across all languages: the same text in two
  languages is two texts, which is what makes `(text)-[:text_language]->(language_human)`
  a relation between two things rather than a field.
- `TextModel` — what a thing in the text domain's model must be: the thing
  domain's model, a text identity, and text. The `uri` domain composes
  `TextModel`, which is the shape of the decision above seen from outside: a
  URI is a thing that reads as text.

## Text with style

Text carries style. HTML and CSS are more expressive than Markdown and are what
article text should be written in.

## Locale text

A `Text` is a name in the human world — a title, a label, a sentence. It need
not be unique, and it is not unique: two things may hold equal text. What is
unique is the text's identity, not its words.

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

## Validation

A `Text` is validated before it is stored, on two counts.

- **Size.** A text may declare a minimum and a maximum length. A text shorter
  than the minimum lacks; a text longer than the maximum overflows. The length
  check belongs to memar's `validators` domain
  ([`ValidateTextLength`](https://github.com/GeniusesGroup/memar)), which owns
  both conditions; the text domain states the requirement, not the check.
- **Characters.** A text may forbid characters that must not appear in it. The
  reason is that a text is rendered into a page: the stored value is a
  candidate for markup that a browser will execute. Reference material for the
  attack surface is the
  [OWASP XSS filter evasion cheatsheet](https://owasp.org/www-community/xss-filter-evasion-cheatsheet)
  and the
  [PortSwigger XSS cheat sheet](https://portswigger.net/web-security/cross-site-scripting/cheat-sheet).
  Two properties of that surface are worth keeping, because they are what a
  naive escaping rule gets wrong: a `script` element inserted through
  `innerHTML` or `insertAdjacentHTML` does not execute, and a template literal
  is not a defence — an `img` carrying an `onload` attribute placed inside one
  still runs.

## Widgets

A text is shown through a widget, and the widget's contract is the same shape
the record domain uses: conditions that say how the widget may render the text,
and services the widget offers.

- Conditions: whether the text overflows the widget it is shown in. The value
  is the same kind of value a CSS `overflow` carries, so the widget and the
  stylesheet cannot disagree about it.
- Services: save, edit, copy the text, open the whole text when it does not fit,
  find the mentions in it, create a link from it, and control whether sensitive
  content in it is shown, hidden, or marked.

## Idea backlog

Review discipline per modules/management/vocabulary-discipline.handoff.md. Nothing below is ratified.

- **Idea**: two levels of index service — user level and global level — must have a strong authorization model. The one proposed solution recorded in the source (both services private, callable only by other services, not by users) "seems not work": a user may change her last choice, e.g. make her content private/public many times in her life, so a static private-to-services stance cannot hold. Still unresolved.
- **Review questions**: GUI/services-layer concern, not a core edge — who enforces visibility for user-level vs global indexes (per-content ACL re-checked per query)? Does the answer live in this module's services or in the pluggable [search-analytic](../../../modules-plugable/knowledge/analytics/search-analytic/) capability? Strong authorization expressed as rules (core never knows rule) or service-layer checks?
