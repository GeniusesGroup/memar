# Khayyam Display Research 002 — What the host already classifies, and what the contract still owes

## Table of contents
- [Status](#status)
- [Question and Goals](#question-and-goals)
- [Participants](#participants)
- [Methodology](#methodology)
- [Findings](#findings)
  - [F1 — The host's own classification: twenty-four token types and eight modifiers](#f1--the-hosts-own-classification-twenty-four-token-types-and-eight-modifiers)
  - [F2 — The super-type mechanism, and what a type with no super type is](#f2--the-super-type-mechanism-and-what-a-type-with-no-super-type-is)
  - [F3 — What the host does with a type nothing matches](#f3--what-the-host-does-with-a-type-nothing-matches)
  - [F4 — The twenty-one roles against the host's classification](#f4--the-twenty-one-roles-against-the-hosts-classification)
  - [F5 — The boundary, and what is missing for a consumer that never sees the code](#f5--the-boundary-and-what-is-missing-for-a-consumer-that-never-sees-the-code)
  - [F6 — Principles, with what each cost](#f6--principles-with-what-each-cost)
- [Open Questions](#open-questions)
- [Related Artifacts](#related-artifacts)
- [Notes](#notes)

## Status
Active. The inquiry is answered; the owner has not reviewed it, and the open questions below graduate to [display.handoff.md](./display.handoff.md) on that review rather than here.

## Question and Goals
### Questions
1. Does the host already define a standard classification of tokens that a provider is meant to use rather than invent, and by what mechanism does a provider declare its own type as a kind of a standard one? — **Answered** (F1, F2)
2. What does the host do with a token whose type is unregistered, unmatched, or declared with no super type? — **Answered** (F2, F3)
3. Are this repository's twenty-one roles a classification or a re-derivation, which of them map onto which standard class, and which are Khayyam's own? — **Answered** (F4)
4. Where is the boundary between what a language publishes and what a consumer decides, for a consumer that may never see the code, and what does the contract still lack for that consumer? — **Answered** (F5)
5. Which of this stretch's work is a lesson worth keeping and which was a dead end, stated as principles? — **Answered** (F6)

### Goals
1. Give the owner the host's own classification, in the host's own terms, read out of the host's own product — so a decision about super types is made against what the host does rather than against what it is assumed to do. — **Met**
2. Say what a re-cut of the role list would have to be built on, without re-cutting it. — **Met**
3. Name the concrete things a non-editor consumer is owed and does not have. — **Met**
4. Keep every lesson phrased as a rule a later session can apply, with what it cost. — **Met**

### Scope
The host's classification, its super-type mechanism, and its rule-matching, as found in the installed product's own bundle and declarations; this repository's contract, manifest, grammar, and language server as the thing being judged. It does not choose a palette, does not change the contract, the manifest, a theme, a grammar, or the server, and does not answer what the *language* calls the identities the roles name — that is a question for [docs/khayyam/](../../../docs/khayyam/) and the owner, and this record does not reach it.

## Participants
- [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) — **Questioner**, **Goal-setter**; review outcome: **Not yet reviewed**.
- [Space Bunny Alpha](../../../CONTRIBUTORS.md#space-bunny-alpha) (space-bunny via [OpenCode](../../../CONTRIBUTORS.md#opencode)) — **Researcher**.

## Methodology
1. Read the installed product's own bundle rather than its documentation about it, and the bundle's own string table for every description the bundle resolves by index. The product is VS Code 1.139.1 at `resources/app/out/vs/workbench/workbench.desktop.main.js`; it is minified, so every claim below names the identifier that survives in it, and a reader finds it by searching for that name. The descriptions are the strings in `resources/app/out/nls.messages.js` at the indices the bundle dereferences.
2. Read the contribution-point schema out of the same bundle, because it is the manifest contract the product enforces at load: the handler for `contributes.semanticTokenTypes`, `contributes.semanticTokenModifiers`, and `contributes.semanticTokenScopes`, and the string table entries the handler's schema points at.
3. Read the API declarations shipped with the product, `resources/app/out/vscode-dts/vscode.d.ts`, for what a provider hands the host and what the host hands it back.
4. Downloaded the protocol's own specifications, 3.17 and 3.18, to compare the predefined type and modifier lists the protocol names against the list the host registers — because the two are not the same list, and a decision made against the wrong one is made against nothing.
5. Read this repository's own artifacts against those findings: the contract, the manifest, the two theme files, the grammar, the server's legend, and the verifier.

Limits: no editor was run, and nothing in this repository was changed. The `contributes.semanticTokenTypes` contribution point is established from the host's source and has never been exercised by this extension, so every statement about what declaring a super type does is a statement about the host's code, not about this repository's behaviour. The colour question is not reopened here; the palette work stands in [display.research.001.md](./display.research.001.md) and in the handoff's decisions, and this record takes no position on any value.

## Findings
### F1 — The host's own classification: twenty-four token types and eight modifiers
The host registers its own classification as a contribution at load. `function T4n()` in the bundle builds the `TokenClassificationContribution` singleton and calls `registerTokenType(id, description, scopesToProbe, superType, deprecationMessage)` twenty-four times, then `registerTokenModifier(id, description)` eight times. Those twenty-four and eight are the classification a provider is meant to use rather than invent, and the descriptions are the host's own words:

| Type | The host's description (string-table index) | Scopes the host probes for it |
| --- | --- | --- |
| `namespace` | Style for namespaces (3820) | `entity.name.namespace` |
| `type` | Style for types (3840) | `entity.name.type`, `support.type` |
| `struct` | Style for structs (3839) | `entity.name.type.struct` |
| `class` | Style for classes (3803) | `entity.name.type.class`, `support.class` |
| `interface` | Style for interfaces (3813) | `entity.name.type.interface` |
| `enum` | Style for enums (3809) | `entity.name.type.enum` |
| `typeParameter` | Style for type parameters (3841) | `entity.name.type.parameter` |
| `parameter` | Style for parameters (3823) | `variable.parameter` |
| `variable` | Style for variables (3842) | `variable.other.readwrite`, `entity.name.variable` |
| `property` | Style for properties (3824) | `variable.other.property` |
| `enumMember` | Style for enum members (3810) | `variable.other.enummember` |
| `event` | Style for events (3811) | `variable.other.event` |
| `function` | Style for functions (3812) | `entity.name.function`, `support.function` |
| `method` | Style for method (member functions) (3818) | `entity.name.function.member`, `support.function` |
| `member` | Style for member functions (3817); super type `method`; "Deprecated use `method` instead" | none |
| `macro` | Style for macros (3816) | `entity.name.function.preprocessor` |
| `keyword` | Style for keywords (3814) | `keyword.control` |
| `comment` | Style for comments (3804) | `comment` |
| `string` | Style for strings (3838) | `string` |
| `number` | Style for numbers (3821) | `constant.numeric` |
| `regexp` | Style for expressions (3826) | `constant.regexp` |
| `operator` | Style for operators (3822) | `keyword.operator` |
| `decorator` | Style for decorators & annotations (3806) | `entity.name.decorator`, `entity.name.function` |
| `label` | Style for labels (3815) | none |

The eight modifiers are `declaration` ("Style for all symbol declarations", 3805), `documentation` (3808), `static` (3837), `abstract` (3801), `deprecated` (3807), `modification` ("Style to use for write accesses", 3819), `async` (3802), and `readonly` (3825). The host also registers composite *default style* selectors — `variable.readonly`, `property.readonly`, `type.defaultLibrary`, `class.defaultLibrary`, `interface.defaultLibrary`, `variable.defaultLibrary`, `variable.defaultLibrary.readonly`, `property.defaultLibrary`, `property.defaultLibrary.readonly`, `function.defaultLibrary`, `member.defaultLibrary` — each pairing a type with a modifier and probing scopes for it.

Two things follow that no document in this folder had. First, **every standard type carries the TextMate scopes that stand for it.** That is a bridge between the host's two mechanisms, published by the host, for the classes a Khayyam role most needs — `class`, `interface`, `type`, `function`, `method`, `variable`, `parameter`, `property`, `keyword`, `comment`, `string`. Second, the list the host registers is **not** the list the protocol's specification names. Protocol 3.18 (`SemanticTokenTypes`, `SemanticTokenModifiers`, in the "General Concepts" section of the Semantic Tokens feature) names twenty-four types including `modifier` and `label` but not `member`, and ten modifiers including `definition` and `defaultLibrary`, which this host does not register as modifiers. A decision about which names exist must be made against the host's list, because the host's list is the one the host enforces.

### F2 — The super-type mechanism, and what a type with no super type is
The mechanism is a contribution point. The product's own schema for `contributes.semanticTokenTypes` (string-table 24925–24929) takes an array of `{ id, description, superType }`, where `id` and `superType` must each match `^\w+[-_\w+]*$` — "Identifiers should be in the form letterOrDigit[_-letterOrDigit]*", 24927 and 24929 — and `description` is required and non-empty (24930, 24931, 24932, 24940). The handler is in `W2t`: a contributed entry is validated and passed to `registerTokenType(id, description, superType)`, which stores the type, gives the theme-styling schema a property for it, and empties the cached hierarchy; a removed entry is deregistered.

`getTypeHierarchy(id)` is the whole of the semantics. It builds `[id]`, then walks `superType` while there is one, and caches the result. **A type that declares no super type has a hierarchy of exactly itself** — that is what the code says, and it is what the host already recorded. `registerTokenType` throws `Invalid token type id.` for a name the pattern rejects, so a provider cannot register `method-argument.khayyam` at all.

Matching is `parseTokenSelector`'s `match`: the rule's key is parsed by `N2t` — scanning back for `.` or `:` — into a type, modifiers, and an optional language; the type must then be found by `getTypeHierarchy(tokenType).indexOf(ruleType)`, and the score rises the nearer in the chain the match is. A rule keyed `type` therefore matches a token whose type is `capsule` declaring `superType: "type"`, and does not match a `capsule` that declares nothing. `*` matches any type.

Registration is not what makes a type stylable; a rule keyed with the type's exact name styles an unregistered type. What registration buys is the super type, and a place for the theme's own schema to name the type.

### F3 — What the host does with a type nothing matches
`SemanticTokensProviderStyling.getMetadata` resolves the legend entry at the token's type index, asks the theme for the style, and returns the value `2147483647` when the type index is not in the legend, when no rule matched, or when a rule matched and produced no field at all. The line builder then refuses to write that token into the line: the token is discarded, and the grammar's own metadata is what the reader sees. So a type nothing matches is not unstyled — it is absent, and the file draws as though the server had said nothing. That is the whole of the "the tree is green and the screen is wrong" class of failure, and it is why a legend entry carrying a separator, or a rule keyed with a spelling the token's hierarchy cannot contain, produces a plausible wrong answer rather than a gap.

One recorded reason is corrected here. The handoff's decision against `contributes.semanticTokenScopes` reads that a bridge is "applied last" and therefore hands the reader the active theme's value for a probed scope. `getTokenStyle` does not say that: it runs the theme's rules, then the settings' rules, and consults the default rules — which is where a bridge's scope probe is registered — **only for the fields those left unset**, so a bridge cannot displace a field a colour rule already set. The decision stands and its ground is firmer than the one recorded: a bridge would not replace a Memar theme's value, it would decide the value for every reader who selects a theme that has never heard of Khayyam, which is the fallback the contract forbids.

### F4 — The twenty-one roles against the host's classification
They are a re-derivation, and the reason they look arbitrary is now nameable: the host's classification has one axis — **what kind of thing is this name** — and the twenty-one spread three questions across one list. The question "what kind" is answered by the token type; "how did it enter this file" and "how wide is its validity" are qualifiers, and the host carries qualifiers in modifiers, of which its standard set has nothing for either. A `superType` expresses kind and nothing else: it does not express origin, and it does not express position or specificity.

| Role | Standard class it would declare as a super type | What the super type does not carry |
| --- | --- | --- |
| `keyword` | `keyword` | — |
| `subtype` | `keyword` | that the word names a Type's category or routes an inclusion |
| `included-type` | `type` | that the name arrived by inclusion |
| `included-variable` | `variable` | that the name arrived by inclusion |
| `file-uri` | `string` | that the string is a source-level path |
| `capsule` | `class` | that a Capsule is one of four categories of Type |
| `abstraction` | `interface` | the same |
| `method` | `method` | that a Method is a Type, and that a call site is the same identity as a declaration |
| `scope` | none — `type` is the nearest, and a Scope is not a generic type | the whole role: the fourth category of Type |
| `type-reference` | `type` | that this file does not state the category |
| `variable` | `variable`, with `declaration` | that the validity is the whole file |
| `method-local` | `variable`, with `declaration` | that the validity is one method body; the host's modifiers have no `local` |
| `method-argument` | `parameter`, with `declaration` | — |
| `method-argument-type` | `type` | that it is an argument's declared type |
| `method-owner-type` | `type` | that it is the owner |
| `capsule-field` | `property`, with `declaration` | that it is private to the Capsule; the host's modifiers have no `private` |
| `identifier-reference` | none | the whole role: it names what the resolver could not resolve, not a kind of name |
| `comment` | `comment` | — |
| `string` | `string` | — (reserved) |
| `invalid-number` | none — `number` is the class for a number the language admits | the whole role: a form the language does not admit |
| `invalid-operator` | none — `operator` is the class for an operator the language admits | the whole role |

Four roles are genuinely this language's own with no standard counterpart: `scope`, `identifier-reference`, `invalid-number`, `invalid-operator`. The first two are a Type category and a resolver's ignorance; the second two are a statement about what the language refuses, which in the host is a diagnostic and a grammar scope rather than a token type at all. The contract's `profiles.lsp.alignment` already says the standard types are a subset of what it needs and that the split is at least Type and Variable; what it does not say, and what F2 makes load-bearing, is that the split must be declared as a super type or the standard type's value never reaches the role.

A re-cut would therefore be built on three things this repository has not yet stated. Each role would carry a **kind** — a standard type it declares as a super type, or an explicit statement that it has none. Each role would carry the **qualifiers** the host's modifier set can express, and the residue would be named as residue rather than spread across new types. And the roles with no counterpart would be marked as roots, because a root's hierarchy is itself, which is what makes a theme's value for it mandatory rather than a formality. Only then does the owner's ruling — one hue per kind, lightness and saturation by origin and by kind — become a derivation from the classification instead of a fresh choice over a re-derived list.

### F5 — The boundary, and what is missing for a consumer that never sees the code
The line the host's own code draws is this. **A language publishes a set of named types, each optionally declaring a standard super type, and publishes nothing about values.** A consumer decides every value, and the host decides how a type reaches one: the theme's own rules, then the user's settings, then the host's defaults probed from scopes, and nothing at all when none of those match. Everything else the host knows about a token type — the id pattern, the rule-key grammar, the discard — is the host's business and is carried in the host's files.

What the contract already gets right, and this research confirms each of it: it names roles and never values; it keys every value by role and attribute and states the two attributes as a map, so a consumer can extend without reshaping a role; it makes a missing value an error rather than a fallback; and it states per role which mechanism can answer it, which is precisely what a consumer that cannot see the code needs to know before it can tell whether it is able to answer a role at all. The `implementedBy` split is the contract's strongest possession and no host mechanism is needed to hold it.

Four things it still lacks for the web-page and Markdown consumer, named concretely.
1. **A portable spelling.** The contract says the token type is "the role's own name, spelled as the contract spells the role", which is right for a server and impossible for a host whose rule keys are parsed at their first separator: thirteen of the twenty-one names carry one. The contract states no spelling a non-editor consumer can key a rule by, so two consumers will invent two, and a consumer that invents a second one produces a file that draws as though the server had said nothing.
2. **A statement that the scope names are one realization's, and which of them reach a host's own probes.** The contract's own `scopes` are this repository's grammar's names, and the handoff already records that "the roles are what port; the scope names are not portable" — yet they sit in the contract, where a portable consumer will read them as the contract's. The rule that decides it is short: a TextMate scope matches by prefix on its dot-separated segments, so a grammar's scope reaches a host's standard type only when it nests under the scope that type probes. Some of this grammar's do and some do not — `comment.line.double-slash.khayyam` nests under the `comment` type's probe, and `entity.name.class.khayyam` nests under nothing the `class` type probes, because that probe is `entity.name.type.class`. So a consumer that styles scopes alone, which is what a code-hosting page and most documentation engines do, gives part of the role list a colour and silently leaves the rest uncoloured, and nothing in the contract says which part or that the split exists.
3. **A statement that a root type's value is mandatory.** A role with a super type is styled by any theme that styles that standard type, whether or not it ever heard of Khayyam, and a role without one is styled by nothing except a rule keyed with its own name. The contract says a theme must value every role and does not say that a theme's value for a role is the *only* mechanism by which that role is ever styled, which is the fact a consumer needs before it decides whether a foreign theme must be extended at all.
4. **A reference value sheet, and a rule for a foreign theme.** The owner wants the colours taken "against the theme the reader chose", and on github.com or in a documentation engine the theme the reader chose is a theme that has never heard of Khayyam. The contract states the value a theme supplies and nothing about the value a consumer supplies when the reader's theme is not one of ours. The missing artifact is named, not chosen: a reference sheet in the contract's own key, plus a stated fallback order for a consumer whose theme knows nothing of Khayyam.

### F6 — Principles, with what each cost
1. **A consumer's mechanism is read out of the consumer, and out of its code where its documentation names a field but not a rule.** The merge is field-by-field with the semantic token supplying every field it has; a rule's key is parsed at its first separator and matched against a hierarchy built only from declared super types; a token that resolves to nothing is dropped from the line rather than left unstyled. *Cost:* three rounds in which the verifier was green, the extension was installed, and the reader saw no semantic colour at all, and the two rules that decide the outcome were not known until the bundle was read. The correction in F3 is the same cost once more: a conclusion was drawn from a reading of a function that had not been read closely enough to support it.
2. **A realization must not reshape the contract.** The contract names roles; a realization names its own legend entries, scopes, and diagnostic codes; a host that reads another form carries the translation in its own files. *Cost:* a language suffix welded into a legend entry, and a spelling that no rule could ever match, discovered only because a file drew as though nothing had been said.
3. **One mechanism per decision, and one decision per mechanism.** Kind is answered by a type, qualifiers by modifiers, values by a theme, and each of those by exactly one owner. *Cost:* a manifest carrying two settings axes, a pair of contributed themes, and no run of the editor that showed which of the three a reader sees; and a twenty-one-entry list that answered three questions in one column.
4. **A name published to be matched is published to a parser.** Any identifier a language hands to a host is subject to that host's grammar for such identifiers — here `^\w+[-_\w+]*$` for a type id, and a rule key split at its first separator — and the constraint is a property of the parser, not of the name. *Cost:* the discarded legend naming, and the absence of any portable spelling in the contract.
5. **Check what the reader sees, not what the checker reads.** A verifier proves that files agree; no run of it proves a colour reached a screen, and a token the host discarded leaves a line that looks grammatically coloured. *Cost:* an unmeasured light sheet, and an extension whose own log lines had to be marked as self-tests so that a working feature would not read as a broken one.
6. **A bridge between two mechanisms is the host's to publish, not yours to add.** The host publishes a scope probe for every standard type, which is the bridge the extension would have had to write for itself. *Cost:* a contribution that was written, measured, and removed.

## Open Questions
Each entry is a decision the evidence does not make.
1. **Does the language, not the display contract, want a standard-class statement?** A super type is a claim about what kind of thing a name is, which is a claim about the language, and the contract currently holds twenty-one such claims under an `origin` field that already marks which are the owner's and which are this toolchain's. Whether `docs/khayyam/` should say, of its own Type categories and its two variable declarations, which of them are kinds of which is not answered here.
2. **What is the portable spelling?** Either the contract names one spelling a non-editor consumer can key a rule by and the editor realization translates, as it already must for the separator, or the contract declares its own spelling authoritative and each stricter host is given an alias. This is a contract change and the owner's.
3. **Is `identifier-reference` a role?** Under a standard classification it is not a kind of name; it is a statement about the resolver's reach, which is what `display.json`'s own `note` on it half-says. Whether it stays a root type or moves out of the role list into the profile section — where the TextMate profile's collapse of every use site already puts it in effect — is the owner's.
4. **Where do the two `invalid-*` roles belong?** The host's classification has no diagnostic class, and the host's own answer to a form the language refuses is a diagnostic plus a grammar scope. Whether the contract holds these as roles at all is unasked.
5. **What does declaring a super type do to a theme's own schema?** The registration gives the token-styling schema a property for the type, so a theme that names a super type is validated by the host. No editor was run against this extension's manifest, and no theme in this repository has been checked against that validation.

## Related Artifacts
- [display.json](./display.json) — the contract. F4's table is the mapping its `roles` and `profiles.lsp.alignment` lack; F5's four gaps are about it, and none of them is answered here.
- [display.md](./display.md) — the contract in prose, including the passage that states the token type is the role's own name spelled as the contract spells it; F5 item 1 is the consumer that spelling cannot reach.
- [display.handoff.md](./display.handoff.md) — where this record's open questions graduate on review, and the home of the decision F3 corrects the stated reason of without changing.
- [display.research.001.md](./display.research.001.md) — the palette inquiry, `Active`, and unopened by this record; its F2 grouping by reader question is the grouping F4 explains.
- [contract.ts](../lsp/src/contract.ts) — the legend the server advertises, one entry per role, the spelling F5 item 1 concerns.
- [package.json](../../../.agents/vscode/extensions/khayyam-language/package.json) — the manifest, which declares no `contributes.semanticTokenTypes`; F2 is what that omission costs.
- [khayyam.tmLanguage.json](../../../.agents/vscode/extensions/khayyam-language/syntaxes/khayyam.tmLanguage.json) — the scope names F5 item 2 measures against the host's probes.
- VS Code 1.139.1, `resources/app/out/vs/workbench/workbench.desktop.main.js` — the product every finding was read out of: `function T4n()`, `registerTokenType`, `getTypeHierarchy`, `parseTokenSelector`, `N2t`, `getTokenStyle`, `getTokenStyleMetadata`, `W2t`, `SemanticTokensProviderStyling.getMetadata`. Descriptions and schema strings are in `resources/app/out/nls.messages.js` at the indices given in F1 and F2.
- `resources/app/out/vscode-dts/vscode.d.ts` — `SemanticTokensLegend` (4253) and `DocumentSemanticTokensProvider` (4396), the host's own account of what a provider hands over and how it is encoded.
- Language Server Protocol specifications 3.17 and 3.18, the Semantic Tokens feature: the `SemanticTokenTypes` and `SemanticTokenModifiers` enums in "General Concepts", and `SemanticTokensClientCapabilities.tokenTypes` — "The token types that the client supports" — which is where a server announces a type the client did not name. *Relation: Reference*; the host's own list in F1 is the one that governs, and it is not this list.
- [Documentation — Research](../../../docs/documentation-research.md) and [Documentation — Practice](../../../docs/documentation.practice.md) — the practice that put this record in this file rather than in a note of an invented kind.

## Notes
- The five collisions between role names and the host's standard types — `keyword`, `method`, `variable`, `comment`, `string` — were reached without a decision, and are recorded here as a fact about the list rather than as a design. Whether a role should keep a name the host already uses is part of open question 2.
- The host's composite default selectors include `*.defaultLibrary`, which is the one place its own classification comes near the question "where did this name come from". It is a style override rather than a class, so a role that wants origin on this host has no type and no modifier to put it in. That is a fact about the host, not a proposal.
- Nothing here states that any colour is right. The palette is the theme's, F1–F3 make no claim about any value, and F4's hue sentence is the owner's already-stated ruling, recorded because a derivation from a classification would satisfy it and a free choice over a re-derived list would not.
