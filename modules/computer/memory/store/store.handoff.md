# Memory Store Handoff
Open work for `store.md`. Entries are mutable current state, revised as each item moves and removed when it resolves or is dropped. See [handoff.md](../../../../modules-plugable/knowledge/documentation/handoff/handoff.md) for what a handoff is.

## Decisions
Each is **Tentative**: taken by task `20261026-T144222Z-11720` (step 1 of `20261023-T074642Z-5420`) where the code needed a name or a rule no abstraction gave, open to the owner's ruling, and each says what changing it costs.
- **An expectation on a store that cannot compare and write is Refused as NotAtomic.** The contract names Malformed, TooLarge and NotAtomic; an expectation needs the medium to compare and write one address atomically, which is an atomicity the adapter does not declare. Changing it costs one reason in `protocol/store.py` and the case `no-compare-refuses-expectation`.
- **A dense store's addresses are the integers below its capacity, big-endian in the fixed address length, and an unwritten one holds zero bytes of the fixed value length (none when the length is any).** The documents say a dense store answers the capacity range and reads no Absent, and name no initial value. Changing it costs `Parameters.unwritten` and the dense cases.
- **The seam is `at_commit_point(hook)` and `drop_derived_structures()`, and a case that reaches another process asks the adapter for `opener()`.** The documents name a seam at the commit point and the deletion of derived structures, and give them no method names; `opener()` (the dotted module, the function and its keyword arguments that open the same adapter in a child) is the suite's input and not the contract's. Changing them costs the seam in `protocol/store.py` and the `durable` and `shared` cases.
- **`changes(since)` answers the addresses alone, and a state the store never answered is Refused.** Whether it also answers the state it reached, and what it answers for a state older than the store keeps, is the open entry of [Memory Handoff](../memory.handoff.md#what-does-the-contract-answer-for-a-changes-token-older-than-the-store-keeps); `volatile` keeps every commit, so it never meets the second.
- **`changes-sees-other-process` is a case of the `shared` group**, since it needs a second process; on an adapter that does not declare `shared_between_processes` it does not run.
- **The `lockable` group is coded in the module that declares the capability** (`modules-plugable/computer/memory/store/lockable/lockable.py`), as [Memory Handoff](../memory.handoff.md#the-division-of-the-memory-contract-into-modules-2026-10-26-tentative) says, and passed to the runner by an adapter's tests; the build task's plan listed it with the suite. Its protocol is `lockable/protocol/lockable.py`, over an address: `lock(address)` waits until the handle holds it and answers what it holds, `unlock(address, value)` writes the value when one is given and releases, a Conflict once the lease has lapsed; the lease is the store's limit `lease`, in seconds, since `lockable.kh` takes no lease and the record task found it is no parameter of `Lock`. `lock-refused-when-not-lockable` is read as "a store offers `lock` exactly when it declares `lockable`", because no reason names a capability not declared. `lockable.kh` beside it still takes a record id and is task `20261024-T052938Z-22844`'s file, not edited here. Changing it costs the protocol and the group.

### Found during the redo (2026-10-30), Tentative notes
Found by task `20261026-T200842Z-21460` (step S4d); notes, not questions.
- **Task `20261030-T051847Z-13004` (critique of the `detail.kh` text) may change the text of the `*.eng.kh` files** that hold the human-facing text of the contract, since `Summary`, `Overview` and `DevActionNote` are written there; the documents of the memory layer link to those files and restate none of the text.
- **The Khayyam has no enum, union, Optional, constant or generic**, so a union is written as a marker abstraction and an optional value as a (value, given) pair. The contract's answers (Found, Absent, Unavailable; Committed, Conflict, Refused) are marker abstractions for that reason, and changing that waits for the language.
- **The critique task `20261030-T051847Z-13004` is Complete, and its report leaves the worked signature unsettled (it turns on the owner's rulings D3 to D7).** Two of its findings reach this redo: F4 says an empty `UserActionNote` or `DevActionNote` pretends a text is written, and every `*.eng.kh` of the redo returns an empty string for both; F5 says the result type is `String` where a text may need structure. Until the owner rules, the `*.eng.kh` files carry the five methods as the current contract has them.
- **The rule [A Rule Is Code Where It Can Be](../../../process/rule/rules/rule-is-code/rule-is-code.md) is in tension with one thing the redo did.** Each redone module has a `NoComments` test that scans its own files for a comment or a docstring: the condition of the no-comment rule is coded, but copied into every module and not in the rule's `rules/` folder. The copies stay until the Rule module settles the notation of a rule as code; then one check replaces them. No other conflict met.

## Open Questions

### Is the `lockable` capability built on a `Locker` that the sync module refuses as a concept?
- State: the owner ruled on 2026-10-25 that `Lock` and `Unlock` are the optional capability `lockable` of a store, on the `Locker` of `modules/process/sync/`, with a lease. [Sync](../../../process/sync/sync.md) refuses `Lock`, `Locker` and `ReadLocker` as that module's concepts and keeps `protocol/locker.kh` as residue, and `locker.kh` declares `Lock()` and `Unlock()` with no lease. So the lease has no abstraction, and the capability rests on a declaration its module disowns. The group is written against `lockable/protocol/lockable.py`, which names the lease as a limit of the store.
- Options: the lease is stated as the abstraction of exclusion with expiry in the module that owns exclusion, and `lockable` rests on it (recommended: the ruling's "with a lease" then has a home); or `lockable` keeps its own lease and the reference to `Locker` is dropped from its comment; or `Locker` gains a lease in `sync`, against that module's refusal.
- Anchor: [Memory Store → What stands where](store.md#what-stands-where), the `lockable` row.
- Blocks: building `lockable` in an adapter; nothing in step 1, which declares the capability and writes its group only.
- Asked: 2026-10-26, Claude (task `20261026-T144222Z-11720`), for Omid Hekayati.

### Should the module-graph test read the Python of a `protocol/` folder as a module's code?
- State: the build task puts the contract's protocol in `store/protocol/store.py`. `bundles/memar/tests/module_graph.py` names a module only by a file named for its folder or code in `services/` or `primitive/`, so `modules.computer.memory.store` is no node of the graph and the edges of `volatile`, `conformance` and `lockable` into it are not seen; no back edge can hide there today, since everything that imports it is kernel or runs toward the kernel. The test also fails when run alone as its docstring says (`python bundles/memar/tests/module_graph.py`), at its first import, unless the checkout's top and `bundles/memar/services` are on `PYTHONPATH`.
- Options: add `protocol` to the folders whose Python is a module's code (recommended: a protocol written in Python is the module's code); or keep Python protocols in `primitive/`.
- Anchor: [Memory Store → The contract](store.md#the-contract).
- Blocks: nothing now; a back edge into `store` would go unseen.
- Asked: 2026-10-26, Claude (task `20261026-T144222Z-11720`), for Omid Hekayati.

### What does `changes` answer: every written address, or only the addresses whose value changed?
- State: `volatile` answers every written address, and `git-store` answers only the addresses whose value changed, because it compares trees, so an address rewritten with the value it held is missing. The contract does not say which.
- Options: every written address, which `git-store` cannot give without a record of the batch (recommended against: it costs the adapter its tree comparison); or only the addresses whose value changed, which `volatile` gives by comparing the value before and after, and which no derived structure keyed by value misses anything by.
- Anchor: [Memory Store → The contract](store.md#the-contract), "Why `state` and `changes`".
- Blocks: nothing now; a derived structure that counts writes would differ between adapters.
- Asked: 2026-10-30, Claude (task `20261026-T200842Z-21460`), for Omid Hekayati.

### What does the contract say of a `since` the store does not know, and of `state` and `stats` on a replicated or fallback adapter?
- State: the contract's Refused conditions for `changes` do not name a `since` the store does not know (the Tentative decision above reads it as Refused), and `state` and `stats` have no Unavailable answer, though an adapter that is replicated or has a fallback can fail to answer them.
- Options: add the Refused condition and the Unavailable answers to the contract and its cases (recommended: the adapters already meet them in fact); or leave both to the adapter.
- Anchor: [Memory Store → The contract](store.md#the-contract), "Why Unavailable is not Absent".
- Blocks: the realization of the Khayyam, which cannot type an answer the contract lacks.
- Asked: 2026-10-30, Claude (task `20261026-T200842Z-21460`), for Omid Hekayati.

### What does the contract say of a held range when dense and capacity disagree with the address length?
- State: `volatile` refuses at build, as Malformed, a held range when the store is dense and its capacity and the address length disagree; the contract is silent on it.
- Options: state the refusal in the contract and add a case (recommended); or leave it to the adapter's build.
- Anchor: [Memory Store → The contract](store.md#the-contract), "Why the contract is parametric".
- Blocks: nothing now.
- Asked: 2026-10-30, Claude (task `20261026-T200842Z-21460`), for Omid Hekayati.

### Which of the stale Go-era `.kh` files of `record` and `lockable` are replaced, and which deleted?
- State: `record/protocol/` (`model.kh`, `save-options.kh`, `data_model.kh`, the `gui-widget-*` files), `record/services/` and `lockable/protocol/lockable.kh` still declare the Go-era design beside the Khayyam of the redo; the redo edited and removed none of them.
- Options: replace each by the Khayyam of the redo and delete the rest (recommended; `uuid.kh`, `uuid.observers.kh` and `data.kh` stay, repointed, since other modules import them); or keep them until the moves task.
- Anchor: [Memory Record → The Go-era Record model this contract replaces](../../../../modules-plugable/computer/memory/store/record/record.md#the-go-era-record-model-this-contract-replaces).
- Blocks: one record abstraction in the folder.
- Asked: 2026-10-30, Claude (task `20261026-T200842Z-21460`), for Omid Hekayati.

### The slow tier of `git-store` cannot finish within 900 seconds without shortening its rounds: what should its tests assert?
- State: two runs of `batch-visible-whole` (about 7 minutes each), `model-equivalence` and `kill-during-batch-is-atomic` cannot finish within 900 s unless their rounds are shortened, which changes what the tests assert.
- Options: shorten the rounds and state in the case what the shorter run still shows; or keep the rounds and raise the budget of the case; or move the slow tier to a separate, named run.
- Anchor: [Memory Git Store → How it meets the suite](../../../../modules-plugable/computer/memory/store/git-store/git-store.md#how-it-meets-the-suite).
- Blocks: a full green run of the `git-store` tests inside the bound.
- Asked: 2026-10-30, Claude (task `20261026-T200842Z-21460`), for Omid Hekayati.
