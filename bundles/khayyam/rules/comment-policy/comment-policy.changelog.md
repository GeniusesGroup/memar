# Khayyam Rule — Comment Policy Changelog

## Changelog

### The documentation fallback is retired: no comment in Khayyam code
- Time: 2026-10-30T12:00:00Z
- Type: Changed
- Ruling: owner, 2026-10-30
- Tasks:
  - 20261026-T200841Z-21460: Complete - the task that moved the comment ban to Type.
- Contributors:
  - [Omid Hekayati](../../../../CONTRIBUTORS.md#omid-hekayati) - decided
  - [Claude](../../../../CONTRIBUTORS.md#claude) (Sonnet 5.5 via Claude Code) - applied

#### What changed
- [The rule](./comment-policy.md#the-rule): the bullet that allowed documentation in comments where no documentation method exists is removed, and the bullet on a type's human-facing text points at the Type rule that owns the ban. The license header stays.
- The handoff's open question on when the clause expires is closed as a decision.

#### Considered and not done
- **Rewriting the ported sources' comments now.** Not done: they are repaired when a task changes a file, as the Type rule says.

### One blank line after the license header, and the header on every source file
- Time: 2026-10-10T08:20:00Z
- Type: Changed
- Ruling: owner, 2026-10-10
- Contributors:
  - [Omid Hekayati](../../../../CONTRIBUTORS.md#omid-hekayati) - requested, decided
  - Auto (model not recorded) via [Cursor](../../../../CONTRIBUTORS.md#cursor) - applied

#### What changed
- [The rule](./comment-policy.md#the-rule): the `.kh` bullet names the header text and requires it on the first line followed by exactly one blank line before anything else. A new bullet extends the header to the repository's other source files in any language — the same text in that language's comment syntax, as the first line after only a line the language or the operating system requires first (a shebang, a Python encoding declaration), followed by one blank line; a format with no comment syntax carries none. The opening sentence covers those files, and [Why it exists](./comment-policy.md#why-it-exists) gives the blank line's reason: readability, the header set apart from the content.
- The repository was brought into line in the same change, touching only each file's head and keeping its line endings, byte-order mark, and every byte after the head: 71 `.kh` files gained the blank line, and 170 code files gained the header and the blank line — 102 `.ts`, 54 `.py`, 4 `.mjs`, 3 `.js`, 2 `.sh`, and one each of `.ps1`, `.cmd`, `.bat`, `.s`, and the extensionless Python launcher `.agents/scripts/memar`. The syntax is `/* … */` for `.kh`, `.ts`, `.js`, and `.mjs`; `#` for Python, shell, and PowerShell; `@REM` for `.cmd` and `.bat`, placed before `@echo off` so it is not echoed; and `//` in the Go-assembly `.s` file, the form that file already used.
- `.agents/scripts/install.sh --help` printed the comment block from line 2, which is now the header; it prints the block after the header's blank line instead.

#### Considered and not done
- **The header above a shebang.** Not possible: a shebang works only as a file's first line, so the rule lets it, and a Python encoding declaration, come first.
- **The PowerShell header inside the comment-based help block.** Not needed: a `#` line and a blank line before `<# .SYNOPSIS #>` leave `Get-Help .agents/scripts/install.ps1` showing the same synopsis and parameters.
- **A header in data and configuration files** (`.json`, `.code-snippets`, `.yaml`, `.freebuff/project-id`). Not done: they are data rather than source, and JSON has no comment syntax.

#### Surveyed
- Generators that write code into this repository: the Go porter (`targets/go/transfer.py`, `targets/go/corpus_port.py`) already emits the header followed by an empty line; the JavaScript target emits into a build cache outside version control; the editor extension's writer emits JSON only. No output template needed a change.
- Code carrying another license: none outside `node_modules/`.
