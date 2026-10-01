# Khayyam Display Research 001 — A colour spectrum the reader can check

## Table of contents
- [Status](#status)
- [Question and Goals](#question-and-goals)
- [Participants](#participants)
- [Methodology](#methodology)
- [Findings](#findings)
  - [F1 — How the two mechanisms actually merge, read out of the editor's own product](#f1--how-the-two-mechanisms-actually-merge-read-out-of-the-editors-own-product)
  - [F2 — The twenty roles fall into eight classes](#f2--the-twenty-roles-fall-into-eight-classes)
  - [F3 — A proposed value per role, per theme, with its measured contrast](#f3--a-proposed-value-per-role-per-theme-with-its-measured-contrast)
  - [F4 — Colour-vision deficiency: what collapses, and what does not](#f4--colour-vision-deficiency-what-collapses-and-what-does-not)
  - [F5 — Which side owns each position, keyed to the grammar's own rules](#f5--which-side-owns-each-position-keyed-to-the-grammars-own-rules)
  - [F6 — What the file looks like with no server running](#f6--what-the-file-looks-like-with-no-server-running)
  - [F7 — What the verification script must gain](#f7--what-the-verification-script-must-gain)
- [Open Questions](#open-questions)
- [Related Artifacts](#related-artifacts)
- [Notes](#notes)

## Status
Active

## Question and Goals
### Questions
1. What colour classes do the twenty roles of [`display.json`](./display.json) fall into, and why is each one a class? — **Answered**
2. What value does each role take in a dark and in a light theme, with its contrast against that theme's own background measured? — **Answered**
3. Which class pairs become indistinguishable under a colour-vision deficiency, and what separates them if not hue? — **Answered**
4. Which positions must the grammar stop colouring, keyed to the grammar's own rules, so that a position is owned by exactly one side? — **Answered**, with a correction to the premise the question was opened on (F1)
5. What must [`verify-roles.mjs`](../../../.agents/vscode/extensions/khayyam-language/scripts/verify-roles.mjs) gain for the spectrum to hold rather than merely exist? — **Answered**
6. Can the owner's requirement that the spectrum hold in both modes be met exactly? — **Open**; it cannot, and the two resolutions with their costs are the owner's to choose ([Open Questions](#open-questions) Q1)

### Goals
1. Give the owner a spectrum he can check rather than admire: every value measured, every rule stated as a condition a check can fail. — **Met**
2. Discharge the owner's three rulings — warm colours reserved for errors and warnings, no purple pair for keywords and method identifiers, several distinct classes rather than a spread of near-identical hues — as rules, not as taste. — **Met**
3. Say which side of the two mechanisms owns each position, and say honestly what the file looks like with no server answering. — **Met**
4. Route the decisions the design cannot make for him. — **Met**

### Scope
The twenty roles, the two shipped theme files, the shipped TextMate grammar, the language server's semantic layer, and the editor's merge of a grammar token with a semantic token. It proposes values and conditions; it changes no contract, no theme, no grammar, no server, and no verification script. It does not answer whether a code-hosting page can be given a resolver, and it does not revisit the light theme's failure to reach the editor ([display.handoff.md → The gap](./display.handoff.md#what-unfinished-is-the-realization-not-the-contract)).

## Participants
- [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — **Questioner**, **Goal-setter**; review outcome: **Not yet reviewed**.
- [Space Bunny Alpha](../../CONTRIBUTORS.md#space-bunny-alpha) (space-bunny via [OpenCode](../../CONTRIBUTORS.md#opencode)) — **Researcher**.

## Methodology
1. Read the four artifacts the design is judged against: the contract and its prose, both theme files, the grammar, and the verification script, and read the language server's semantic layer for what it emits at each position.
2. Read the merge out of the editor the reader actually has, rather than from a description of it. The installed product is VS Code 1.139.1; the merge is `TokenStore.prototype.addSparseTokens` in `out/vs/workbench/workbench.desktop.main.js`, and the bit tests are legible there in the minified form (F1). The field each tested bit belongs to was read from the `TokenMetadata` accessors in the same bundle and from the semantic styling class that sets those bits.
3. Built every value in OKLCH, converted to sRGB, and refused any value outside the sRGB gamut before measuring it. Clipping is a defect in a value sheet: a theme states a hex triple, and a clipped one is not the colour that was designed.
4. Measured contrast with the WCAG 2.x relative-luminance definition against each theme file's own `editor.background`, which is `#1F1F1F` for `khayyam-dark.json` and `#FFFFFF` for `khayyam-light.json`.
5. Estimated colour-vision deficiency by simulating protanopia, deuteranopia and tritanopia with the Machado, Oliveira and Fernandes (2009) matrices at severity 1.0, applied in linear RGB, and measuring the result in CIE L\*a\*b\* (D65) as ΔE76. **This is an estimate, not a measurement of a reader's vision**: it is a two-degree-simulator arithmetic on a matrix published for a 100% severity case, and the ΔE76 thresholds quoted below (10 for "close", 25 for "clear") are conventions this record adopts, not standards. The contrast ratios and the gamut checks are exact for the values stated.
6. The whole computation is one script, kept outside the repository, reading nothing from it. Every number below is reproducible from the OKLCH triples in F3 with the five steps above.

Limits: no editor was run, so nothing here claims what the editor draws; the CVD figures are estimates of what a reader perceives, not measurements of it; the design is one proposal, and the owner may take a different one and keep the conditions in F7.

## Findings
### F1 — How the two mechanisms actually merge, read out of the editor's own product
The two mechanisms do not both own a character. In the installed editor, the grammar's tokens are written into the model's token store first, and each semantic token is then merged into that store by `addSparseTokens`, which builds a mask from the **semantic** token's own metadata and takes the masked bits from it and the rest from the **grammar**:

```js
let b = lineTokens.getMetadata(g);
let S = ((b&1?2048:0)|(b&2?4096:0)|(b&4?8192:0)|(b&8?16384:0)|(b&16?16744448:0)|(b&32?4278190080:0))>>>0,
    y = ~S>>>0;
... merged = grammarMetadata & y | semanticMetadata & S
```

Read against the `TokenMetadata` accessors in the same bundle, the semantic token's low six bits mean: bit 0 italic is present, bit 1 bold, bit 2 underline, bit 3 strikethrough, bit 4 **a foreground is present**, bit 5 a background — and the same bundle's semantic styling class sets exactly those bits, setting bit 4 whenever it resolves a foreground and setting the whole value to `2147483647` when it resolves none.

Two consequences, and the second is the one this research was opened to settle:

1. **The direction is the reverse of the premise the question was opened on.** A semantic token wins every field it supplies, and the grammar supplies the rest. Where a semantic token's styling rule names no colour for its type, the editor gives it the `2147483647` sentinel, which still sets bit 4, so it still overrides the grammar — that is the "no style, do not draw" path, not a silent fall-through to the grammar.
2. **The design rule is the same under either direction, and only the bill changes.** For each position, exactly one side may own the colour. Under the premise as stated, the side that must stop claiming is the **grammar**; under the product as read, the side that must stop claiming is the **server** at the positions the grammar is already right about, and the grammar's claim at a position the server resolves is a fiction that only happens to be overridden.

F5 states ownership under the product as read, and also marks every position where the premise's version would make the grammar yield, so the owner can rule on either.

### F2 — The twenty roles fall into eight classes
A class is a question the reader is asking, and colour answers it. Eight questions are being asked about a line of Khayyam, and the twenty roles are their answers.

1. **A reserved word** — `keyword`, `subtype`. `tp`, `vr`, and the five subtype keywords are the language's own vocabulary; there is no name behind them and nothing to resolve. One value, because a reader identifies these by their fixed place in a line and by being two or three characters long, not by hue. This is the class the owner's ruling about two purples reaches: it is a green, not a violet, and it is not the pale half of a pair.
2. **A Type** — `capsule`, `abstraction`, `method`, `scope`, `type-reference`, `method-argument-type`, `method-owner-type`. Seven roles, one value, because the language states Type as one concept with four categories and the subtype keyword on the same line already names which one, and because four hues in one family is the spread of near-identical hues the owner refused. The cost is named in Q3. The method role is here, and this value is a blue, not a violet, so the second half of the ruling is discharged too.
3. **A name that arrived from another file** — `included-type`, `included-variable`. This is a class because the reader's question is *where did this come from*, and because the contract's `fontStyleChannel` already gives this exact question the italic. Hue says "not mine"; italic says "not from here". Both roles share it: the reader does not need to know whether a borrowed name is a type or a variable before reading the sentence around it.
4. **A name this file owns** — `variable`, `capsule-field`. A field and a `vr` name are both declared here, and both are the reader's own. Shared, with the cost named in Q3.
5. **A parameter** — `method-argument`. A class of one, and it earns it: a parameter's lifetime is one signature, it arrives from the caller, and it is the one name a reader scans a signature for. Hue shared with class 4, so that the family of "names" stays a family; separated by bold and by the largest lightness step in the ordinary set.
6. **A use the file cannot resolve** — `identifier-reference`. The negative class, and the reason it must exist: without it a use site reads as a declaration, and a reader is told that a name from another file is this file's own. It is drawn as a cool low-chroma grey — cooler and dimmer than ordinary text, more present than a comment — so the mechanism saying "unknown here" is visible as a distinct state.
7. **Text that is not a name** — `comment`, `file-uri`, `string`. Not an identity at all: prose the author marked as not code, a path an inclusion routes to, and a reserved quoted literal. A four-step grey ladder, so the lane recedes and the three never compete with a class that is.
8. **A form the language does not admit** — `invalid-number`, `invalid-operator`. The only class the owner's ruling permits a warm colour to, and the only class that uses one: a red for the bare number, an amber for the operator character.

A reader can tell a parameter from a local from an imported name without a table: the parameter is bold and the lightest thing on a dark background (the darkest on a light one), the imported name is italic and cyan, and the local is plain green — three different physical differences, not three shades of one.

### F3 — A proposed value per role, per theme, with its measured contrast
The grid is a lookup, not a rule; the rules it satisfies are stated in F7.

| Role | Class | Dark | Ratio | L\* | Light | Ratio | L\* |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `keyword` | 1 | `#8CC05E` | 7.71 | 72.3 | `#51811A` | 4.66 | 48.9 |
| `subtype` | 1 | `#8CC05E` | 7.71 | 72.3 | `#51811A` | 4.66 | 48.9 |
| `capsule` | 2 | `#63B0FC` | 7.18 | 70.0 | `#005BAF` | 6.74 | 38.9 |
| `abstraction` | 2 | `#63B0FC` | 7.18 | 70.0 | `#005BAF` | 6.74 | 38.9 |
| `method` | 2 | `#63B0FC` | 7.18 | 70.0 | `#005BAF` | 6.74 | 38.9 |
| `scope` | 2 | `#63B0FC` | 7.18 | 70.0 | `#005BAF` | 6.74 | 38.9 |
| `type-reference` | 2 | `#63B0FC` | 7.18 | 70.0 | `#005BAF` | 6.74 | 38.9 |
| `method-argument-type` | 2 | `#63B0FC` | 7.18 | 70.0 | `#005BAF` | 6.74 | 38.9 |
| `method-owner-type` | 2 | `#63B0FC` | 7.18 | 70.0 | `#005BAF` | 6.74 | 38.9 |
| `included-type` | 3 | `#46CCDA` italic | 8.56 | 75.8 | `#007686` italic | 5.34 | 45.2 |
| `included-variable` | 3 | `#46CCDA` italic | 8.56 | 75.8 | `#007686` italic | 5.34 | 45.2 |
| `variable` | 4 | `#59AD73` | 6.00 | 64.4 | `#00662B` | 7.15 | 37.3 |
| `capsule-field` | 4 | `#59AD73` | 6.00 | 64.4 | `#00662B` | 7.15 | 37.3 |
| `method-argument` | 5 | `#ACF2BE` bold | 12.71 | 89.9 | `#003702` bold | 13.57 | 19.0 |
| `identifier-reference` | 6 | `#7A999C` | 5.39 | 61.1 | `#264346` | 10.64 | 26.4 |
| `comment` | 7 | `#687686` | 3.55 | 49.0 | `#515F6E` | 6.54 | 39.7 |
| `file-uri` | 7 | `#A0B0C1` | 7.44 | 71.1 | `#2C3947` | 11.78 | 23.4 |
| `string` | 7 | `#B6C6D7` | 9.46 | 79.2 | `#1D2A37` | 14.60 | 16.5 |
| `invalid-number` | 8 | `#ED5350` | 4.67 | 56.9 | `#9B0007` | 8.76 | 31.8 |
| `invalid-operator` | 8 | `#FEB98B` | 9.83 | 80.5 | `#925019` | 6.21 | 41.1 |

Every value is inside the sRGB gamut. Every value meets or exceeds 4.5:1 against its own background, with one exception: `comment` in the dark theme is 3.55:1. That is deliberate and is put to the owner as Q5 — a comment is the one role that must recede, and the current shipped dark comment is 3.15:1, so this proposal is already an improvement on it.

Three of the shipped values are warm on an ordinary role and are wrong by the owner's ruling, not by taste: `included-type` `#f6c531` is a yellow, `included-variable` `#eca683` is an orange, and `file-uri` `#a5b87a` is a yellow-green. In the proposal all three are out of the warm band, and the band is occupied by class 8 alone. The pale and saturated purples the owner named — `#bf9ddd` on `method-owner-type` and `#9b77ee` on `method-argument` in the dark theme, `#5f2c8c` and `#4213ae` in the light one — are gone: `method-owner-type` joins the Type blue and `method-argument` becomes a pale green. The pair that most resembles the one the owner objected to, the two greens `#52cbb3`/`#56bdd2`/`#6ed891`/`#46a4a1` on the four declared Type categories, is exactly the near-identical spread he refused, and it is one value.

### F4 — Colour-vision deficiency: what collapses, and what does not
Deuteranopia and protanopia remove the red–green axis; tritanopia removes the blue–yellow one. This spectrum puts its three name classes — the reserved word, the file's own name, and the parameter — in the red–green band, and its Type class and the two imported-name lanes in the blue–cyan band, so it is built to survive the first pair and to lean on lightness for the second.

Measured, on the dark theme, every class pair stays at ΔE76 ≥ 10 under all three simulations except one: the reserved word against `invalid-number` reaches 10.2 under deuteranopia. Measured on the light theme three pairs fall below 10, and each is separated by something that is not hue:

1. `method-argument` against class 8, protanopia, ΔE76 4.0. A dark green and a dark red converge. What separates them: the parameter is **bold**, and a bare number is a form the language does not admit at all, so the two never both appear in a well-formed file. This is the weakest pair in the spectrum and it is stated as weak.
2. `included-*` against `comment`, protanopia, ΔE76 8.1. Separated by **italic**, and by the fact that one is an identifier inside a declaration and the other is a `//` or `/* */` region.
3. `method-argument` against `identifier-reference`, tritanopia, ΔE76 9.2. Separated by **bold** and by a 7.4 L\* step.

The structure that makes the owner's requirement checkable is a rule, not a palette: **two classes in the same lightness band must differ by at least 35° of hue, and if they do not, they must differ by at least 15 L\*.** The two purples he refused fail that rule by construction — two purples at the same lightness are the canonical case — which is why the ruling is discharged by the rule and not by two separate rulings about two specific roles.

### F5 — Which side owns each position, keyed to the grammar's own rules
Ownership under the product as read (F1): the server owns every position it emits a role for, and the grammar owns every position the scanner does not hand the server. Read from [`core/src/scan.ts`](../core/src/scan.ts), the scanner emits no token at all for a comment, and a character that is neither a letter, a quote, nor one of `{}().,;` is refused as `unexpected-character` and **takes the rest of its line with it**. So the server is silent over comments, over bare numbers, over operator characters, and over everything after one on that line, and the grammar is the only thing that colours those.

The grammar-owned positions, which need no change:
1. `repository.comments` — both forms. Role `comment`.
2. `repository.illegal-numbers` and `repository.illegal-operators` — and, because the scanner stops the line, the whole rest of the line after such a character. Roles `invalid-number` and `invalid-operator`.
3. The receiver slot in `(self {owner})` between the first parenthesis and the owner type: the server deliberately says nothing about it, so the grammar's `identifiers` claim is the only claim.
4. Every position where the two agree, which the verifier already proves by spelling: the keywords and subtype keywords, a declaration's own name, the name at an `in` inclusion and its path, a `vr` name, a capsule field name, a `.name(` call, a `vr` and a `cp`/`ab` block's type that this file does not bind, and a `string` in a body.

The contested positions, where the grammar currently claims a role and the server answers a different one. Each is keyed to the rule that claims it, and each is a position where the server is right, because a role follows the binding and not the position:
5. `repository.identifiers` — the catch-all `\b[\p{L}_][\p{L}\p{Nd}_]*\b` over `variable.other.reference.khayyam`. **Every use site in the file.** This is the single largest contested position and the one the owner observed. The grammar's claim is right only where the file binds nothing; everywhere else it is the negative class standing where a positive one belongs.
6. `repository.method-declaration`, capture 4, `entity.name.type.owner.khayyam`. The server resolves the owner name to the role of what it is bound to, and answers `method-owner-type` only for a name this file does not bind.
7. `repository.method-declaration`, captures 6, 8, 10, 12, 14, 16, 18 and 20, `entity.name.type.parameter.khayyam`. The same shape, for each argument's declared type. The server resolves it the same way it resolves the owner.
8. `repository.method-declaration`, the pairs its pattern leaves uncaptured. A fifth and later pair in a group falls through to `identifiers` and takes `identifier-reference`; the server walks the groups as they stand and answers `method-argument` for as many parameters as the source writes. Already open in [display.handoff.md → Method-signature groups](./display.handoff.md#method-signature-groups-the-grammar-caps-at-four-pairs-the-server-takes-any-number); it is listed here because it is a contested position, not because it is new.
9. `repository.variable-declaration` capture 3, and the two block rules of `repository.capsule-declaration` and `repository.abstraction-declaration`, all three emitting `entity.name.type.khayyam`. The server resolves each to the role of the bound type, answering `type-reference` only for a name this file does not bind.
10. `repository.method-call` — its pattern requires a leading dot, so a bare `name(` in a body is `identifier-reference` to the grammar and `method` to the server.

Under the premise as stated in the question the bill is the other way round: the grammar must drop items 5 to 10, `identifier-reference` then has no emitter at all, and `verify-roles.mjs` fails its "role not implemented" check while the contract's conformance rule reads that a realization which never emits a role has abandoned it. That is the whole of the tension, and it is Q1.

### F6 — What the file looks like with no server running
Honestly: with the grammar alone, every class the syntax determines keeps its own colour, and every class that depends on knowing what a name binds collapses into one.

What survives, because the syntax determines it: the reserved words, the subtype keywords, the name at every `tp` and `vr` declaration and the category the subtype keyword names, the name and the path of an `in` inclusion, a `vr` name, a capsule's field names and the abstraction names in a composition block, the first four argument names and their types in each method group, a `.name(` call, a comment, and every bare number and operator character — the last two in the warm band, which is the one place a reader is told the file is wrong.

What collapses: every use site. A `vr` name reads as a declaration, a parameter reads as a plain word in the body, a name brought in by `in` reads as a plain word at its use, and a type named in a signature reads as a plain word. So `tp Error in "…"` shows the cyan italic, and every `Error` below it shows the cool grey of class 6 — the reader is told the file brought a name in and then not told anything about where it is used. The file reads as well-formed code with a great deal of its origin and scope information missing, and it says so, which is the point: class 6 exists so that a use site never reads as a declaration.

That is the cost of the TextMate profile, and it is the honest answer to the owner's requirement. The spectrum itself does hold in both modes — every value drawn with no server running is a value from the same twenty-pair sheet, and the classes that survive are drawn in their own class's colour — but the parameter/local/imported distinction does not, because no TextMate grammar can make it. See Q1.

### F7 — What the verification script must gain
`verify-roles.mjs` today proves that the three files agree. It does not prove that the values are usable, and nothing in the tree would fail if every value were replaced by a near-identical one. Stated as conditions, so a reader can check them and a later session can implement them:

1. Every value is a six-digit hex triple whose sRGB components are all in range, and every theme's own `editor.background` is read from that theme file rather than assumed.
2. Every role's value meets or exceeds 4.5:1 against its own theme's background, except a role the contract names as one that must recede, which has a floor of 3:1 stated in the contract rather than in the check.
3. No two roles in different classes whose `fontStyle` values are equal are within 15° of hue and 12 L\* of one another in the dark theme, and the same condition holds in the light theme. This is the generalized form of the owner's ruling about two purples.
4. No value for a role outside the class the contract names as the diagnostic one falls in the reserved warm band, and every value that does fall in it belongs to that class.
5. Every class pair in a theme is at least ΔE76 10 apart under each of the three dichromacy simulations the check names, **unless** the pair's roles differ in `fontStyle` or the check records the pair and the reason. A pair that fails silently is the defect; a pair that fails with a stated reason is a decision.
6. Every position the contract lists as server-owned is checked against a fixture: for each character range the server reports, the range is a position the contract lists as server-owned, or the server's role equals the grammar's role for those characters. This is the check that makes F5 an enforceable claim rather than a document, and it needs the ownership list to live in `display.json` so that the contract and the check read one thing.
7. The check reports, in its own output, that the contributed `package.json` values are one theme's and which one, so the light theme's forty pairs being rendered by nothing stays a stated fact rather than a discovery.

## Open Questions
Each entry is a decision the design cannot make for the owner, with the choice and its cost. They graduate to [display.handoff.md](./display.handoff.md) when this research completes, which is on the owner's review.

- **Q1 — Can the spectrum hold in both modes?** No, and it is not a colour question. Under the product as read, the server's colour lands wherever the server answers and the grammar's is used elsewhere, so the two modes are both correct; under the premise as stated, the grammar wins and the server's answers are discarded wherever the theme gives the grammar a foreground, which is the failure the owner saw. Two resolutions, and the second costs the contract:
  1. **Declare ownership and let the merge decide.** The contract gains the F5 list; the grammar keeps every scope, so every role stays implemented and `verify-roles.mjs` keeps passing unchanged; the theme supplies one value per role, so both mechanisms draw from one sheet. **Cost:** at a contested position the colour a reader sees depends on the host's merge rather than on the contract, and a TextMate-only consumer — a code-hosting page — shows the grammar's answer, which is class 6 for every use. This is the design the contract already describes and the one this proposal assumes.
  2. **Make the grammar yield at contested positions.** The ten positions in F5 stop emitting their scopes, those characters fall to the default foreground, and the editor's merge stops mattering. **Cost:** `identifier-reference` has no emitter, so the contract's conformance rule and the verifier's "role not implemented" check both need an exception for server-owned positions, and a code-hosting page then shows a file whose every use is uncoloured — a worse picture for the consumer the contract most clearly owes, since it claims the same roles govern a rendered page.
- **Q2 — Does `variable` split?** The owner named three variable classes: imported, file-level, and method-local. The contract has one `variable` role, stated to cover a `vr` at file level **or in a method body**, so a method-local variable and a file-level one are the same role by the contract's own words. The proposal gives them one value. **Choice:** leave it, and a reader cannot tell a method's own local from a file-level variable; or add a role for a block-local variable, which is a contract change — and the contract says a new display distinction is added as a role there first, never smuggled in through a grammar or a theme. **Cost of the second:** one more class, one more value, one more check, and a re-run of the class-separation measurement in F4, where the red–green band is already the tightest part of the spectrum.
- **Q3 — Are the four declared Type categories and the field one value or several?** The proposal gives `capsule`, `abstraction`, `method`, `scope`, `type-reference`, `method-argument-type` and `method-owner-type` one value, and `capsule-field` the same value as `variable`. **Choice:** one value each, and the reader learns a Type's category from the subtype keyword beside it, which is the position that states it; or four hues in one blue family, which is the near-identical spread the owner refused, or a hue for the field, which costs one more class in the tightest band. **Cost of one value:** a reader scanning a call site sees a method's name in the same colour as a Capsule's, and the only thing that separates them is the dot.
- **Q4 — `included-type` and `included-variable` share one value.** The contract's `fontStyleChannel` gives italic to both, so the origin question is answered by the style, and the hue is free to say "a name from elsewhere". **Choice:** share, and a reader cannot tell a borrowed Type from a borrowed Variable without reading the line; or split, and spend a hue. **Cost of splitting:** one more class in the blue–cyan band, where tritanopia is already the binding constraint.
- **Q5 — Is the dark comment below 4.5:1?** The proposal puts it at 3.55:1, and the shipped one is 3.15:1. **Choice:** hold 4.5:1 for every role including the comment, which needs a lighter comment and eats one lightness step of the four-step grey lane; or keep a floor of 3:1 for the one role that must recede, stated in the contract so that F7's condition 2 can name it rather than exempt it ad hoc. **Cost of holding 4.5:1 everywhere:** `identifier-reference` and `comment` come within about 5 L\* of each other in the dark theme, and the pair that must be told apart — a name the file cannot resolve, and text that is not code — becomes the spectrum's weakest pair in the band where hue helps least.
- **Q6 — Which side's reading of the merge is the design premise?** F1 read the product and found the semantic token winning. If the owner rules that the premise as stated is the one to design inside, F5's contested list is unchanged in membership but inverted in obligation, and Q1 resolves the other way. **Cost of ruling the other way:** the design is correct only on a host whose merge matches the premise, and this host's does not.

## Related Artifacts
- [display.json](./display.json) — the twenty roles, the attributes, and where the ownership list in F5 would have to live for F7's condition 6 to read one thing.
- [display.md](./display.md) — the contract in prose; the place a settled F2 or F5 graduates into, and where the class list becomes part of what a consumer is told.
- [display.handoff.md](./display.handoff.md) — carries Q1 to Q6 on completion, and carries the open gap this research does not touch: the light theme's forty pairs are valued and rendered by nothing.
- [khayyam-dark.json](../../../.agents/vscode/extensions/khayyam-language/themes/khayyam-dark.json), [khayyam-light.json](../../../.agents/vscode/extensions/khayyam-language/themes/khayyam-light.json) — the values in F3 replace these, and `package.json`'s contributed rules duplicate the dark sheet.
- [khayyam.tmLanguage.json](../../../.agents/vscode/extensions/khayyam-language/syntaxes/khayyam.tmLanguage.json) — the rules named in F5.
- [verify-roles.mjs](../../../.agents/vscode/extensions/khayyam-language/scripts/verify-roles.mjs) — what F7 would add to it.
- [semantic.ts](../lsp/src/semantic.ts), [scan.ts](../core/src/scan.ts) — what the server emits, and what the scanner hands it.
- [Documentation — Practice](../../docs/documentation.practice.md) → Results and companions, and [Documentation — Research](../../docs/documentation-research.md) — the routing that put this record in this file rather than in a note of an invented kind.
- VS Code 1.139.1, `out/vs/workbench/workbench.desktop.main.js` — the product F1 was read out of.

## Notes
- The twenty roles are unchanged by this record: it names no new role and revises no existing one. Q2 is the one place where a role would be added, and that is the owner's ruling and a contract change.
- The `fontStyle` channel keeps the meaning [`display.json`](./display.json) → `fontStyleChannel` gives it: italic for a name that entered from another file, bold for a name that entered from outside the method it appears in, empty for the other eighteen. The proposal uses no third style, so a theme that reads the channel differently is a theme choice the contract already permits.
- F2's "eight classes" is a statement about the reader's questions, not about the contract's role list. Two roles are in one class in this proposal and three decisions (Q3, Q4, and `included-*`) are what would split them; the contract permits two roles to share a value, and a theme that gives each its own is still conformant.
- The three warm values the current sheets put on ordinary roles — the yellow `included-type`, the orange `included-variable`, the yellow-green `file-uri` — are called out in F3 because the owner's ruling reaches them and the ruling is not this record's to relax. The proposal's answer is to move all three out of the warm band, not to argue that a yellow path is harmless.
- No editor was run. Every statement about the merge is read out of the installed product's own bundle and cited to the function it was read from; every statement about contrast and gamut is computed from the values in F3; every statement about what a reader perceives is an estimate and is labelled one.
