# Binding Model Changelog

## Changelog

### The owner's placement of atomicity recorded
- Time: 2026-10-04T05:42:25Z
- Type: Added
- Cited:
  - [modules/process/sync/sync.md](../../process/sync/sync.md) - Implements: the module the owner's ruling places the release's indivisibility and order in, and the model of the two guarantees it owns.
  - [docs/process.md](../../process/process.md) - Depends_on: Constraints Belong to the Constraining Concern, which places the rule about when a portion is free with the ring rather than with the guarantee; and Concurrency at `:232`, which is why a release that is indivisible but unordered is wrong on one core as well as two.
  - [docs/protocols/computer/concurrency.md](../concurrency/concurrency.md) - Depends_on: `:11` claims to state the synchronization primitives its body never names, which is what the new requirement now waits on.
  - [docs/khayyam/abstraction.md](../../../docs/khayyam/abstraction.md) - Depends_on: `:100`, which is why the release must be a method of the buffer's capsule rather than of an abstraction.
  - [modules/computer/buffer/protocol/index.kh](../buffer/protocol/index.kh) and [buffer.kh](../buffer/protocol/buffer.kh) - Record: `:2` an empty `Buffer_Index ab` composed by nothing, `:22` `Computer_Buffer ab` composing indexes and lengths and no cursor.
  - [docs/khayyam/khayyam.md](../../../docs/khayyam/khayyam.md) - Depends_on: **Syntactic Atomicity and Semantic Clarity**, whose line numbers in this folder's two files were corrected from `:233`-`:234` to `:234`-`:235`.
  - [docs/documentation.md](../../../modules-plugable/knowledge/documentation/documentation.md) - Extends: File Naming, under which this folder takes a changelog beside its base document.
- Contributors:
  - [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) - ruled that atomicity in the driver-application design is carried by a method of the buffer module using a module similar to Go's `sync`, and that the synchronisation module itself may be generated
  - Auto (model not recorded) - recorded the ruling in the model, worked out what the method needs beyond indivisibility, and established and modelled the module it names
- Propagates to:
  - [binding.md](./binding.md): Updated - the abstract, **The execution method**, the categories list under **Each party is a module of an existing category**, the name-collision note under **The execution method**, and questions 23 and 24.
  - [binding.handoff.md](./binding.handoff.md): Updated - a new decision, the state of the indivisibility question, a related-artifact row, an anticipated-work entry, and a dated note of what this session wrote.
  - [../../process/sync/sync.md](../../process/sync/sync.md): Added - the module's model, which carries the working-out this folder's ruling depends on.
  - [../../../docs/protocols/computer/concurrency.md](../concurrency/concurrency.md): Needed - a section stating at least one synchronization primitive and its guarantee. Not edited in this session; carried as the first open question in the synchronisation module's handoff.

#### What changed
- Recorded the owner's ruling under **The execution method**: the indivisibility of a ring's release is a method of the buffer module, whose receiver is a capsule and may therefore name the region, and the guarantee it rests on belongs to the synchronisation module.
- Added what that ruling does not carry. **Indivisibility alone does not free the region** — the driver must also observe the application's earlier writes to it — so the release carries a second requirement, modelled as **Sequencing** beside **Atomic Operation** in the synchronisation model, and question 24 owes a fourth contract term where it owed three.
- Named the synchronisation module among the categories the two parties rely on, as a peer of the buffer rather than a part of it, and recorded that its realization is what the same-artifact obligation under question 19 now rides on twice over.
- Narrowed question 23 to what the ruling leaves open: whether the crossing *also* states the requirement, and whether the guarantee is a property of the design or of the organization's posture.
- Corrected the `khayyam.md` line numbers for **Syntactic Atomicity and Semantic Clarity** in both files of this folder from `:233`-`:234` to `:234`-`:235`. Against the tree as it stands `:233` is blank, the heading is at `:234`, and the principle sentence is at `:235`.

#### Considered and not done
- **The ruling recorded as "an atomic release is a declared method", with no further consequence.** That was already the model's answer before this revision, and it left the reader with a guarantee whose meaning stopped at indivisibility. Rejected because a region freed by an indivisible but unordered advance is not safe to refill, which makes the second half a requirement of the design rather than an implementation detail, and because a model that states the requirement without it would have been a model whose sharpest instance cannot be built correctly.
- **The indivisibility left as a term of the crossing, on the strength of the model's own checkability test.** The test says a term is worth stating only if one party can check it alone, and atomicity fails it, which argued for keeping it a provision. Rejected as the whole answer only because it did not survive being written down next to the ring: the checkability failure tells the crossing what it cannot rely on, not that the release needs nothing beyond indivisibility.
- **The synchronisation module modelled as one concept, with the order carried as a required contract term of it.** One concept would have matched the owner's word, which names one thing. Rejected because nothing in this repository states the order at all, so folding it into the indivisibility would have made the ring's actual requirement look stated while having no sentence that says it, and because the two answer different halves of a question the buffer method must answer.
- **The synchronisation module's own protocol section written here, in the protocol document, as part of this change.** That is the one thing the new requirement most needs and the one thing this revision cannot supply. Rejected because `docs/` is outside what this work was permitted to write, and because a protocol section written from a model's finding rather than from a decision would make the implementation the protocol's own authority.
- **Question 23 deleted, on the ground that the owner's ruling answered it.** Rejected because the ruling settled which of three candidates the indivisibility is and left the other two standing, and deleting the question would have retired a term that may still owe the crossing one.
- **A new open question added for the order the release establishes, making this folder carry twenty-six.** Rejected under [Modeling → A Relation Several Domains Need Is Defined Once](../../../docs/modeling.md#a-relation-several-domains-need-is-defined-once): the question is one question - which document owns a place crossing's contract terms - and it is held at question 24, with the fourth term named inside it and in the synchronisation module's own handoff rather than as a second entry here.
