---
ID: 20261030-T051913Z-13004
Title: Derive the normative-reference lists instead of keeping them by hand
Status: Queued
Start Date: 2026-10-30T05:19:13Z
Project: C:\Sync\Persons\Geniuses.Group\github.com\memar
Parent: 20261026-T200841Z-21460
Conversation: 20261022-T182206Z-3248
Priority: 5
Labels:
  - design(01a14a04-6531-73d5-8eeb-6e37ddce016d)
  - memar-scripts(01a14a13-1972-7b1b-8056-e00b30bb0067)
---
# Derive the normative-reference lists instead of keeping them by hand

## Request
The owner (2026-10-30) dislikes that the normative-reference lists in `modules/knowledge/content/rules/normative_references/` are written by hand, one entry and one `reviewed` hash per section, although it is the practice for now. Design how they are derived instead: for example each section or rule declaring the acts (kinds) it binds, so that `memar content get-act-context` builds a kind's list, and so that a changed section is found from the declaration and not from a hand-held hash. Keep what the lists give today: a kind's passages printed whole, a review mark that a changed section invalidates, the every-act sections no project may drop, and a project's own drops with reasons. Name what moves where, the migration of the existing entries, and the cost.

**Check (done when):** a design recorded in the normative-references document and its handoff, reviewed by a fresh agent, with implement tasks queued for the migration; at most 10 lines under `## Decisions needed`.

**Model facts:** the owner reviews; the judgment is open; every task reads these lists, so an error is costly: standard level.

## Why
A list kept by hand drifts, and it already reports a section changed since it was reviewed whenever another task edits it.

## Steps
1. (local) Read the normative-references module, `memar content get-act-context --help` and its code, the lists, and the rule that the Normative References own the claim.
2. (delegated, fresh reviewer, critique) Review the design.
3. (local) Apply findings, queue the migration.

## Next
Step 1.
