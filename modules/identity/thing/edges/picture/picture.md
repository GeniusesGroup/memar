# Picture rating

## Model

- Candidate (unconfirmed): a rating label on the thing's picture — a 0–3 `PictureRating` scale attached to the object's picture (source is `package label` holding only the scale comments — no edge code).
- Distinct from *which* picture is the object's ([object](../object/object.md)) — this edge rates the picture's content.

## Policies (rules)

- `0`: "Suitable for display on all websites with any audience type."
- `1`: "May contain rude gestures, provocatively dressed individuals, the lesser swear words, or mild violence."
- `2`: "May contain such things as harsh profanity, intense violence, nudity, or hard drug use."
- `3`: "May contain hardcore sexual imagery or extremely disturbing violence."
- No who-may-set/what-it-triggers recorded — the label must not be ratified as an edge until those exist (no bare edges).

## Placement

- **The structural label stays here** — which depiction is the thing's picture, and what marks it, is object identity; same family as [icon](../icon/icon.md) and [object](../object/object.md) (prefer the existing home — thing already owns its object labels).
- **Enforcement is not thing's:** "suitable for all audiences" is policy — core never knows Rule. A filtering capability that *acts* on the rating (the knowledge/content claim in the standing review) lives with that capability or the rules engine; thing carries only the structural label the evaluation reads.
- The 0–3 scale is a value list, not processing semantics (parameters vs semantics): one vocabulary as configuration — never grounds a new module; per-jurisdiction variants are rule configuration over the same edge, not second vocabularies.
- Not analytics — nothing here is a discovered/derived query (analytics is always pluggable; does not apply).

## Open questions

- Does content rating belong to knowledge/content instead of thing? — answered above: the label attachment rides the picture here; any *use* of the rating moves with the capability that uses it.
- Is the 4-level scale one vocabulary, or per-jurisdiction policy (rule configuration over one edge)?
- Who may set the rating, and what does setting it trigger (no bare edges)?
- Rating vs assignment: does this converge with `UserPicture`/`UserPrimaryPicture` ([object](../object/object.md)) — one picture edge with a rating field, or two edges (parameters vs semantics)?
- Direction and naming unconfirmed — nothing ratified.

