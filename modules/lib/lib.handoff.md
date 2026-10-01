# Lib Handoff

Open work for `lib.md`. Entries are mutable current state — revised as each item moves, removed when it resolves or is dropped. See the repository's [documentation-handoff.md](../../docs/documentation-handoff.md) for what a handoff is.

## Decisions
- **The module's root is `lib/`, and the old `libgo/` root is gone** — Decided (owner, 2026-09-26). The whole tree moved to `modules/lib/` and every `in` address beginning with the old root was rewritten (18 addresses in 9 files). Reason: the old name said "Go's libraries", which named an implementation and claimed nothing about authority; the module holds Khayyam realizations of foreign protocol surfaces and no Go, so the name was the wrong claim. Rejected: keeping `libgo/` as a second root and moving nothing; renaming to `foreign/`, which lengthens the most common address for a word the rule already defines.
- **The moved tree's `net/` level lands inside the existing `modules/lib/net/`, not beside it** — Decided (owner, 2026-09-26). `modules/lib/net/` existed and was empty, and the tree carried its own `net/http/` and `net/soap/`. Placing them inside gives one `net` in the tree; placing them beside would have produced `lib/net/http/` and `lib/net/soap/` beside a folder named the same thing, which is the one outcome the tree cannot afford. Reason: two folders with one name at one level is not a decision anyone can read. Rejected: deleting the empty `modules/lib/` and moving the tree wholesale, which is the same shape as the move above and one step longer.
- **The second level is a Memar category name, and that is left as it is** — Decided (owner, 2026-09-26) for the move only. The tree's internal structure is preserved: `codec/`, `net/`, `process/` came with the move and were not restructured, so every address under the new root is the old address with a shorter prefix. Reason: the owner asked for the tree to move with its structure intact; whether that structure is also the right long-run shape is the open question below, and deciding it inside the same change would have made the move unverifiable. Rejected: flattening to `lib/json/`, `lib/http/`, `lib/soap/` in the same pass.

## Open Questions

### Should `lib/` group foreign protocols under a Memar category, or sit flat?
- State: the module's rule says the path itself must carry the claim "this exists here, but it is not Memar's", and the second level undercuts half of that claim. `modules/lib/codec/json/` reads as *a codec's JSON* — and `codec` is Memar's own category, with its own abstractions in `modules/codec/protocol/codec.kh` that JSON realizes. `modules/lib/process/command/` has the same shape. Against that, the category grouping is not decoration: it says what the foreign surface attaches to, and an ungrouped `lib/json/` says nothing about why JSON is in the module at all.
- The question: is the second level allowed to name a Memar category, and if so does the path still say what the rule says it says? Three answers are open: keep the grouping and let the rule claim the *leaf* only; drop the grouping and name only the foreign protocol under `lib/`; or invert it, `lib/<category>/<protocol>/` where the category is a tag of the foreign world rather than of Memar. Nothing in the corpus depends on the answer — all 18 addresses under the new root are internal and would be rewritten in one pass whenever it lands.
- Blocks continuation: yes for any *new* foreign protocol, which would otherwise be filed by copying the shape that is under question.
- Path: owner ruling. The [main document](./lib.md) records the shape as it stands and says plainly that it is unsettled.

### Is the minifier a foreign protocol, or a codec capability?
- State: `codec/minify/protocol/minify.kh` came in with the move and is the one item in the folder the rule does not obviously cover. It declares `Minify_Minifier` with a `Minify` method over a `Codec` — a capability any implementation may provide, and not a contract any outside world defines and enforces. Its neighbours in `modules/codec/compress/` share the shape and are not here, which is a second reason to doubt the placement: if minification is a codec capability, the category that owns codecs is where it belongs, and `lib/` is holding a Memar concern.
- The question: does "a protocol that is not Memar's own" reach a transformation no outside world specifies? Two things any answer meets: a minifier's *contract* is the outside world's when the format being minified is one the world defines, and Memar's own when the transformation is a general capability over any codec; and the module's rule cannot both admit this file and refuse `modules/codec/compress/`, which is the same kind of thing one folder over.
- Blocks continuation: nothing in code. It blocks only deciding where the next transformation-shaped abstraction is filed.
- Path: owner ruling, then either a move to the owning category or a stated reason this one is different. Until then it stays where the tree put it, and the [main document](./lib.md) marks it contested rather than claiming it.

### Two `Stringer` shapes and two length shapes
- State: the move created, or rather exposed, a duplication the old name had been hiding. `modules/codec/string/protocol/stringer.kh` declares `Stringer`, `Stringer_To`, and `Stringer_From`; `modules/lib/codec/string/protocol/stringer.kh` declares the same three shapes as `Codec_Stringer`, `Codec_Stringer_To`, and `Codec_Stringer_From` — same method signatures, same comment, different names. The old root's own name was the reason for the prefix: a mirror needed to mark itself as a mirror, and the prefix is that mark. Under the new root the mark is the path, so the prefix has nothing left to do. The same holds for length: `modules/codec/protocol/length.kh` declares `Field_Codec_Length` and `modules/lib/codec/json/protocol/length.kh` declares `Field_JSON_Length`.
- The question: one shape or two? If JSON's length is a distinct contract from a codec's length, the two are right and the distinction needs arguing. If it is the same contract seen from the format that requires it, one declaration is right and the second address is the cost of the duplication the module is here to end.
- Blocks continuation: yes for any name that collides with the shape it duplicates — every such name is currently kept distinct by prefix, and the prefix is now unmotivated.
- Path: read the two `length.kh` files against each other and decide whether JSON's constraint is the codec's constraint. This is a corpus question, not a placement question, and how the surviving declaration is named is the [qualified names rule](../khayyam/rules/qualified-names/qualified-names.md#when-qualification-cannot-separate-two-declarations)'s.

### The timer's import address, which the move did not fix — and a later edit did
- Resolved (2026-09-27, checked against the files). `modules/time/timer/protocol/timer.kh` now names `modules/time/timer/protocol/listener.kh` — the timer's own listener file, at its real path — and imports nothing from this module. The M1 frontend accepts the file, where before the move and after it the frontend refused it `unresolved-import`. The move itself is not what fixed it, and the record of the move is what this entry first said: at move time the mechanical rewrite carried both addresses to `modules/lib/time/timer/protocol/listener.kh`, which resolved to nothing, exactly as the old `libgo/…` addresses had. The correction was a separate edit in the time module's file, which this module's move was not entitled to make.
- What is not in dispute, and is the reason the entry is kept: a Memar subject was reachable at a second address, and the address that survived the move was the wrong one. That is the clearest single piece of evidence for the rule this module states.
- Blocks continuation: nothing. The file resolves, and the question the entry carried — whether the address is corrected here or as a separate change — was answered by the separate change.

### Names outside this module that a foreign protocol has already claimed
- State: this module holds HTTP, JSON, and SOAP, and the corpus holds other surfaces the outside world also owns — under other names and in other categories. If the rule in [the main document](./lib.md) is the repository's rule and not only this folder's, those are the same kind of thing filed as Memar's own. Nothing was moved, and nothing under `modules/khayyam/` was touched. What the survey found is recorded as a report to the owner rather than as a claim, because whether each is Memar's own is a judgment about authority that the module's membership criterion does not settle on its own.
- The question, per item: does this surface's contract change only with Memar's agreement?
- Blocks continuation: no. It blocks nothing in this module; it decides whether the rule grows beyond this folder.
- Path: owner ruling per item, then one move each or one argument that the item is Memar's own. Listed in the report accompanying the move.

## Anticipated Work
- A `.kh`-level check that a folder under `lib/` is not duplicating a subject a Memar category already owns — the duplication the prefix was hiding, made structural. Nothing in the toolchain can decide authority, so such a check can only report the collision, not rule on it.
- Whatever an ungrouped `lib/` needs so that a foreign protocol can be filed without a second address being invented for it.

## Assumptions
- **The corpus's only realization language here is Khayyam** — Stability: Strong; every `.kh` source under this folder is Khayyam and the toolchain here is Khayyam's. What changes it: a second realization language adding sources under `lib/`, which would make the same duplicate-name problem a per-language one.
- **"Authority is outside this project" is a workable test for membership** — Stability: Weak. It decides the clear cases — HTTP, JSON, SOAP — and it is untested on a transformation-shaped abstraction like the minifier, which the criterion may not reach at all. What changes it: the first subject filed under `lib/` that no outside world specifies.
- **A path can carry the claim "not Memar's"** — Stability: Unexamined; the claim is the module's reason for existing and it rests on the second level naming foreign things, which the open question above puts in doubt. What changes it: the ruling on grouping, and whether the leaf alone is judged to carry it.

## Related Artifacts
| Artifact | Relation | Action |
| --- | --- | --- |
| [`lib.md`](./lib.md) | Base — the module's subject and its placement rule | Its contents table names the contested items; edit it when one is ruled on |
| [`README.md`](./README.md) | Reference — the folder's pointer | None |
| [`../README.md`](../README.md) | Depends_on — the layer's own kinds of folder | Its "By responsibility" row lists `lib/` without saying what it is for |
| [`../khayyam/rules/qualified-names/qualified-names.md`](../khayyam/rules/qualified-names/qualified-names.md) | Reference — the naming rule a duplicated shape's surviving declaration follows | None (read) |
| [`../time/README.md`](../time/README.md) | Depends_on — the category that owns the timer | None; the timer's address is settled |

## Notes
- The move was mechanical: 18 `in` addresses in 9 files, every one a prefix substitution, verified by a round-trip comparison that aborts on any other difference. The two unresolved addresses in `modules/time/timer/protocol/timer.kh` were unresolved before the move and were unresolved after it, at a new path; a later separate edit corrected them to the timer's own `listener.kh` (see that entry), and the file is accepted by the frontend today.
- Nothing was staged, nothing was committed, and nothing under `docs/` was touched.
