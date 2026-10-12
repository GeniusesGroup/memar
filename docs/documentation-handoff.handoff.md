# Documentation — Handoff Handoff

## Topic & Purpose
Open questions and anticipated work for the Handoff facet's governing specification (`documentation-handoff.md`), relocated there when the documentation method removed unresolved-question lists from base documents' bodies.

## Status
Active

Open work for `documentation-handoff.md`. Entries are mutable current state — revised as each item moves, removed when it resolves or is dropped. See [documentation-handoff.md](./documentation-handoff.md) for what a handoff is; this file demonstrates the pattern on the facet's own specification.

## Open Questions

### Concluded handoff disposition
- State: whether a concluded handoff is deleted, archived, or left in place marked Complete — deletion loses the trail; retention accumulates files. The practice file carries the working answer; this specification may adopt it once real usage shows which cost dominates.
- Next: decide from real usage evidence.

### Where a project's sessions live
- State: owner observation (2026-10-12): each project that uses Memar should keep its own temp folder, and its sessions there, not in Memar's `temp/sessions/`; today the sessions of the `organization` project sit in Memar's. `memar session --help` already honors a project's `sessions` key in its `.agents/memar/preferences.md`; open is whether that becomes the default, how existing sessions move, and what Memar's daily sweep and `claims --project` then reach. Blocks nothing in [Queued Work and Its Hand-Back](./documentation-handoff.practice.md#queued-work-and-its-hand-back), but decides where every queued session is written.
- Next: queued session `20261012T155915Z-12312-0` reviews it and records options with a recommendation for the owner.

## Anticipated Work

### Running queued sessions unattended
- State: the practice has a person or an agent start every run; starting queued sessions on a schedule, with no one present, is out of scope here and belongs to the `organization` project later.
- Next: none in this repository until that project takes it up.
