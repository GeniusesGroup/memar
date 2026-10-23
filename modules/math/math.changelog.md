# Math Changelog

## Changelog

### Initial Draft — the number tower protocol
- Time: 2026-09-29T11:17:00Z
- Type: Added
- Cited:
  - Encapsulation in Khayyam → Primitive Capsule Specification (`docs/khayyam/encapsulation.md#primitive-capsule-specification`) - Premise: numeric tower content belonged at the protocol layer, not in the language document.
  - Encapsulation in Khayyam Handoff (`docs/khayyam/encapsulation.handoff.md`) - Premise: numeric open questions and owner notes carried from the memar-go port session.
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) - decided: implementation and protocol-domain content must not live under `docs/khayyam/`
  - Auto (model not recorded) via [Cursor](../../CONTRIBUTORS.md#cursor) - applied

#### What changed
- `math.md`: initial Draft with the number tower (`I`/`W`/`R`), complex and platform-sized exceptions, and realization membership (from `modules/math/README.md`).
- `math.handoff.md`: numeric open questions, the owner's earlier notes, the `Bool`/`Boolean` question, and numeric implementation residue, moved from Khayyam handoffs and the deleted module documents.
- `modules/math/README.md`: replaced with a symbolic link to `../../docs/protocols/math/math.md`.

#### Considered and not done
- Keeping tower rules in `encapsulation.md`: rejected; they are protocol-domain, not Khayyam grammar.

---

### The research record's Participants corrected to the systems that did the work
- Time: 2026-10-05T10:56:50Z
- Type: Fixed
- Propagates to:
  - [Math Research 001 → Participants](./math.research.001.md#participants): Done — the section names the delegating party and the sub-agents it delegated to, and the sentence claiming the session's runtime exposed no sub-agent facility is gone.
- Contributors:
  - [Space Bunny Alpha](../../CONTRIBUTORS.md#space-bunny-alpha) (space-bunny via [OpenCode](../../CONTRIBUTORS.md#opencode)) — argued, applied

#### What changed
- [Math Research 001 → Participants](./math.research.001.md#participants): the paragraph headed "Sub-agent roles: none convened", which stated that the session's runtime exposed no sub-agent facility and that the bounded-exploration work was therefore carried in the main session, is replaced by a participant entry for the sub-agents of [Space Bunny Alpha](../../CONTRIBUTORS.md#space-bunny-alpha) who took part in it, in the role the memar skill's session-economy section reserves for delegated scanning.
- The `Researcher` entry now records Space Bunny Alpha as the party that delegated, and the sub-agent entry names the work they carried — the scans this record reports and the declaration-level reading under [Methodology](./math.research.001.md#methodology) — and records that their output entered the record as reports the delegating party merged and checked against the passages behind them. The facet requires one entry per participant who took part and makes the reviewer's outcome explicit; naming no sub-agent left the record's own account of its method unexaminable ([Documentation → Research → Participants](../knowledge/documentation/research/research.md#participants-mandatory)).
- The questions, the goals, the findings, the open questions, and the status are unchanged: the record stays `Active`, because an `Active` research is a mutable working record and a false statement about who took part is a repair of that record, not a revision of what it found.

---

### Review of the uncommitted changes of 2026-10-12
- Time: 2026-10-12T09:47:00Z
- Type: Changed
- Contributors:
  - [Claude](../../CONTRIBUTORS.md#claude) (Sonnet-5.5) — reviewed, revised

#### What changed
- Reviewed the uncommitted change to this changelog (the *Participants corrected* entry), `math.handoff.md` (the new entry on `modules/math/per/`), and the new `math.research.001.md` (read whole). The links and anchors resolve (`memar content check`).
- `math.handoff.md` → *Every type under `modules/math/per/` is a bare abstraction*: the entry said the archives give every type a symbol method and that the sign survives only in the comments at `cent.kh:3` and `myriad.kh:3`. The files show a `Calculate` receiver for all nine types (Go archive), a `Symbol` method only for `Cent` and `Myriad` (JS archive), and a sign comment on line 3 of every file; the entry now says so.
- `math.research.001.md`: about a dozen line citations were one line off against the files as committed (`signed.kh`, `hash.kh`, `unsigned-8.kh`, `signed-16.kh`, `float-64.kh`, `equivalence.kh`, `adt-container-index.kh`) and are corrected; `per-mille` is `mille`; the record's `protocols/README.md` labels and `docs/protocols/math/` now name `modules/README.md` and `docs/modules/math/`, with the census and the symlink's former content marked as taken before the folder's rename; the Participants entry's reference to a "session-economy section" of the memar skill, which the skill no longer has, now says its delegation rule.
- The *Participants corrected* entry above still names that "session-economy section"; it is history and is left as written.

#### Considered and not done
- **Re-running the census of base documents per folder (not done)**: the record dates it to its scan, and a count of the renamed tree would be a new finding, not a correction.
- **Rewriting the research's status language ("which this chat is not to edit")**: left; it states that record's own session constraint, and the record stays `Active`.
