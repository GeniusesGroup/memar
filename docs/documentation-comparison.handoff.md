# Documentation — Comparison Handoff

## Open Questions
- **The symlink's staged mode must survive the commit.** This repository has `core.symlinks = false`, so the working-tree file for `docs/comparisons/README.md` is the target path as plain text, and a plain `git add` of that path records it back as a regular file. The entry is staged with `git update-index --cacheinfo 120000,<blob>,docs/comparisons/README.md`; whoever commits must re-assert that mode before committing, or the symlink silently becomes a two-line stub.
- **`content check docs` reports a false problem on the symlink.** It reads the target path as text and reports "no newline at end of file". Adding a newline to satisfy it would break the link. It is the first symlink under `docs/`, so no earlier check pass saw it; a session that treats the report as real will "fix" it.
- **The four dated method requirements have never been applied to an essay.** They apply from 2026-10-07, and every essay in `docs/comparisons/` predates them. Whether an existing essay should be brought under them — which means editing a record its own rule calls its own record — is undecided. The disclosure quota is the one that would change the most: it asks each essay to say what it could not verify, which four of them currently answer in the opposite register.

## Next Steps
- Re-read the four essays written before 2026-10-07 against [Method requirements added by practice](./documentation-comparison.md#method-requirements-added-by-practice) and decide, per essay, whether to correct in place or to leave the record as it stands.
- The critique that shaped this document proposed additions that were declined for cost rather than on principle: an approval line in the required shape, a sharper test for rule 4, and folding the standing-principles list into the numbered obligations. Revisit when a comparison is written that needs them.
