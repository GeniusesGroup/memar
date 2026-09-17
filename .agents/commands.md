# Commands
Commands are recorded as ready-to-paste invocations. Each carries the one-line "why" so a future session does not have to re-derive it. Paths are relative to the repository root.

- list of files and directories: `tree /F /A`
  Windows `cmd` built-in: `/F` includes files (not only directories), `/A` uses ASCII box characters so the output pipes cleanly into logs and agent tool output.
- `git mv {source} {destination}`
  For files **already tracked by git**, move/rename with `git mv`, never with a plain `mv` (or Explorer): `git mv` records the rename in the index so `git log --follow` keeps the file's history attached across the move. Commit the rename **by itself** — a commit containing only renames, so the diff is a pure `R` rename with no content changes mixed in — and apply any content edits afterwards as separate commits. A rename-plus-edit in one commit defeats rename detection and orphans the history.
- `[math]::Truncate([DateTimeOffset]::UtcNow.ToUnixTimeSeconds() / 3600)`
  PowerShell: whole hours since the Unix epoch — a coarse, collision-free timestamp for cache keys and temp-folder names that stay valid within the hour and expire deterministically.
- Batch rename `Get-ChildItem -Filter *.md | ForEach-Object { git mv $_.Name "docs/$($_.Name)" }`
  PowerShell: moves every `*.md` of the current directory into `docs/` through `git mv` (same history rule as above). Run in the source directory; dry-run first by replacing `git mv` with `Write-Host git mv` if the file set is uncertain.
- Resolve Memar root (clone-or-reuse, prints path): `python .agents/skills/memar/scripts/memar-root.py` (add `--update` to pull)
  Prefer a local checkout: `--root PATH`, or `$MEMAR_ROOT`, or a sibling folder named `memar` next to the current project (e.g. `.../memar` beside `.../organization`). Temp clone is last resort.
- Resolve doc refs: `python .agents/skills/memar/scripts/memar-doc.py path docs/cognition.md` (bare names are MSYS-safe; `--from docs/system.md` for document-relative links)
- Judge relevance cheaply: `python .agents/skills/memar/scripts/memar-doc.py meta docs/framework.md` (front matter + Abstract)
- Extract one section: `python .agents/skills/memar/scripts/memar-doc.py section docs/framework.md "Goal-Oriented Frameworks and Purpose Space"`
- Full-text search: `python .agents/skills/memar/scripts/memar-doc.py search "polymorphism"` (extra args = extra regexes, all must match)
  The two bundled scripts own all Memar-document resolution and search; prefer them over hand-written `git`/`grep`/`rg` incantations. If Python is absent, read the script source and reproduce the step — see the skill's [Documentation navigation](skills/memar/SKILL.md#documentation-navigation) section.
