---
ID: 20261030-T051847Z-13004
Title: Critique how a type's human-facing text is written in code (detail.kh), now that comments are banned, and settle its worked signature
Status: Complete
---
# Report
The critique is written. The check is met: findings are tied to passages and the decisions fit in 10 lines. The worked signature is not settled, because it turns on owner rulings (D3 to D7); this report gives the candidates and one recommendation. Nothing was edited: no change to `detail.kh` or to a language document. Proposed changes are listed under `Left open`, to be written into the handoffs once the owner answers.

## What ran
Read whole in this context: `modules/computer/type/protocol/detail.kh` (the working copy, which differs from the committed one by 13 deleted comment lines in the Go residue; who made that edit was not checked); [No Comments in Code](/modules/computer/type/rules/no-comments-in-code/no-comments-in-code.md); `bundles/khayyam/rules/comment-policy/comment-policy.md` with its handoff and the last changelog record; `modules/knowledge/label/label.md`. Read by section: Khayyam → Self-Documenting Code and Naming, and the handoff entry "Which method returns human-facing text, and on which owner?"; `docs/type.md#human-facing-identity`; `modules/computer/type/type.md` → Type details and human-facing identity; the type handoff entry "Companion artifacts per language, or a method per language?"; Documentation → A Fact in Code Is Written Once; the Text handoff's rulings of 2026-10-24. Read from earlier tasks, as claims and not as decisions: the report of 20261013-T160504Z-20140 (a language file per human language) and of 20261014-T113225Z-24048 (a `Text` abstraction and the quoted text body), both ended Blocked on the owner.
Measured with grep on 2026-10-30: 112 tracked `*.locale.*.kh` files; 41 `TAGS()` implementations, 37 returning `[]string{}` and 4 returning `nil`, none returning a tag; 41 `Summary()` implementations, 8 of them returning `""` on one line.
Not read, so not relied on: the roughly 390 ported comment blocks (the plan's figure, not re-counted); the `Labels` field and its Python declarations beyond what `label.md` says of them; the authorization domain; Documentation's other facets.
No second reader. A different model should review before the owner relies on F2 and F3.

## Check
Met as the plan words it. The report separates what holds from what does not, ties each finding to a passage, and keeps `Decisions needed` to 7 lines.

## Result

### Understanding
`Details` composes `Quiddity` and requires five methods, each `mt (self Details) () (s String)`: `Domain`, `Summary`, `Overview` (about the Type, read with no occurrence at hand) and `UserActionNote`, `DevActionNote` (about an occurrence, read by whoever meets it). The ban says a type's text is said by these methods; Khayyam says another language is another method; Type says the text lives in a companion file per language, never inline. The signature (which method, on which owner, how a locale is named) is open in the Khayyam handoff. Go residue holds a sixth method, `TAGS() []string`.

### What holds
- **S1. The type owns its text, once.** Khayyam → Self-Documenting Code and Naming, Type → Human-facing identity and Documentation → A Fact in Code Is Written Once agree: a description of a code fact is the type's, a document names the code and never retypes it. The ban follows from them. Not challenged.
- **S2. The split between the type's own text and an occurrence's text is real.** `detail.kh:13-18` gives the reason (a manager listing types reads another text than a user facing an error), and the audiences differ.
- **S3. No string-keyed translation map.** Type → Human-facing identity gives a reason (drift), not a taste. Not challenged.
- **S4. The ban can stand before the signature**, as the plan says: the five methods exist as a contract, so a rule that says "the methods" is not empty. It is weaker than it reads (F1).

### What does not hold
- **F1. The ban has nothing live to point at.** The five methods have no Khayyam implementation: all 41 `Summary()` bodies sit inside `TODO(go-migrate)` comment blocks, and the earlier task 24048 found none either. The rule's "every type follows them" therefore has no example to follow, and a changed file that loses its comment loses its only prose. That is the reason the owner gave on 2026-09-26 for keeping the fallback (comment-policy handoff, Decisions), and the 2026-10-30 changelog record removes the fallback without saying what became of that reason. Until the signature exists, "repair when a task changes the file" is a removal of information with no destination; Documentation holds that removal, not recording, is what needs care.
- **F2. The contract breaks its own ban, and cannot be fixed the way the ban says.** `detail.kh:6-41`: 23 of the 41 lines of the live contract are `//` lines, including the definition of each of the five methods. By the ban those are the type's own text. But `Details` is an abstraction (`ab`), and task 24048 (a proposal, not accepted) holds that an abstraction has no bodies, so it cannot carry a method that returns text. If that holds, the text of every abstraction, which is where most ported comment blocks sit, has no home in the five methods. This is the weakest-supported but largest finding: it turns on a claim about abstractions that no accepted document states. Unverified.
- **F3. Three statements of how a locale is named disagree, and the ban breaks no tie.**
  - Khayyam: another language is another method on the type. This makes the language set part of the contract: an abstraction requiring `SummaryFa` forces every type to be written in Persian, and a new language changes every type. A contract that grows with the set of languages is not closed.
  - Type: a companion file per language, `<base>.<lang>`, never inline.
  - Task 20140 (Blocked): one method taking a language value, with the files supplying the text. Better on the first point, but it finds the files "by path alone" with "no registry". A dependency that exists only by file-name convention is a hidden edge, against the rule that verification scope equals source scope (type handoff, Anticipated Work).
  - Task 24048, Candidate A, has `locale.eng.kh` and `locale.per.kh` each declare the same method `Summary` on the same owner. Two declarations of one signature need something that picks one, which is the Go build tag that 20140 rejected for run time.
  None of the four is both closed in languages and explicit in its edge. Nothing in the repository settles it.
- **F4. `Details` mixes two subjects, and the second is not every type's.** `UserActionNote` and `DevActionNote` are meaningful for an occurrence, "typically an Error" (`detail.kh:15`). The ban makes all five obligatory for every type, so `W32` must answer what a user should do when facing it. The residue shows the result: the time `epoch` files return `""` for both notes. An empty string says "no text" and "text that is empty" alike (task 20140, item 5, keeps them apart). By the Modeling rule of independent responsibilities and lifecycles, the occurrence notes are a second abstraction composed by Error-like types, not a part of every Type's details. Confidence: moderate.
- **F5. The result type is `String`, which is the wrong thing and unsettled.** A fixed text is a constant (Encapsulation → Constants as Capsule-Returned Values), and `String` is the changeable container. The Text handoff (2026-10-24) rules that a text always comes with its structure and that markup is annotation on spans, so an `Overview` of "multi line text" in a plain value contradicts it. Task 24048 proposes `Text` and it is Blocked. A signature chosen before this is settled is chosen twice.
- **F6. `type.md` and `detail.kh` list different things.** `type.md` names three groups of detail: about the Type, about an occurrence, and the Type's own record (documentation address, issue date, expiry date, replacement). `detail.kh` holds the first two only. Dates and an address are data and not human-facing text, so the likely fix is in `type.md`, but the two disagree today.
- **F7. `detail.kh` also holds 235 lines (53-288) of an archived JavaScript language registry** (language IDs, ISO codes, text direction). It is not the Type's text; it is the closed set of languages that task 20140 asks for as code, and `modules/knowledge/language-human` is its home. It is quarantined as comments, which the ban forbids on a file being changed. Moving it is not a conversion of a type's text.

### TAGS and the label domain (your question)
Your reading is right: `TAGS()` is the label domain's job, written as an array of words.
- **Evidence it has no use.** 41 implementations, none returns a tag. The only consumers are a template line in the Go SDK generator that prints it and a JavaScript service sketch that gives `TAGS: [""]`. Its stated purpose (`detail.kh:48`) is grouping types "e.g. in GUI to help org manager to give service delegate authorization to staffs".
- **Why it duplicates Label, in three places `label.md` already rules.** (1) "A word alone is no label": `TAGS` returns bare words, a label has an identifier, and `design` as a topic and `design` as a task kind are two labels. (2) "A word declared nowhere is refused": `TAGS` is a free array that declares nothing. (3) Label's words are in the Text domain, so a label's per-language text is reached through two domains: `TAGS` returns "locale" tags, which makes the label's word part of the type's contract and per language. Also (4): "a label describes; it does not identify, and may be lost without the content ceasing to be itself". A method on the contract makes the labels a part of the type's definition and forces every type to answer it, which is why 41 files carry an empty stub.
- **Delete and hope?** Deleting is right: it costs nothing. Hoping is not a mechanism, and it is not what the repository does elsewhere: the join already exists and runs in two directions. A label's own words come from the label type's detail methods (`label.md`, Where labels are declared: "explained by its type's detail methods"), and a thing takes a label by attachment, `(thing)-[:label]`, held where the thing's record is (a manifest's `labels`, a record's `Labels`, an edge), never by a method on the thing. What is missing is one sentence at the entry point of each owner: Type's details section (`type.md`) says a type's classification is the Label module's, by attachment; `label.md` lists Type among the things that take labels. With those, an agent that starts at Type reaches Label by a link, as `label.md` requires of every naming rule ("each rule cites this module").
- **The purpose stated in `detail.kh:48` is not classification.** Grouping services so that a manager can delegate authorization to staff is a grant of rights. It belongs to the authorization domain's own grouping and not to a tag on the type, and labels would serve only the finding. I did not read that domain (see D4).
- **The same for Documentation, with less duplication.** A document's name is a label and its `Labels` field is the attachment, both Label's. The overlap with Details is the opposite kind: a document's Abstract and a type's `Summary` are both a summary of something. Documentation → A Fact in Code Is Written Once already gives the direction: the description of a code fact is the type's, a document states the concept, the reason and the audience, and refers to the code. What it does not say is which wins when a module is both a document and a type with a `Summary`. A one-line rule closes it; it is not a defect of either domain.

### What a type with no detail yet may carry meanwhile
Nothing in code. Not an empty method (F4: an empty string pretends the text is written), and not a comment (the ban). The missing text is reported as missing by a check, and the idea that the type needs one, if it must be kept, is a sentence in the module's document or its handoff (Cognition → Report absence rather than supplying it). This costs a type nothing it had; the residue is the evidence (8 of 41 summaries empty).

### How the roughly 390 ported comment blocks become detail values
A one-to-one conversion is the wrong frame, because a comment block is not a detail value. Sort each block by the five questions of Documentation → A Fact in Code Is Written Once:
1. **A description of what the type is or does** → `Summary` / `Overview` of that type, in the language file. This is the minority of blocks that are written about a type as a whole.
2. **A reason, trade-off, history or warning** → text, not code: the module's document, handoff or changelog. The ban's own exception clause admits it in code only if no declaration can hold it, and none can say a reason.
3. **A statement about a member (a method, a field)** → this needs each declaration to be a Type with details of its own. Khayyam declares methods with `tp`, which suggests it is, but no accepted document says a method has `Summary`. Unverified, and it decides the density question left open in the comment-policy handoff (how thoroughly a declaration is documented).
4. **The `TODO(go-migrate)` residue and the `TODO(js-idea)` blocks** → not converted at all: they leave when the file is ported or retired (the ban: "repaired when a task changes them").
Doing this by a sweep would repeat the removal F1 warns of. The conversion is per file, at the time the file is changed, and only after the signature exists.

### Assumptions
| Assumption | Type | Stability | If false... |
|---|---|---|---|
| A type's text is returned by a method of the type (S1) | stated | strong: three documents | the whole ban needs another carrier |
| An abstraction has no body and so cannot return its own text | unstated, from task 24048 | weak: an unaccepted proposal | F2 falls and `Details` documents itself like any type |
| The language set must stay out of the contract | unstated here | strong: Type rejects string maps for the same reason | a method per language (Khayyam today) is acceptable |
| Every declaration, not only every type, may carry details | unstated | unexamined | the density question stays open and items 3 above stay unconverted |
| The roughly 390 blocks figure | stated by the plan | not re-counted | the conversion's size is unknown |

### Suggestions
Offered because there is a stronger alternative on F3 and F4, not as a decision.
1. **Contract.** Keep `Domain`, `Summary`, `Overview` in `Details`; move the two notes into a second abstraction composed by Error-like types (F4). Delete `TAGS`.
2. **Locale.** One method per text, taking the language as an input and writing a `Text` (F3, F5). To avoid the hidden edge, the owner's type declares the language files it uses with `in`, like any other dependency, instead of the base finding them by path. This is the part I could not settle: the declaration of one base method with several bodies still needs a mechanism, and I did not find one in the documents.
3. **Meanwhile.** Nothing in code (above).

## Left open
Written into the handoffs after the owner answers, not before (no language document was edited):
- Khayyam handoff, "Which method returns human-facing text": the contract's own comments break the ban (F2), the three statements of locale (F3), and the result type (F5).
- Type handoff, "Companion artifacts per language": F3, F6.
- Label handoff or `label.md`: that a type takes labels by attachment (TAGS).
- Comment-policy handoff: F1, and the density question made sharper by item 3 of the conversion.
- `language-human`: the registry in `detail.kh` (F7).

## Decisions needed
D1. Is `TAGS` deleted, with one sentence in Type and in Label saying a type is labelled by attachment? (Recommended: yes.)
D2. Is the purpose in `detail.kh:48`, grouping for delegated authorization, the authorization domain's job rather than a label's?
D3. Do the occurrence notes (`UserActionNote`, `DevActionNote`) leave `Details` for an Error-like abstraction?
D4. Does the contract name the language as an input of one method, in place of a method per language?
D5. May an abstraction carry text of its own (F2)? If not, where does the text of an abstraction live?
D6. Is the result `Text` (task 24048) and not `String`?
D7. Does a member (a method, a field) carry details of its own, or only a type?

## Owner answers (2026-10-30, after the report)
- D1 yes: `TAGS` is deleted. D2 yes, with the note that Label itself groups services (for example `critical`) and a role with the needed access level calls that group. D3 no: the notes stay in `Details`, because the question covers every type; the owner reads `UserActionNote` as the place to tell a user what a service essentially does (this reading differs from `detail.kh`'s old wording, which said what action to take; asked back). D4: each language is written in a file of its own, the same method declared in each. D5: an abstraction is a type and may carry its own text in its language file. D6: the result stays `String`. D7: methods may carry details; a field is a variable and takes the details of its type, not its own per instance.
- Applied: `detail.kh` now holds the license header and the declarations only (all comments, the `TAGS` residue and the two archived JavaScript blocks removed); `detail.eng.kh` is new and carries the text of the `Details` type through `FromCharacterRun`; the language registry data went to `modules/knowledge/language-human/language-human.handoff.md`. Both `.kh` files pass the Khayyam frontend gate (parse and imports only; a body is not checked by it). Not done: texts for the five method types, `UserActionNote` of `Details`, the `.runtime.kh` side file, and the 112 other locale files.

## Owner answers, second round (2026-10-30)
- A method with no text is still written, empty, because a type that does not write all five methods does not implement `Details` (this replaces the report's "nothing in code"). `UserActionNote` may say what the user can do; no conflict with "what the service does". The error of `FromCharacterRun` is disregarded through a `VoidError` variable of the error module, not a local `err`. The language is chosen as the need of the caller; the extension is not important, and the module reaches a text in a language by another way than a file name. `eng`, `per` and `fas` are preferred codes, not forced.
- Applied: `detail.eng.kh` now writes the five methods for each of the six types (`Details` and its five methods), 30 methods, each former comment turned into the `Summary` or `Overview` of its method type; empty ones are `""`. `modules/process/error/protocol/void-error.kh` declares `vr VoidError Error`; its place and form are my choice, not a ruling. Both pass the frontend gate, which does not check bodies, nor whether a method type and its owner sharing a name (`Summary` on `Summary`) is legal.
