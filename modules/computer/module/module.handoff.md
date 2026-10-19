# Module Handoff

Open state for [module.md](./module.md). See the repository's
documentation-handoff practice for what a handoff is.

## Topic & Purpose

Converting this domain's three protocol files from the Go they carry to Khayyam,
and recording what the conversion could not settle — a near-collision with
memar's own module concept, a dropped type parameter, and a field the Go left
commented out.

## Status

Active — all three `.kh` files accept under the Khayyam frontend. One finding
(`Module`, below) is an owner's decision and not mine to close.

## Converted

- `protocol/dt-uuid.kh` — `Field_ModuleID` + `ModuleID () (t ThingUUID)`
- `protocol/model.kh` — `ModuleModel`, composing `ThingModel` and `Field_ModuleID`
- `protocol/bs.kh` — `Module` (`Source`, `DependOn`, `Pages`, `Services`,
  composing `DataType`, `Identifier_MediaType`, `Capsule_LifeCycle`),
  `Computer_Modules` (`RegisterModule`, `Modules`, `GetModuleByID`,
  `GetModuleByMediaType`), and the three collections `Array_Module`,
  `Array_Page`, `Array_Service`

## Unblocks

`[rights/contract/edges/terms/protocol/dt-data.kh](../../../rights/contract/edges/terms/protocol/dt-data.kh)`
returns a bare `ThingUUID` for `Field_ContractTermsModule`, where the Go's `Data`
struct had `moduleID module_p.UUID`. Its handoff already says what the fix is —
the field accessor becomes a composition:

```
tp Field_ModuleID in "modules/computer/module/protocol/dt-uuid.kh"
```

Two other files name this domain and are not converted, so nothing else is
blocked on it: `[knowledge/text/edges-loop/query/protocol/data_model.kh](../../../knowledge/text/edges-loop/query/protocol/data_model.kh)`
carries `// bm_p.Field_ModuleID // TODO::: Isn't a filter??`, and
`[computer/request/protocol/storage.kh](../../../computer/request/protocol/storage.kh)`
carries `// bm_p.Field_ModuleID` commented out. The first is an open question of
its own domain, not a missing declaration.

## Blocking finding

**memar's `computer/module` already declares `Module`.**
`memar/modules/computer/module/protocol/module.kh` holds:

```
tp Module ab {
    DataType
    Observer_DataTypes
}
```

Both this domain and that one sit at the module path `computer/module`, and the
qualified-names rule says qualification cannot separate two declarations the
same module path would give the same name — a counter or a step up the path is
"a report, not a name". So if the two are one concept, the answer is one
declaration including the other, and that is a decision about which repository
owns the concept.

**My judgment, recorded so it can be overturned:** they are *not* the same
concept, so I declared `Module` here.

- memar's `Module` is a **manifest entry** — its Go is `struct { name string;
  optional bool }`, it cites the Cargo manifest, and it composes
  `Observer_DataTypes`: a declared module says which data types it provides.
- this domain's `Module` is a **loaded application module** — it has a `Source`
  (domain, URL), a dependency set, pages, services, a media type, and teardown.

The distinction is declaration side vs runtime side. What makes me uneasy, and
what would change my mind: both compose `DataType`, both are reachable from an
application, and this repository's `computer/software` file has
`Modules() []module_p.UUID` commented out inside its `Model` — a place where the
manifest's module list and the runtime's module list are the same sentence. If
the owner decides they are one concept, this file's `Module` goes away and
`Computer_Modules`'s members become the single surface.

## Decisions

1. **`Field_ModuleID` returns `ThingUUID` and no `ModuleUUID` abstraction was declared.** The Go wrote `type UUID record_p.UUID`; the repository's identifier ownership decision makes that one concept owned by [identity/thing](../../identity/thing/protocol/dt-uuid.kh). The Go's own comment — "Applications module identifier e.g. product, content, ... domain" — is extracted into [module.md](./module.md).
2. **`ModuleModel` composes `Field_ModuleID`, which the Go's `Model` did not.** The Go's `Model` was `thing_p.Model` alone. This follows [knowledge/edge/protocol/model.kh](../../knowledge/edge/protocol/model.kh), where `EdgeModel` carries `Field_EdgeID` although the Go did not, and it fits this domain: a module node whose identifier is its domain name should be able to answer what that name is. A reviewer who disagrees loses one line.
3. **The Go's `[STR string_p.String]` type parameter is gone; `Source` returns `String`.** Khayyam has no generic syntax, and an abstraction-owned signature may name abstractions only. `String` is memar's abstraction at `memar/modules/codec/string/protocol/string.kh`. Nothing is lost: the parameter appeared in exactly one position, a return, and covariant return types already let a module return a narrower string than the abstraction.
4. **The registry abstraction is `Computer_Modules`, not `Modules`.** The Go had an interface `Modules[STR]` with a method `Modules()`, legal because Go keeps interface names and method names in different namespaces; Khayyam has one flat namespace per file, so the two met. The receiver-method-names rule settles which side yields — the method keeps the bare name, the declaration is qualified — so the method is `Modules` and the abstraction is `Computer_Modules`. `Array_Module`, `Array_Page` and `Array_Service` follow the same qualification because `Module` is the element they hold.
5. **`GetModuleByMediaType`'s parameter is `mediaType`, not `mt`.** The Go's `mt` is one of Khayyam's seven declaration keywords and the frontend refuses it as an identifier (`keyword-as-identifier`). `mediaType` says the same thing.
6. **`GetModuleByMediaType` takes `Identifier_MediaType`, not `String`.** The Go took a `string` because `mediatype_p.MediaType` was `type MediaType = string`. Khayyam's memar side names that concept `Identifier_MediaType` and declares it as an abstraction, which is what a signature owned by an abstraction may name.
7. **`capsule_p.LifeCycle` became `Capsule_LifeCycle`, not `Datatype_LifeCycle`.** memar has two, and they are different: `computer/capsule/protocol/life_cycle_contract.kh` declares `Capsule_LifeCycle` carrying `Deinit` only, while `computer/datatype/protocol/life-cycle.kh` declares `Datatype_LifeCycle`, the software release lifecycle. The Go's `Module` embedded the capsule one. Worth knowing either way: memar's `DataType` already composes `Observer_Datatype_LifeCycle`, so a module composed as it stands already carries the release lifecycle by way of `DataType` — composing `Datatype_LifeCycle` here would have said it twice.
8. **`bs.kh` keeps both abstractions and all three collections.** The file-layout rule's strong default is one abstraction per protocol file, with an explicit exception for declarations that form one cohesive family. `Module` and `Computer_Modules` are the registered thing and the registry of it, in the Go's one file, and `Array_Module` exists only because `DependOn` returns it. Splitting them would put a registry and its element in two files that each have to open the other.
9. **`Module` does not compose `Field_ModuleID`.** The Go's `Module` interface did not include `Field_ModuleUUID`, and [module.md](./module.md) does not say a loaded module knows its own domain name. `Computer_Modules.GetModuleByID` looks a module up by `Datatype_ID`, so the identifier is the registry's business. Left open below rather than assumed either way.

## Findings

1. **`service_p.Service` moved.** The Go imported `memar/operation/service/protocol`, a path this repository's memar checkout does not have. `Service` is now `memar/modules/process/service/protocol/service.kh`, and it is a real abstraction composing `Capsule_LifeCycle`, `DataType`, `Observer_MediaType`, the request/response observers and `Importance`. Any other domain importing the old path is broken the same way.
2. **`mediatype_p.MediaType` is `Identifier_MediaType`, `datatype_p.ID` is `Datatype_ID`, and `datatype_p.DataType` is `DataType`.** The Go reached all three through `memar`-rooted aliases. Recorded because the qualified names are not derivable from the Go names by pattern.
3. **`// DomainID() UUID` was left commented in the Go and stays unconverted.** A commented-out method is a note that a second identifier was wanted — a module's domain name as distinct from its node identity — and nobody has said whether that is a second field or the same field read another way. It is the first entry in the Open Questions below, not a declaration.

## Open Questions

1. **Is a module's domain name a second identifier?** `Field_ModuleID` returns the node's `ThingUUID`. The Go's commented `DomainID()` asks for the name itself — `product`, `content` — which [module.md](./module.md) now describes as what the identifier *is*. Either the name is the identity and `Field_ModuleID` should read it out, or the two are genuinely different and `DomainID` is a real second accessor. Deciding it decides whether this file has one field or two.
2. **Does a loaded module know its own identifier?** See decision 9. `Computer_Modules.GetModuleByID` finds a module by `Datatype_ID`, but the module it returns is not required to answer with one.
3. **Does a software carry its modules?** `computer/software/protocol/model.kh` has `Modules() []module_p.UUID` commented out inside its `Model`, and [computer/rule](../rule/rule.handoff.md) records the same gap from the rule side. Whether a rule governs software *and* which software carries which modules is one question asked from two directions, and neither domain has answered it.
4. **`Module` or not — the collision above.** Left open deliberately.
5. **`bs.kh` is the only file in this domain with a body-less method set of any size, and none of it has an implementation to point at.** Rule 2 of this repository's map puts the bodies behind a generator driven by an `abstraction.Implements` intent. `Module` has four methods and `Computer_Modules` four; whichever capsule realizes them will need the generator before the protocol layer means anything at runtime.