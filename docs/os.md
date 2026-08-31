---
Title: "OS - Operating System"
Status: Draft
Start Date: 2026-08-28
ID: 496644
---

# OS - Operating System
This document answers the question "how should an operating system be built under this architecture?" by stating, for every requirement the OS must meet, an explicit capability and an explicit constraint — what the OS does, and what it must not do — with no presupposition inherited from the traditional view.

## Abstract
An operating system's responsibility is limited to providing the foundational guarantees higher-level systems need in order to operate safely: resource isolation, exclusive access control, privilege boundaries, and controlled interaction with hardware resources. Everything above those guarantees — networking models, communication abstractions, application architecture, domain models, execution strategies — is an architectural decision made by the systems built on top, not something the OS defines. The kernel itself is a layer concept, not an OS-exclusive one: a system's kernel is the foundational layer carrying its non-removable domains, so a user-space application can have one — and in the unikernel approach the OS image really is an application binary carrying its own kernel as libraries. The hypervisor, with the bootloader and the firmware, is read as part of the OS itself: the founding layers that carry its most foundational duties. On that basis the document answers each requirement area in one place — compute (cores, not threads), storage (block abstractions, not filesystems), networking (frame delivery, not communication meaning), identity (principals, not users), and the default applications — each stated as a capability and a constraint, so an OS built from this document inherits nothing from the traditional view, which misleads precisely by presenting a historical bundle of guarantees, abstractions, applications, and conventions as essence; the industry's famous names — virtual machine, container, POSIX — are read as packaging or compatibility choices, not concepts. **The OS provides guarantees; the architecture defines meaning.**

## Introduction

### Motivation
Take the request this document must answer: someone asks to develop an operating system following this architecture, and expects the answer to carry no presupposition from the world's existing systems — because every question has been asked and answered here first. Meeting that standard takes more than rejecting a few traditional components: the traditional view bundles guarantees, standard abstractions, default applications, and identity conventions so tightly that rejecting components one by one lets the bundle's assumptions return through the survivors. This document therefore states the OS's responsibility boundary first, then treats each requirement area in its own topic — one coherent statement of what the OS does and what it must not do — so the answer can be read as a whole without the old taxonomy ever becoming the starting point.

### Methodology
The method this document follows is the project's standing architectural method, not a survey of tools: identify the requirements that genuinely need an answer, and argue where the better place to answer each one is. The traditional OS's components are never the starting taxonomy here; they appear only as evidence — answers someone once gave — so that each requirement is placed on its own merits rather than by precedent.

The document is organized by requirement area, not by traditional component: each topic states one area's capability and constraint, and where a concept has its own governing document — [Process](./process.md), [Agency](./agency.md), [Modularity](./modularity.md), [Chapar](./chapar.md) — this document defers to it rather than restating it. Provenance — citations, contributor attribution, revision history — lives outside this document, never in its body: a reader of the current design needs the design, not the path it took to get here.

## Explanation

### The OS responsibility boundary
An operating system should not be considered the owner of application execution semantics or architectural models.

The responsibility of an OS is limited to providing foundational guarantees required for higher-level systems to operate safely. These guarantees include resource isolation, exclusive access control, privilege boundaries, and controlled interaction with hardware resources.

Higher-level concepts such as networking models, communication abstractions, application architecture, domain models, and execution strategies should not be defined by the OS. They are architectural decisions made by the systems built on top of these foundational guarantees.

For example, an OS may provide controlled access to network hardware and enforce permission boundaries, but the concept of a socket, connection lifecycle, communication protocol, or network abstraction belongs to higher-level systems.

This separation allows frameworks and architectures to define their own models without inheriting unnecessary assumptions from traditional operating-system abstractions.

**The OS provides guarantees; the architecture defines meaning.**

#### Discussion

##### Rationale and alternatives
- **Let the OS define the standard abstractions (rejected for this project)**: this is what traditional operating systems do — the socket, the POSIX process, the general-purpose filesystem — and every system built on top inherits those abstractions' assumptions whether or not they fit. Under the boundary principle, an abstraction needed by a higher-level system is defined by that system and implemented against the guarantees, so the assumptions stay where the meaning is.

##### Prior art
The exokernel research program is the strongest independent evidence for this separation: its kernel design deliberately provides only secure multiplexing of hardware resources — no abstractions — and moves every abstraction into application-level library operating systems, demonstrating that the guarantee/meaning split is implementable, not merely aspirational. The end-to-end argument reaches the same shape of conclusion from a different direction: functions placed below the level where their meaning is known tend to be misused or wasted.

##### Unresolved questions
1. Where device drivers sit on this boundary is not settled: a driver enforces access control to hardware (a guarantee) but is also shaped by device semantics (meaning). The standard objection — that drivers must live inside the kernel — is circumstantial, not architectural: para-virtual device interfaces and hardware partitioning (VirtIO, SR-IOV) already demonstrate that device access can be structured as a narrow, semantics-free interface between the guarantee and the hardware, rather than as kernel-resident meaning. A position is still needed before any implementation decision can reference this document honestly.

### The kernel is a layer concept, not an OS-exclusive one
The word *kernel* does not belong to operating systems. In this architecture, a system's kernel is the foundational layer of that system which carries its non-removable domains — the domains that cannot be removed or relocated without the system ceasing to be the system it is. Nothing in that definition mentions an OS, and nothing in it restricts the concept to one: an application running entirely in user space can have a kernel, and often does.

The unikernel approach makes this visible. What a unikernel build calls an "OS image" is, from this side of the boundary, an application binary: the parts of the traditional OS the application actually requires are compiled in as libraries, so the application binary itself carries its own kernel portion. What differs between systems is therefore not *whether* they have a kernel but *where* their kernel lives. The traditional structuring names — monolithic, microkernel, exokernel, unikernel — are recorded answers to exactly that question: in one privileged body; in a minimal core with the domains pushed out to servers beside it; in a thin hardware multiplexer with the domains in a per-application library; or inside the application binary itself. They are kept here as evidence, with a caveat: each name was coined while assuming the kernel in question belonged to *the* operating system, so the names carry that presupposition — this document keeps the answers and drops the assumption.

The kernel layer, once located, carries its own internal categorization — and that categorization belongs to each system, not to this document. An enterprise application's kernel portion is its core functional domains: the modules whose removal would destroy the system's identity, organized as that system's own kernel-category modules. A video-editing application's kernel portion is its media pipeline and frame domains. In a unikernel-shaped system, the application's core modules are joined in the kernel category by the OS duties the image requires — compiled in as libraries — so the kernel category grows by composition rather than by tradition. Which domains are non-removable is each system's own judgment, made with the same discipline this project applies to foundational concepts elsewhere; this document deliberately does not enumerate kernel contents.

Two questions the traditional literature runs together must now stay apart:

- **Where does a given system's kernel live?** — a structuring decision about one system's own foundational layer, answered by the four approaches above. Which answer this project's own OS takes is an architectural decision recorded elsewhere (see [Relationship to PersiaOS](#relationship-to-persiaos)).
- **Which duties belong to the OS's own founding layers** — the firmware, the bootloader, the hypervisor — the layers beneath every system's kernel? This is a question about the OS itself, treated in [The OS's founding layers](#the-oss-founding-layers-firmware-bootloader-hypervisor).

The two questions must stay apart, because merging them is what lets the past's taxonomy pose as the present's analysis: the structuring names answer the first question; the hypervisor answers the second. The hypervisor does not structure anyone's kernel — it precedes every kernel, and is treated with the founding layers below.

#### Discussion

##### Rationale and alternatives
- **Put the hypervisor inside the structuring list (rejected)**: the list then reads as one spectrum, but its members answer different questions — the structuring names answer where a system's kernel lives, while the hypervisor is one of the OS's founding layers. The conflation is the same defect the [traditional-view critique](#the-traditional-os-view-is-misleading-not-wrong) names: past presuppositions read as present essence.
- **Discard the four structuring names entirely (rejected)**: despite their presuppositions, they are the best-recorded evidence for where kernel domains can live, and each encodes a real trade. Discarding them would force this document to re-derive those trades from nothing; keeping them with the question made explicit loses nothing.

##### Prior art
The four structuring names come from OS research history — the monolithic/microkernel debate, the exokernel program, the unikernel literature. The generalized reading matches how the unikernel literature itself describes its artifacts (application and OS compiled into one image) and how kernel-like layers appear inside ordinary applications: in-process schedulers, resource managers, and embedded runtimes are kernels of their systems under this definition, however modest their scale. One historical objection to the low-meaning positions — every application needing its own device drivers — has been dissolved by para-virtualized device interfaces: modern virtualized hardware presents a handful of standard device shapes, so the driver library a unikernel links is small and standard rather than per-device. The objection was circumstantial, and it has lapsed.

##### Unresolved questions
1. What makes a domain *non-removable* for a given system? The criterion needs the same discipline this project applies to foundational concepts elsewhere — see [Modularity](./modularity.md)'s foundational-status test — and has not yet been adapted to the kernel-layer reading.

### The OS's founding layers: firmware, bootloader, hypervisor
Under the boundary principle, the OS is not one component but a stack of layers that together carry its most foundational duties. The correct reading places the hypervisor inside the OS — it is the layer that takes on the most foundational duties of all — and extends the same reading downward to the layers tradition filed outside "the OS": the bootloader, and the machine's firmware, whether the legacy BIOS or its successor UEFI. All of these are part of the system's agency (see [Agency](./agency.md)); together they form the OS layer, and none of them is more "the OS" than another merely because tradition drew the box differently.

The discipline this imposes is duty accounting: for each founding layer, determine exactly which duties genuinely belong to it — and give it nothing beyond them. Working from the guarantee side, the candidate duties are: bringing the machine up and initializing hardware (firmware); locating the next layer and transferring control to it (bootloader); multiplexing whole machines and guaranteeing tenant isolation (hypervisor); serving as the first enforcement point of exclusive hardware access (all of them). What does *not* belong, by the same test applied at every layer: general-purpose abstractions, network stacks, driver models grown beyond the hardware actually present, application platforms. The traditional layers' history is precisely a history of duties accumulating past a layer's founding role — UEFI's growth into a firmware-resident application platform, complete with drivers, shells, and network stacks, is the clearest current example — and each accumulated duty is a duty some higher layer must now carry whether it needs it or not.

#### Discussion

##### Rationale and alternatives
- **Treat firmware and the bootloader as outside the OS's scope (rejected)**: they execute before any kernel and shape what every later layer can guarantee — a privilege boundary the firmware does not enforce cannot be created retroactively above it. Excluding them would leave the OS's guarantees resting on layers whose duties this document never examined.
- **Settle the founding layers' exact duty partition here (rejected for now)**: which duty belongs to firmware versus bootloader versus hypervisor is a real design task that must be argued duty by duty. This document records the discipline and the candidate duties; the partition is deferred until it can be argued against real hardware, not invented in the abstract.

##### Prior art
The thin-firmware direction already exists in practice: boot protocols that hand a kernel the machine with minimal mediation (the Linux kernel's own boot protocol), and projects that strip UEFI down to a loader or replace it outright. Their existence shows the founding layers can be thin; the duty-accounting discipline above says why they should be.

##### Unresolved questions
1. When UEFI runtime services remain available after boot, are they part of the OS's founding layer — or a default app running with founding-layer privileges?
2. Does the hypervisor's duty set reduce to tenant isolation plus whole-machine multiplexing, or does measured/secure boot make it also the root of the trust chain — and if so, is trust a guarantee under this document's definition?

### The traditional OS view is misleading, not wrong
The traditional view — from the old mainframe operating systems down to Linux, which explicitly frames itself as "just a kernel" — bundles at least four different kinds of thing under one name: the foundational guarantees (isolation, privilege boundaries, resource multiplexing), the standard abstractions (socket, filesystem tree, process, thread, signal), the default applications (shell, launcher, init, login manager, package manager), and identity conventions (user accounts, groups, home directories). The bundle works — that is why it spread — but treating the bundle as the definition of "operating system" is deeply misleading for architecture, for three reasons.

First, it makes historical accidents look like necessities. A component is in the bundle because Unix needed it in its era or because a given kernel happened to grow it, not because the guarantee/meaning boundary requires it; an architect who starts from the bundle inherits decisions that were never made on their merits.

Second, it mislocates meaning. Most of the bundle's mass is meaning — abstractions, policies, conventions — which the [boundary principle](#the-os-responsibility-boundary) assigns to the systems above the guarantees. Reading the bundle as "what an OS is" trains architects to push meaning downward, into the layer least able to know what that meaning should be.

Third, it hides the OS's actual product. Under the bundle, what the OS fundamentally offers — enforceable guarantees that any higher-level meaning can be built against — is invisible behind the specific meanings that ship with it, so systems that provide the same guarantees with entirely different meanings (a unikernel, a hypervisor tenant, a capability-based system) do not even register as operating systems.

This is a claim about clarity, not about correctness: the traditional view is not wrong — its bundle satisfies real needs, and Linux demonstrably works. The claim is that the bundle's shape is history, not essence, and that an architecture must not adopt it as its default.

#### Discussion

##### Rationale and alternatives
- **Say the traditional view is simply wrong (rejected)**: it is not — it is a working, battle-tested bundle, and dismissing it wholesale would discard the parts that genuinely belong at the OS level. "Misleading" is the precise defect: the bundle misleads exactly where it is read as essence rather than as history.
- **Leave the traditional framing unexamined and only define our own boundary (rejected)**: unexamined, the bundle returns through the back door — every component list, every "OS feature" checklist, and most OS literature start from it, so an architecture that does not explicitly mark the bundle as tradition will re-import it item by item.
- **Solve isolation gaps by inventing new tools (rejected)**: OS-level-virtualization tools — containers and the like — appeared because isolation guarantees were missing, and they bundle those guarantees with a particular choice of abstractions on top. The problems they solve belong to the layer that owns isolation; once the founding layers provide isolation as a guarantee, such tools become unnecessary rather than improved.

##### Prior art
The exokernel authors made the sharpest version of this critique from within OS research — arguing that traditional kernel abstractions encode policy that applications should control. Linux's own self-description ("just a kernel", with everything else delegated to user space) is itself partial evidence: it concedes that most of the traditional bundle already lives above the kernel, while the assembled kernel-plus-tooling whole is still presented as "the operating system".

The bundle's dominance is not evidence for it. The best-recorded account of why the traditional kernel won is sociological and economic, not architectural: timing (the rival family was paralysed by litigation while the project meant to complete the free stack lacked its kernel), license economics, the pragmatic "working code today" posture against academic perfectionism, and — decisively — network-effect lock-in: once investment concentrated on the bundle's interfaces, the cost of leaving exceeded the cost of enduring the bundle's defects, so defects stopped being selection pressure. Tooling ecosystems form around immediate pain and are further shaped by the commercial interests of whoever funds them; adoption is therefore evidence of what was convenient, not of what the boundary requires. The same skepticism applies in reverse when reading sources: a claim about a system's observable behavior is reliable regardless of its maker; a claim about that maker's motives is self-assessment, not evidence.

##### Unresolved questions
1. How far does the critique generalize — are there components in the traditional bundle that are guarantees in disguise (policy only in appearance)? The decomposition below is the working method for answering this case by case.

### Famous names: VM, container, and what they actually are
Virtual machine, container, hypervisor, socket, POSIX — these names carry weight in the industry, and that weight invites reading them as primitives with intrinsic value. In this architecture they have none: each is a packaging or compatibility choice the traditional bundle made, and each misleads exactly insofar as it is treated as a concept the OS must own. What they actually are:

- **Virtual machine (VM)**: a tenant of a hypervisor — one instance of the founding layer's whole-machine multiplexing, with a tenant-isolation guarantee attached. The name suggests a kind of computer; it is a deployment unit.
- **Container**: a process tree on a traditional kernel, sharing every one of that kernel's abstractions, with namespace-based *labeling* standing in for isolation. The name suggests a sealed unit; the seal does not hold.
- **POSIX**: a compatibility surface — one historical bundle's meaning, offered so that old code keeps running. It is meaning sold above the guarantees, not an OS requirement.

The container deserves the sharpest statement, because it is the name most often taken for a solved problem. A container does not close the neighbor problem: much of what appears isolated is not. Kernel-side memory — network buffers, page cache, connection state — is shared and unaccounted, so a busy neighbor consumes memory the tenant's own accounting never sees. The traditional remedy is blunt limits: cap the number of active file descriptors, shrink buffer pools — which does not remove the sharing, it throttles the input: an application forced to refuse work it had the CPU and memory to perform, one resource rationed while others sit idle. Under the boundary principle the diagnosis is short: a container is isolation bolted onto a kernel never designed to provide it as a guarantee. Isolation is a founding-layer duty (see [The OS's founding layers](#the-oss-founding-layers-firmware-bootloader-hypervisor)); a tenant that needs real isolation needs a hypervisor boundary, not namespaced labels.

#### Discussion

##### Rationale and alternatives
- **Adopt the industry names as concepts of this architecture (rejected)**: the names encode the traditional bundle's answers — using them as primitives imports those answers through every design conversation, which is precisely the import path this document exists to close.
- **Rebut each famous name in its own catalogue entry (rejected for now)**: the demystification generalizes into a test — which guarantee does this name provide, and which meaning does it define? A maintained catalogue of rebuttals would age; the test does not.

##### Prior art
Attempts to repair container isolation by inserting a kernel *below* the containers, and large providers' choice of VM-per-tenant (microVMs) where neighbor effects matter, are observable behaviors consistent with this topic's claim: label-based isolation is known to be incomplete by the very industry that named it. The same pattern continues outward — providers offloading tenant isolation onto dedicated hardware (DPUs, SmartNICs); if label-based isolation were a solvable kernel feature, the industry would not keep paying to move the problem outside the kernel.

##### Unresolved questions
1. Is there a subset of kernel-side memory that a shared-kernel tenant arrangement could fully account and isolate — or is honest multi-tenancy on one kernel impossible in principle, making the hypervisor boundary the only honest tenant boundary? Not yet argued through.

### Decomposing the OS without presupposition
Instead of starting from the traditional component list, start from the guarantee side of the [boundary principle](#the-os-responsibility-boundary) and classify everything the name "operating system" has historically carried. The test for OS-level status is: *would removing this component break a guarantee — or only a habit?* What remains is:

- **Guarantees (the actual OS)**: resource isolation, exclusive access control, privilege boundaries, controlled hardware interaction, and the minimal multiplexing machinery that enforces them — elaborated per requirement area in the topics below. Exclusivity is granted through **resource entitlements**: declared bounds per application (a minimum and a maximum) that the OS arbitrates against and accounts for. Entitlements are how the OS says *how much*, never *how* — they are the mechanism of exclusive access, not scheduling policy.
- **Default applications**: full user-level applications that a traditional OS ships purely by habit. A launcher is a GUI app a user runs to list and start other apps; a shell is a text-driven app doing the same; an init system is an app that starts other apps at boot; a login manager authenticates and starts a session; a package manager, a file manager, a text editor are applications. Each answers a real need, but none needs a special OS-level abstraction — they are clients of the guarantees like any other app. Calling them *default* apps (apps this OS happens to ship) rather than *system* components keeps their status honest: ordinary, swappable, architecturally unexceptional.
- **Traditional abstractions (meaning, pushed up)**: the socket, the filesystem tree, the thread, the process with its signals and file descriptors — each is one possible meaning built on the guarantees, and belongs to the system that needs that meaning. The requirement areas they belong to are worked out in their own topics: [Compute](#compute-cores-not-threads), [Storage](#storage-block-abstractions-not-filesystems), and [Networking](#networking-frame-delivery-not-communication-meaning).
- **Identity conventions (re-examined)**: the traditional *user* is a bundle, not a concept — treated in [Identity](#identity-principals-not-users).

#### Discussion

##### Rationale and alternatives
- **Keep the traditional component names but redefine them (rejected)**: redefining "user" or "process" while keeping the word invites the old meaning back through every reader's prior associations. Where a traditional word's meaning genuinely changes, this document describes the thing rather than reusing the label; naming is revisited once the concepts stabilize.
- **Declare the default apps outside the OS's concern entirely (rejected)**: they are outside the OS's *guarantees*, but an OS distribution still has to ship something that starts and manages applications — the point is their status (ordinary, replaceable apps), not their absence.

##### Prior art
Capability-based systems (seL4, Capsicum, Fuchsia) already shrink identity to principals-with-capabilities and treat shells and file managers as ordinary programs; the exokernel program treated even the filesystem as a library. The default-app framing generalizes the same move to components — launcher, init, login — that are usually discussed as OS subsystems rather than as applications.

##### Unresolved questions
1. What vocabulary should replace the bundled terms — for the process-like unit, for the default apps? Naming should wait until the concepts have stabilized across more of this project's documents.
2. Does the boot path change the analysis — is the first code that enforces the guarantees itself a default app, or part of the guarantee machinery? The [founding-layers](#the-oss-founding-layers-firmware-bootloader-hypervisor) topic takes up the layers below that code.

### Compute: cores, not threads
This document's execution claims are deliberately narrow, and their conceptual footing is [Process](./process.md)'s: understand the process before selecting the mechanism; a thread — like a transaction, a queue, or a lock — is a mechanism that may participate in executing a process, not the process itself and not an intrinsic requirement of one. The rejection of the thread as an OS-level concept is that same separation applied downward: the thread is a mechanism with a name, and mechanism names must not become the OS's vocabulary.

What remains at the OS level is the guarantee side only: exclusive use of a core's time — assign a core slice to some execution, enforce the privilege boundary around its address space, and take the core back when the slice ends or the execution gives it up. The unit at this level is *something running with an address space and a core-time entitlement* — process-like in shape, but carrying none of the traditional process's bundled meaning (signals, credentials, file descriptors, a controlling terminal), because that meaning belongs to the systems above. Concurrency is not an OS-level question: which activities may progress simultaneously, under which constraints, and whether a synchronization mechanism is needed at all are questions the process itself answers, by [Process](./process.md)'s method — and the OS must not presuppose their answers in its own vocabulary. Multiplexing many executions onto few cores *is* a genuine OS guarantee (exclusive access means someone must arbitrate); *how executions relate, communicate, or wait for each other* is meaning, defined above.

#### Discussion

##### Rationale and alternatives
- **Answer concurrency questions here (rejected)**: this document's neighbor, [Process](./process.md), already governs them — concurrency is treated there as a property of how a process's parts may progress, with locking and synchronization as possible mechanisms selected only after the process is understood. Restating or specializing those answers here would risk contradicting them, and the OS layer must not carry concurrency meaning the process layer has not assigned to it.
- **Keep threads at the OS level as the price of preemption (rejected for now)**: preemption is a guarantee-side mechanism (taking the core back is exclusive-access enforcement), but the core-time entitlement is a thinner preemptible unit than the thread; what the traditional thread adds beyond it — identities, priorities, signal delivery — is policy and meaning.

##### Prior art
[Process](./process.md)'s own records are the direct basis for this topic: its Motivation came from public discussions where mechanisms (rollback, locking, Saga) were treated as requirements; its modeling-errors list rejects treating concurrency as locking and treating execution representation as execution responsibility; and its "a thread is not a process" ruling is precisely the separation this topic applies at the OS boundary.

##### Unresolved questions
1. What does the guarantee side owe an execution that must wait — for a device to complete, a timer to expire, another entitlement's slice to end? A completion mechanism exists within the guarantees (controlled hardware interaction), but its exact shape must be worked out together with [Process](./process.md)'s treatment of progression, and must not violate its principles.
2. Can parallelism within one address space be expressed as several core-time entitlements over one address space — and should that be modeled through [Process](./process.md)'s Worker concept rather than a new OS-level unit?
3. Does preemptive arbitration of cores need scheduling policy at the OS level, or can the policy live in a default app (or a higher-level system) with the OS enforcing only the exclusivity it is told to enforce?

### Storage: block abstractions, not filesystems
A filesystem is an upper-level abstraction and has no place at the OS level. What the OS provides for storage is the same kind of answer it provides for volatile memory: an exclusive, bounded block abstraction granted per application — per OS image, in the unikernel reading — with the privilege boundary enforced around it, and nothing more.

The analogy with memory is exact and deliberate. The OS multiplexes volatile memory down to exclusive page grants but does not decide — or even comprehend — how an application manages the memory it holds: which allocator, which data structures, which caching policy. Non-volatile storage deserves the same restraint. The OS grants block ranges exclusively and enforces the boundary; how those blocks become records, tables, logs, journals, or object stores is meaning, defined by the application or the system above it — this project's own reevaluation of the filesystem ([Filesystem](./filesystem.md)) is where that meaning is worked out, not here. A general-purpose filesystem — one tree and one set of semantics imposed on every application — is precisely the down-pushed meaning the boundary principle rejects, and the unikernel finding that general-purpose filesystems are not universally required is the empirical confirmation of this position.

#### Discussion

##### Rationale and alternatives
- **Keep a filesystem in the OS because applications expect one (rejected)**: an expectation formed by the traditional bundle is not a requirement. An application that wants tree semantics carries the library that provides them — exactly as a unikernel does — and pays only for the semantics it uses.
- **Push block arbitration into each application entirely (rejected)**: exclusive access to raw devices is a guarantee the OS must arbitrate — two applications cannot both hold the same blocks. The position is not "no OS in storage" but "no storage meaning in the OS": the OS stops at exclusive, bounded block grants.
- **Keep log-as-file because observability tooling expects it (rejected)**: the traditional log is the filesystem's meaning pushed into observability — structured events flattened into an unstructured byte stream, then re-structured downstream by dedicated tooling. Under this topic's position, an application's diagnostic output is storage meaning defined above the OS: events as events, delivered to whoever observes them, needing no file at all.

##### Prior art
The exokernel program placed filesystem semantics in per-application library operating systems; unikernel builds compile in only the storage semantics the application needs. The memory analogy is the long-standing observation that the OS hands out pages, not heaps.

##### Unresolved questions
1. Does the block abstraction include arbitration of device throughput between applications — entitlement to bandwidth as a guarantee-side duty — or does throughput policy follow the same core-time-entitlement reasoning as compute? Not yet argued through.

### Networking: frame delivery, not communication meaning
The network requirement decomposes the same way as every other. What the OS does: provide exclusive, privilege-bounded access to network hardware; deliver frames to and from the wire for the applications entitled to them; and arbitrate the hardware between those applications by their entitlements. What the OS does not do: define what a connection is, own a protocol, terminate, transform, or interpret communication, or impose a transport vocabulary. Sockets, connection lifecycles, sessions, and application protocols are upper-level meaning — this project's own protocols, such as [Chapar](./chapar.md) at the data-link level or [sRPC](./sRPC.md) between services, are built against the guarantees, not inside the OS.

Even packet routing can be an application: a router is a service holding an entitlement to the network hardware, not a sanctified OS subsystem. And the same OS serves servers, clients, and routers alike without a device-class concept at the OS level — what a machine is *for* is a deployment and application decision, not a property of the OS: no editions, no device taxonomy inside it. The OS's constraint is only that the hardware is never shared without exclusive-access arbitration and that privilege boundaries hold at the wire; the OS neither interprets nor alters what passes through it — it delivers. Everything above that is communication meaning, and meaning lives above.

#### Discussion

##### Rationale and alternatives
- **Ship a network stack with the OS (rejected)**: a stack is a bundle of protocol meanings — transport semantics, addressing conventions, naming — that every application then inherits whether or not they fit. The traditional stack exists because the traditional bundle pushed meaning down; under the boundary principle, each system selects or defines its protocols above the guarantees.

##### Prior art
The exokernel program moved protocol semantics into library operating systems; the end-to-end argument holds that functions placed below the level where communication meaning is known tend to misserve it. The strongest recent confirmation is QUIC: a transport protocol implemented in user space over an existing datagram protocol, because injecting new protocol semantics into the traditional kernel had become impractical — meaning forced to escape the OS rather than be defined by it, exactly the inversion this document's position predicts and removes. Project-internal evidence: [Chapar](./chapar.md) defines data-link protocol behavior as its own document, not as an OS feature.

##### Unresolved questions
1. Does frame delivery itself belong to the OS, or can even that be a default app holding an entitlement to the NIC — with the OS providing only exclusive hardware access? The answer decides how thin the OS's network duty really is, and has not been argued through.

### Identity: principals, not users
The OS does not need the traditional concept of *user* — an account with a name, a home directory, a login shell. That is a bundle of tradition, not a concept the guarantee side requires. What the guarantees actually need is narrower: a notion of **principal** that privilege boundaries can attach to — something that can hold exclusive access, be granted capabilities, and be held accountable for what it does with them.

Whether a principal resembles a person, a service, a device, or none of these is a decision of the system being built. The mapping of humans onto principals belongs to a default app (a login manager), and a home directory is storage semantics owned by a higher-level system — neither is an OS concept.

#### Discussion

##### Rationale and alternatives
- **Keep "user" but redefine it (rejected)**: reusing the word invites the traditional meaning back through every reader's prior associations; this document describes the thing without the label, and naming is revisited once the concept stabilizes.
- **Drop identity from the OS entirely (rejected)**: privilege boundaries need something to attach to; without principals, exclusive access control has no subject.

##### Prior art
Capability-based systems (seL4, Capsicum, Fuchsia) shrink identity to principals-with-capabilities; the wider identity concepts — accounts, profiles, home directories — live in applications above them.

##### Unresolved questions
1. What relationship holds between a principal here and the Principal concept in [Agency](./agency.md)? The two documents use the same word for related but not yet reconciled concepts; the reconciliation is its own session.

### Implementations and providers
Concrete anchors for the unikernel position, recorded so the abstract discussion above has verifiable referents:

- **Nanos** — an open-source unikernel: <https://github.com/nanovms/nanos>
- **NanoVMs** — the company providing and supporting Nanos: <https://nanovms.com/>

These are examples, not requirements; any implementation that compiles an application with only the OS code it needs into a single image instantiates the position. The direction is visible in current practice: large cloud providers run per-tenant microVMs — virtual machines trimmed to a single application — and offload networking and storage to programmable hardware placed in front of the host, reducing the traditional kernel's role toward booting and legacy compatibility. These are observable behaviors, recorded as evidence that the industry already separates founding duties from the traditional kernel — not as endorsements.

#### Discussion

##### Unresolved questions
1. Whether Nanos actually respects the boundary principle — or defines traditional abstractions (a POSIX-ish surface, a general-purpose network stack) inside its library set — has not been evaluated. Recording it as an example does not certify it.
2. Whether observability without the traditional process abstraction — events and entitlements as the diagnostic surface — can match the traditional tooling's debugging expectations has not been argued; those expectations are themselves bundle-shaped.

### Relationship to PersiaOS
PersiaOS ([persia_os.md](./persia_os.md)) is a project built on this architecture that delivers applications; it is not part of the architecture itself, and its own document is a project document, not an architect-level one. The architect-level claims its earlier document carried — the isolation-first principle, routing as an application, per-application resource entitlements, device-class neutrality — have been absorbed into this document where they hold. Its project-specific decisions (dedicated network protocols, firewall placement, accounting defaults) remain PersiaOS's own, and its document should stand as an application of, and a reference into, this document rather than as a restatement of it.

#### Discussion

##### Unresolved questions
1. Which kernel-structuring answer PersiaOS takes, and where its project documents live once re-scoped out of the architect's documentation, are PersiaOS's own decisions; until then, its document should be read as a project brief that references this one for every architect-level claim.

## Results
Insufficient time has passed since this document was formed to report real, observed outcomes from its use. This section will be filled in once there is such experience to draw on.

## Discussion

### Drawbacks
Organizing by requirement area rather than by traditional component means a reader arriving with a traditional name — "threads", "filesystem", "network stack" — must map it to the requirement topic that owns it. The mitigation is deliberate: each such name is answered exactly once, in the topic that states the area's capability and constraint, and the cross-references to the concept's own governing document ([Process](./process.md), [Filesystem](./filesystem.md), [Chapar](./chapar.md)) carry the reader the rest of the way.

### Rationale and alternatives
- **Organize by the traditional component list (rejected)**: the list is the bundle this document argues against; using it as the table of contents would make the old taxonomy the navigation model even where the text rejects it.
- **State each requirement wherever it first becomes relevant (rejected)**: scattering a requirement's capability and constraint across topics is exactly how the traditional view's assumptions survive a critique — one topic per requirement keeps each answer checkable and referenceable as a whole.

### Unresolved questions
1. Does the project need a dedicated document recording *which* kernel-structuring answer its OS takes, once decided — or should that decision live inside the PersiaOS architecture document, with this document linked as the conceptual foundation?

### Future possibilities
- If the device-driver question (see the boundary topic's unresolved questions) is resolved, this document gains a topic defining what "controlled interaction with hardware" means precisely enough to implement against.
- If new requirement areas emerge that no topic covers, they join the same pattern — one topic, one capability-and-constraint statement — rather than growing the existing topics sideways.









