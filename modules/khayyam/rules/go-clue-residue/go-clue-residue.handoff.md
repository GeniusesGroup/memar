# Khayyam Rule — Go Clue Residue Handoff
Open state for [go-clue-residue.md](./go-clue-residue.md). See the repository's [documentation-handoff.md](../../../../docs/documentation-handoff.md) for what a handoff is.

## Status
Active — applied 2026-09-28 to the ported corpus under `modules/` (excluding `modules/khayyam/`): 826 blocks shrunk and 87 removed with their markers, 913 license headers, 704 members, and 262 whole types removed, in 911 files. A second run changes nothing.

## Decisions
- **Remove only what the Khayyam file carries** — Decided (2026-09-28, owner). A Go method leaves only when its Khayyam method exists; the tests show it kept otherwise.
- **A Go comment is part of its declaration** — Tentative (2026-09-28, applied by the tool; awaiting the owner's review). A declaration whose comment the Khayyam file does not carry stays, so no prose of the reference is lost. Example: `SecondElapsed` in `modules/time/protocol/time.kh` stays because its trailing `// From Epoch` is not in the Khayyam file.
- **A sealed block is removed whole or not at all** — Decided (2026-09-28). The three sealed blocks under `modules/math/boolean/` keep their `sha256` valid.
- **A raw string spanning lines is counted by its lines** — Decided (2026-09-28). The first corpus run counted a Go raw string as one line, removed three wrong lines from `modules/memory/record/services____/service-{delete,wipe,write}-sdk.kh`, and was repaired: each file was rebuilt, the rebuild was proven by replaying the faulty run onto it, and the lexer and a test were corrected.
- **The blocks are committed with the corpus, not withheld** — Decided (2026-10-01, owner). A commit boundary was proposed that stages only the `.kh` files carrying no block; it is rejected, because [`modules/khayyam/core/test/matrix.test.ts`](../../../../modules/khayyam/core/test/matrix.test.ts) reads five block-bearing units as its `accept` rows (`computer/runtime/protocol/concurrency.kh`, `computer/capsule/protocol/life_cycle.kh`, `time/duration/nano-in-second.kh`, `net/srpc/protocol/srpc.kh`, `math/float/float-32.kh`) and further rows fail on transitive imports of block-bearing units, so that commit would enshrine a tree whose standing Test cannot pass. The block is the transfer's correspondence, not residue to be hidden from history. **What retires a block is unchanged and is this rule**: `tidy --rule go-clue-residue`, whose end state is zero blocks.

## Open Questions
- **Whether a port rule belongs in this catalog.** The [membership criterion](../README.md#membership-criterion) asks that a rule's subject be Khayyam itself; this rule's subject is the port's clue block, which is Go text in a Khayyam comment. It is kept here beside the other rewrite rules until the owner says whether port rules belong here or with the port's own tooling.
- **Where the clue block's format is stated.** No governed document states the `// TODO(go-migrate):` block or its `* /` escape; the rule states the format it reads. The format's home is not decided. Committing the blocks raises what this decision costs: from 2026-10-01 the corpus in version control is 815 files whose block is governed only by a rule document.

## Related Artifacts
| Artifact | Relation | Action |
| --- | --- | --- |
| [go-clue-residue.md](./go-clue-residue.md) | Base — the rule | Keep in sync with the tool |
| [qualified-names.md](../qualified-names/qualified-names.md) | Depends_on — how a Go name maps to its Khayyam counterpart | None (read) |
| [targets/go/abstraction_bridge.py](../../targets/go/abstraction_bridge.py) | Implements — `tidy --rule go-clue-residue` | Keep in sync |
| [targets/go/test_abstraction_bridge.py](../../targets/go/test_abstraction_bridge.py) | Implements — the `Tidy` tests | Keep in sync |
