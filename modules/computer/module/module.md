# Modules
Use to store modules that shape the application.
Also indicate which modules include in any type of applications e.g. GUI, server, CMD, ...

## Model

- `(software)-[:---]->(software_module)`

## Identifier

A module's identifier is its **domain** — the name the application knows it by,
e.g. `product`, `content`. It is the module node's identity in the graph, so
`Field_ModuleID` returns the same `ThingUUID` every other node identifier in this
repository returns. See [module.handoff.md](./module.handoff.md) for the Go
comment this came from and for the field the Go left commented out.

## Runtime surface

`protocol/bs.kh` carries two abstractions, and the difference between them is
the module's whole runtime story:

- `Module` — one module of an application. It names where it came from
  (`Source`), what it needs (`DependOn`), what it contributes to the running
  application (`Pages`, `Services`), and it is a `DataType` with a media type and
  a teardown surface.
- `Computer_Modules` — the registry an application holds them in. Modules are
  registered before the registry is read, so `RegisterModule` and `Modules` are
  not a pair a caller may interleave; `GetModuleByID` and `GetModuleByMediaType`
  are the lookups, and both can fail.
