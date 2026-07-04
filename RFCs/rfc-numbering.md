---
RFC Number: 000000  # PLACEHOLDER — replace at commit time with `date -u +%s` (UTC unix seconds). Do not assign earlier; see Reference-level explanation.
Title: "RFC Numbering Scheme"
Status: Draft
Start Date: 2026-07-04
Applied to: ["README.md#rfcs"]
Supersedes: null
Superseded by: null
Related:
  Depends_on: []
  Extends: []
  Conflicts with: []
Author(s): []  # ["My Name (me@example.org)"]
---

## Summary

RFC Number is a UTC unix timestamp (seconds), generated once at the moment the RFC file is created, and never reused or reassigned afterward. It carries no meaning about domain, subsystem, or importance — only creation order. Filenames do not contain the number; they contain only a short, human-readable, hyphenated slug derived from the Title. The number lives solely in the `RFC Number` front-matter field and is looked up via full-text search or the README index, not via the filename or directory position.

## Motivation

Three separate problems, discovered across earlier attempts at this project, motivate this RFC:

1. **Domain-encoded ranges create coupling.** An earlier informal scheme reserved number ranges per domain (e.g. 1–999 for Khayyam). This tied a supposedly permanent identifier to a classification that can itself change over time (e.g. deciding the standard library should be its own domain, separate from Khayyam). Any such reclassification would force renumbering, and renumbering breaks every existing cross-reference (`Depends_on`, `Extends`, `Supersedes`) across the whole RFC graph.
2. **A single incrementing counter needs a coordinator.** A project intended to span multiple generations and, potentially, multiple contributors working without constant synchronization cannot safely rely on a single "next number" counter without some registration authority (this is the same reasoning that has pushed distributed storage systems away from auto-increment primary keys).
3. **Encoding domain or filename content into the number is redundant with, and weaker than, other fields.** `Start Date` already records chronology explicitly; a domain field (if one exists) already records classification explicitly. The number does not need to duplicate either.

## Guide-level explanation

When starting a new RFC:

1. Copy `000000-rfc-template.md` to `<short-descriptive-slug>.md` (no number in the filename — e.g. `sRPC-connection-identity.md`, not `001500-sRPC-connection-identity.md`).
2. Leave `RFC Number` as the placeholder until the moment you actually add the file to the repository. At that moment, run `date -u +%s` and put the resulting integer in the field.
3. Once set, this number never changes again for the lifetime of the RFC — even if the RFC is later rejected, superseded, or the title/slug is revised (a title change that alters the concept is treated as a new RFC per existing convention, with its own new number).
4. To find an RFC by number later, use a text search for `RFC Number: <value>` across the RFCs folder, or consult the README index, which lists Number, Title, and Status together.

## Reference-level explanation

- **Value**: UTC unix time in whole seconds, taken at file-creation time, written as a plain decimal integer (e.g. `1783141825`). UTC is mandatory to avoid ambiguity across contributors in different time zones.
- **Uniqueness**: In practice, at the cadence RFCs are produced in this project (at most a handful per day), a second-level collision is not expected to occur. If it does, resolve manually: whichever RFC was proposed first is confirmed as-is; the other is bumped forward by whole seconds until a free value is found. There is no automated tie-break based on sub-second precision — sub-second timestamps are not stored, only compared informally if a collision is ever noticed.
- **Filename**: `<slug>.md`, where slug is a short, hyphenated, lowercase-or-natural-case rendering of the Title, with no number and no domain prefix. The slug is expected to remain stable once the RFC reaches Final status, consistent with the existing rule that a meaningful rename constitutes a new RFC.
- **Retroactive numbering for pre-existing RFCs**: RFCs written before this scheme was adopted should be assigned a timestamp derived from their recorded `Start Date`, using midnight UTC of that date unless a more precise creation time is known. Where multiple pre-existing RFCs share the same `Start Date`, order them arbitrarily but consistently (e.g. by their current legacy number) and space their assigned timestamps by whole seconds to keep them distinct.
- **Lookup**: Because the number is not in the filename, discovery relies on (a) full-text search for the `RFC Number:` field, and (b) the README index table, which should list Number, Title, Status, and (optionally) any relevant domain/tag metadata defined by other RFCs.

## Drawbacks

- The number is no longer purely arbitrary — it now encodes creation order, which is a form of meaning. This is a deliberate exception to the earlier "the number should carry no meaning" principle, justified because creation time is an immutable historical fact and cannot later be "reclassified" the way a domain label can. It is a different kind of meaning than domain-coupling, but it is meaning nonetheless, and worth naming explicitly rather than treating this as a fully meaning-free scheme.
- A ten-digit decimal number is longer and less immediately memorable than the six-digit sequential number previously used, and offers none of the "small, aesthetically continuous number" property that other RFC-style projects (see Prior art) have explicitly valued enough to design around.
- Collision handling, as specified, still requires a manual, human-mediated resolution step at the moment a collision is noticed. It reduces the likelihood of collision compared to a naive shared counter, but does not remove the need for a coordination point entirely.
- An unsigned 32-bit representation of unix seconds overflows in 2106. Given this project's explicit multi-generational framing, this ceiling may be worth a documented decision rather than silence, even though it is roughly 80 years away.
- Retroactive backfilling for pre-existing RFCs sharing the same `Start Date` has no principled ordering signal (only date-level, not time-level, precision is recorded), so the ordering for those specific RFCs will be arbitrary rather than historically accurate.
- The exact moment that counts as "creation" (idea first discussed, file first drafted, or file first committed to the repository) is not the same for every RFC produced through this process, since drafting and committing may be done by different people at different times. Without a fixed convention, the field's meaning could become inconsistent across RFCs.

## Rationale and alternatives

- **Domain-encoded ranges (rejected)**: couples the identifier to a classification that can change, forcing renumbering and broken cross-references when it does.
- **Single incrementing counter, assigned at creation (rejected)**: requires a central coordinator to avoid collisions in any scenario with more than one simultaneous contributor.
- **Single incrementing counter, assigned only at "Final" / merge time (the leading alternative, not chosen here)**: this is the approach used by the Rust RFC process (see Prior art) — files carry a `0000-` placeholder until a natural, already-unique event (the pull request number) is available, and are renamed only then. This avoids the coordination problem without needing timestamps, and also avoids ever assigning a number to unstable Draft content. It was not chosen here because Omid indicated a preference for a number that exists from the moment an RFC is first proposed, including so that very old, already-existing RFCs can be assigned identifiers retroactively based on when they were actually conceived — something a merge-time-only scheme cannot do naturally.
- **Hash of the filename/slug (rejected)**: does not provide content-integrity guarantees (the underlying content can still change after the hash is fixed, since the hash is computed from the name, not the content), produces a long, non-memorable identifier, and does not solve any problem that the timestamp does not already solve more simply.

## Prior art

The Rust RFC process assigns no number when an RFC is first drafted; the file is created with a `0000-` placeholder, and the RFC's number is set only once a pull request exists, using that pull request's own number, at which point the file is renamed. Rust's own internal design discussion around this scheme considered and explicitly rejected using something other than a small, continuous-feeling number, on the grounds that continuous small numbers are more attractive to work with than sparse or arbitrary ones, even though using the PR number leaves gaps.

IETF RFCs are also strictly sequential and assigned by a central RFC Editor, with no domain-based range reservation; the number denotes only publication order, not subject matter.

## Unresolved questions

1. What exact event counts as "creation" for the purpose of generating the timestamp — first mention of the idea, first file draft, or the moment the file is actually committed to the repository? This needs a fixed convention.
2. Should the timestamp be displayed as a raw decimal integer, or encoded more compactly (e.g. base36) for shorter human-facing citation? Not resolved here.
3. Is the 2106 overflow ceiling of unsigned 32-bit unix seconds worth a documented mitigation now, or safe to revisit later (and if later, by when)?
4. Does the rare-collision case ever warrant tooling (a script that checks for and avoids collisions), or is manual resolution sufficient indefinitely given the current single-author scale? Revisit if/when multiple contributors are producing RFCs concurrently.
5. What tie-breaking convention should be used when retroactively assigning timestamps to multiple pre-existing RFCs that share the same recorded `Start Date`?

## Future possibilities

A small helper script (or shell alias) that prints `date -u +%s` and optionally checks the RFCs folder for an existing collision before a new file is created, once the number of contributors or RFCs justifies the tooling investment.
