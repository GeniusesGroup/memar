# Agency Rule — A composition version fixes its entries
Status: Draft

## The rule
- **A composition version is the cryptographic hash of the entries of an ordered composition,** taken in order over each entry's locator bytes, layer tag and normative mark. Two compositions that differ in order, membership, layer or mark have different versions. The version is the key a takeup is bound by; it is not a content address and agency mints no second address type for materials.
- **Resolving a version returns the same ordered entries every time,** and returns entries, never bodies and never a path; a call that supplies a path fails. Bodies are obtained from the content owners by a widget that aggregates the resolve ([Widget Aggregates](/modules/computer/ui/rules/widget-aggregates/widget-aggregates.md)).
- **Binding is defined only for a version that resolves.** After a bind of principal P to version V with an optional event E, resolving V is defined, or the bind is refused. Two binds with the same P, V and E are equivalent, and E may differ between binds without changing V. A bind writes no task fact, no content body and no search index.
- **Invalidation is by the normative mark content reports changed.** Every version whose entries include that mark is invalid for new binds, and resolving it refuses with a stated error; the service returns the count of versions it invalidated and lists none.

## Why it exists
Continuity of context across chats rests on a version meaning one sequence of materials. The types and signatures are declared in [the protocol](/modules/management/agency/protocol/composition-version.kh) and its services; this rule holds the behaviour no signature carries.

## How a check would run
The realization's tests in `modules-plugable/management/agency/tests/durable_context.py` decide each sentence against a stated input.
