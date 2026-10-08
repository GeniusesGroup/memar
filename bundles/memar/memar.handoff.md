# Memar Handoff
Open work for [memar.md](./memar.md). Entries are mutable current state — revised as each item moves, removed when it resolves or is dropped. See [documentation-handoff.md](../../docs/documentation-handoff.md) for what a handoff is.

## Status
Active. Created on 2026-10-07, when `modules/modules/` — a folder `memar-go` had for its own command-line tool — was distributed into the modules that own its files. What had no owning module came here: the program's entry and command registration, `app/`, and `locale/`. The same day the folder moved out of `modules/` into `bundles/` (see Direction). Every file is still the port's archived Go; nothing here is a realization yet.

## Direction (owner, 2026-10-07)
- **A server, not a command line.** The command-line tool is set aside as the way to reach Memar's operations; the direction is a server. `main.kh` already carried the question as `TODO::: act as a server??`, and this is its answer. The command files the port carried — `init-cmd.kh` and `cmd.kh` here, and `module-cmd.kh` in [`computer/module/`](../../modules/computer/module/) and [`gui/`](../../modules/gui/) — are registration for that command line, and are to be replaced by the server's surface rather than ported as they are.
- **The files here become independent modules on a plan, not by porting.** What the files say may look useful, but each is to be reshaped into a good independent module in an order this handoff records as it is decided; until then a file here is a record of what `memar-go` did, not a commitment to do it the same way.
- **A bundle, not a module.** The server runs operations that modules own and owns none itself, so it sits under [`bundles/`](../README.md), the layer for what runs or aggregates modules, and `modules/` keeps only reusable modules. This answers where it goes in the layout: it has no counterpart under [`docs/modules/`](../../docs/modules/README.md#one-layout-for-both-trees), and a part of it that a second bundle or project comes to need leaves for `modules/`.
- **`.agents/scripts/` rewritten in Khayyam, and soon.** The scripts are to move into modules as Khayyam realizations. Where each one lands follows its responsibility; this module receives only what only the server does.

## Open Questions
- **Whether the Khayyam toolchain's operations are served here.** The owner's leaning is one Memar server that also performs Khayyam's operations, so that there is no server specific to Khayyam. [`khayyam.handoff.md`](../khayyam/khayyam.handoff.md) already asks to "extend the Memar server" with a capability that generates a service from its name and path, and says no document defines that server; whether the language server under [`khayyam/lsp/`](../khayyam/lsp/) is one of this server's faces or stays its own program is undecided.
- **Where `app/` belongs.** Building, initializing, updating and deploying an application is a lifecycle, and [immutable infrastructure](../../docs/modules/runtime/immutable_infrastructure.md) specifies deployment; `app/` is parked here because the category that would own it is itself under review (see [Modularity Handoff → The category layout](../../docs/modularity.handoff.md#the-category-layout-of-this-repository)).
- **Whether localization is a module.** `locale/services/details/` is a command printing a locale's details, and every module carries `locale.*.kh` files of its own. Whether a locale is a responsibility with its own module, or only a per-module concern, is not stated anywhere.
## Related Artifacts
| Artifact | Relation | Action |
| --- | --- | --- |
| [memar.md](./memar.md) | Base — what this module is | Keep in sync |
| [khayyam.handoff.md](../khayyam/khayyam.handoff.md) | Reference — the Memar server named as the home of service generation | Keep in sync |
| [Bundles](../README.md) | Reference — the layer this folder belongs to, and its membership test | Keep in sync |
| [Modularity Handoff](../../docs/modularity.handoff.md) | Reference — the review of the category layout `app/`'s place depends on | Keep in sync |
