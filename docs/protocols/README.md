# Protocols (`/docs/protocols/`)
This directory holds the specifications of **Memar's own protocols** — the named sets of declarative rules Memar owns and expects systems built with it to conform to, independent of any programming language and of any implementation. See [Protocol](../protocol.md) for the general concept; a document here answers "what is *Memar's* protocol for X?", not "what is X?".

## Membership criterion
A document belongs here when it specifies, or is expected to grow into the specification of, one of Memar's own protocols — a contract, rule set, or wire/encoding format any language or stack can realize. Documents enter at whatever [Status](../documentation-explanation.md#status) they carry, including Draft, and are developed here toward their full protocol form: a Draft that currently records the *why* and the open questions is expected to mature in place until it states the protocol itself. What an organization may hold a different view on, and what the OS leaves to the system above it, are stated in the documents themselves as parts of the protocols, not decided here.

What does **not** belong here:
- **Concept documents** (System, Type, Process, [Protocol](../protocol.md), Modeling, ...) — these model general concepts and lenses; they stay at `docs/` root.

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
