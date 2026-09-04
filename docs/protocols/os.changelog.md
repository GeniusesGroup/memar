# OS — Guarantees and Kernel Models Changelog

## Changelog

### Initial draft consolidating the OS-boundary note and the unikernel notes
- Time: 2026-08-28T12:06:35Z
- Type: Added
- Cited:
  - [Unikernels: The Rise of the Virtual Library Operating System](https://dl.acm.org/doi/book/10.1145/3442482) — Reference: absorbed from the pre-merge `unikernel.md` note, with its reason preserved — demonstrates that general-purpose filesystems are not universally required, though not necessarily obsolete everywhere.
  - [Exokernel: An Operating System Architecture for Application-Level Resource Management (SOSP '97)](https://www.ece.cmu.edu/~ganger/papers/exo-sosp97/exo-sosp97.html) — Evidence: supports the guarantee/meaning separation — a kernel providing only secure multiplexing of hardware, with all abstractions in library operating systems, is implementable.
  - [nanos](https://github.com/nanovms/nanos) — Reference: a maintained open-source unikernel, used as an existence proof that the unikernel position is implementable (not an endorsement).
  - [NanoVMs](https://nanovms.com/) — Reference: the commercial provider of Nanos, recorded alongside it for the same reason.
- Propagates to:
  - persia_os.md: Pending — should reference this document for the OS-boundary principle and the kernel-model spectrum instead of restating kernel-concept material locally (its current architecture section lists the concepts without the principle behind them).
  - unikernel.md: Done — content fully absorbed into this document (topics, implementation links, and the ACM citation); file deleted. It never had Explanation-facet form (no front matter or ID), so no Superseded pointer was created, per the merge rule for pre-Final documents.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — claimed, argued: wrote the original OS-boundary principle and the unikernel notes this document consolidates; directed the merge and upgrade.
  - [Super Z](../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — drafted: merged the two notes, restructured the result under the Explanation facet, and wrote this changelog entry.

#### Summary
Created the merged Explanation-facet document `os.md` (titled "OS — Guarantees and Kernel Models"), as Draft. It states the OS responsibility-boundary principle (the OS provides foundational guarantees; higher-level systems define meaning), then presents monolithic, microkernel, exokernel, and unikernel as positions on a single spectrum ordered by how much meaning the kernel defines — with the unikernel as the endpoint (library OS compiled into a single application image). The pre-merge `os.md` principle and the fragmentary `unikernel.md` material (implementation and provider links, the ACM citation, the general-purpose-filesystem finding) were absorbed unchanged in substance; no gaps were filled with invention — the device-driver placement, the microkernel's satisfaction of the boundary principle, unikernel guarantees without other tenants, and Nanos's conformance to the principle are recorded as unresolved questions.

#### Rationale and alternatives
The merge follows the project's rule that pre-Final documents consolidate without new citations pointing to abandoned ones — both source notes predated Explanation-facet form, so nothing was formally superseded. Keeping the documents separate was rejected because the unikernel note's subject is a position on the boundary the OS note defines; their separation was an artifact of note-taking history, not of the subject matter. Choosing a kernel position for the project's own OS was deliberately kept out of scope — that is an architecture decision belonging to PersiaOS's document, which is flagged as Pending in Propagates to.

### Added the hypervisor position and the de-traditionalization topics
- Time: 2026-08-28T12:33:36Z
- Type: Added
- Propagates to:
  - persia_os.md: Pending — its "User Manager" and POSIX-adjacent framing may need reexamination against the decomposition and identity topics in this document; its kernel-concept list should also gain the hypervisor position.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — argued: identified the missing hypervisor position on the spectrum; challenged the traditional OS view — including the "Linux is just a kernel" framing — as misleading rather than wrong; requested the presupposition-free decomposition of the OS; supplied the launcher example and the objection to the traditional user concept; and proposed testing whether the CPU core suffices in place of the thread, with concurrency not assumed to be the OS's problem.
  - [Super Z](../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — drafted: extended the machine-model spectrum with the hypervisor, wrote the three new topics (the traditional-view critique, the decomposition with the default-app classification, and the execution analysis), and added the open questions each leaves.

#### Summary
Extended the document in four moves. First, the machine-model spectrum gained the hypervisor (and the topic was renamed from "kernel models" to "machine models", since a hypervisor is not a kernel): it multiplexes whole machines, guarantees tenant isolation, defines almost no meaning beyond the virtual-hardware shape, and pairs naturally with unikernels. Second, a new topic argues the traditional OS view — from mainframe systems to Linux's "just a kernel" framing — is not wrong but deeply misleading, because it presents a historical bundle of guarantees, standard abstractions, default applications, and identity conventions as essence. Third, a decomposition topic re-derives the partition without that presupposition, using the test "would removing this component break a guarantee — or only a habit?": what survives are the guarantees; the rest falls into default applications (launcher, shell, init, login manager — ordinary user-level apps with no special OS-level abstraction), traditional abstractions that belong to systems above, and identity conventions that reduce to principals for privilege boundaries — the traditional "user" is a bundle, not a concept. Fourth, an execution topic argues the OS-level resource is the core (a core-time entitlement over an address space — process-like, but stripped of the traditional process's bundled meaning), that the thread is a traditional abstraction rather than an OS concept, and that concurrency is not a question the OS must answer.

#### Rationale and alternatives
- **Add the hypervisor as its own separate document (rejected)**: it answers the same guarantee/meaning question as the other models and belongs on their spectrum; a separate document would re-derive the boundary principle for no added precision.
- **Frame the traditional-view critique as "the traditional view is wrong" (rejected)**: the bundle demonstrably works; the precise defect is that its shape is history read as essence, which misleads architects — wording chosen to keep the claim defensible.
- **Keep thread/scheduler analysis out until a runtime document exists (rejected)**: the thread presupposition is one of the strongest ways the traditional bundle re-enters an architecture, so marking it non-essential at the concept level — with the open questions stated — belongs in this document now.

### Restructured: kernel as a layer concept, founding layers, process-aligned execution
- Time: 2026-08-28T12:56:51Z
- Type: Revised
- Propagates to:
  - none — self-contained restructuring of this document (the persia_os.md pending from earlier entries is unchanged).
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — argued: required the methodology to state the requirements-first method explicitly; established that the kernel is not OS-exclusive (any system's foundational layer carrying its non-removable domains is a kernel, and a unikernel OS image is really an app binary), making the hypervisor's placement inside the structuring list misleading and the list's ordering presupposition-laden; required the execution/concurrency treatment to align with process.md's approach rather than risk violating it; and read the hypervisor as part of the OS carrying its most foundational duties, with the bootloader, UEFI, and legacy BIOS examined as part of the system's agency and of the OS layer.
  - [Super Z](../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — drafted: rewrote the Methodology, replaced the machine-model spectrum with the kernel-as-layer-concept topic and the founding-layers topic, and rewrote the execution topic to defer to Process's principles.

#### Summary
Four structural changes. First, the Methodology now opens by stating the document's method: identify the requirements that genuinely need an answer and argue where the better place to answer each one is — the traditional components appear only as evidence, never as the starting taxonomy. Second, the machine-model spectrum topic was replaced by "The kernel is a layer concept, not an OS-exclusive one": a kernel is any system's foundational layer carrying its non-removable domains; a unikernel's "OS image" is an application binary carrying its own kernel as libraries; the four traditional structuring names are kept as recorded answers to where a system's kernel lives, with their OS-exclusive presupposition dropped. Third, a new topic, "The OS's founding layers: firmware, bootloader, hypervisor", reads the hypervisor as part of the OS — the layer carrying its most foundational duties — and brings the bootloader, UEFI, and legacy BIOS inside the OS layer as parts of the system's agency, under a duty-accounting discipline (each founding layer gets only duties that cannot be answered higher, with UEFI's accumulation of duties as the cautionary example). Fourth, the execution topic now defers to Process: the thread's rejection is grounded in process.md's "a thread is not a process" and process-before-mechanism principles, concurrency questions are explicitly routed to process.md's method rather than answered here, and the OS-level claims are narrowed to the guarantee side (core-time entitlement over an address space).

#### Rationale and alternatives
- **Keep the hypervisor in the structuring list with the ordering defended (rejected)**: the user's objection stands — the members of that list answer different questions, and the ordering embedded past presuppositions the document elsewhere commits to exposing rather than reproducing.
- **Rewrite the concurrency analysis independently of process.md (rejected)**: this project's documents form one model; an OS document that re-derives concurrency on its own terms would inevitably drift against Process's settled rulings. Deference here is the same cross-document consistency discipline process.md itself applied to system.md.

### Rewritten by requirement area; history and provenance removed from the body
- Time: 2026-08-28T13:27:51Z
- Type: Revised
- Propagates to:
  - persia_os.md: Pending — unchanged from earlier entries.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — argued: renamed the document to the plain "OS" so the title carries no presupposition; ruled that the main document must never reference the changelog or its own past, since history carries no information for a reader of the current design and only adds cognitive cost; asked for the kernel layer's per-system internal categorization to be stated (core functional domains as one module category, with unikernel-supplied OS modules joining that category); required the filesystem to be stated precisely as an upper-level abstraction, with the OS providing a per-image block abstraction exactly analogous to memory management and no interference in how non-volatile memory is organized; and requested the document be rewritten by requirement area — one coherent capability-and-constraint statement per requirement — so that someone asking "build an OS under this architecture" receives a complete answer with no old-world default.
  - [Super Z](../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — drafted: rewrote Motivation, Methodology, and Abstract; removed every history and changelog reference from the body; added the kernel-categorization passage and the Storage, Networking, and Identity topics; slimmed the decomposition topic into the classification method pointing at the per-concept topics; and rewrote the document-level Discussion without history-based content.

#### Summary
The document was rewritten around requirement areas instead of historical narrative. Every reference to the paired changelog and to the document's own past (source notes, earlier revisions, merge decisions) was removed from the body — the body now states the current design only; this file remains the sole record of how it got here. A passage was added stating that each system's kernel layer carries its own internal categorization: core functional domains as that system's kernel-category modules, joined in unikernel-shaped systems by the OS duties compiled in as libraries. Two new requirement topics were added: Storage (a filesystem is an upper-level abstraction; the OS grants an exclusive, bounded block abstraction per application — per OS image — exactly as it does for volatile memory, and does not interfere with how non-volatile memory is organized) and Networking (the OS provides exclusive, privilege-bounded access to network hardware and frame delivery; connection, protocol, and transport semantics are upper-level meaning, with routing itself possible as an application). Identity was extracted from the decomposition topic into its own topic (principals, not users, with the relationship to Agency's Principal left open). The decomposition topic now serves as the classification method pointing into the per-concept topics, and the document-level Discussion was rewritten without history-based content.

#### Rationale and alternatives
- **Keep the merge history in the body as context (rejected)**: the user's ruling is adopted as the document's convention — the body answers "what is the design", not "how did it get here"; past-state questions belong to this file, where they cost a reader who wants history nothing and cost a reader who does not everything.
- **Fold Storage/Networking content into the boundary topic instead of separate topics (rejected)**: scattering each requirement's answer across topics is what made the previous revision hard to use as an implementation brief; one topic per requirement, each stating capability and constraint, is the form the document's own test demands — could a reader build an OS from it without importing the old world's defaults.

### Absorbed the architect-level content from the PersiaOS project document
- Time: 2026-08-28T13:46:01Z
- Type: Revised
- Propagates to:
  - persia_os.md: Pending — re-scoped as a project-level document: PersiaOS is a project on the architecture delivering applications, not part of the architect's documentation; its document should be rewritten as a project brief referencing this one for every architect-level claim, keeping only its project-specific decisions.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — argued: ruled that PersiaOS's document no longer belongs at the architect level since PersiaOS is a project delivering apps on the architecture, not a part of the architect; asked for a review of the old document with anything of value transferred here, with explicit caution that the document is very old and may contradict the current architectural thinking.
  - [Super Z](../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — drafted: reviewed the old document claim by claim, transferred the architect-level content in corrected form, and recorded the rejections.

#### Summary
Reviewed the PersiaOS project document and transferred four architect-level insights, each corrected to current thinking. First, the isolation-first principle: OS-level-virtualization tools (containers and the like) appeared because isolation guarantees were missing, and the fix belongs at the layer that owns isolation — added as a rejected alternative in the traditional-view topic. Second, resource entitlements: exclusive access is granted through declared per-application bounds (a minimum and a maximum) used for arbitration and accounting — the OS says *how much*, never *how*; added to the decomposition topic's guarantees bullet. Third, device-class neutrality: the same OS serves servers, clients, and routers without an OS-level device concept — no editions, no device taxonomy; added to the Networking topic alongside routing-as-an-application and the OS's delivery-only constraint (it neither interprets nor alters what passes through). Fourth, [sRPC](./sRPC.md) joined [Chapar](./chapar.md) as an example of protocols built above the guarantees. The Relationship-to-PersiaOS topic was rewritten to state the new framing: PersiaOS is a project on the architecture, its document is project-level, and the architect-level claims it carried have been absorbed here. Claims deliberately not transferred: the "Users Manager" (superseded by the principals position in Identity), OS-level packet scheduling (now an unresolved question about policy versus arbitration), the POSIX placeholder, and the Giti/GP protocol and firewall specifics (project decisions, not architect-level).

#### Rationale and alternatives
- **Transfer the old document's claims verbatim (rejected)**: the review's purpose was to filter, not to copy — several claims (device-class bundles like "Users Manager", OS-level scheduling policy, isolation by tooling) predate and contradict positions this document has since argued for; transferring them unchanged would re-import the very presuppositions the document exists to exclude.
- **Leave the PersiaOS document in place untouched (rejected for now)**: its re-scoping into a project document is its own transition, recorded as Pending rather than executed here, since where project documents live is a project decision.

### Added the famous-names demystification and the strong arguments from an external review discussion
- Time: 2026-08-28T14:16:09Z
- Type: Revised
- Propagates to:
  - persia_os.md: Pending — unchanged from earlier entries.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — argued: asked for a new topic stating that the industry's famous names (virtual machine, container, POSIX) carry no intrinsic value in this architecture and mislead when treated as concepts the OS must own, supplying the container analysis: much of what appears isolated is not (kernel-side memory such as network buffers is shared and unaccounted), and the traditional remedy of blunt limits (capping file descriptors, shrinking buffers) throttles the input instead of removing the sharing, wasting the other resources; and supplied a discussion containing arguments to be evaluated and absorbed where strong.
  - [Super Z](../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — drafted: evaluated the discussion's arguments claim by claim and absorbed the strong ones into the existing topics rather than a new survey.

#### Summary
Added the topic "Famous names: VM, container, and what they actually are" — each famous name read as a packaging or compatibility choice of the traditional bundle, with the container stated sharpest: a container does not close the neighbor problem, because kernel-side memory (network buffers, page cache, connection state) is shared and unaccounted, and the traditional remedy of blunt limits does not remove the sharing, it throttles the input — an application forced to refuse work it had the resources to perform. Absorbed from the discussion: the argument that the traditional bundle's dominance is sociological and economic evidence (timing, licensing, network-effect lock-in), not architectural evidence — added to the traditional-view topic; QUIC as the strongest recent confirmation that meaning is forced to escape the traditional kernel rather than be defined by it — added to the Networking topic's prior art; the para-virtualization and hardware-partitioning counter to the standard "drivers must live in the kernel" objection (VirtIO, SR-IOV show device access can be a narrow, semantics-free interface) — added to the boundary topic's driver question; and providers' DPU/SmartNIC offloading as continued evidence that label-based isolation is incomplete — added to the famous-names topic's prior art. Observability-without-traditional-abstractions was already carried by the implementations topic and was not duplicated.

#### Rationale and alternatives
- **Give each famous name its own catalogue entry maintained over time (rejected)**: a catalogue of rebuttals ages; the underlying test does not — which guarantee does this name provide, and which meaning does it define? The topic states the test and applies it, rather than accumulating per-name entries.
- **Absorb the discussion's arguments as a quoted external position (rejected)**: provenance belongs to this file; the body states arguments on their own merits, wherever they were first heard.

### Answered the app-status cost objection for drivers and frame delivery in the Networking topic
- Time: 2026-09-01T16:16:25Z
- Type: revised
- Cited:
  - [Giti (GP)](./giti.md) — Reference: the GP redesign discussion raised the objection (a driver as an independent app seemingly multiplying processing cost) while resolving mixed-level endpoint addressing through this document's model.
- Propagates to:
  - giti.md: Done — its mixed-level communication ruling references this topic's answer.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — decided: the cost objection must be answered here, not in the protocol document — and the answer is structural: the isolation mechanism that separates applications is the same one that grants hardware access, so no kernel↔app context switch sits on the packet path; and one step beyond traditional models, the NIC's memory can be granted into the destination application's address space so packet data lands there directly — without the kernel copying it or even observing each packet. Security is supplied by exclusive granting, not by kernel mediation of every packet.
  - [Super Z](../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — applied.

#### Summary
The Networking topic gained the paragraph dissolving the driver-as-app cost objection: isolation costs, not per-packet mediation — no context switch on the packet path, and a direct NIC-memory grant into the destination application's buffers as the permitted cheaper path that traditional kernel-mediated stacks never take. The topic's unresolved question (frame delivery as a default app holding the NIC entitlement) stays open, but the cost argument against that reading is now answered in advance.
