# Comment Handoff

## Topic & Purpose

State of converting the comment edge — `modules/knowledge/content/edges-loop/comment/protocol/` — from Go to Khayyam under the seven governing rules in [`../../../../../Khayyam.practice.md`](../../../../../Khayyam.practice.md). The domain is one file and one requirement; what is recorded here is the identity decision, the placement question the Phase 0 review left open, and what the edge does not yet say.

## Status

Active — `protocol/dt-uuid.kh` is converted and returns `accept` from the Khayyam frontend against a root where the import roots resolve.

## Decisions

- **Decided: a comment is a content, so this edge declares no UUID of its own.** `protocol/dt-uuid.kh` includes `ThingUUID` from the thing domain rather than declaring a `CommentUUID`. Reason: the Go source wrote `type UUID content_p.UUID`, and `content_p.UUID` is `thing_p.UUID`, which is `record_p.UUID` — one identifier, already owned by `thing/protocol/dt-uuid.kh` and stated there as "MUST be unique ID in all domains". A second value abstraction over it would be two abstractions claiming one concept. This is the same collapse `text`, `time`, `uri` and `calendar` took. Every `comment_p.UUID` in the tree — `content/widgets/pin`, `content/widgets/reply`, `content/widgets/group` — is this same identifier and now spells it `ThingUUID`.
- **Decided: `Field_CommentID` keeps its Go name and gains the accessor `CommentID`.** Unlike the label protocol, no rename was owed: the Go name was already `Field_CommentID`, the `…ID` suffix is the one this repository's converted files use, and bare `CommentID` is unclaimed in the corpus. The result parameter is named `t`, after the type, per the result-parameter-names rule.
- **Placement, settled by the evidence rather than by this conversion.** The migration map's Phase 0 review left "comment (knowledge vs content)" open. The tree answers it: this edge lives under `content/edges-loop/`, and it is a loop-edge because a comment may reply to another comment in the same group — `content/widgets/reply/protocol/data_model.kh` writes `ReplyTo() comment_p.UUID` with the note that a comment can be a reply to another comment only in the same group. `modules/knowledge/content/content.handoff.md` records the decision behind that: "Comment is not an independent entity — Content + a `reply_to` relation." A comment is therefore a content carrying a relation to another comment, which is exactly what a loop-edge over content is, and the `content` home is the one that follows.
- **Rule 6, recorded rather than papered over:** `Field_CommentID` is an empty `ab`. It is faithful to the Go source, and it is the shape rule 6 calls a design smell — the domain states one requirement and no behavior. What the domain needs and does not declare: the behavior of a comment as a content — being written, edited, hidden, deleted, and read in the order a discussion shows them — and the authority over each. None of that is here, and `comment.md` is two lines of dictionary. This is a real gap in the domain document, not a conversion defect.

## Ambiguities Resolved

- Whether the comment identifier and the content identifier are two concepts: one. The Go chain `comment_p.UUID` → `content_p.UUID` → `thing_p.UUID` → `record_p.UUID` ends at the storage record UUID, and every link in it is a restatement rather than a new concept.
- Whether `CommentID`'s receiver should be the abstraction or a data model: the abstraction, as Go had it. `content/widgets/protocol/widget.kh` composes `Field_CommentID` directly, so the requirement has to stand on its own.

## Open Questions

- **What makes a comment a comment?** The domain document carries only the linguistics entry (topic and comment, rheme and focus). Nothing states the difference between a comment and the reply to it — both are contents with a `reply_to` relation, and nothing says which end is which. `content/widgets/reply` and `content/widgets/pin` both carry `Field_CommentID`, so the two are the same node kind and the distinction has to live in the relation, not in a type.
- Is the ordering of a discussion part of the comment, or a property of the group? Nothing in this edge answers it, and `content/widgets/group/protocol/data_model.kh` is where an answer would be read from.
- May a comment be a reply across groups? The Go note says "just in the same group", which reads as a decided rule; whether anything enforces it is undeclared.

## Assumptions

- **`ThingUUID` is the name the thing domain declares** — stability: Strong. `modules/identity/thing/protocol/dt-uuid.kh` is already converted and declares it.
- **The `org/` and `memar/` import roots resolve through a manifest that does not exist in this repository** — stability: Strong, and named as the hard gate by rule 7 of the migration map. Run against the checkout as it stands, every converted file refuses `unresolved-import` for that reason alone.
- **`Field_CommentID` is the name the content widget domains will import** — stability: Strong for the surface, since fifteen files already compose `comment_p.Field_CommentID` by that name in Go and none of them has been converted.

## Proposed Next Steps

1. Write the behavior of a comment as a content into `comment.md`, and give the edge a requirement beyond its identifier, which is what rule 6 asks for.
2. Decide the ordering and the same-group rule for replies, and record them on the edge or on the group.
3. Convert the content widget domains that compose `Field_CommentID` — `group`, `group-user`, `log-activity`, `mentioned`, `object`, `pin`, `reply`, `tag`, `user_status` — plus `modules-plugable/gui/page-discussion/` and `modules/knowledge/text/widgets/text/`, the two consumers outside the content domain and the last of which was waiting on this file.

## Related Artifacts

- [`../../../../../Khayyam.practice.md`](../../../../../Khayyam.practice.md) — the seven governing rules. The Phase 0 review that carries the placement question this handoff settles is in [`../../../../../Khayyam.handoff.md`](../../../../../Khayyam.handoff.md).
- [`comment.md`](comment.md) — the domain document; two lines, and the reason the behavior above is missing rather than merely unconverted.
- `modules/knowledge/content/content.handoff.md` — records "Comment is not an independent entity — Content + a `reply_to` relation".
- `modules/identity/thing/protocol/dt-uuid.kh` — the owner of the identifier this edge includes.
- `modules/knowledge/content/widgets/reply/protocol/data_model.kh` — where the reply-to-another-comment relation is written, and the evidence that this edge is a loop-edge.
- `modules/knowledge/text/widgets/text/protocol/gui-widget.kh` — a consumer of `Field_CommentID` outside the content domain.

## Notes

- The frontend was run through `node modules/khayyam/targets/go/frontend_check.ts` against a root built by copying every `.kh` of this repository into `org/` and every `.kh` of the memar repository into `memar/`, preserving relative paths. `protocol/dt-uuid.kh` returns `accept`.
- `modules/knowledge/text/widgets/text/protocol/gui-widget.kh` was checked by override against this file to confirm the exported name is the one it asks for; it accepts. That override is a check, not an edit — the file belongs to another domain and was not written here.
- The Go source of this file carried no comments, so rule 5's extraction pass had nothing to move into `comment.md`; the gap that pass would have exposed is recorded above instead.
- The `// TODO(go-migrate):` block is left in place, per the conversion brief and memar's `go-clue-residue` rule.
