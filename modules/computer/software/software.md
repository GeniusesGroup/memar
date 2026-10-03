# Software
Software in computer science is written programs or procedures or rules and associated
documentation pertaining to the operation of a computer system, stored in read/write memory.

## Identity

`Field_SoftwareID` is the software domain's own identity and resolves to `ThingUUID`, the base
identifier every converted domain in this repository shares. `SoftwareModel` is a thing; the Go
source's commented `Modules() []module_p.UUID` says a software may also report the modules it
carries, and that has not been decided.

## Accepted protocols

Which contact protocols a person accepts — email, SMS, phone call. The Go source packed the three
into one `uint8` of bit flags (`AcceptedProtocols_Email`, `…_SMS`, `…_PhoneCall`, with
`…_Unset` for none) behind a single `AcceptedProtocols()` accessor. Khayyam has no primitive and
the bit-flag carrier is a machine representation rather than a domain concept, so the record now
answers the three questions separately, as three observers composed into `Field_AcceptedProtocols`.

## Manifest

`ApplicationManifestDataModel` is what an application publishes about itself: an icon, a domain
name, an email address, and the local operating-system application id. The Go source also declared
`ContentPreferences()` and `PresentationPreferences()`, both returning nothing at all; what they
would answer is recorded in the handoff rather than invented here.

## Human-facing text is not converted

`internal/captcha/` and `services/errors.kh` carry the captcha domain's four errors
(not found, expired, answer not valid, not solved) and, in `locale.eng.kh` / `locale.per.kh`, their
English and Persian names, summaries, overviews, user notes and developer notes. In Go that text is
written by build-tag-gated `init()` functions that call `SetDetail`. There is no method on a type
that writes it yet — the same reason `knowledge/text` was left in the same shape — so these files
keep their Go block and carry no Khayyam.
