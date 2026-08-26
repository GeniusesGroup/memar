# Implementing Chapar Changelog

## Changelog

### Created the Practice companion for Chapar
- Time: 2026-08-26T05:29:13Z
- Type: added
- Cited:
  - [Chapar - Data Link Protocol](./chapar.md) — Depends_on: every step in this file restates normative behavior defined there; the procedures are meaningless without it.
  - [Documentation — Practice](./documentation-practice.md) — Reference: the schema followed (name/description-only front matter, imperative style).
- Propagates to:
  - chapar.md: Done — the practice file derives only from behavior already normative there; nothing needed to change in the spec.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — requested: specified the four-file structure (`<base>.md`, `<base>.practice.md`, `<base>.changelog.md`, `<base>.practice.changelog.md`) as part of migrating the Chapar documentation to the current method.
  - [ox-alpha](../CONTRIBUTORS.md#ox-alpha) — wrote: derived and authored the procedures.

#### Summary
Created `chapar.practice.md` alongside the consolidated base specification during the same consolidation that merged the four companion documents into `chapar.md`. Its content is an imperative restatement of behavior that was already normative in the spec (switch frame processing, endpoint Unicast sending, Discovery participation, ChaparKhane path composition, and known failure modes); it introduces no new semantics, so the base document required no change.
