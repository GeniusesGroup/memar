# Text Changelog

## Changelog

### Research on what the text domain is for, its kernel, and the owner's questions
- Time: 2026-10-16T00:30:00Z
- Type: added
- Cited:
  - [Modules → Placement](../../modules.md#placement) - Reference: the kernel and pluggable tests the research applies
  - [Modeling → The Attribute-or-Edge Test](../../../docs/modeling.md#the-attribute-or-edge-test) - Reference: names Text as the abstraction that owns holding, validating, versioning, internationalizing and searching words
- Contributors:
  - [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) — requested the work (2026-10-15)
  - An AI agent (Claude, model claude-sonnet-5-5 as reported by the runtime; no CONTRIBUTORS.md entry) — researched and drafted

#### What changed
- [text.research.001.md](text.research.001.md) is added: fourteen scenarios from several cultures and industries; a proposal that a text is a slot with persistent identity and immutable content-addressed values; a five-element kernel; five rival models with a recommendation (unratified); a mapping of every edge, loop, protocol and widget folder; six pluggable capabilities and thirteen missing pieces sketched; thirty-two test scenarios; fifteen contradictions reported, not resolved; and nineteen owner questions with defaults.
- [text.handoff.md](text.handoff.md) gains the nineteen questions with their defaults and what each blocks, seven Next Steps, and the research in Related Artifacts.
- This is the domain's first changelog entry. Nothing in [text.md](text.md), in any edge document, or in any `.kh` file was changed; nothing was moved or deleted.

---

### The services that cover a search requirement
- Time: 2026-10-24T09:40:00Z
- Type: Added
- Cited:
  - [Knowledge](../knowledge.md#the-modules-of-this-category) - Reference: a search over text is not a domain
- Tasks:
  - main:.agents/tasks/20261018-T133018Z-26648/: Partial - the split of the content module's services
- Contributors:
  - [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) — ruled that the search services belong in Text, with the caution that Text may not see the structure it holds
  - An AI agent (Claude, model claude-sonnet-5-5 as reported by the runtime; no CONTRIBUTORS.md entry) — moved

#### What changed
- `services/` gains `content_search.py`, `content_find.py`, `index.py` (the sections ranked), `corpus.py` (which files of a checkout are content), `file_text.py` (reading and writing a text file without damaging it) and `text_check.py` (the bytes half of `memar content check`); `primitive/` gains `corpus_source.py` (where the corpus is read from).
- The index asks the Markdown module for a document's sections by loading it at run time; the relationship Text should expose for this is not designed, and Text itself may have no view of the structure it holds (owner, 2026-10-24). It is recorded in the handoff.

#### Considered and not done
- A module named search (refused: services, not a domain).
