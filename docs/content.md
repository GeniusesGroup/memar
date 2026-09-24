---
Title: "Content"
Status: Draft
Start Date: "2026-07-27"
ID: 495880
---

# Content

## Abstract
This document defines **Content** as a conceptual model — independent of any markup language, authoring syntax, or rendering technology. It originated from a decade-old idea to eliminate CSS-first thinking in UI development ("write semantic HTML, let a Design Language render it"), but through sustained discovery evolved into something broader: a model of how meaning, reference, composition, arrangement, and interaction relate to one another when describing any piece of content, for any consumer (human via GUI/VUI/Braille, or non-human: search engines, AI agents, accessibility tools).

The document does not propose a new markup language. It identifies distinct **concerns** — Semantic Reference, Addressability, Composition, Layout, Theme, Event — that existing languages (HTML, Markdown, XML, JSX) conflate into a single syntax, and defines what each concern *means* without dictating how it is implemented. Implementation of most of these concerns belongs to library and module implementations; the Khayyam modules hosted in this repository are one current realization, alongside consumer projects such as `organization`; this document is concerned with the *concept*, not the *mechanism*.

A central discovery running through the document: much of what appeared at first to require new semantic primitives turned out to already be solved — better — by a proper type system with absolute encapsulation (no unwrapped primitives). What remains genuinely outside any type system's reach is **unstructured content**: free text and untyped media, where no predefined field exists to carry meaning. This is where the [Semantic](#semantic-definition-and-scope) and [Addressability](#addressability) topics concentrate their weight.

Several concerns remain genuinely open at the end of this document — most notably the relationship between Layout and Theme, and where the boundary lies between necessary structural notation and embedded semantic tagging within an Authoring Syntax itself. These are documented as open questions, not resolved.

## Introduction

### Motivation
The originating idea was narrow: developers should not think about CSS while writing markup. Standard, semantic HTML should be sufficient; a pluggable Design Language should handle all visual rendering. Today's frameworks invert this — Bootstrap's `btn btn-primary`, Material's `mdc-button`, React's `<Button variant="contained">` all mix semantic intent with presentational styling in the same syntax. The original goal was closer to what SQL promised for databases but never fully achieved due to vendor fragmentation:

```
Application → Semantic HTML → Design Language (pluggable renderer)
```

Early exploration treated this as an HTML-extension problem: catalog HTML5 elements and ARIA attributes, find the gaps, propose new attributes like `importance="primary"`. This approach was abandoned as a starting point (though HTML/ARIA remain valuable *observational corpus*) for a specific reason: cataloguing existing tags anchors thinking to HTML's historical accretion rather than to the underlying concepts HTML happens to express imperfectly. A recurring pattern emerged instead — `disabled` is not intrinsic to `<button>`, `href`/`src` are not fundamentally different, `role` is not intrinsic to any one element, hyperlink is not intrinsic to `<a>`. Each investigated "primitive" turned out to be a **composition** of something more fundamental, or to belong to a **different concern** than initially assumed (semantic vs. interaction vs. rendering vs. composition).

This document is the outcome of that discovery process, not a continuation of the HTML-extension approach.

### Methodology
Several methodological commitments shaped this document, consistent with the project's general modeling principles:

**Discovery precedes design.** Concepts are extracted by examining real, concrete cases (legacy code the author had written a decade earlier, actual HTML/ARIA usage, actual research literature) before any abstraction is proposed. Multiple early proposals (a six-way `Type/Role/Capability/State/Relation/Rule` matrix; a `Group A–J` HTML attribute catalog) were explicitly rejected as premature projection — borrowed from other domains before being earned through discovery in this one.

**Existing languages are corpus, not authority.** HTML, ARIA, RDF, RDFa, JSON-LD, Markdown, and others are treated as evidence of what problems real systems have historically tried to solve, and how — not as the correct model to extend or emulate. Where existing languages converge on a solution (e.g., "hyperlink" as a concept present across virtually every hypertext system studied), that convergence is treated as a *signal worth investigating*, not as *proof of correctness*.

**Concept precedes implementation mechanism.** Throughout discovery, most concerns that appeared to need a new semantic layer were found to already be properly addressed by a rigorous, strongly-typed capsule language (Khayyam) — provided that language forbids unwrapped primitive types and enforces absolute encapsulation. Where this document defines a concern (e.g., Composition, Layout, Theme, Event), it defines *what the concern means*, and explicitly delegates *how it is mechanically expressed* to host languages and consumer projects.

**A semantic model must not depend on how a human ultimately perceives or interacts with content.** This principle, arrived at through repeated correction of GUI-centric bias (e.g., "Input is Data Entry" — a GUI framing rejected in favor of "Input is a Receive action"), applies uniformly whether the eventual consumer is a sighted GUI user, a voice interface, a Braille display, a search engine, or an AI agent.

**Numeric claims from AI-generated research are qualitative judgments, not measured data**, and are never cited as such in this document. See [Documentation — Research → Findings](./documentation-research.md#findings).

---

## Explanation

### What "Content" Means Here, and What This Document Is Not
**Content is a conceptual model, not a syntax.** HTML, Markdown, XML, JSON, and any future authoring language are alternative *representations* of the same underlying model — never the model itself. This document does not attempt to design a better markup language; it attempts to discover the conceptual model that any content language, present or future, should be built upon.

This document's scope is broader than its early working title ("Semantic Interface Architecture") suggested. Through discovery, "Semantic" (in the narrow, linguistic sense of meaning/reference) turned out to be only one of several concerns that content genuinely requires — alongside Composition, Layout/Arrangement, Theme/Rendering-mapping, and Event/reactive propagation. All of these are addressed here, each with the same structure: **what the concern means** is defined in this document; **how it is mechanically realized** is delegated to host languages (chiefly Khayyam) and to consumer projects (chiefly `organization`, an independent project built using Memar's approach, not a component of Memar itself). Silence about a concern here would not be neutral: a reader encountering Layout or Theme with no guidance from this document would default to ecosystem assumptions (CSS, Flexbox, component-based theming) that this project explicitly does not want to inherit uncritically. Acknowledging and bounding each concern — without resolving its implementation — is therefore itself part of this document's job.

### Foundational Principles
- **Discovery precedes design.** Concepts here were extracted from concrete cases, not from committee-style enumeration of a "complete" taxonomy up front.
- **Existing representation languages (HTML, ARIA, Markdown, RDF, RDFa, JSON-LD, and future languages) are observational corpus, not architectural authority.** They inform discovery; they do not define correctness.
- **Semantic is not a serialization format.** A semantic relationship (e.g., "this text references that concept") is equally true whether expressed as an HTML attribute, a JSON-LD block, a graph database edge, or nothing visible at all. The relationship precedes and outlives any particular encoding of it.
- **A semantic model must not depend on the consumer.** The same underlying relationship must remain valid whether the eventual consumer is a sighted human, a screen reader, a voice assistant, a search engine crawler, or an AI agent. If a definition changes depending on consumer type, part of Interaction or Rendering has leaked into the Semantic layer.
- **Concept ≠ Implementation Mechanism.** This document defines what a concern means, why it exists, and where its boundaries lie. It does not define data structures, algorithms, or concrete syntax for realizing that concern — those live in host languages and libraries.

### Semantic: Definition and Scope
Two senses of "semantic" were repeatedly conflated early in discovery and must be kept separate:

- **Linguistic [semantics](https://en.wikipedia.org/wiki/Semantics)** — meaning as studied by linguistics: the relationship between an expression and the concept(s)/object(s) it denotes (the classical *sense* vs. *reference* distinction).
- **What this document needs** — closer to: *information that increases what another system can know about represented content, without modifying the content itself.*

The working definition adopted:

> **Semantic information is information that increases what another system can know about represented content without modifying the content itself.**

This definition deliberately avoids the word "meaning" in favor of "what another system can know" — because the definition must remain valid regardless of which system (renderer, AI, screen reader, search engine) eventually consumes it. Under this definition:

- Declaring a passage's language increases available knowledge without touching the text.
- Marking a passage as a quotation increases available knowledge without touching the text.
- Asserting that a passage references an external concept increases available knowledge without touching the text.

None of these require embedding a tag inside the content stream. This motivates the position developed in [Reference as a Relation, Not a Property](#reference-as-a-relation-not-a-property): semantic relationships are edges in a graph, not properties embedded in markup.

### Reference as a Relation, Not a Property
Nearly every existing markup language treats reference as an *attribute of an element* — `href` on `<a>`, `src` on `<img>`, `[text](url)` in Markdown. This framing was tested against a concrete counter-example: what happens when a single piece of content (e.g., an image) needs *more than one* reference simultaneously (a link to a higher-resolution version, a link to its source, a link to a related product)? Under the attribute model, this forces either multiple ad-hoc attributes or an awkward `Reference` "type" that a node can only hold one of. Neither is satisfactory.

**Conclusion: Reference is a relation (a graph edge), not a property of a type.**

```
Thing ──references──▶ Thing
Thing ──references──▶ Locator
```

A single Thing can carry an unbounded number of reference edges without needing a new "type." This is more consistent with graph modeling generally: identity and relationships are separate concerns, and forcing a node to declare a bounded set of typed attributes for something inherently unbounded (references) reintroduces the same rigidity being avoided elsewhere.

**Reference vs. Locator.** These are distinct and must not be collapsed:

- *Reference* means "this content is related to that content" — a semantic fact.
- *Locator* means "here is a mechanism to retrieve/find the referenced content" — `URL`, `URN`, `ISBN`, `DOI`, a database identifier, etc.

A reference may have zero, one, or several locators (a book referenced by title alone; the same book with an ISBN and several mirror URLs). Conflating the two — as HTML's `href` implicitly does — forces every reference to also be a location, which is not always true or desirable.

**`URI` is preferred over `URL`** as the general locator concept, since it accommodates `URN`-style identifiers (e.g., referencing a book by ISBN without committing to a specific retrieval location) without further extension.

**Hyperlink is not a primitive; it is a composition.** What HTML calls a "hyperlink" is better understood as: a Reference, plus a Locator, plus an **Affordance** (the assertion that a consumer may act on/follow this reference). None of these three, individually, requires a dedicated element or tag. A renderer decides — per modality — how to expose that affordance: underlined blue text, a spoken prompt, a QR code, a footnote number, or no visible cue at all.

**Navigation is not intrinsic to Reference.** `<a href="/article/123">` asserts only "this resource references that resource." That a browser, upon click, changes the visible page is a *behavior the browser chose to attach to that relation* — an Interaction/Rendering-layer decision, not a property of the Reference itself. The same reference relation could instead trigger a tooltip, a sidebar preview, or nothing.

### Lexical Token vs. Sense — Handling Ambiguity
If Reference is a graph edge from *some node* to a target, a hard question follows immediately: what is that source node's identity, when the source is a word or phrase repeated many times inside a larger body of free text?

**The uniqueness decision:** a given string (e.g., "Architecture") is treated as a single, globally unique **Lexical Token** — analogous to how a single physical product (a bottle of dish soap) remains one product even when sold by many different vendors under many different terms. Multiple parties may attach different relations/annotations to the same lexical token without this threatening its identity.

This alone does not resolve ambiguity, however, because a single lexical string frequently denotes *more than one distinct concept*. Two genuinely different linguistic phenomena were identified, and must be handled differently:

- **Polysemy** (related senses sharing a common root): "Architecture" as building-design and "Architecture" as software-design share a conceptual root (design/structure). In this case, disambiguation happens through **token composition**: "Software Architecture" is itself a distinct, dependent lexical token that links back to the bare token "Architecture," rather than the bare token acquiring multiple independent sense-edges. Two adjacent tokens (e.g., "S" and "A" forming a bigram) both remain individually identifiable, and both also connect to the surrounding text; the compound resolves ambiguity without contradicting the base word's core meaning.
- **Homonymy** (unrelated senses that happen to share spelling/pronunciation by historical accident, not shared meaning — e.g., Persian "شیر": lion, water-tap, milk — three etymologically unrelated words that converged phonetically). Here, no amount of "the phrase must be a non-contradictory refinement of the word's meaning" rule applies, because there is no single core meaning to refine. **This is an explicit exception** to the general disambiguation-by-composition rule and must be documented as such, or the general rule will silently break on real-world homonyms.

**Bare, unmodified tokens may remain unresolved.** A document that contains only the word "Architecture" — a title, a tag, a project name with no surrounding disambiguating phrase — has no compositional context to resolve which sense is meant. The correct behavior is to **let the ambiguity stand explicitly** (the lexical token exists with no resolved sense-edge, or with multiple candidate sense-edges left unranked) rather than forcing a guess. **This is not an error state.** Any engine built on top of this model must not assume every token eventually resolves to exactly one sense.

**Why ambiguity exists in natural language at all** (background, not architecture): partly cognitive economy (metaphorical extension of existing words costs less than inventing new ones for every related concept), and partly pure historical accident (etymologically distinct words converging phonetically over centuries). Artificial disambiguation-first languages (e.g., Lojban) demonstrate that unambiguous vocabularies *can* be built, but natural languages never migrate toward them because ambiguity resolved cheaply by context is more efficient for everyday communication than maintaining large precise vocabularies. Technical documentation is the opposite case — the cost of ambiguity typically exceeds the cost of precise terminology — which is consistent with this project's general preference (seen elsewhere, e.g., [framework.md](./framework.md)) for exact, non-overlapping definitions.

### Addressability
A second, related question surfaced from the same discovery thread: reference edges require *some* identifiable node on each end — but what, exactly, is allowed to be a node? Can a single word inside a long paragraph be one? A rectangular region of an image? A time range inside a video?

**Working principle (with an acknowledged flaw):**

> Any part of content that needs to carry an independent relation, property, or rule should become an independently addressable entity.

This was deliberately phrased as **Addressable Entity**, not "Thing," because it remains unresolved whether, in the eventual model, this coincides with the project's general `Thing` primitive or is a distinct concept.

**This principle is honestly circular and this document does not resolve the circularity.** One cannot know in advance that a fragment "needs" a relation until that need actually arises — but by then, the fragment has often already been produced/stored without independent addressability, making retrofitting costly. The principle explains *after the fact* why a fragment became addressable; it does not tell an author, *in advance*, which fragments to make addressable. An alternative framing worth pursuing in future work: instead of asking "what might need a relation," ask "what units are *naturally* independently referenced within a given medium's own conventions" (a word, a sentence, an image region, a video timestamp) — an observable, empirical question rather than a predictive one.

**Addressability is recursive and applies beyond text.** The same reasoning that motivates addressing a word inside a paragraph applies unchanged to addressing a Widget inside a Page (deep-linking to a specific dialog; a comment that targets one specific component, not the whole page; a partial-page refresh). This suggests Addressability is a **general primitive shared between unstructured content and Composition**, not two separate concepts that happen to look similar — see [Composition](#composition) and [Multi-Instance and Addressable Runtime Identity](#multi-instance-and-addressable-runtime-identity) for the composition-side consequences.

**Automatic discovery vs. explicit assertion are distinct and must not be conflated.** A system inferring "this paragraph likely mentions a person" (automated semantic discovery, with confidence, possibly wrong, possibly using a more precise boundary — a dotted outline around a face rather than a bounding box) is architecturally different from a human explicitly asserting "this exact span refers to this exact concept." Both are legitimate, and a model should be able to hold both simultaneously about the same content without one overwriting the other — but they are not the same kind of fact and should not be represented identically.

### Composition
Content is rarely atomic. A product listing contains a title, price, image, and an action; an invoice contains line items; a paragraph may itself be composed of sentences carrying independent semantic weight. The relation "this Thing contains/consists-of these Things" is real, necessary, and unavoidable — the question is how it should be modeled.

**Composition is real semantic information about Content, but its concrete mechanics are not defined by this document.** Where Composition is expressed for a well-typed structure (a form, a widget, a domain aggregate), it is fully — and better — expressed in a host language's type/capsule system (e.g., Khayyam), where fields carry real types (`Price`, not `string`) and derived values can be guaranteed correct by construction rather than manually kept in sync across multiple call sites. A concrete legacy example examined during discovery showed exactly the failure mode this avoids: four separate code paths each manually incrementing/decrementing the same running totals, with no single source of truth — a class of bug that a proper Aggregate/derived-property model eliminates by construction.

**A critical distinction discovered during this analysis: Composition appears in at least two structurally different graphs, and conflating them is a specific, observed failure mode.**

- **Aggregate composition** — the domain-consistency boundary. Example: an `Invoice` and its `LineItems`, where totals must remain correct. This graph has business-rule obligations (consistency, transactional integrity) and belongs entirely to the type/capsule system.
- **Presentation composition** — how a given Aggregate is arranged for a particular consumer (a GUI widget tree, a printed layout, a spoken reading order). This graph has no domain-consistency obligation of its own — an "increase quantity" button in a presentation tree has no counterpart node in the domain model at all; it exists purely to let a consumer act upon the Aggregate.

Both are legitimate uses of a general "contains" relation, but **they are not the same graph and must not be collapsed into one.** The observed failure mode (a single `<table>` element simultaneously carrying structural nesting, domain data, and display styling) is precisely what results from collapsing them.

**Implementation note:** The concrete mechanics of expressing composition — how a capsule declares its parts, how instances are constructed, how consistency is enforced — belong to the host language's type/capability system (Khayyam), not to this document.

### Layout / Spatial and Sequential Arrangement
Once multiple Things are composed together, Composition alone does not answer a further, distinct question: in what **arrangement** do the parts relate to one another, for a given consumer? Side-by-side or stacked? In what order does a screen reader visit them? What happens when available space changes — narrow phone, wide monitor, or no visual space at all in a voice-only context?

**Why this is a genuinely distinct concern from Composition, not a sub-case of it:** Composition answers "what is part of what" — a fact that stays true regardless of consumer. Layout answers "how are these parts related *spatially or sequentially*, for *this* consumer" — an answer that legitimately changes per rendering context, per device, per modality, and even per era of design practice.

That last point has architectural weight. Layout methodology is one of the fastest-moving areas of interface design: table-based layout gave way to floats, which gave way to Flexbox, which was found insufficient for certain problems and supplemented (not replaced) by Grid — and further approaches will likely follow. This history is presented here purely as evidence of a fast-evolving space, not as a recommendation of any specific algorithm; a framework that locked in one specific layout model at the architectural level would both go stale within a few years and be presumptuously narrow today, since GUI arrangement is only one of the modalities this project cares about — VUI reading order, Braille sequencing, and spatial arrangement in AR/VR are equally legitimate arrangement problems, each with different rules entirely, none of which reduce cleanly to a 2D box model.

XML/HTML-family markup conflates all three of Role (`<button>`), Composition (nested children), and Layout (document order = default visual order) into a single syntax by construction — even with zero CSS, the mere order of tags in a document implies a default top-to-bottom, left-to-right arrangement. This is precisely the conflation this project set out to avoid, and precisely why "document order" cannot be trusted as an implicit arrangement signal once VUI, Braille, or AR/VR consumers are taken seriously: reading order for a screen reader is not necessarily the same as visual arrangement order.

What can be stated today without over-committing to a specific solution:

- Whatever "arrangement" turns out to be, it is a relation **between siblings within a Composition**, not a property of a single node in isolation — tentatively suggesting it belongs to the same relational family as `contains`, rather than being an attribute like a role or a state.
- Arrangement is consumer-dependent in a way Composition is not: the same composed structure legitimately requires multiple, simultaneously valid arrangements (a phone layout and a desktop layout are not two different Compositions of the same content — they are two arrangements of one Composition).
- Whether this project needs *any* shared, rendering-agnostic arrangement vocabulary (even something minimal and algorithm-agnostic, e.g., "these siblings form an ordered sequence" vs. "these siblings form an unordered set," without specifying how that sequence is physically rendered) — or whether arrangement should be left entirely to each Design Language/Renderer with zero shared vocabulary — is genuinely unresolved.

**Implementation note:** Any concrete arrangement vocabulary is expected to live in renderer and library modules, potentially beginning in a local module such as the Khayyam modules in this repository or in consumer projects such as `organization`, and may migrate into shared architecture only once real usage justifies a stable abstraction — not before.

### Theme / Role-to-Rendering Mapping
Separate from spatial arrangement is the question of how a given semantic Role is rendered in isolation — what a "primary action" looks like, sounds like, or feels like. This concern's shape is more settled than Layout's, though still not resolved in detail.

If composed nodes carry a Role (e.g., `PrimaryAction`, `DestructiveAction`, `Heading`), a Design Language can define a one-time mapping from Role to concrete rendering — analogous to how a browser's default stylesheet maps HTML tag names to default styles, except here the mapping is explicit and pluggable rather than implicit and singular to one engine. This is the mechanism through which the original motivating idea (see [Motivation](#motivation)) is realized: the same semantic markup renders as a Material raised button, a Fluent filled button, or a spoken confirmation prompt, purely by swapping the active Role→Rendering mapping.

**User freedom is intrinsic to this concept, not an add-on.** A Theme is simply another Role→Rendering mapping, authored by whoever wants one, without requiring changes to the semantic/composition model itself. This directly addresses a gap the author identified in the current web ecosystem: no widely-adopted framework cleanly supports arbitrary user-authored themes precisely because Role and Rendering are rarely factored apart in the first place — instead, styling is scattered as classes with weak semantic weight (a pattern the author's own decade-old `button.css` prototype also fell into, despite good intentions).

Naming conventions for Roles, how mappings are registered, and how conflicts between overlapping mappings are resolved all remain open — but the *shape* of the answer (Role as the stable interface, mapping as the replaceable implementation) is comparatively settled relative to Layout.

#### Where Theme's Authority Ends
The relationship between [Layout](#layout--spatial-and-sequential-arrangement) and Theme is genuinely unresolved, and this document does not claim otherwise. In much of the existing ecosystem, Layout is informally treated as a sub-concern of Theme — a Theme "includes" spacing and arrangement rules alongside color and typography. But this framing does not survive scrutiny once non-web platforms are examined: on Android, for instance, a **Theme** governs visual styling, but a separate concept, the **Launcher**, enforces structural decisions (which surfaces exist, how the home screen and app drawer are organized, what can and cannot be rearranged by the user) that a Theme alone does not control and cannot override. This demonstrates that "everything visual/structural is Theme" is not a universal truth — it is one platform's particular choice about where to draw a boundary, and a different platform draws it differently.

This project does not yet have a settled answer to where the Theme/Layout boundary should sit, or whether a third concept (analogous to a Launcher — something that can enforce structural constraints a Theme cannot override) is needed. A further, more radical possibility was raised and is recorded here explicitly rather than resolved: **should the freedom this document grants for user-authored Themes extend even further, to user-authored Page and Widget composition itself** — i.e., should end users (not just Design Language authors) be able to compose their own arrangements of Widgets into Pages, constrained only by what the underlying Semantic Graph exposes, the way a Launcher lets a user rearrange (but not redefine) home-screen content? This is not decided. It is recorded here because it directly affects how much authority a future Theme/Layout document should claim, and premature closure on this question would risk designing Layout/Theme too narrowly.

**Implementation note:** Role naming conventions, mapping registries, and conflict resolution are library/renderer concerns, not defined here.

### Event / Reactive Propagation
Multiple independent parts of a composed structure frequently need to react when one part changes — a running total recalculating when a line item changes, a footer updating when a list changes, a sidebar refreshing when a related record updates elsewhere. Manually keeping such derived values synchronized at every call site was identified as a concrete, recurring source of bugs in reviewed legacy code (the same invoice example referenced in [Composition](#composition)).

**This concern is considered resolved in direction, though not yet implemented.** No dedicated Event primitive or vocabulary is defined by this document. The direction that emerged is both narrower and more general at once: **any capsule that adopts a general Observable/Dispatchable capability becomes a valid event source** — request/response interaction with a service is simply one possible dispatchable action among others, not a special case requiring its own event vocabulary. If a need for a dedicated event abstraction ever arises beyond this, that need itself signals that the underlying service abstractions were modeled incorrectly, and the fix belongs in the modeling of those abstractions, not in a new Event primitive.

**Implementation note:** This concern's mechanics belong entirely to Khayyam's capability system (an `Observable`/`Dispatchable` capability any capsule can adopt), generated by tooling rather than hand-implemented per capsule.

### Type Reference — Where Semantic Meets a Type System
RDFa-style annotation (`property="price"`) attempts to solve a real problem — asserting that a piece of content is an instance of some external, well-defined concept — but does so by conflating two separate acts that must be kept apart:

1. **This node refers to an externally-defined concept** (a Reference/edge, as in [Reference as a Relation, Not a Property](#reference-as-a-relation-not-a-property)).
2. **What that concept's structure is** (a Type Definition — fields, constraints, validation) — which belongs to a domain model, not to the content layer.

Carried into this project's terms: a content node carries a `refers-to-type` edge to a Type Definition (e.g., `Price`), and that Type's full structure — currency handling, validation, formatting — is defined exactly once, in Khayyam, in the consuming domain model. The content layer never repeats or re-derives that structure. This directly resolves a concrete legacy problem examined during discovery: a decade-old template (`<ins title="Payable price" property="price" content="${p.PayablePrice}">${p.PayablePrice}</ins>`) that scattered the same value and its associated metadata across four separate places in one tag — a template maintenance hazard that a Compiler-mediated separation (Authoring Model → Semantic Graph → rendered outputs, see [Authoring Syntax vs. Semantic Graph](#authoring-syntax-vs-semantic-graph)) removes structurally rather than through developer discipline.

**Architecture defines the mechanism of reference; it does not define a default vocabulary.** What must be standardized is only the `refers-to-type` edge itself — the capability for any node to reference a Type Definition. What Types exist (`Price`, `Currency`, `Person`, `Password`), what fields they carry, and what constraints they enforce are left entirely to consuming projects such as `organization`, whose modeling choices may legitimately diverge from external vocabularies (e.g., modeling `Password` as a kind of connection-token rather than following schema.org's or any other external vocabulary's framing). This mirrors how RDF standardizes the triple mechanism without prescribing which predicates exist — that is left to external vocabularies such as schema.org, which sit *above* RDF, not inside it.

**Case study: search-engine structured data.** Investigation into whether shared vocabularies like schema.org remain relevant confirmed they do, and arguably more so as of 2026: entity-disambiguation markup (`SameAs`, `knowsAbout`) has become a high-leverage signal for AI-driven search citation, even as certain rich-result *types* (FAQ, HowTo) have been deprecated by search engines independently of the underlying vocabulary's validity. This volatility is itself evidence for the architectural position taken here: a project's internal model should never be authored *as* a specific external vocabulary, because that vocabulary can change or be deprecated on a timeline outside the project's control. Instead, compatibility with any external vocabulary (schema.org, JSON-LD, or a future replacement) should be produced by an optional, separate **mapping/compiler layer** that translates the internal model outward — the same mechanism already used to render the same internal model to HTML, voice, or Braille (see [Authoring Syntax vs. Semantic Graph](#authoring-syntax-vs-semantic-graph)). schema.org becomes one of several possible *targets* of a Reference edge, never a foundation the internal model is built upon.

The historical migration from RDFa/Microdata (embedded inline in markup) to JSON-LD (a separate `<script>` block) in the SEO industry is worth noting for a different reason: it was driven by tooling convenience, not by architectural superiority, and it reproduces exactly the dual-source-of-truth problem this document rejects (content in one place, its structured-data description in another, requiring manual or semi-manual synchronization). The Compiler-mediated model in [Authoring Syntax vs. Semantic Graph](#authoring-syntax-vs-semantic-graph) avoids this dual-source problem entirely — neither inline annotation nor a separate JSON block is ever hand-authored; both are generated outputs, independently reached from the same underlying Semantic Graph, so synchronization is a compiler property, not a discipline the author must maintain.

### Multi-Instance and Addressable Runtime Identity
A concrete legacy failure examined during discovery: an `invoicePage` implemented as a single global singleton object (`this.invoiceList`), which made it structurally impossible to have two invoices open simultaneously, including across browser tabs that arguably should have stayed synchronized. This is presented as a cautionary case, not as a solved problem.

**Widgets and Pages should support multiple simultaneous instances by default,** the same way any other capsule in a properly-typed language is freely instantiable — singleton behavior, where genuinely needed, should be an explicit design choice at the point of use, never an accidental consequence of how the abstraction happens to be structured.

**Cross-runtime state synchronization (e.g., between browser tabs) is a distinct concern**, belonging to the Platform layer (PersiaOS), not to this document — it is a runtime-synchronization problem, not a content-modeling problem, even though the failure mode that motivated noticing it originated in content-layer code.

**Page as a specialized Widget, not a separate primitive.** Building on the recursive-addressability conclusion in [Addressability](#addressability): if a Widget nested deep inside a Page can, like any addressable fragment of unstructured content, legitimately need an independent address (deep-linking to a specific dialog; a comment targeting one specific sub-component), then the meaningful difference between "Page" and "Widget" is not a difference in *kind* but a difference in **degree of addressability** — a Page is simply a Widget with the additional property of being addressable at the top level (via something resembling a URL). This suggests a simplification: rather than two separate primitives (`Page`, `Widget`), a single primitive (`Widget`, composable and optionally, recursively addressable) may suffice.

### Authoring Syntax vs. Semantic Graph
A cross-cutting concern surfaced repeatedly across the concern topics above: **the syntax an author physically types must not be conflated with the Semantic Graph the model actually operates on.** A recurring architectural shape emerged, but it must be described carefully as two distinct relationships, not one:

```
Authoring Model  (concise, readable, blends free prose with structured data)
        │  compiles to
        ▼
Semantic Graph   (the single, canonical, format-independent model)
```

```
                          Semantic Graph
                                │
        ┌───────────┬───────────┼───────────┬───────────┐
        │           │           │           │           │
   reached by   reached by  reached by  reached by  reached by
        ▼           ▼           ▼           ▼           ▼
  GUI Renderer  GUI Renderer  Voice     Braille    SEO Mapper
  (Theme A)     (Theme B)     Renderer  Renderer   (JSON-LD)
```

These two relationships are not symmetric. **Authoring compiles to the Graph** — a many-to-one relationship in the sense that different authoring syntaxes could in principle compile to the same graph shape, but for any single authored document, there is one resulting graph. **The Graph is reached by many independent Renderers** — a one-to-many, fan-out relationship. No single "compilation" produces "the" output; rather, each Renderer (a specific Theme's GUI renderer, a Voice renderer, a Braille renderer, an SEO mapping layer, a programmatic API renderer) independently traverses the same canonical Graph and derives its own representation from it, on its own schedule, without the others being aware of it. This is precisely *why* this layer needs to exist at all: the whole motivation from the [Introduction](#introduction) — one semantic source, many simultaneous renderings — only holds if the Graph is a stable thing multiple independent readers can reach, not a one-shot compilation target that produces a single fixed output.

**A cautionary case examined against the Authoring side of this shape:** Pug/Jade and JSX were investigated as candidate precedents for a compact authoring syntax and found instructive for the opposite reason expected — both correctly identified real problems with HTML (mixing logic and markup harms readability; HTML's tag vocabulary is historically bloated and inconsistent) but "solved" the second problem by *removing all constraints on tag creation*, letting any developer invent any tag freely. This is the exact opposite of this project's direction (reducing an unconstrained vocabulary to a small set of discovered primitives, not replacing one unconstrained vocabulary with an even less constrained one). The conclusion drawn: a workable Authoring Syntax must be compact and readable, but **constrained to the primitives actually discovered through this document's process** — not an open invitation to invent arbitrary new tags.

**Type-system verbosity is not, by itself, a reason to abandon strong typing for content templates.** Concern was raised that a verbose, strongly-typed language like Khayyam might make content templates unreadable if used directly and unaided. The resolution reached: this is a solved problem in general-purpose programming (JSX, Vue's Single-File-Component syntax, Terraform's HCL — none of these were adopted because their underlying execution model was incomplete; each exists because writing the underlying API directly, by hand, for every UI/config unit, would be unreadable at scale). The correct response is therefore a dedicated, compact Authoring Syntax that *compiles to* Khayyam graph/capsule calls — not raw Khayyam typed by hand for every template, and not abandonment of Khayyam's typing discipline in favor of an untyped markup language.

Two decade-old legacy examples examined during discovery (`${hamburgerMenuWidget.ConnectedCallback()}` embedded directly in an HTML template; an invoice table row template binding fields such as `${pr.Quiddity.Title}` and `${pr.PayablePrice}` directly into table cells) were read, in retrospect, not as isolated hacks but as symptoms of the author already reaching, a decade prior and without the vocabulary to name it, toward exactly this Composition-as-typed-graph model — treating a Widget as a composable function call rather than a Custom Element, and treating a table row as a typed Composition of `Product Title / Original Price / Payable Price / Quantity / Actions` rather than as an HTML `<table>` structure.

### "Khayyam-manner" Languages, Not Khayyam-Only
The architectural preference throughout this document for a strongly-typed capsule language should not be read as a hard dependency on Khayyam specifically — the intent is a **class of languages sharing certain properties**, of which Khayyam is the first and most disciplined instance. Dynamic-typed languages can, in principle, approximate this class, though with more friction; but the two properties that matter cannot be abandoned without losing the benefits this document relies on throughout:

- **No unwrapped primitive types** flowing through the system without a meaningful, named Type wrapping them (the direct lesson behind Khayyam's own elimination of bare primitives).
- **Absolute encapsulation** — no accidental exposure of internal structure that would let a caller bypass a Type's own invariants.

### Structural Notation Within an Authoring Syntax Itself
A question is recorded here precisely because it is unresolved and directly tests the principles established above against a concrete, everyday case: **is the structural notation of an authoring format itself a form of embedded semantic tagging?**

The concrete trigger: this project's own documentation is authored in Markdown, and Markdown documents in this project also carry a YAML front-matter block for metadata (Title, Status, Citations, Contributors — as at the top of this very document). This means **two separate mechanisms currently coexist for attaching non-prose information to a document**: inline notation within the text stream itself (`#` for headings, `-` for list items, `**bold**` for emphasis) and a separate front-matter block at the top of the file. This is precisely the "two competing places for the same kind of information" problem this document has otherwise argued against (the RDFa-vs-JSON-LD case in [Type Reference](#type-reference--where-semantic-meets-a-type-system)) — except here it appears inside the very format used to write documents like this one, not in a hypothetical external example.

The deeper question this raises: does a Markdown heading marker (`#`) merely delimit where one Text unit ends and another begins (a purely structural fact about the stream, arguably necessary at some level for any serialization to exist at all) — or does it simultaneously **assert semantic information** (this line has `Importance = 1`, this line has the `Role: Heading`) **inline**, in exactly the way [Reference as a Relation, Not a Property](#reference-as-a-relation-not-a-property) argued a Reference must *not* be embedded as an attribute, and [Type Reference](#type-reference--where-semantic-meets-a-type-system) argued Type information must *not* be scattered across a template? If `#` is doing the latter, then by this document's own logic, that Importance/Role assertion should be an external edge from an addressable Text fragment to a Role/Type — not a character embedded in the text stream itself — and Markdown's heading syntax is a smaller-scale instance of the exact problem this document exists to correct, not an innocent structural convenience.

**This question is not resolved here.** Two candidate positions were identified, neither adopted:

- **Position A — Pure delimiter, not semantic.** `#` merely marks a boundary in the raw text stream (equivalent to a paragraph break), and any *interpretation* of what that boundary means (a heading, its importance level) is a separate act performed by a parser producing a `refers-to-type` edge afterward — the character itself carries no semantic weight, only structural segmentation, analogous to how a comma delimits list items in CSV without asserting anything about their meaning.
- **Position B — Implicit semantic tagging.** `#` is functionally indistinguishable from writing `role="heading" importance="1"` inline — it *does* assert a Role, merely with a terser syntax than an explicit attribute, and therefore violates the same principle established for Reference and for Type: information about a Text fragment's role should be an edge external to the fragment, not a character prefixing it in the stream.

If Position B is correct, the implication extends beyond headings to every structural marker in every authoring format examined so far — Markdown's `-`/`*` (list-item role), numbered-list digits (ordinal-position role), `**bold**`/`*italic*` (emphasis role) — each would need to be re-examined as implicit semantic tagging requiring an external edge, not inline notation. This would materially affect the still-unresolved Authoring Syntax question in [Authoring Syntax vs. Semantic Graph](#authoring-syntax-vs-semantic-graph): a fully consistent Authoring Syntax under Position B could carry **no** inline structural notation at all, only boundaries between minimal, addressable Text units, with every interpretive fact (heading, list-item, emphasis, and beyond) expressed as an edge from those units — a considerably more radical Authoring Model than anything proposed so far.

#### Concrete Evidence: Tree/Graph Notation in This Very Document
A self-referential piece of evidence bears directly on the Position A/B question above, and was noticed only by examining this document's own authoring habits rather than any external system.

Throughout this document (in [Reference as a Relation, Not a Property](#reference-as-a-relation-not-a-property), [Composition](#composition), [Authoring Syntax vs. Semantic Graph](#authoring-syntax-vs-semantic-graph), and elsewhere), tree and graph structures are represented using spatially-arranged ASCII notation:

```
Thing ──references──▶ Thing
```

or

```
Semantic Graph
        │
   ┌────┼────┐
   ▼    ▼    ▼
Renderer Renderer Renderer
```

This notation relies on **two-dimensional spatial arrangement** — indentation depth, vertical alignment of branches, the horizontal position of an arrow — to encode structural and semantic information: which node is a child of which, which edges originate from which source, sibling ordering. This is, without qualification, a **visual/GUI convention**, no different in kind from a Flexbox layout: it assumes a reader capable of parsing two-dimensional spatial relationships on a rendered page or screen.

This matters as direct evidence for Position B, not merely a hypothetical concern: a screen reader, a Braille display, or a plain sequential token stream (the kind an AI language model actually consumes, character by character, with no privileged access to two-dimensional layout) cannot recover the same structural information from this notation without either (a) a GUI-style rendering step that reintroduces exactly the visual dependency this document argues against, or (b) treating the whitespace/indentation/arrow characters themselves as implicit structural markers requiring special-cased parsing — which is exactly the "inline structural notation instead of an external edge" problem Position B describes, just at the diagram level rather than the Markdown-heading level. In other words: **at least for tree/graph diagrams, Position B is not merely plausible — it is directly demonstrable**, because the author and both AI participants writing this very document have been unable to avoid GUI-shaped notation even while explicitly arguing against GUI-centric modeling elsewhere in the same document. This is a stronger form of evidence than the Markdown-heading case, which remains debatable; this one is self-evident from the document's own text.

This also reframes a claim commonly made about Markdown's own design goal — that it was created specifically to remain meaningful even without rendering, as plain text. That goal, examined against this evidence, is itself GUI-adjacent rather than GUI-neutral: "readable as plain text" implicitly assumes a *sighted* reader scanning a monospaced grid, for whom indentation and alignment are legible structural cues. It does not extend to a non-visual consumer (a screen reader reading character-by-character, a Braille display without spatial layout, or a language model without privileged access to a rendered grid) for whom the same whitespace carries no reliable structural signal at all. "Meaningful unrendered" and "meaningful without any visual/spatial parsing whatsoever" are not the same claim, and Markdown — like the diagrams in this very document — only satisfies the first.

This is recorded as evidence, not as a final resolution of the broader question above — the appropriate replacement for tree/graph notation in a fully non-visual-neutral Authoring Model is left open, along with the rest of this topic.
