# Title Handoff

## Topic & Purpose
The abstraction of the title module, written in Khayyam on 2026-10-31 for task 20261030-T163540Z-10624: Title, Field_Title, its validation, storage, retrieval, display and refusals. The task domain embeds Field_Title and calls Title_Check; it declares no title.

## Status
Written and accepted by the analyzer; reviewed by a fresh sub-agent, whose findings were applied. No realization and no tests yet; the Python `checked_title` in the plan file service stays read-only until a realization replaces it.

## Decisions
- **The thing domain drops the concept of a title.** A title is too basic a concept: any attempt of a domain to name it makes a strange relation between domains. The title module owns the relation of a thing to its title. *(decided, owner, 2026-10-31)* The thing domain's mentions (its `dt-uuid.kh` comment, a find-quiddity-by-title service) are still to be removed; that is the thing domain's own work.
- **A blank title is refused;** nobody may set an empty title on anything. `Title_Error_Empty` is the refusal. *(decided, owner)*
- **No `dt-` prefix in a file name;** the files of this module are `title.kh` and so on. *(decided, owner)*
- **Every abstraction is written in a `protocol/` folder,** so that the content meant is plain; a service and a widget each has a `protocol/` folder of its own, so the module's main `protocol/` stays small. The realizations sit beside it. *(decided, owner, applied here)*
- **A document restates no code:** what a Khayyam file can say is not written in `title.md`. *(decided, owner)*

## Open questions

1. **A protocol module.** The owner accepted `modules/knowledge/protocol`, with `docs/protocol.md` moved to it, a `rules` folder of rules for writing a protocol (the `protocol/` folder of a service or widget first), and rules recorded elsewhere by mistake moved in. The module must offer a label `protocol`, which is today elsewhere and must be moved to the right place: a content may be labeled protocol, be a widget and be a member of a module at once. Handed to another session.
2. **The name under which a title text is kept** (a prefix and the thing's id) is left to the realization; the owner did not rule on it.
