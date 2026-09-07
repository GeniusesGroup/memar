# OS Handoff

Open work for `protocols/os.md`. Entries are mutable current state — revised as each item moves, removed when it resolves or is dropped. See [documentation-handoff.md](../documentation-handoff.md) for what a handoff is.

## Open Questions

### The OS responsibility boundary
- State: whether the OS should define the standard abstractions was considered and rejected for this project — under the boundary principle, an abstraction needed by a higher-level system is defined by that system and implemented against the guarantees, so the assumptions stay where the meaning is (recorded in os.changelog.md).

### Device drivers on the guarantee/meaning boundary
- State: where device drivers sit is not settled: a driver enforces access control to hardware (a guarantee) but is also shaped by device semantics (meaning). The standard objection — that drivers must live inside the kernel — is circumstantial, not architectural: para-virtual device interfaces and hardware partitioning (VirtIO, SR-IOV) already demonstrate that device access can be structured as a narrow, semantics-free interface between the guarantee and the hardware, rather than as kernel-resident meaning. A position is still needed before any implementation decision can reference os.md honestly.
- Next: state the position; it gates the "controlled interaction with hardware" definition (see Anticipated Work).

### What makes a domain non-removable
- State: the criterion for a domain's non-removability (the kernel-layer reading's membership test) needs the same discipline this project applies to foundational concepts elsewhere — see [Modularity](../modularity.md)'s foundational-status test — and has not yet been adapted to the kernel-layer reading.
- Next: adapt Modularity's foundational-status test to the kernel layer.

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

### The boot path's status
- State: does the boot path change the analysis — is the first code that enforces the guarantees itself a default app, or part of the guarantee machinery? The founding-layers topic takes up the layers below that code.
- Next: settle alongside the founding layers' duty partition.

### What the guarantee side owes a waiting execution
- State: what does the guarantee side owe an execution that must wait — for a device to complete, a timer to expire, another entitlement's slice to end? A completion mechanism exists within the guarantees (controlled hardware interaction), but its exact shape must be worked out together with [Process](../process.md)'s treatment of progression, and must not violate its principles.
- Next: joint session with the Process document.

### Parallelism within one address space
- State: can parallelism within one address space be expressed as several core-time entitlements over one address space — and should that be modeled through [Process](../process.md)'s Worker concept rather than a new OS-level unit?
- Next: decide with the Process document and the concurrency realization work.

### Scheduling policy's residence
- State: does preemptive arbitration of cores need scheduling policy at the OS level, or can the policy live in a default app (or a higher-level system) with the OS enforcing only the exclusivity it is told to enforce?
- Next: decide with the first multi-core arbitration realization.

### Storage throughput arbitration
- State: does the block abstraction include arbitration of device throughput between applications — entitlement to bandwidth as a guarantee-side duty — or does throughput policy follow the same core-time-entitlement reasoning as compute? Not yet argued through.
- Next: argue through with the first storage realization.

### Frame delivery's residence
- State: does frame delivery itself belong to the OS, or can even that be a default app holding an entitlement to the NIC — with the OS providing only exclusive hardware access? The answer decides how thin the OS's network duty really is, and has not been argued through.
- Next: argue through with the networking realization work.

### Principal's relationship to Agency's Principal
- State: what relationship holds between a principal in os.md and the Principal concept in [Agency](../agency.md)? The two documents use the same word for related but not yet reconciled concepts; the reconciliation is its own session.
- Next: dedicated reconciliation session.

### Nanos's boundary-principle compliance
- State: whether Nanos actually respects the boundary principle — or defines traditional abstractions (a POSIX-ish surface, a general-purpose network stack) inside its library set — has not been evaluated. Recording it as an example does not certify it.
- Next: evaluate before relying on it as a reference implementation.

### Observability without the traditional process abstraction
- State: whether observability without the traditional process abstraction — events and entitlements as the diagnostic surface — can match the traditional tooling's debugging expectations has not been argued; those expectations are themselves bundle-shaped.
- Next: argue when the first diagnostic tooling is designed.

### Which kernel-structuring answer the project's OS takes
- State: which kernel-structuring answer PersiaOS takes, and where its project documents live once re-scoped out of the architect's documentation, are PersiaOS's own decisions; until then, PersiaOS documentation should be read as a project brief that references os.md for every architect-level claim. Related: does the project need a dedicated document recording *which* kernel-structuring answer its OS takes, once decided — or should that decision live inside the PersiaOS architecture document, with os.md linked as the conceptual foundation?
- Next: PersiaOS's own decision; revisit the dedicated-document question then.

## Anticipated Work

- If the device-driver question is resolved, os.md gains a topic defining what "controlled interaction with hardware" means precisely enough to implement against.
- If new requirement areas emerge that no topic covers, they join the same pattern — one topic, one capability-and-constraint statement — rather than growing the existing topics sideways.
- The lock-in that sustains the traditional bundle is a cost asymmetry: leaving costs more than enduring. If the cost of redefining and rebuilding abstractions keeps falling — AI agents producing library-level meaning against the guarantees fast enough that rewriting becomes cheaper than hacking around the bundle — the asymmetry erodes and the ecosystem objection to the boundary principle loses force over time. This is recorded as a possibility the architecture should not price out, not as a prediction its positions depend on.
