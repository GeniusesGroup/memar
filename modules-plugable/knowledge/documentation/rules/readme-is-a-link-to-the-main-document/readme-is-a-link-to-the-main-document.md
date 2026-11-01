---
Title: "Documentation Rule — A README Is a Link to the Main Document"
Start Date: 2026-11-01
---
# Documentation Rule — A README Is a Link to the Main Document
A rule of this repository, held for [Documentation](../../documentation.md), which owns the claim in [A README Points; Content Gets a Document](../../documentation.md#a-readme-points-content-gets-a-document). This rule states the check applied to every README a change creates, moves or rewrites.

## The rule
- **A folder that has a main document takes its `README.md` as a symbolic link to it.** The main document is the one that states what the folder is for. A folder of peers, of companions to documents held elsewhere, or of code has none, and its README is a real file carrying content of its own, without restating what the files already say.
- **Content moves before the link replaces the file.** What the README says that belongs to the main document (what the folder is for, the criterion for what belongs in it) moves into the main document; what the main document does not own (where a reader goes next, a note no single document holds) stays.
- **The link's target is the main document's file name, resolved from the README's own folder,** and git records it as mode `120000`. A text file that names its target is a text file that points at a sibling, not a link, whatever it says inside.
- **A bulk edit skips every path of mode `120000`.** On a host that keeps each link as a small text file holding its target with no final newline, a pass that adds final newlines, normalizes line endings or rewrites links turns the target into a name that does not exist.
- **A README has no companion,** and a decision about a folder (its criterion, its layout) is written in the README as the rule it now is.

Where the filesystem refuses the link, it is recorded in the index with `git update-index --add --cacheinfo` at mode `120000`, the file's content being the target path with no trailing newline, and `git ls-files -s` reports `120000` for it.

## Why it exists
On 2026-10-18 one such pass added a final newline to 89 links in the organization repository, and each pointed to a name that did not exist. A README that is a copy of the main document drifts from it, and a README that is a link cannot.

## Keep it or drop it
An organization may keep a real README beside a main document. It then keeps what the folder is for in two files, and the two disagree after the first edit of either.

## What this rule does not claim
- It does not say which document is a folder's main document when two compete; the reader who wants to know what the folder is for decides.
- It does not require a link on a host that cannot hold one; the index records it.
