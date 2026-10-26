# Memory Version Changelog

## Changelog

---

### The versioning vocabulary gets a module of its own
- Time: 2026-10-26T14:00:00Z
- Type: Added
- Cited:
  - [Memory Handoff](../memory.handoff.md#what-becomes-of-protocolversionkh-and-of-the-kernel-files-that-import-storage_block-and-storage_page) - Reference: the open entry that asked for the fate of the file
  - [Category](../../../knowledge/label/labels/category.md#the-rules) - Reference: a category keeps no `protocol/` of its own
- Tasks:
  - main:.agents/tasks/20261024-T160310Z-25344/: Partial - the file moved from `memory/protocol/version.kh` and the twenty-three importers were repointed
- Contributors:
  - An AI agent (Claude, model claude-sonnet-5-5 as reported by the runtime; no CONTRIBUTORS.md entry) — decided the fate within the moves task's list of importers, wrote the document; no `approved` is recorded

#### What changed
- `version.kh` moved unedited to `protocol/version.kh` of this module; the kernel importers and the pluggable ones name its new path.
- The document states why the module stays kernel and when it is retired.

#### Considered and not done
- Moving it to a pluggable module: three kernel files import it, and that is a back edge.
- Dropping it with the record contract's lack of versions: the importers still declare it; they go first.
