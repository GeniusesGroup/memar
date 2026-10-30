---
Title: Organizational rule: files for each human language (per.kh, eng.kh): how description files in several languages work
Status: Complete
Opened: 2026-10-13T16:05:04Z
Project: C:\Sync\Persons\Geniuses.Group\github.com\memar
Parent: 20261013-T142915Z-8820
Conversation: 20261013-T034406Z-30084
Priority: 7
Labels:
  - memar-khayyam-types
---
# Organizational rule: files for each human language (per.kh, eng.kh): how description files in several languages work

## Request
Proposal S2 part 1. Read .agents/tasks/20261013-T142915Z-8820/report.md (the proposal) and the owner's rulings of 2026-10-13: (1) the four-question rule is accepted and he adds a fifth, first: the presumption is that EVERYTHING is code unless shown otherwise; (2) where a fact is in code, no place may keep a copy: a help text or document refers to a type by calling the type's methods (for a help text) or by naming it (for a document), never by retyping its text, because a copy is a cache of information; (3) concepts are shown in code and documents refer to that code, so no text duplicates it; (4) human-language descriptions: one separate file per human language (for example `.per.kh` and `.eng.kh` suffixes), the way such files work is a rule beyond the language and even beyond any compiler (an organizational rule that applies beyond Khayyam, though implemented in Khayyam first); (5) the `dt-` and even `t-` prefixes are wrong now that Memar's `type` is precisely defined; every service is also a type. Each of these tasks is independent and small. Do not commit. Report with Status front matter; write report.md THROUGH `memar content write --create FILE --content-file SCRATCHFILE`. Owner: the way per-language description files work is an organizational rule, not a language or compiler matter, and applies beyond Khayyam. Decide, for the Geniuses Group, which method it implements: the file naming (suffix per language), how a type finds its language files, what a missing language means, who writes and reviews translations, and how a tool such as a help text gets the right language. Compare with the existing Memar statements (docs/khayyam/khayyam.md 'self-documenting code and naming', modules/computer/type/protocol/detail.kh, docs/modules/computer/type.md 'Type details and human-facing identity' and its handoff question 'Companion artifacts per language, or a method per language?'). Propose, for the owner's approval; apply nothing. The organization repository is private and must not become the functional basis of Memar: write the rule so Memar can adopt it by reference only after the owner agrees.

## Why
The owner approved the split of the code-versus-text task into independent tasks.

## Steps

## Next
Closed 2026-10-30: the owner withdrew this design as a first attempt on 2026-10-13 (see its report's Owner response). The redesign is the queued task 20261014-T113220Z-26268; the rule on exceptions to one-file-per-type is written (task 20261014T113224Z-23972-0).
