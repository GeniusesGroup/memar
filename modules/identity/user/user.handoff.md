# User — Handoff

Open state for the `identity/user` domain. Converted 2026-10-02.

## `UserUUID` is empty, and that is the question
`tp UserUUID ab` carries no requirements, so any capsule satisfies it
structurally and nothing about a user identifier is stated. The Go said nothing
either — `type UUID thing_p.UUID` is a re-spelling, not a contract. Before
implementers arrive, decide whether a user UUID must require behavior: render for
the text domain (the thing UUID's comment said "usually use to SET/GET and show
locale title by knowledge/text domain"), equality for comparison, or nothing.
Until that is decided, `UserUUID` states nothing that `ThingUUID` does not.

Rule 6 treats the empty abstraction as a design smell, so this is recorded rather
than shipped silently.

## The UUID is one concept under many names
`thing/protocol/dt-uuid.kh` declares `ThingUUID`. This file declares `UserUUID`,
which the Go defined as `type UUID thing_p.UUID` — the same concept re-spelled.
Khayyam has no alias form, so the corpus now holds two declarations of one
concept. `identity/organization` imports `UserUUID`; `identity/time` and
`identity/uri` import `ThingUUID`. That fork needs one ruling: either every domain
imports the thing declaration, or the concept is declared once and the per-domain
files import it. It is not settled here, because the ruling belongs to the thing
domain, which owns the concept.

## A dangling note in the Go
The Go source carried a comment "// Register new user — TODO::: not yet designed;
was a dangling comment in the Go source." on `UserID`. It names an event that was
never designed. It is recorded here rather than in the source, per rule 5, and it
is still undesigned.

## Method naming across the corpus
`UserID` here takes its name from the owner (`User`), following the Go and the
one converted sibling. `identity/time` produced `TimeID` on `Field_TimeID` and
`identity/uri` produced `URIID` on `Field_URIID`, while memar's own converted
protocols spell the same thing `GetURI`, `GetURI` style. The repository should
pick one convention and sweep the ninety-odd `dt-uuid.kh` files; the two
conventions now disagree inside this repository.

## What the conversion did not settle
- Whether a user's identity may ever diverge from its thing identity. `URIModel`
  in `identity/uri` composes `ThingModel`, so a URI record's identity is its thing
  identity; the same question applies here.
- The concrete UUID capsule: it belongs to the implementation layer, not to
  `protocol/`. Its home directory is undecided.