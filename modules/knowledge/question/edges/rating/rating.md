# Rating

## Model

- Candidate (unconfirmed): rating scale label vocabulary — the source recorded only `labels:` followed by five bare labels (see [Source](#source)); attachment presumably rides the rating edge's labels field ([rating-labels](../rating-labels/protocol/data_model.kh)).
- Sibling scale structures already in this folder: `Type_LikertScale_Emoji` / `Type_LikertScale_Color` / `Type_LikertScale_Range` / `Type_Star` / `Type_Number` in [dt-type.kh](protocol/dt-type.kh).

## Policies (rules)

- No rules recorded in the source — five labels only; how a scale binds (all five, subset, order) is unconfirmed.

## Placement

- **Correct here — home is the rating edge in `question/edges/rating`.** The rating capability already keeps edge and processing together in this folder (data model, scale types, storage); the five labels are a *parameter* vocabulary for that edge, not processing semantics — parameters-vs-semantics ⇒ one rating capability plus per-organization label configuration, no new module.
- Not the rule domain: the scale does not decide who may rate or what a rating triggers; where such decisions appear they stay generic rule attachments (core never knows rule).
- Label identity follows [label](../../../label/label.md): names are labels, UUIDs are identity — these five strings are candidate label names, never behavior bindings.

## Open questions

- Which scale family consumes these five labels — the verbal Likert ladder (vs the emoji / color / range / star / number siblings in this folder)?
- Closed kernel vocabulary or organizational-open (org-defined scales)?
- Relation to the `Type_Rating` answer-shape flag in `question.go (no such file yet)` and the standing review in [question.md](../../question.md)?
- Is the ordering (Worse < Bad < Normal < Good < Excellent) stored on the edge, or derived from label configuration?

