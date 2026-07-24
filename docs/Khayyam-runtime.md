# Khayyam Runtime Specification (Reference Architecture)
*Note: Khayyam is a syntax and a set of architectural rules. It does not dictate a specific runtime. However, this document outlines the Memar runtime architecture (the Memar Framework) designed to maximize Khayyam's potential, particularly for high-performance and Unikernel/Exokernel environments.*

## Concurrency and Execution Model
Unlike traditional languages that hardcode concurrency primitives (like `channels` or `mutexes`) and black-box schedulers into the language core, the Khayyam ecosystem delegates these entirely to the runtime library.

* **User-Space Scheduling:** Thread management, yielding, and context switching are handled by user-space schedulers provided by the framework. This eliminates the overhead of kernel-level context switches.
* **Library-Driven Primitives:** Synchronization tools (Channels, Mutexes, WaitGroups) are capsules (libraries) rather than syntax keywords. This allows developers to swap, rewrite, or bypass them entirely based on domain needs.
* **Core Affinity & Lock-Free Design:** The runtime framework MUST provide mechanisms to pin specific tasks (e.g., handling TCP packets for a specific IP/Port pair) to dedicated CPU cores. This empowers developers to achieve true lock-free concurrency, entirely avoiding the performance penalties of `mutexes` for isolated state mutations.

## Change logic in runtime
You can write code to change(add or remove) modules binary code in runtime. It is like `WASM` idea. It can be very dangerous feature and MUST tag as `unsafe`. It is useful to add or remove modules in microservice way but as describe by [this paper from google expert software developers](https://dl.acm.org/doi/pdf/10.1145/3593856.3595909)
