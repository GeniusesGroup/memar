---
Title: "Lib"
Status: Draft
Start Date: 2026-09-26
ID: 510442
---

# Lib
## Abstract
This document states what the `modules/lib/` module is and fixes the placement rule that gives it a reason to exist: **a protocol that is not Memar's own belongs here.** An HTTP, a TCP, a JSON codec, a SOAP envelope — anything an outside world already speaks and will speak without Memar's agreement — is realized in this repository under `lib/`, so that the path itself carries the one claim that matters about such a thing: *this exists here, but it is not Memar's*. Anything Memar itself offers is not here; it lives in the category that owns it, under its own name, with no separate shelf. The module's unfinished state is in the paired [handoff](./lib.handoff.md).

## What this module is
The module holds realizations of **foreign** protocol surfaces. Each is a contract whose authority is outside this repository: RFC 8259 for the JSON grammar, the W3C's and IETF's HTTP specifications for the request and response shape, the SOAP and WSDL specifications for the envelope. Memar conforms to them and may implement them, and this is where the Khayyam realization of that conformance lives.

`docs/protocols/` states *Memar's position* on such a surface — [http.md](../../docs/protocols/net/http.md) is that document, and it is where any divergence from the outside world's rule is argued. This module is the other half: the declarations that position is realized in. The two are not the same thing, and neither is a copy of the other; [the protocol index](../../docs/protocols/README.md#where-implementations-live) fixes the split, this folder fixes its address.

## The rule
1. **A protocol Memar does not own belongs under `lib/`.** The test is authority, not familiarity. If changing the contract would require the agreement of someone outside this project, it is a foreign protocol and it is realized here — whatever language it is written in, and however much of it Memar relies on.
2. **The folder's second level is the foreign protocol's own name, spelled the way the outside world spells it.** `http`, `soap`, `json` are the names those worlds use. A name Memar coined does not qualify for this folder; it belongs in the category that owns the concern.
3. **A protocol Memar owns belongs in the category that owns it, with no separate shelf.** No mirror of a Memar module is ever created under `lib/`, and no module is duplicated here in a renamed form. A material that is genuinely Memar's is one folder, at its own address, reachable by the same `in` address as everything else.

Rule 3 is the one that was broken, and the [handoff](./lib.handoff.md) records what the break cost. It is stated here as a rule because the corpus already had the counterexample: a timer is Memar's own — [the Time module](../time/README.md) owns it, its contract is stated in [`docs/protocols/time/time.md`](../../docs/protocols/time/time.md), and the shape of its declarations is settled there — so a `libgo`-rooted copy of it was a second address for one subject, and the second address was the one two files in the time module actually imported from.

## What does not belong here
- **Memar's own protocols.** Their specification is in [`docs/protocols/`](../../docs/protocols/) and their realization is in the category that owns the concern — control flow under [`modules/process/`](../process/), the runtime and its mechanisms under [`modules/computer/runtime/`](../computer/runtime/), identity under [`modules/identifier/`](../identifier/). A subject that is Memar's has exactly one home.
- **A generic mechanism wearing a protocol's name.** An abstraction that any implementation might satisfy and that no outside world defines is not foreign by being in this folder. A minifier, for instance, is a capability; whether it earns this folder is an open question, not a settled one.
- **A host language's standard library.** A `lib`-named shelf that mirrors another implementation's library names an implementation, not a protocol surface — which is the mistake that made this module's own previous name wrong. `libgo` said "Go's libraries"; the module holds no Go and claims no Go. The corpus's Go reference implementation is a different repository (`memar-go`), and the `.kh` sources here are Khayyam's, held in the repository where the specifications are.
- **Specifications.** This module realizes; it does not restate. A divergence from the outside world's rule is argued in [`docs/protocols/`](../../docs/protocols/), not here.
- **Generated output and a language's own toolchain.** Build products are git-ignored, and anything specific to one compiler lives under [`modules/khayyam/`](../khayyam/).

## The contents at a glance
Three protocol families are held, in three of the categories the corpus already had open. What each is here for is what makes this a reading rather than an inventory.

| Address | The foreign surface | Why it is here rather than in a Memar category |
| --- | --- | --- |
| [`net/http/protocol/`](./net/http/protocol/) | The HTTP request/response shape — method, status, version, header, pseudo-header, body | An HTTP request is defined by the IETF and the W3C, not by Memar. [`modules/net/`](../net/) holds Memar's own networking concerns, of which HTTP is a consumer and never a part |
| [`net/soap/protocol/`](./net/soap/protocol/) | The SOAP envelope, its header, its fault, and its handler | A W3C specification, built on a socket Memar's net module owns. Nothing in it is Memar's to change |
| [`codec/json/protocol/`](./codec/json/protocol/) | The JSON grammar and the marshal/unmarshal shapes over it | The grammar is fixed by [RFC 8259](https://datatracker.ietf.org/doc/html/rfc8259). [`modules/codec/`](../codec/) holds Memar's own codec abstractions, which JSON realizes and does not define |
| [`codec/string/protocol/`](./codec/string/protocol/) | The human-readable text shape, `dt-text.kh`, and a stringer over it | A claim on how data is rendered for a person, inherited from the ecosystem's own vocabulary rather than stated by Memar |
| [`codec/minify/protocol/`](./codec/minify/protocol/) | The minifier shape | **Contested** — carried here by the move, not by an argument. See the handoff |
| [`process/command/protocol/`](./process/command/protocol/) | The command-line argument and sub-command shape | The argv convention and the `getopt`-style reading of it are the shell's and the operating system's, not Memar's |

The second level is still a Memar category name — `codec/`, `net/`, `process/` — which the rule permits but does not require, and which is the sharpest thing the owner has yet to rule on: whether `lib/` groups foreign protocols under the Memar category they attach to, or sits one level flatter with only the foreign names under it. The rule's claim is weakened by a path that reads `lib/codec/…`, since `codec` is a Memar category. The handoff carries it.

## Membership criterion
Material belongs in this folder when its subject is **a protocol surface Memar does not own** — the declarations a conformance is written in, for a contract whose authority is outside this project. It does not belong here: a protocol Memar owns, a Memar position on a foreign surface (that is [`docs/protocols/`](../../docs/protocols/)), a generic mechanism, or an implementation's own library naming.

## Related artifacts
| Artifact | Relation | Action |
| --- | --- | --- |
| [`docs/protocols/net/http.md`](../../docs/protocols/net/http.md) | Reference — Memar's position on the HTTP surface this module realizes | None (read) |
| [`modules/README.md`](../README.md) | Reference — the layer's own kinds of folder | Its "By responsibility" row should say what `lib/` is for |
| [`modules/time/README.md`](../time/README.md) | Depends_on — the category that owns the timer, whose stray import address this module's move exposed | None (read) |
| [`lib.handoff.md`](./lib.handoff.md) | Base — this module's open state | Follows this document |
