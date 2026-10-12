# Lib (`/docs/modules/lib/`)
This directory holds **Memar's positions on what Memar does not own**: for each surface whose authority lies outside this project, what Memar keeps of it, what it refuses, and on what conditions a system Memar governs relies on it. A document here answers "what is Memar's position on depending on X?", not "what is X?" and not "what is Memar's module for X?" ([Modules](../README.md)). It stands opposite `modules/lib/` (`modules/lib/lib.md`), which holds the realizations of the same foreign surfaces, and follows that module's placement rule from the specification side.

## Membership criterion
A document belongs here when its subject is a surface whose meaning **Memar cannot change without the agreement of someone outside this project** — the authority test of Lib → The rule (`modules/lib/lib.md#the-rule`), applied to positions rather than to declarations. Two kinds pass it:
- **A protocol surface owned outside Memar** that Memar's stack conforms to and may itself realize — [http.md](./net/http.md) is the application-protocol case, [filesystem.md](./memory/filesystem.md) the storage case.
- **A design name that circulates with senses Memar does not inherit** — [ddd.md](./process/ddd.md) is the case. Such a name is not a protocol surface and has no realization under `modules/lib/`; it is here because the authority over what the name means is outside Memar, which is the test, and not because of the form its subject takes.

A protocol another organization offers for the same process is that organization's, decided against its own requirements ([Protocol → Who Defines a Protocol](../../protocol.md#who-defines-a-protocol)); a document here states Memar's position on relying on it and never restates its requirements as Memar's own. Where Memar's position grows into rules of its own — a divergence from the outside world's rule, argued here — those rules are Memar's, and conformance to them is decided as for any module ([Protocol → Conformance](../../protocol.md#conformance)).

What does **not** belong here:
- **Memar's own modules** — a subject that is Memar's is specified in the category that owns it under [`docs/modules/`](../README.md), with no second shelf here.
- **Realizations** — declarations in the foreign surface's shape live under `modules/lib/`; this folder states positions and does not hold them.

## Layout
The layout is the one `modules/lib/` uses: the second level is the Memar category the surface attaches to, and the document is named for the surface as the outside world spells it. Whether `lib/` should instead sit one level flatter, with only the foreign names under it, is open in `modules/lib/lib.handoff.md` and is decided there for both trees.
