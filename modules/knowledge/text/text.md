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

## Durable storage
A text’s durable value is the character sequence of the `Text` — the bytes of that sequence as the text domain stores them as a memory part. How a Files body codec embeds those part bytes inside one node body is private to the bound codec and is not Text’s concern. **Escaped JSON** that wraps a long body (the JSON codec’s `$files.text` object) is **not** Text’s durable form. Memar projects follow [Text Rule — Long Body Not JSON-Escaped](rules/long-body-not-json-escaped/long-body-not-json-escaped.md): bind a Files body codec that does not force that shape; JSON is not mandatory; [Syllab](../../computer/codec/syllab/syllab.md) is the intended bind once its Files body codec exists.

## Text with style
Text carries style. HTML and CSS are more expressive than Markdown and are what
article text should be written in.

## Locale text
A `Text` is a name in the human world — a title, a label, a sentence. It need
not be unique, and it is not unique: two things may hold equal text. What is
unique is the text's identity, not its words.

## Text Search
As [describe in the wikipedia](https://en.wikipedia.org/wiki/Full-text_search) in text retrieval, full-text search refers to techniques for searching a single computer-stored document or a collection in a full-text database. Full-text search is distinguished from searches based on metadata or on parts of the original texts represented in databases (such as titles, abstracts, selected sections, or bibliographical references).

The kept structure that ranks texts by likeness, with the measurements, is in [Text Likeness](likeness/likeness.md).

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

## Lexical tokens and senses
If [Reference is a graph edge](../content/content.md#reference-as-a-relation-not-a-property) from *some node* to a target, a hard question follows immediately: what is that source node's identity, when the source is a word or phrase repeated many times inside a larger body of free text?

**The uniqueness decision:** a given string (e.g., "Architecture") is treated as a single, globally unique **Lexical Token** — analogous to how a single physical product (a bottle of dish soap) remains one product even when sold by many different vendors under many different terms. Multiple parties may attach different relations/annotations to the same lexical token without this threatening its identity.

This alone does not resolve ambiguity, however, because a single lexical string frequently denotes *more than one distinct concept*. Two genuinely different linguistic phenomena were identified, and must be handled differently:

- **Polysemy** (related senses sharing a common root): "Architecture" as building-design and "Architecture" as software-design share a conceptual root (design/structure). In this case, disambiguation happens through **token composition**: "Software Architecture" is itself a distinct, dependent lexical token that links back to the bare token "Architecture," rather than the bare token acquiring multiple independent sense-edges. Two adjacent tokens (e.g., "S" and "A" forming a bigram) both remain individually identifiable, and both also connect to the surrounding text; the compound resolves ambiguity without contradicting the base word's core meaning.
- **Homonymy** (unrelated senses that happen to share spelling/pronunciation by historical accident, not shared meaning — e.g., Persian "شیر": lion, water-tap, milk — three etymologically unrelated words that converged phonetically). Here, no amount of "the phrase must be a non-contradictory refinement of the word's meaning" rule applies, because there is no single core meaning to refine. **This is an explicit exception** to the general disambiguation-by-composition rule and must be documented as such, or the general rule will silently break on real-world homonyms.

**Bare, unmodified tokens may remain unresolved.** A document that contains only the word "Architecture" — a title, a tag, a project name with no surrounding disambiguating phrase — has no compositional context to resolve which sense is meant. The correct behavior is to **let the ambiguity stand explicitly** (the lexical token exists with no resolved sense-edge, or with multiple candidate sense-edges left unranked) rather than forcing a guess. **This is not an error state.** Any engine built on top of this model must not assume every token eventually resolves to exactly one sense.

**Why ambiguity exists in natural language at all** (background, not architecture): partly cognitive economy (metaphorical extension of existing words costs less than inventing new ones for every related concept), and partly pure historical accident (etymologically distinct words converging phonetically over centuries). Artificial disambiguation-first languages (e.g., Lojban) demonstrate that unambiguous vocabularies *can* be built, but natural languages never migrate toward them because ambiguity resolved cheaply by context is more efficient for everyday communication than maintaining large precise vocabularies. Technical documentation is the opposite case — the cost of ambiguity typically exceeds the cost of precise terminology — which is consistent with this project's general preference (seen elsewhere, e.g., [framework.md](../../../docs/framework.md)) for exact, non-overlapping definitions.

## Authoring syntax
The syntax an author types is not the model it compiles to. This section was moved here from [Content → Authoring Syntax vs. Semantic Graph](../content/content.md#authoring-syntax-vs-semantic-graph), which keeps the half about the graph and its renderers.

A cross-cutting concern surfaced repeatedly across the concern topics of [Content](../content/content.md#explanation): **the syntax an author physically types must not be conflated with the Semantic Graph the model actually operates on.** A recurring architectural shape emerged, but it must be described carefully as two distinct relationships, not one:

```
Authoring Model  (concise, readable, blends free prose with structured data)
        │  compiles to
        ▼
Semantic Graph   (the single, canonical, format-independent model)
```

**A cautionary case examined against the Authoring side of this shape:** Pug/Jade and JSX were investigated as candidate precedents for a compact authoring syntax and found instructive for the opposite reason expected — both correctly identified real problems with HTML (mixing logic and markup harms readability; HTML's tag vocabulary is historically bloated and inconsistent) but "solved" the second problem by *removing all constraints on tag creation*, letting any developer invent any tag freely. This is the exact opposite of this project's direction (reducing an unconstrained vocabulary to a small set of discovered primitives, not replacing one unconstrained vocabulary with an even less constrained one). The conclusion drawn: a workable Authoring Syntax must be compact and readable, but **constrained to the primitives actually discovered through [Content's](../content/content.md#methodology) process** — not an open invitation to invent arbitrary new tags.

**Type-system verbosity is not, by itself, a reason to abandon strong typing for content templates.** Concern was raised that a verbose, strongly-typed language like Khayyam might make content templates unreadable if used directly and unaided. The resolution reached: this is a solved problem in general-purpose programming (JSX, Vue's Single-File-Component syntax, Terraform's HCL — none of these were adopted because their underlying execution model was incomplete; each exists because writing the underlying API directly, by hand, for every UI/config unit, would be unreadable at scale). The correct response is therefore a dedicated, compact Authoring Syntax that *compiles to* Khayyam graph/capsule calls — not raw Khayyam typed by hand for every template, and not abandonment of Khayyam's typing discipline in favor of an untyped markup language.

Two decade-old legacy examples examined during discovery (`${hamburgerMenuWidget.ConnectedCallback()}` embedded directly in an HTML template; an invoice table row template binding fields such as `${pr.Quiddity.Title}` and `${pr.PayablePrice}` directly into table cells) were read, in retrospect, not as isolated hacks but as symptoms of the author already reaching, a decade prior and without the vocabulary to name it, toward exactly this Composition-as-typed-graph model — treating a Widget as a composable function call rather than a Custom Element, and treating a table row as a typed Composition of `Product Title / Original Price / Payable Price / Quantity / Actions` rather than as an HTML `<table>` structure.

## Structural notation within an authoring syntax
Moved here from [Content → Structural Notation Within an Authoring Syntax Itself](../content/content.md#structural-notation-within-an-authoring-syntax-itself), per the owner's ruling of 2026-10-24 recorded in the handoff. The diagram passages that follow it there are not moved: they split to other documents.

A question is recorded here precisely because it is unresolved and directly tests the principles established in [Content](../content/content.md#foundational-principles) against a concrete, everyday case: **is the structural notation of an authoring format itself a form of embedded semantic tagging?**

The concrete trigger: this project's own documentation is authored in Markdown, and Markdown documents in this project also carry a YAML front-matter block for metadata (Title, Status, Start Date, ID — as at the top of [content.md](../content/content.md)). This means **two separate mechanisms currently coexist for attaching non-prose information to a document**: inline notation within the text stream itself (`#` for headings, `-` for list items, `**bold**` for emphasis) and a separate front-matter block at the top of the file. This is precisely the "two competing places for the same kind of information" problem the Content document has otherwise argued against (the RDFa-vs-JSON-LD case in [Type Reference](../content/content.md#type-reference--where-semantic-meets-a-type-system)) — except here it appears inside the very format used to write documents like this one, not in a hypothetical external example.

The deeper question this raises: does a Markdown heading marker (`#`) merely delimit where one Text unit ends and another begins (a purely structural fact about the stream, arguably necessary at some level for any serialization to exist at all) — or does it simultaneously **assert semantic information** (this line has `Importance = 1`, this line has the `Role: Heading`) **inline**, in exactly the way [Reference as a Relation, Not a Property](../content/content.md#reference-as-a-relation-not-a-property) argued a Reference must *not* be embedded as an attribute, and [Type Reference](../content/content.md#type-reference--where-semantic-meets-a-type-system) argued Type information must *not* be scattered across a template? If `#` is doing the latter, then by the Content document's own logic, that Importance/Role assertion should be an external edge from an addressable Text fragment to a Role/Type — not a character embedded in the text stream itself — and Markdown's heading syntax is a smaller-scale instance of the exact problem this document exists to correct, not an innocent structural convenience.

**This question was not resolved when it was recorded.** Two candidate positions were identified, neither adopted:

- **Position A — Pure delimiter, not semantic.** `#` merely marks a boundary in the raw text stream (equivalent to a paragraph break), and any *interpretation* of what that boundary means (a heading, its importance level) is a separate act performed by a parser producing a `refers-to-type` edge afterward — the character itself carries no semantic weight, only structural segmentation, analogous to how a comma delimits list items in CSV without asserting anything about their meaning.
- **Position B — Implicit semantic tagging.** `#` is functionally indistinguishable from writing `role="heading" importance="1"` inline — it *does* assert a Role, merely with a terser syntax than an explicit attribute, and therefore violates the same principle established for Reference and for Type: information about a Text fragment's role should be an edge external to the fragment, not a character prefixing it in the stream.

The owner's ruling of 2026-10-24 (handoff) that markup is annotation on spans of one plain value takes Position B's model for Text; Position A stays true of an encoding's own delimiters. The owner confirmed on 2026-10-30 that the ruling settles Position B for Text.

If Position B is correct, the implication extends beyond headings to every structural marker in every authoring format examined so far — Markdown's `-`/`*` (list-item role), numbered-list digits (ordinal-position role), `**bold**`/`*italic*` (emphasis role) — each would need to be re-examined as implicit semantic tagging requiring an external edge, not inline notation. This would materially affect the still-unresolved Authoring Syntax question in [Authoring Syntax vs. Semantic Graph](../content/content.md#authoring-syntax-vs-semantic-graph): a fully consistent Authoring Syntax under Position B could carry **no** inline structural notation at all, only boundaries between minimal, addressable Text units, with every interpretive fact (heading, list-item, emphasis, and beyond) expressed as an edge from those units — a considerably more radical Authoring Model than anything proposed so far.

## Checking text
A check answers whether a node's text is fit to be kept and read. [Content](../content/content.md#checking-a-node) is the dispatcher: the check of a node asks each domain the node belongs to, and content fixes none of those domains' rules.
- **What this domain judges.** Bytes and encoding: a byte-order mark, invalid UTF-8, the replacement character, the fingerprints of mojibake, mixed line endings and a missing final newline. The other domains a node belongs to judge their own: an authoring syntax the conventions of the syntax a text is written in (for Markdown the blank lines under a heading and the anchors it names), and the documentation domain what a document owes the others (its links and anchors, its normative references, its propagations and its owed marks).
- **When a check runs.** When a text node is written, the one function of the text domain through which a text node is written (a writer above the named-text view `Text_Place`, whose `WriteText` runs no check) runs the checks that decide from the text's bytes alone, those of this domain, as part of the batch that stores it, and invalid text is refused with nothing stored; a content that is not text points to a `blob` node, whose bytes no text check judges; the migration of the old task folders is the one named exception, a legacy mode of the same function that stores a failing text byte for byte with the label `legacy-unchecked`, declared by this module, which the text check reports as a warning and not a problem; the memory contract stays blind to encodings, since it holds bytes under addresses ([Memory → The contract](../../computer/memory/memory.md#retention-is-reached-through-one-contract)). The checks that need other nodes, as a link does, or that a draft may break midway, as a convention may, run as a query: `check --id` for one node, and over a selection of nodes for a set.
- **A node belongs to a domain by a label,** and a text node names the authoring syntax it is written in by a label, the syntax's id; a text with none is judged by this domain alone.

## Structure of a text
A text is read as a structure apart from how any language writes it: sections of a level, items with an optional name and links placed in their value, each node saying which part of the encoded form it was decoded from, with mutators that change a node while the encoding keeps the bytes of the rest. The Khayyam abstractions are the root `Text_Section` (level 0) with its `Text_Item` entries, `Text_Link`, `Text_Span`, their editable forms, `Text_Nodes` that makes nodes, the codec `Text_Structure_Codec` and the named-text view `Text_Place` in [`protocol/`](protocol/) (Draft). Only a codec says that a section of level 2 is written `##`; a domain that reads a text as a structure, such as the changelog, names no markup symbol. How this structure relates to the ruling that markup is annotation on the spans of one plain value, and to the caution that Text may have no view of the structure of a document, is open: see the handoff.

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
- **Review questions**: GUI/services-layer concern, not a core edge — who enforces visibility for user-level vs global indexes (per-content ACL re-checked per query)? Does the answer live in this module's services or in a pluggable search-analytic capability (no module at that path yet)? Strong authorization expressed as rules (core never knows rule) or service-layer checks?
