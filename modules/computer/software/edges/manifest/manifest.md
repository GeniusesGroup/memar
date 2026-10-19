# Manifest (software)

## Model

- `ApplicationManifestDataModel`: `GetIcon() ApplicationManifest_Icon` (an `Array_Dynamic`), `GetDomainName() String`, `GetEmail() String`, `GetLocalID() U16` — the local OS application id.
- The Go service residue binds the fuller record: a society (`Society`, `SocietyUUID`, `SocietyID`), the app (`appUUID` derived as SHA-256 of the domain name, `appID`), email, icon, per-language `AppDetail` (organization, name, description, terms of service, license, tags), and `RequestedPermission` — service ids such as internet-in-background and notifications.
- The Go's `ContentPreferences()` and `PresentationPreferences()` were declared with empty results; they are the open question in `software.handoff.md`.

## Policies (rules)

- The Go `init()` derives the app UUID deterministically from the domain name. No policy governs who may publish a manifest, or what granting a requested permission means.

## Placement

- The record hangs off the app/software side and reaches a society by UUID; as an ordinary two-node relation that is an `edges/` relation of the software domain. Not moved and not relabelled: the edge label is stated nowhere, and the app node itself lives in `edges/app`.

## Open questions

- Which node the manifest hangs on — the app node of `edges/app`, the software node, or the society — and with what edge label: the Go struct holds society and app together with the payload and names no relation.
- The same domain-name hash is SHA-256 here and SHA-512/256 in `instance_of/edges/node-metric`'s manifest; one idea, two hashes.
- The `services/` capsule is Go residue only (unconverted), and its test rides along.

## Source

> Source: `modules/computer/software/edges/manifest/protocol/data_model.kh`, `modules/computer/software/edges/manifest/services/manifest.kh` (in code).
