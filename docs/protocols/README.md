# Protocols (`/docs/protocols/`)
This directory holds the specifications of **Memar's own protocols** — the named sets of declarative rules Memar owns and expects systems built with it to conform to, independent of any programming language and of any implementation. See [Protocol](../protocol.md) for the general concept; a document here answers "what is *Memar's* protocol for X?", not "what is X?".

## Membership criterion
A document belongs here when it specifies, or is expected to grow into the specification of, one of Memar's own protocols — a contract, rule set, or wire/encoding format any language or stack can realize. A second kind also belongs here: a document stating **Memar's position on an external protocol surface Memar implements** — a rule set owned outside Memar (the filesystem's POSIX/VFS surface, HTTP as an application protocol), which Memar's stack conforms to and may itself realize, e.g. in [memar-khayyam](https://github.com/GeniusesGroup/memar-khayyam/); such a document answers "what is Memar's position on depending on X?", not "what is X?" — [filesystem.md](./filesystem.md) is the storage case; [http.md](./http.md) is the application-protocol case. Documents enter at whatever [Status](../documentation-explanation.md#status) they carry, including Draft, and are developed here toward their full protocol form: a Draft that currently records the *why* and the open questions is expected to mature in place until it states the protocol itself. What an organization may hold a different view on, and what the OS leaves to the system above it, are stated in the documents themselves as parts of the protocols, not decided here.

What does **not** belong here:
- **Concept documents** (System, Type, Process, [Protocol](../protocol.md), Modeling, ...) — these model general concepts and lenses; they stay at `docs/` root.
- **Khayyam language documents** — the language's own design and specification lives in [`../khayyam/`](../khayyam/README.md); the protocols here are what Khayyam conforms to, not the language itself.

**Citation direction.** The layering carries a citation rule: where a document here derives from, applies, or is projected onto a base document's principles, the citation runs from the protocol document *down* to the base document — never back up. A base document's rules stand on its own layer's adopted principles, so it holds no reference up to a protocol document as the authority for them: where it must name a concern whose working-out is owned by the protocol layer, it names that ownership without a link, as [Modeling](../modeling.md) does for the retention concepts. Referencing a protocol document as a **consumed contract** — a document outside this layer applying the protocol's definitions in its own working, rather than deriving its own principles from them — is a different relationship and remains legitimate (as the [Control Flow](./control-flow.md) design consumes [The Error](./error.md): the protocol owns what an error is, once and language-independently, while the grammar refuses error semantics entirely — see [Khayyam → The Grammar Refuses Protocol Semantics](../khayyam/khayyam.md#the-grammar-refuses-protocol-semantics)).

The documents themselves are not listed here — the folder listing is the index. This file only states the folder's role and criterion, which do not change when documents are added.

## Where implementations live
This folder is each protocol's source of truth — **not executable code**. An agent that needs running code for one of these protocols does not need to read these documents as an implementation specification at all; it should go to the implementing repository instead. For example, the Error protocol in Go lives at [memar-go](https://github.com/GeniusesGroup/memar-go/), concretely under [`process/error`](https://github.com/GeniusesGroup/memar-go/tree/dev/process/error).

### Implementation repositories
All implementing repositories share one structure — the same package path, with file extensions naturally differing per language. The repositories that exist today:

| Repository | Language |
| --- | --- |
| [memar-khayyam](https://github.com/GeniusesGroup/memar-khayyam/) | Khayyam |
| [memar-go](https://github.com/GeniusesGroup/memar-go/) | Go |
| [memar-js](https://github.com/GeniusesGroup/memar-js/) | JavaScript |
| [memar-rust](https://github.com/GeniusesGroup/memar-rust/) | Rust |
| [memar-c](https://github.com/GeniusesGroup/memar-c/) | C |

### Missing an implementation for your language?
If the package your language needs has not been developed yet, two paths are open:

- **Develop it yourself** and send us a PR. A practical way to start: port from the implementation of a language close to yours, and verify the result against this folder's document for the protocol — the documents here are the source of truth the porting must satisfy.
- **Open an issue** in the relevant repository, and we will develop it at the earliest opportunity.

If your language does not even have a `memar-{language}` repository yet, open an issue in [memar](https://github.com/GeniusesGroup/memar/) asking for that repository to be created.

One exception to note for now: Memar is not stable yet, and idea-testing commits currently land on the `dev` branch rather than `main`, so the links above point into `dev`. `main` remains the primary branch, and `process/error` is the real — and almost certainly final — package path.
