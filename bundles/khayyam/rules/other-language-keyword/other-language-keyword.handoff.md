# Khayyam Rule — Other-Language Keyword Handoff
Open state for [other-language-keyword.md](./other-language-keyword.md). See the repository's [documentation-handoff.md](../../../../modules-plugable/knowledge/documentation/handoff/handoff.md) for what a handoff is.

## Status
Active — drafted 2026-10-03 on the owner's ruling that even the absence of a keyword may leave the language documents and become a Rule that warns about suspicious words such as `if` or `goto`, that a language document declares what the language has while a Rule tells a reader what to do when they reach for something the language does not have, and that the Rule is written imperatively in the catalog's own voice.

## Vocabulary
The catalog already had a term for the condition this Rule is about, and the Rule says so in its own body rather than claiming a new name. The four import-resolution rules are the family's existing statement of it:

- [unresolved-import](../unresolved-import/unresolved-import.md) — an `in` path with nothing behind it.
- [name-not-declared](../name-not-declared/name-not-declared.md) — an `in` naming what the target does not declare. Its own text already records the lesson this Rule generalizes: a label that borrows another language's vocabulary sends the reader looking for that language's mechanism, and `declaration` was chosen because it is the language's own word.
- [kind-mismatch](../kind-mismatch/kind-mismatch.md) — a form disagreeing with the declared kind.
- [unbound-type-name](../unbound-type-name/unbound-type-name.md) — a type name nothing declares or includes.

Those four say what is refused. None of them says **which word** was refused or **why the reader expected it**, and that difference is the whole of this Rule. It is therefore the same check seen from one narrower angle, not a fifth resolution rule, and the document says so.

A second, adjacent term was checked and found not to be the same thing: [scope-visibility](../scope-visibility/scope-visibility.md) governs the names a block may use, and [Linter → A rule's home is its subject's document](../../../../modules/computer/linter/linter.md#a-rules-home-is-its-subjects-document) is the general principle behind it. Neither states what a reader is told when a name resolves to nothing.

**The name follows the catalog's own rule** — a name locates a subject and the document then speaks about it, a verdict in the name leaves the document nothing to say, and a name borrowed from another language sends the reader to that language's mechanism. `other-language-keyword` locates the subject: a word that is a keyword elsewhere and a name here. `suspicious-word` was refused because "suspicious" is one tool's reading of an occurrence and not a thing the rule governs; `foreign-keyword` was refused for the same reason as a borrowing; `unknown-keyword` was refused because the word is not unknown, it is undeclared. No spelling of the concept is settled beyond this.

## Placement
The Rule is in `bundles/khayyam/rules/` because its subject is this repository's reading of Khayyam source: the check is a tool's, but the tool is the Khayyam module's, and [Rule → Which Module a Rule Belongs To](../../../../modules/process/rule/rule.md#which-module-a-rule-belongs-to) fixes a Rule's home by its subject. [comment-forms](../comment-forms/comment-forms.md) is the standing precedent — a tool's condition over the characters it reads, held in this catalog because the reading belongs to this module's toolchain. What the Rule is **not** is a rule about the language: a program violating it is already refused by `name-not-declared` or `unbound-type-name`, so turning it off changes no program's meaning, which is the test at `modules/process/rule/rule.md:77` and the catalog's own floor-and-ceiling criterion.

A folder of this repository's diagnostics rather than of the language's was considered and not taken: no such module exists, and inventing one to hold a single condition would give a second home for the reading of Khayyam source that this catalog already holds.

## Open Questions
- **How much of the refusal the report covers.** This Rule states the narrowest form: the unresolved name is recognizably another language's keyword. Whether the report also fires on a name nothing supplies that is not recognizably a keyword anywhere — a plain typo, or a name whose declaration is simply missing from an `in` — is an organization's configuration question and is not settled here.
- **How an organization states its vocabulary.** The list is the tool's and the report's wording is the organization's; nothing states a required format for either. Whether the vocabulary may be extended with words from a language this repository does not use is likewise unstated.
- **Whether the two resolution rules should say where their own reports name the cause.** Their documents each record that the diagnostics contract is deferred and the label an implementation label. This Rule depends on that deferral rather than closing it; a repository that later fixes a diagnostics contract may find this Rule either absorbed into it or left as the one place a report explains itself.

## Related Artifacts
| Artifact | Relation | Action |
| --- | --- | --- |
| [other-language-keyword.md](./other-language-keyword.md) | Base — the Rule | Keep in sync with the owner's further rulings on diagnostics |
| [name-not-declared.md](../name-not-declared/name-not-declared.md) | Depends_on — the refusal this Rule speaks inside, and the borrowed-vocabulary lesson at its `:14` | None (read) |
| [unbound-type-name.md](../unbound-type-name/unbound-type-name.md) | Depends_on — the second refusal this Rule speaks inside | None (read) |
| [comment-forms.md](../comment-forms/comment-forms.md) | Precedent — a tool's reading condition held in this catalog | None (read) |
| [Khayyam → Language Keyword in a Glance](../../../../docs/khayyam/khayyam.md#language-keyword-in-a-glance) | Owns — the seven declaration words, and what an identifier may spell | None (read) |
| [Khayyam → Minimal Legislation](../../../../docs/khayyam/khayyam.md#minimal-legislation-a-principle) | Decides — that this is a tool's rule, at `:177` | None (read) |
| [bundles/khayyam/rules/README.md](../README.md) | Catalog index | Row added this session |
| This folder's `README.md` | Convention — a folder with a main document takes a symlink to it | Written as the documented fallback: the file's content is `other-language-keyword.md`, with no trailing newline, as the sibling rule folders already carry. It is still a text file pointing at a sibling, not a link; recording the link is a git operation this session may not perform |

## Notes
- Every document line the Rule names was read at the line it names. No file under `modules/**` was cited as evidence for any claim in the Rule.
- Files this session wrote: this folder and `bundles/khayyam/rules/README.md`. No git command of any kind was run and no test suite was executed.
