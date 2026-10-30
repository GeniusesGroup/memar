---
ID: 20261030-T051847Z-13004
Title: Critique how a type's human-facing text is written in code (detail.kh), now that comments are banned, and settle its worked signature
Status: Complete
Start Date: 2026-10-30T05:18:47Z
Project: C:\Sync\Persons\Geniuses.Group\github.com\memar
Parent: 20261026-T200841Z-21460
Conversation: 20261022-T182206Z-3248
Priority: 5
Labels:
  - critique(01a14a04-6532-76bf-b48e-4b7cc539bf44)
  - khayyam(01a14a13-19e7-74d9-ba0b-8335ceaab682)
---
# Critique how a type's human-facing text is written in code (detail.kh), now that comments are banned, and settle its worked signature

## Request
The owner (2026-10-30) asked for a critique of how a type's human-facing text is written in code, which `modules/computer/type/protocol/detail.kh` raises, now that [No Comments in Code](/modules/computer/type/rules/no-comments-in-code/no-comments-in-code.md) bans comments and the Khayyam fallback of `bundles/khayyam/rules/comment-policy` was removed. Questions to critique: whether the five methods (Domain, Summary, Overview, UserActionNote, DevActionNote) are the right set; the worked signature that `docs/khayyam/khayyam.md#self-documenting-code-and-naming` and its handoff still call open (which method, on which owner, how a locale is named); how text in several languages is held without a prose line above a declaration; what a type that has no detail yet may carry meanwhile; and how the ported sources' roughly 390 comment blocks become detail values. Read the cognition norms for a critique first. Keep the owner's word that the way code is written must be clear.

**Check (done when):** a report that separates what is sound from what is not, with each finding tied to a passage, and at most 10 lines under `## Decisions needed`. No edit to `detail.kh` or the language documents: a proposed change goes to the handoff of the document it concerns.

**Model facts:** the owner reads the critique; the judgment is open; an error is costly because every type follows it: standard level.

## Why
The rule bans comments but cannot say where a type's text goes until the signature is settled; the owner wants the way code is written to be clear. Not done in the task that wrote the rule: the ban stands without it, using the five existing methods.

## Steps
1. (local) Read detail.kh, the Self-Documenting Code section and the language handoff's open question, type.md Human-facing identity, the comment-policy rule and its changelog.
2. (local) Write the critique report.

## Next
Step 1.
