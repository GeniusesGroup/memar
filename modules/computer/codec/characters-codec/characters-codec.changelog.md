# Characters Codec Changelog

## Changelog

### Characters and octets are not numeric widths
- Time: 2026-09-29T11:17:00Z
- Type: Added
- Cited:
  - [Math Handoff → Does the tower hold widths the reference does not declare?](../../../math/math.handoff.md#does-the-tower-hold-widths-the-reference-does-not-declare) - Premise: owner ruling item (e) on byte, rune, and character abstractions.
- Contributors:
  - Auto (model not recorded) via [Cursor](../../../../CONTRIBUTORS.md#cursor) - applied

#### What changed
- `characters-codec.md`: new section stating that characters and octets are not numeric widths and naming the existing character abstractions in the sources.

---

### The body's open state moved to a handoff
- Time: 2026-10-05T17:39:20Z
- Type: refactor
- Propagates to:
  - characters-codec.handoff.md: Done - created; it carries the two items the retired `## Still considering` section held and the disagreement between `## Encoding` and `## Goals` over the maximum effective-byte count
- Contributors:
  - [Space Bunny Alpha](../../../../CONTRIBUTORS.md#space-bunny-alpha) (space-bunny via [OpenCode](../../../../CONTRIBUTORS.md#opencode)) - argued, applied

#### What changed
- `characters-codec.md`: the `## Still considering` section is removed from the body, heading and both bullets with it. Its two items move to the new `characters-codec.handoff.md` as questions: whether some ASCII codes may be reused for other characters, and whether each human language needs a number character.
- The body's internal disagreement is not stated as such anywhere in the document: `## Encoding` concludes that 4 effective bytes are enough and that more are not needed, while `## Goals` says the same reach and then that the system "can use for more than 4 bytes and can increase to n bytes", and the Self-synchronization goal's "backing up at most 3 bytes to find the leading byte" holds only under the first of those. That disagreement moves to the handoff as its own question, together with what its absence leaves undefined - no rule states a maximum, so a decoder's obligation is undefined. The three sections that carry the disagreement keep their own text; the resolution, when it comes, is what will change them.
- `characters-codec.handoff.md` is created: a plain H1 title in the base document's own form (`Harf - Character Codec Handoff`), one line of what it is open work for, and an `## Open Questions` section carrying all three items, each with `State:` and `Next:`.
- The body's remaining sections, `## Encoding`, `## Compression`, `## Goals`, `## Non Goals`, `## Characters and octets are not numeric widths`, and `## Others`, are unchanged.

#### Considered and not done
- **Rewriting the body's `## Encoding` and `## Goals` sentences so they agree (not done)**: which cap holds is the open question itself, and choosing one here would answer it without a ruling. The handoff names both texts as they stand so the next chat sees the disagreement in the words rather than in a summary of it.
- **Adding a `Status` or `Anticipated Work` section to the new handoff (not done)**: the handoff carries one section because it has one category of state, and per the handoff facet an empty header is never left in place.
- **Renaming the base document's H1 to match this changelog's title (not done)**: the changelog names the artifact by its filename while the body names itself `Harf - Character Codec`; the handoff follows the body's own title, which is what the handoff facet's format rule keys on, and reconciling the two names is a separate question.

---

### Review of the uncommitted changes of 2026-10-12
- Time: 2026-10-12T09:45:50Z
- Type: Reviewed
- Contributors:
  - [Claude](../../../../CONTRIBUTORS.md#claude) (Sonnet-5.5) — reviewed

#### What changed
- Reviewed; no change needed. Checked the uncommitted change of this family: the body's open state moved into the new `characters-codec.handoff.md` (three questions). Verified against the base document and the commit that made it: the `## Still considering` items are present in `6739e67` verbatim in substance and absent from the current body; the cap disagreement is real (`## Encoding` says four bytes suffice, `## Goals` says it can grow to n bytes, the self-synchronization goal's 3-byte backup holds only for four); the handoff's quotes match the body. The earlier changelog entry's `corpus` became `sources` (the repository's current term for the `.kh` tree); kept as a vocabulary update. `syllab.md` has no changelog of its own; its `DataTypeID` to `TypeID` rename follows the Type family rename and is consistent within the file.
