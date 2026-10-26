---
Title: "Guest"
Status: Draft
Start Date: 2026-10-17
ID: 497842
---

# Guest
## Abstract
**Guest** is the label of a module whose subject is a surface that Memar does not own: a protocol the outside world already speaks and will keep speaking without Memar's agreement — HTTP, TCP, a JSON grammar, a SOAP envelope — or a design name that circulates with senses Memar does not inherit. A guest module is placed like any other module, by the tests of [Kernel](./kernel.md) and [Pluggable](./pluggable.md), and carries `guest` among the `labels` of its manifest. The label, not a path, is what says "this exists here, but it is not Memar's". It replaces the `lib/` category, whose path carried that claim and could not carry it without a second place for every subject ([Placements → Decisions](../placements.handoff.md#decisions)).

## What the label claims
A module labelled `guest` holds Memar's side of a foreign surface and nothing else:
- **The realization** of a contract whose authority is outside this project — RFC 8259 for the JSON grammar, the IETF's and the W3C's specifications for the HTTP request and response shape, the SOAP and WSDL specifications for the envelope. Memar conforms to the surface and may implement it; the Khayyam realization of that conformance sits in the module.
- **Memar's position** on relying on the surface, as the module's main document. [http.md](../../../../modules-plugable/net/http/http.md) states Memar's position on HTTP, and it is where a divergence from the outside world's rule is argued. A position is not a copy of the requirements: those are their owner's ([Protocol → Who Defines a Protocol](../../../../docs/protocol.md#who-defines-a-protocol)), and a position document never restates them as Memar's.
- Where Memar's position grows into rules of its own — a divergence argued in the module — those rules are Memar's, and conformance to them is decided as for any module ([Protocol → Conformance](../../../../docs/protocol.md#conformance)).

## The test
A module earns the label when its subject is a surface whose meaning **Memar cannot change without the agreement of someone outside this project**. The test is authority, not familiarity, and it applies to positions as well as to declarations. Two kinds of module pass it:
- **A protocol surface owned outside Memar** that Memar's stack conforms to and may itself realize — the application-protocol case ([http.md](../../../../modules-plugable/net/http/http.md)) and the storage case ([filesystem.md](../../../../modules-plugable/computer/memory/filesystem/filesystem.md)).
- **A design name that circulates with senses Memar does not inherit** — [ddd.md](../../../../modules-plugable/process/ddd/ddd.md) is the case. Such a name is not a protocol surface and has no declarations; it is labelled because the authority over what the name means is outside Memar, and not because of the form its subject takes.

## The rule
1. **A protocol Memar does not own carries the label `guest`.** If changing its contract would require the agreement of someone outside this project, the module is a guest whatever language it is written in and however much of it Memar relies on.
2. **The module's name is the foreign protocol's own, spelled the way the outside world spells it.** `http`, `soap`, `json` are the names those worlds use. A name Memar coined does not qualify for the label.
3. **A protocol Memar owns never carries the label, and is never mirrored.** No copy of a Memar module is made under a guest's name, and no module is duplicated in a renamed form: a subject Memar owns has exactly one home, at its own address, reachable by the same `in` address as everything else. The timer is the counterexample that made the rule necessary: it is Memar's own, so a second address for it, rooted under the foreign shelf, was a second address for one subject, and the second address was the one two files actually imported from.
4. **A guest's place follows the module it attaches to.** The guest stands at the mirror of the Memar module it attaches to, as a [pluggable](./pluggable.md) module ([Category Depth](../../label/rules/category-depth/category-depth.md)), because the claim of the label no longer depends on the path. HTTP attaches to the networking Memar owns and stands under `net`; the JSON grammar attaches to the codecs and stands at `computer/codec/json`.

## What does not carry the label
- **Memar's own protocols.** Their specification and realization are in the category that owns the concern, under its own name, with no separate shelf.
- **A generic mechanism wearing a protocol's name.** An abstraction that any implementation might satisfy and that no outside world defines is not foreign by sitting beside one. The minify abstraction is such a mechanism and is Memar's own; whether a minifier of a given format earns the label is decided per format ([Placements → Open Questions](../placements.handoff.md#where-each-minifier-implementation-goes)).
- **A host language's standard library.** A module that mirrors another implementation's library names an implementation, not a protocol surface; that was the mistake in the name the shelf once had. The sources' Go reference implementation is a different repository (`memar-go`).
- **Restated requirements.** A foreign surface's requirements are its owner's, and a position states Memar's position on relying on it.

## Related artifacts
| Artifact | Relation | Action |
| --- | --- | --- |
| [Placements](../placements.md) | Base — the module that defines the labels and the placements | None (read) |
| [Pluggable](./pluggable.md) | Depends_on — where a guest is placed | None (read) |
| [`placements.handoff.md`](../placements.handoff.md) | Reference — the open questions the label inherited from the `lib` category | Follows this document |
