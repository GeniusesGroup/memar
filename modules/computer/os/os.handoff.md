# OS Handoff
Open work for `modules/computer/os.md`. Entries are mutable current state — revised as each item moves, removed when it resolves or is dropped. See [documentation-handoff.md](../../documentation-handoff.md) for what a handoff is.

## Open Questions

### Device drivers on the guarantee/meaning boundary
- State: narrowed 2026-10-05; the mixed case is what the test is for, and the test answers it. What the document settles: only the guarantee half of a driver is a founding-layer duty, and the device-semantics half is meaning that belongs above the guarantees. [Decomposing the OS without presupposition](./os.md#decomposing-the-os-without-presupposition) states the test — *would removing this component break a guarantee, or only a habit?* — and a driver fails it as a whole while passing it by halves: remove the access control and exclusive hardware interaction, a stated OS guarantee, breaks; remove the device semantics and only a habit breaks. [The OS's founding layers: firmware, bootloader, hypervisor](./os.md#the-oss-founding-layers-firmware-bootloader-hypervisor) names the excluded side in the same terms — driver models grown beyond the hardware actually present do not belong to a founding layer — and [The kernel is a layer concept, not an OS-exclusive one](./os.md#the-kernel-is-a-layer-concept-not-an-os-exclusive-one) records that the drivers objection was circumstantial and has lapsed. The para-virtual interfaces and hardware partitioning the entry names therefore decide how the guarantee half is served, not where it sits.
- What remains: no sentence in os.md states the split, and the guarantee half is served by nothing the document names — the narrow, semantics-free device interface between the guarantee and the hardware is the possible answer, and os.md does not say that it is the answer. The position also gates the "controlled interaction with hardware" definition (see Anticipated Work).
- Next: write the split as one sentence into [The OS's founding layers: firmware, bootloader, hypervisor](./os.md#the-oss-founding-layers-firmware-bootloader-hypervisor), naming what the founding layer's device surface is; then the gated topic.

### UEFI runtime services after boot
- State: when UEFI runtime services remain available after boot, are they part of the OS's founding layer — or a default app running with founding-layer privileges?
- Next: decide during the founding layers' duty-partition work.

### The hypervisor's duty set and the trust chain
- State: does the hypervisor's duty set reduce to tenant isolation plus whole-machine multiplexing, or does measured/secure boot make it also the root of the trust chain — and if so, is trust a guarantee under os.md's definition?
- Next: argue during the founding layers' duty partition (deferred until it can be argued against real hardware).

### How far the traditional-bundle critique generalizes
- State: are there components in the traditional bundle that are guarantees in disguise (policy only in appearance)? The decomposition topic is the working method for answering this case by case.
- Next: apply the would-removing-this-break-a-guarantee test per component as cases arise.

### Honest multi-tenancy on one kernel
- State: is there a subset of kernel-side memory that a shared-kernel tenant arrangement could fully account and isolate — or is honest multi-tenancy on one kernel impossible in principle, making the hypervisor boundary the only honest tenant boundary? Not yet argued through.
- Next: argue through when the first shared-kernel deployment decision arises.

### Vocabulary replacing the bundled terms
- State: what vocabulary should replace the bundled terms — for the process-like unit, for the default apps? Naming should wait until the concepts have stabilized across more of this project's documents.
- Next: revisit naming once the concepts stabilize.

### What the guarantee side owes a waiting execution
- State: what does the guarantee side owe an execution that must wait — for a device to complete, a timer to expire, another entitlement's slice to end? A completion mechanism exists within the guarantees (controlled hardware interaction), but its exact shape must be worked out together with [Process](../../process.md)'s treatment of progression, and must not violate its principles.
- Next: joint session with the Process document.

### Parallelism within one address space
- State: narrowed 2026-10-05. What the document settles: the OS level holds no unit for it, so the question's second half is already answered. [Compute: cores, not threads](./os.md#compute-cores-not-threads) defines the OS-level unit as something running with an address space and a core-time entitlement, and states that concurrency is not an OS-level question — which activities may progress simultaneously is answered by [Process](../../process.md)'s method, and the OS must not presuppose those answers in its own vocabulary. Parallelism within one address space is therefore [Process](../../process.md)'s Worker concept and not a new OS-level unit; [this document's changelog](./os.changelog.md) records that answering concurrency questions here was rejected as restating [Process](../../process.md)'s answers.
- What remains: whether an entitlement is granted per application or per execution — [Decomposing the OS without presupposition](./os.md#decomposing-the-os-without-presupposition) states declared bounds per application, a minimum and a maximum — which decides what several core-time entitlements over one address space would even be granted to. No sentence in os.md covers an address space carrying more than one execution.
- Next: decide with the Process document and the concurrency realization work; the wording this needs is one sentence in [Compute: cores, not threads](./os.md#compute-cores-not-threads).

### Scheduling policy's residence
- State: narrowed 2026-10-05. What the document settles: scheduling policy is not an OS duty, so the question's own alternative is the one already in force. [Decomposing the OS without presupposition](./os.md#decomposing-the-os-without-presupposition) states that entitlements are how the OS says *how much*, never *how* — they are the mechanism of exclusive access, not scheduling policy — and [Compute: cores, not threads](./os.md#compute-cores-not-threads) states that multiplexing many executions onto few cores is a genuine OS guarantee (exclusive access means someone must arbitrate) while how executions relate, communicate, or wait for each other is meaning defined above. What is left is the other half of the entry's own phrasing, which no passage answers: what the arbiter is told, and by whom.
- What remains: who holds the entitlement whose bound the arbiter enforces, and whether an arbiter that takes a core back when a holder neither ends its slice nor gives it up — the case [Compute: cores, not threads](./os.md#compute-cores-not-threads) names — needs any policy of its own, or only the enforcement the bounds state.
- Next: decide with the first multi-core arbitration realization; the wording this needs is one sentence in [Compute: cores, not threads](./os.md#compute-cores-not-threads).

### Storage throughput arbitration
- State: narrowed 2026-10-05. What the document settles: throughput follows the core-time-entitlement reasoning, and the block abstraction carries bandwidth but not throughput policy. The rule is stated once and generally — entitlements are how the OS says *how much*, never *how* ([Decomposing the OS without presupposition](./os.md#decomposing-the-os-without-presupposition)) — and the same shape is already carried for another device: [Networking: frame delivery, not communication meaning](./os.md#networking-frame-delivery-not-communication-meaning) has the OS arbitrate the network hardware between applications by their entitlements, which is arbitration of a device among entitled applications without a policy of its own. Bandwidth is a bound, so it is an entitlement like core time; the policy that spends it is meaning above.
- What remains: the sentence naming bandwidth as one of the bounds a storage entitlement declares. [Storage: block abstractions, not filesystems](./os.md#storage-block-abstractions-not-filesystems) grants block *ranges* exclusively and enforces the boundary, and is silent on throughput — so the reasoning is available but the topic does not carry it.
- Next: write that sentence into [Storage: block abstractions, not filesystems](./os.md#storage-block-abstractions-not-filesystems); argue the enforcement through with the first storage realization.

### Frame delivery's residence
- State: does frame delivery itself belong to the OS, or can even that be a default app holding an entitlement to the NIC — with the OS providing only exclusive hardware access? The answer decides how thin the OS's network duty really is, and has not been argued through.
- Next: argue through with the networking realization work.

### Principal's relationship to Agency's Principal
- State: what relationship holds between a principal in os.md and the Principal concept in [Agency](../../agency.md)? The two documents use the same word for related but not yet reconciled concepts; the reconciliation is its own session. Two things no longer belong to the residue. Neither document's principal is a `user` or a `group`: [Framework → What the Framework Does Not Specify](../../framework.md#what-the-framework-does-not-specify) states that Memar's architecture-level vocabulary carries neither concept, and this document's [Identity topic](./os.md#identity-principals-not-users) already leaves whether a principal resembles a person, a service, or a device to the system being built. So the reconciliation cannot be reached by mapping either concept onto an account or a bundle of accounts. What is left is narrower and remains open: whether the OS-level principal that a privilege boundary attaches to and the Agency-level Principal that a system acts on behalf of are the same concept, two facets of one, or distinct concepts that merely share a word — and if they are one concept, which document owns its definition.
- Next: dedicated reconciliation session.

### Nanos's boundary-principle compliance
- State: whether Nanos actually respects the boundary principle — or defines traditional abstractions (a POSIX-ish surface, a general-purpose network stack) inside its library set — has not been evaluated. Recording it as an example does not certify it.
- Next: evaluate before relying on it as a reference implementation.

### Observability without the traditional process abstraction
- State: whether observability without the traditional process abstraction — events and entitlements as the diagnostic surface — can match the traditional tooling's debugging expectations has not been argued; those expectations are themselves bundle-shaped.
- Candidate source: [Clive](https://github.com/fjballest/clive), recovered 2026-10-04 from a retired session note and unexamined since — an operating system the note describes as designed for distributed and cloud environments. Whether it must answer this question rather than inherit it, whether its diagnostic surface is built from events and entitlements, and what that costs a user expecting a debugger, is what would make it evidence here rather than a link. Not read.
- Next: argue when the first diagnostic tooling is designed.

### Which kernel-structuring answer the project's OS takes
- State: which kernel-structuring answer PersiaOS takes, and where its project documents live once re-scoped out of the architect's documentation, are PersiaOS's own decisions; until then, PersiaOS documentation should be read as a project brief that references os.md for every architect-level claim. Related: does the project need a dedicated document recording *which* kernel-structuring answer its OS takes, once decided — or should that decision live inside the PersiaOS architecture document, with os.md linked as the conceptual foundation?
- Next: PersiaOS's own decision; revisit the dedicated-document question then.

## Anticipated Work
- If the device-driver question is resolved, os.md gains a topic defining what "controlled interaction with hardware" means precisely enough to implement against.
- If new requirement areas emerge that no topic covers, they join the same pattern — one topic, one capability-and-constraint statement — rather than growing the existing topics sideways.
- The lock-in that sustains the traditional bundle is a cost asymmetry: leaving costs more than enduring. If the cost of redefining and rebuilding abstractions keeps falling — AI agents producing library-level meaning against the guarantees fast enough that rewriting becomes cheaper than hacking around the bundle — the asymmetry erodes and the ecosystem objection to the boundary principle loses force over time. This is recorded as a possibility the architecture should not price out, not as a prediction its positions depend on.
- Re-point, not rejection, for the five `persia_os.md` Pendings in os.changelog.md: the file is absent from this tree and its English successor after language unification is unlocated — closing them as moot would mistake a move for a deletion. Find the successor, re-point each Pending at it; only if none exists do they close as moot.
