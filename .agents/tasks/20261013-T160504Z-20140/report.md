---
Title: Organizational rule: files for each human language (per.kh, eng.kh): how description files in several languages work
Status: Complete
---
# Report
Blocked on the owner's approval of a design. Nothing was applied, queued, or committed; the only file written is this one, and plan.md's Status was set to match.

## What ran
Read, by the sections named: the proposal at memar/.agents/tasks/20261013-T142915Z-8820/report.md (Proposal B and the owner outcome); docs/documentation.md#file-naming; docs/khayyam/khayyam.md#self-documenting-code-and-naming; docs/modules/computer/type.md (the paragraph "Type details and human-facing identity" and its module text, via modules/computer/type); docs/modules/computer/type.handoff.md (the entry "Companion artifacts per language, or a method per language?"); modules/computer/type/protocol/detail.kh; the existing language files in the organization repository (bundles/Achaemenid/achaemenid/errors/*.locale.eng.kh and locale.per.kh) and modules/time/utc/weekday.locale.fa.kh. Counts, measured with find on 2026-10-13 and not re-verified: the organization repository has 25 files ending `.eng.kh` (17) or `.per.kh` (8); Memar has 30 `<base>.locale.<lang>.kh` (23 eng, 5 per, 1 en, 1 fa); all are archived Go under TODO(go-migrate), none is live Khayyam. Unverified: the rest of type.md, docs/modeling.md, documentation-changelog.practice.md (how a review is recorded), and any translation workflow in docs/agency.md. The check was the owner's approval; it has not been given.

## Check
Not run. The design below answers each question the Request names, compares with the four existing Memar statements, and keeps Memar free of any dependence on the private organization repository.

## Result

### The design, in one paragraph
A human-facing text is kept once per language, in a file of its own that sits beside the thing it describes and is named `<base>.<lang>.<ext>`. The thing itself (a type, a service, a document) never holds the words. A tool or a type finds the words by the thing's path and a language code, never by a map keyed by strings; one method asks for them with a language value, and a text that is missing is reported as a missing text, never as an empty string.

### Split the rule in two, so Memar can adopt it by reference
- Part 1, the method (portable): file naming, finding, missing, authorship, review, staleness, language choice. It names no organization, path, person, or tool of the Geniuses Group, so it can be read by anyone and adopted unchanged.
- Part 2, the Geniuses Group's choices (organization only): which languages exist, which language is the source, which are required, who reviews. These are facts of the organization and stay in its repository; a later project or organization states its own.
The organization repository is private, so Memar never links to it ("a base document may not link up to private code"). When the owner agrees, Memar states Part 1 as a document of its own (the natural home is beside docs/modules/computer/type.md's Type details, since the Type is where the text belongs) and organization's Part 1 then refers to that document, which is the allowed direction. Until then the rule lives only in the organization, and nothing in Memar cites it.

### Part 1, the method

1. Presumption (the owner's fifth ruling). A text a person reads about a thing is code, not a document. It is a value the thing's own method returns. A document refers to the thing by naming it, and a help text by calling its method. No place retypes the text, because a copy is a cache of information.

2. Naming. `<base>.<lang>.<ext>`, beside `<base>.<ext>`: `bad_request.kh` with `bad_request.eng.kh` and `bad_request.per.kh`; for a document, `<base>.<lang>.md`. The extension stays last so tools that sort by kind still work. The language code is exactly one entry of the closed set in item 7. A region or script is added by a hyphen inside the code (`eng-GB`), and only when a project needs the difference.
   Departure from the present 30 files: they read `<base>.locale.<lang>.kh`. This design drops `locale`, as the owner wrote (`.per.kh`, `.eng.kh`). Reason for dropping: the code is a closed set, so the middle word tells a reader and a tool nothing; reason for keeping it would be that docs/documentation.md#file-naming makes the dot carry a facet key (`.observers`, `.handoff`), and a language code is a value of a facet. Either is consistent; this design follows the owner's wording and states the facet in the rule, not in each name.

3. How a thing finds its language files. By path alone: the file of language L for the thing declared in file F is F with `.<L>` inserted before the extension, in the same folder. No registry of files, no list in the base file, no string-keyed translation map (the type module already forbids that map). The folder listing is the list of available languages; a tool that wants it lists the folder.

4. What a language file holds. Only the text values of one language for one base, and nothing a program branches on. It declares no new behavior, no condition, no loop. A check can then say "a language file contains text declarations only", which is what lets a translator change words without a developer and without the development environment. For a Khayyam type the base declares the methods once; the language file supplies the text each method returns for that language.

5. What a missing language means. Three cases, kept apart:
   a. The project does not require the language: nothing is missing; the file need not exist.
   b. The project requires it and the file is absent, or the file lacks an entry the base file declares, or an entry is empty: this is a defect, reported by a content check, and it blocks a release of the thing; it is not a runtime error.
   c. A tool asked at run time for a language whose text is absent: it serves the next language in the chain (item 8) and says which language it served; it never prints an empty string and never silently switches. The source language (item 6) missing is always the error.

6. Source language, writing, review. One language per project is the source: the author writes it first, and it is the meaning the others translate. A translation is not a copy but a new statement of the same meaning, so a copy ruling does not forbid it; what it must carry is the proof of what it translates, to avoid a silent stale translation:
   - Each language file declares, as typed values in the file, its status (Draft or Reviewed), the writer, the reviewer, the date, and the digest of the source file's text values it was written against.
   - The tool recomputes that digest; a difference makes the translation stale, reported like a missing text (5b).
   - The writer and the reviewer are different parties. A reviewer reads the target language natively. An agent may write a Draft; only a person fluent in the language may mark it Reviewed, and a user-facing text that is only Draft is reported but not blocked unless the project says so.
   - Review is recorded as docs/documentation-changelog.practice.md#recording-an-approval says; this design does not make another record.
   - The author of the base changes the source language file only through the base; a translator changes only their language file, and the check in item 4 proves no function changed.

7. The closed set of languages is one definition in code: the code (`per`, `eng`), the aliases a protocol uses (`fa`, `en`, as `Accept-Language` sends), the native name, the direction (right-to-left for `per`). Direction, name, and aliases are facts of the language, not of any file. The codes `per` and `eng` follow ISO 639-2; `per` is the bibliographic form of Persian (the terminology and ISO 639-3 form is `fas`), so the registry holds `fas`, `fa` and `fa-IR` as aliases of `per` and a tool resolves any of them. The two stray files `weekday.locale.en.kh` and `weekday.locale.fa.kh` are renamed to the codes.

8. How a tool gets the right language. The chain, first found wins: the explicit choice (a flag or a request header), the user's own content preference as the system holds it, the project's default, then the source language. The tool turns the choice into a language value and calls the type's method with it, so a help text contains no words of its own: its sentences are the types' Summary and Overview, and the tool's own words (`usage`, `options`) are types too, with language files of their own. This is the owner's fifth ruling applied: every service is a type, so a service's help is its type's details. The tool states, in the output, the language it served when it is not the one asked.

9. Scope. The rule covers descriptions: name, abbreviation, summary, overview, notes to the user and to the developer, labels on screen. It does not cover design argument, reasons, history, or identifiers; a document that argues stays in one language, and an identifier's language is the identifier rules' business. This is the limit Proposal B already set.

### Part 2, the Geniuses Group's choices (for the owner to fill)
Source language: not decided by anything found (the existing files hold English as the more complete set: 17 eng against 8 per). Required languages: `per` and `eng` (the owner's two examples). Reviewer for `per`: the owner or a person he names; for `eng`: likewise. Default if nothing is chosen: `eng`.

### Comparison with the existing statements
| Statement | Says | This design |
|---|---|---|
| khayyam.md, Self-Documenting Code and Naming | text is a value a method writes; "another language is another method on that type" | Agrees that the type owns the text and a method returns it. Differs on one point: it is one method taking a language, not one method per language, so a missing language becomes a checkable gap (item 5) and a tool can choose at run time. The sentence "another language is another method" would be reworded when the rule is adopted. |
| modules/computer/type/protocol/detail.kh | Details with Domain, Summary, Overview, UserActionNote, DevActionNote; no language anywhere | Compatible once each takes a language value; the file does not need other methods. The five-method set is unchanged. |
| type.md, Type details and human-facing identity | companion artifacts per language, same base name qualified by language, never inline, never a string-keyed map; a translator changes words with no developer round-trip | This design is the convention that paragraph asks for and does not state: name, finding, content, check. It adds nothing against it. |
| type.handoff.md, Companion artifacts per language, or a method per language? | open: is the companion the source the methods read, or a second carrier beside them? | Answered: both are one thing. The companion is the only place the text lives, and one method reads it. There is no second carrier. This closes that entry, and the paired Khayyam entry (Which method returns human-facing text), when adopted. |
| Existing 30 + 25 files (`.locale.eng.kh`, `.eng.kh`) | `//go:build lang_eng` tags choose a language when building | Rejected for run time: a build tag fixes one language per binary, so one help command cannot answer two readers. Kept only as the history of the convention. |

### Cost and risk
- Renaming 30 files in Memar and the organization's `.locale.` ones is mechanical but touches names that other files import; the `locale.<lang>.kh` files with no base name (for example bundles/Achaemenid/achaemenid/errors/locale.per.kh) need a decision (they hold a package-level domain string, not a type's text).
- A digest in every translation is more machinery than a date; the alternative (no digest) lets a translation go stale unseen, which is the failure the owner's ruling about copies exists to prevent.
- The TypeDetail rewrite of type.md waits for this rule (the owner's outcome says so); it is not part of this design.

## Left open
No entry was written in a handoff (the questions below are for the owner now, not entries). If the owner agrees, the following would then be recorded where they belong: the closing of the two handoff entries named above, and a handoff entry on the `locale.<lang>.kh` files that have no base name.

## Decisions needed
1. Approve the split: method (Part 1, portable, to be stated in Memar later) and the Geniuses Group's choices (Part 2, organization only)?
2. File name `<base>.<lang>.<ext>` (your wording, drops `locale`) or keep `<base>.locale.<lang>.<ext>` (the 30 files today)?
3. One method with a language value (recommended) or one method per language (khayyam.md today)?
4. Language codes `per`/`eng` (ISO 639-2) with `fa`, `fas`, `en` as aliases a tool resolves: agreed?
5. Source language of the Geniuses Group: `eng` or `per`? Required languages: both?
6. Translation carries a status and a source digest (stale translations are reported): yes, or a date only?
7. May an agent write a Draft translation, with only a fluent person marking it Reviewed?
8. Until a Reviewed text exists, does a Draft block a release, or only get reported?
9. Where in the organization repository does the rule live (it has no docs or rules folder; a top-level `rules/per-language-files/` is proposed)?
10. May the next task rewrite the type.md paragraph and close the two Memar handoff entries on the basis of this?

## Owner response (2026-10-13)
The subject belongs to Memar, not organization (which has no file system; everything is Content related as a graph). A language file implements the abstract type (it has behaviour, not only text values); no strings-file model; meaning change versus correction must be explicit; language codes cannot be fixed. Redesign queued in Memar (topic memar-khayyam-types). This design is withdrawn as a first attempt.

## Closed (2026-10-30)
The design above stays withdrawn. Its open decisions were answered by the owner in task 20261030-T051847Z-13004 and applied in `modules/computer/type/protocol/detail.eng.kh`: the file is named `<base>.<lang>.<ext>`; the language file implements the abstract type and declares the same method in each language's file; the language is chosen by the need of the caller, and the module reaches a text by a means other than the file name; the Geniuses Group's official language is `eng`, needing no owner approval, and no translation is made for now; the codes `eng`, `per` and `fas` are preferred and not forced; no status and digest on translations for now. The redesign it called for is that task's work.
