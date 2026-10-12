# Bundles (`bundles/`)

## What this layer is
A **bundle** is a named composition that runs or aggregates modules toward a requirement no single module states: a server a person or an agent reaches, an executable, a toolchain that reads, checks, and emits a language. Its parts are modules; what the bundle adds is the composition — which modules it brings together, how they are started and reached, and what it ships. The layer exists so that [`modules/`](../modules/README.md) holds only reusable modules, each a bounded responsibility that another bundle, or another project, could take without this one (owner decision, 2026-10-07).

## The test
A folder belongs here when both answers are yes:
- **Does it run or aggregate modules, rather than state a responsibility of its own?** The Khayyam toolchain under [`khayyam/`](./khayyam/khayyam.md) is the language's compiler frontend, language server, and emit targets put together; the Memar server under [`memar/`](./memar/memar.md) is the program through which Memar's operations, each owned by a module, are reached.
- **Would removing it leave every module whole?** Dependence runs from a bundle into `modules/` and never back: no module includes anything under `bundles/`. A folder another module has to reach into is a module, whatever runs it today.

## What a bundle may own
A bundle always names a composition, and it may also hold parts that serve only that composition — a toolchain's own rules and services, a server's command registration. Such a part stays inside its bundle and is laid out with the role folders a module uses (`rules/`, `services/`, `tests/`, per [Modules → The kinds of folder here](../modules/README.md#the-kinds-of-folder-here)). Once a second bundle or project needs it, it is a reusable module and moves to `modules/`. A bundle's own documents — its domain document, handoff, changelog — sit at its root, as a module's do.

This folder's membership is not a taxonomy. A bundle is opened when a composition has no honest home among the modules, and it can be merged, renamed, or retired later; that is cheaper than keeping a runner inside the layer of reusable parts.

## What does not belong here
- **A reusable module** — it lives in [`modules/`](../modules/README.md), under the category layout [docs/modules → One layout for both trees](../docs/modules/README.md#one-layout-for-both-trees) decides.
- **A record that runs nothing** — a record sits with the subject it records, not here as a bundle of its own: the Go port's residue, once the folder `modules/go-port/`, is the Go target's [research record](./khayyam/targets/go/target.research.001.md), inside the bundle whose target it records.
- **Specifications and general claims** — those live in [`docs/`](../docs/README.md); a bundle realizes a composition, it does not restate the contracts of the modules it composes.
- **Generated output** — compiled artifacts and caches live in git-ignored `build/` folders inside the bundle that produces them.
