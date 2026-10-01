# Token Changelog

## Changelog

### Seed — the token protocol, from the display contract's evidence
- Time: 2026-09-29T11:50:18Z
- Type: Added
- Cited:
  - [Modules → What does not belong here](../../modules/README.md) - Depends_on: the placement rule this document follows — specifications and general claims live in the repository's `docs/`, and the modules layer realizes them rather than restating them.
  - [Khayyam module → Local placement](../../modules/khayyam/README.md) - Depends_on: the same rule as a row of that module's placement table, which sends cross-cutting host-independent design to `docs/` and protocols to `docs/protocols/`.
  - [Protocols → Where implementations live](./README.md) - Depends_on: this folder is each protocol's source of truth and is not executable code, which is why the subject belongs here and the realization that exercised the evidence does not.
  - [Linter handoff → Topic & Purpose](./computer/linter.handoff.md) - Evidence: the record of the lift that moved memory, linter, compiler, and runtime out of `modules/` into `docs/protocols/` and rewrote them as language-independent protocols — the decision this document's placement honours rather than repeats.
  - [Khayyam Display Research 002](../../modules/khayyam/display/display.research.002.md) - Evidence: the host's own published classification, the super-type mechanism, what a type nothing matches becomes, the boundary between what a language publishes and what a consumer decides, and the principles with their costs.
  - [Khayyam Display Research 001](../../modules/khayyam/display/display.research.001.md) - Evidence: the ownership findings and the measured contrast and colour-vision work behind one realization's sheet, used for the value-side boundary and for the fault that reads as an absence.
  - [Khayyam Display](../../modules/khayyam/display/display.md) - Evidence: the twenty-one-role contract in prose, its two mechanisms, and the rule that a role names what an identifier is rather than where it appears.
  - [Khayyam Display Handoff](../../modules/khayyam/display/display.handoff.md) - Evidence: the four host mechanics a realization must be designed against, the corrected ground for refusing a bridge, and the owner's open question on the four roles no standard class can express.
  - [Khayyam display contract (JSON)](../../modules/khayyam/display/display.json) - Evidence: the machine form of the same contract — the three-answer kind statement, the two-way statement of what implements a role, the theme contract, and the drift policy.
  - [verify-roles.mjs](../../.agents/vscode/extensions/khayyam-language/scripts/verify-roles.mjs) - Evidence: what a check that reads the consumer's own list refuses, and the matching arithmetic stated in the consumer's numbers rather than asserted.
  - [Content → Theme / Role-to-Rendering Mapping](../content.md#theme--role-to-rendering-mapping) - Depends_on: the consumer-independence position at the base layer, which this protocol states once for classified things and the values a consumer decides.
  - [Lexer](./computer/lexer.md) - Depends_on: the sibling protocol this one is divided from; its output is a lexical unit and its own naming is deliberately unsettled.
- Propagates to:
  - [CONTRIBUTORS.md](../../CONTRIBUTORS.md) - Done: the model that drafted this entry has its own entry under the Stealth Models entity, recorded in the same session.
  - [Display handoff → Where this material belongs in the long run](../../modules/khayyam/display/display.handoff.md#where-this-material-belongs-in-the-long-run--owner-ruling) - Pending: the citations this entry and the base document carry point into `modules/khayyam/display/`, and the owner ruling on that folder's home moves them; the content of those records is unaffected either way.
  - Token handoff (`token.handoff.md`, not yet created) - Pending: a `Draft` carrying the owner's open decisions has no paired handoff yet, so the resolution work — what would settle each open question, and in what order — has no home.
  - [Protocols → Membership criterion](./README.md) - Rejected: the folder states its criterion and does not list its documents, so no index entry is added.
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) - requested, decided
  - [Space Bunny Alpha](../../CONTRIBUTORS.md#space-bunny-alpha) (space-bunny via [OpenCode](../../CONTRIBUTORS.md#opencode)) - drafted

#### What changed
- Created `docs/protocols/token.md` as a `Draft` protocol document: the class of requirement is that a consumer — an editor, a Markdown preview, a code-hosting page, any renderer — can colour a file it is not told the contents of, consistently, against the theme the reader chose, without each language inventing its own vocabulary.
- The document states what a token is (a named class, and never a value, a piece of text, or an occurrence), what it is not, and which two other concepts in this repository carry words a reader may confuse with it: the Lexer's lexical unit and Content's Lexical Token.
- It divides the subject from the Lexer protocol: the Lexer owns how a source is decomposed; this protocol owns how a classified thing reaches a reader who sees it; the seam is the occurrence, and each rule has one home.
- It states what a producer publishes for each token — a name a consumer can key a rule by, what the token applies to, its kind as one of exactly three answers, and which mechanism can answer it — and what a producer is not owed: no value, no promise that a foreign theme will style it, no scope names, and no obligation on a consumer to render two distinct tokens differently.
- It states what a consumer decides: every value, by exactly one mechanism, with an unresolved token discarded rather than defaulted and the unanswerable named rather than guessed.
- It rules six things the evidence settles, and lays out the one it does not — whether a token is identified by a standard class, a published label, both, or nothing the producer publishes — as four options with what each makes possible and impossible, what each costs, what the evidence does and does not say, and what would settle each. Two consequences that follow whichever is chosen, the portable spelling and the owner of the kind claim, are stated with the same three parts.
- It records seven standing costs as principles a later realization can apply, each with what it cost.
- Placement: the decision that language-independent development documents do not live under `modules/` and that the ones already there were moved into `docs/` is already recorded — in the two module READMEs' placement statements and in the lift recorded in the linter handoff — so it was found and honoured, not re-decided here and not restated in the body.
- No code, contract, theme, manifest, or file under `modules/` was written, and nothing was staged, committed, deleted, or renamed.

#### Considered and not done
- **Writing this subject as an extension of the Lexer protocol, or as a section of the Lexer document** — rejected: the two have different subjects and different failure owners, and a rule stated in both is a rule that drifts apart.
- **Restating the placement decision inside the new document** — rejected: the decision has one home already, and a body sentence restating it is a second copy that will drift from the first.
- **Ruling the identity question and marking the document `Proposed`** — rejected: the evidence constrains all four answers and closes none, and the owner raised the question against the current work rather than answering it.
- **Creating the paired handoff in the same change** — rejected as out of scope for this change; the open decisions are therefore stated in the body as claims that say they are unsettled, and the resolution work has no home until the handoff is created.
- **Carrying a colour, a contrast floor, a palette rule, or a claim that any classification is correct** — rejected: the value is the consumer's decision, and no document here states that any of them is right.

#### Related work
- [display.research.002.md](../../modules/khayyam/display/display.research.002.md) — the inquiry that read one consumer's own published classification and its super-type mechanism out of its implementation, mapped twenty-one roles against it, and drew the boundary this protocol states as its own: a language publishes a set of named types, each optionally declaring a standard super type, and publishes nothing about values; a consumer decides every value. Its F6 supplies the standing costs above in the same form.
- [display.research.001.md](../../modules/khayyam/display/display.research.001.md) — the inquiry that read the merge out of the consumer's product and found a token no style resolves is discarded rather than left unstyled, which is why an unresolved token is ruled an absence here rather than a visible nothing.
- [Content → What a Host's Own Mechanism Costs a Realization](../content.md#what-a-hosts-own-mechanism-costs-a-realization) — the four host mechanics already stated at the base layer, of which ruling 1 and the parser rule are this protocol's form and the value- and setting-shaped ones stay the host's.

#### Deliberation
- The owner directed that the concepts this stretch of work stumbled into be written down as a protocol beside the Lexer protocol, so that a class of requirement is answered once and language-independently rather than per language, and named the requirement in one sentence: a consumer must be able to colour a file it is not told the contents of, consistently, against the theme the reader chose, without every language inventing its own vocabulary (Omid Hekayati — directed).
- The owner put the identification question to the current work directly — a standard class the consumer already knows, a symbolic label the language publishes, or something else — and required each answer's cost, what it makes impossible, and who is right to be stated (Omid Hekayati — asked).
- Reading the evidence rather than the account of it moved the question: the host's own code showed that identity must be a name a rule can be keyed by, that a type with no declared super type is unreachable by any rule keyed on a standard type, and that a token no rule styles is discarded rather than defaulted. What that settles is what identity is made of, not which vocabulary it is drawn from, so the four options were laid out rather than closed.
- The bridge's original ground was read in the same artifacts and does not stand; the cost that survives is that a second mechanism decides the value for every reader whose theme has never heard of the language, and the document states that ground and not the withdrawn one (OpenCode — argued, drafted).

#### Decision
- Applied: a token is a named class carrying no value; identity is a name a consumer can key a rule by; a kind is a separate statement with exactly three answers; a token names what a thing is and not where it stands; one mechanism decides a value; an unresolved token is an absence and the unanswerable is named.
- Not applied, and left to the owner: which of the four forms the identity takes, who owns the kind claim, whether this protocol fixes a portable spelling or each consumer translates, and whether a token with no counterpart in a consumer's vocabulary is a token at all.
