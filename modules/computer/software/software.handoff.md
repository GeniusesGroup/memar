# Software Handoff

## Topic & Purpose

Conversion state of `modules/computer/software` from Go to Khayyam (2026-10-03), and the open
design questions the Go source left unanswered.

## Status

Active — five files converted; the captcha services, the manifest capsule and the build-tag-gated
human text are deliberately unconverted, and the reasons are recorded below.

## Decisions

- **`Field_SoftwareID` resolves to `ThingUUID`.** The Go `type UUID record_p.UUID` is the same
  record identity that `computer/rule/protocol/dt-uuid.kh`, `computer/module/protocol/dt-uuid.kh`,
  `computer/datatype/protocol/dt-uuid.kh`, `knowledge/text/protocol/dt-uuid.kh`,
  `knowledge/label/protocol/dt-uuid.kh` and `knowledge/edge/protocol/dt-uuid.kh` already resolve to
  `ThingUUID`. A second software UUID would be the architecture error the qualified-names rule
  names. The accessor is `SoftwareID mt (self Field_SoftwareID) () (t ThingUUID)`, following the
  `Field_RuleID` / `Field_ModuleID` / `Field_DataTypeID` shape.
- **`SoftwareModel` composes `ThingModel` only.** The Go `Model` had `thing_p.Model` and nothing
  else; `Modules() []module_p.UUID` was already commented out in the source. This matches
  `UserModel` and `EstateModel`, which also carry only `ThingModel`. `RuleModel` and `ModuleModel`
  additionally compose their own `Field_XID` — that inconsistency is the corpus's, not this
  conversion's, and is worth settling once (see Open Questions).
- **`AcceptedProtocols` stops being a bit flag.** The Go carried three independent flags in one
  `uint8` behind one accessor. `Field_AcceptedProtocols` now composes three observers —
  `Observer_AcceptedEmail`, `Observer_AcceptedSMS`, `Observer_AcceptedPhoneCall` — each answering
  `Boolean`. The domain question ("which contact protocols does this person accept?") is unchanged;
  the carrier is now three domain questions instead of one machine representation. `…_Unset` is
  the `false` of all three and is not a separate declaration.
- **The manifest record is four observers.** `Icon`, `DomainName`, `Email` and `AppID` became
  `Observer_ApplicationManifest_Icon` / `_DomainName` / `_Email` / `_LocalID` composed into
  `ApplicationManifestDataModel`, per the observer-mutator rule (`Observer_X` with a
  `Get<Concept>` accessor). The Go accessor `AppID()` returned `uint16`; it is `GetLocalID` here
  because the Go comment already said what the number is — "local OS application ID" — and a local
  id is not the application manifest's own identity.
- **`Icon` is a named byte run.** `[]byte` becomes `ApplicationManifest_Icon ab { Array_Dynamic }`,
  the shape `knowledge/text` and this repository's other byte-carrying fields already take; the
  memar `Array_Dynamic` documentation says exactly this about a Go `[]T` field.
- **`Status()` in the language-human data model was not converted.** The Go method returns nothing
  and names no type, so there is no behavior to carry. Rule 6 says an empty requirement is a
  design smell and its missing behavior belongs in the handoff, not in an invented abstraction.

## Open Questions

- **What does `Status()` return on the software↔language-human edge?** The Go declared
  `Status()` with an empty result. The captcha services use `protocol.Software_PreAlpha`, so a
  software status exists in the older library; nothing in this tree declares it. A
  `Software_Status` abstraction, and a `Field_SoftwareStatus` observer on
  `SoftwareLanguageDataModel`, is the shape to add once the status vocabulary is decided.
- **What do `ContentPreferences()` and `PresentationPreferences()` answer?** Both declared on the
  manifest data model with no result. They are the manifest's behaviour contract, not its identity,
  and it is not stated whether they are observers over stored preferences or commands that change
  them.
- **Three edge folders have no domain document at all.** `edges/accepted_protocols/`,
  `edges/language-human/` and `edges/manifest/` each hold a `protocol/` file (and, for manifest, a
  `services/` capsule and a test) with no `README.md` and no `<name>.md`. The Phase 0 rule is one
  folder per edge: a document plus a one-line README, with sections Model, Policies, Placement,
  Open questions. `edges/language-human-ability/` next to `edges/language-human/` also suggests the
  two are one relation seen twice; the Phase 0 review's "wrong kind-folder" pass has not been
  applied yet.
- **Should `SoftwareModel` carry `Field_SoftwareID`?** `RuleModel` and `ModuleModel` do;
  `UserModel`, `EstateModel` and now `SoftwareModel` do not.
- **The captcha domain has no home.** `internal/captcha/` implements a captcha service pool
  (`PhraseCaptchas`, `PhraseCaptcha`, image and audio rendering, expiry, solve/check), and
  `services/` wires three services — get-new-phrase, get-phrase-audio, solve-phrase — but the
  domain is filed under `computer/software` as an `internal/` package. It is an authentication
  concern, and `edges-loop/authentication-deny_password/` and
  `edges-loop/authentication-force_use_2factor/` are the software domain's other authentication
  material. Whether captcha deserves its own domain, or belongs to `rights/access` or wherever
  authentication lives, is a placement question this domain cannot settle.
- **The captcha Go has three unimplemented things marked `TODO:::`** that a re-modelling would have
  to answer: `randomMath()` returns an empty string, `createAudio()` returns an empty byte slice
  (so `GetPhraseCaptchaAudio` always returns silence), and `lenAsString()` returns an empty string
  (so the dev-mode expiry log always prints nothing). `Difficulty` is read by nothing — there is a
  `// TODO::: Difficulty??!!` at the image renderer.
- **The manifest's society and permission fields exist only in the capsule.** `Manifest` in
  `edges/manifest/services/manifest.kh` also carries `Society`, `SocietyUUID`, `SocietyID`,
  `appUUID`, `AppDetail`, and `RequestedPermission`, none of which the protocol data model
  declared. `identity/society` is another unconverted neighbour, so this could not be settled here.

## Left unconverted

| File | Why |
| --- | --- |
| `internal/captcha/errors.kh`, `internal/captcha/locale.eng.kh`, `internal/captcha/locale.per.kh` | Human-facing text written by `SetDetail` inside `init()`. There is no method on a type that writes human-readable text yet, so there is nothing to convert to; the same reason `knowledge/text` was left in this shape. `locale.*.kh` are additionally build-tag gated (`//go:build lang_eng`, `lang_per`). |
| `services/errors.kh` | The same four errors and the same localized detail text, in one ungated file — a second copy of `internal/captcha/errors.kh` plus both locale files merged. Also human-facing text. |
| `internal/captcha/init.kh` | `ImageFormat` (PNG, JPEG) and `AudioFormat` (declared with an empty constant list). A value type in an implementation package; Phase 3. |
| `internal/captcha/status.kh` | `Status_Created`, `Status_LastAnswerNotValid`, `Status_Solved` — label vocabulary over a `uint8`. |
| `internal/captcha/phrase.kh`, `internal/captcha/phrase_test.kh` | The captcha pool: structs, methods with bodies, goroutine expiry loop, image rendering. Implementation logic; Phase 3. |
| `edges/manifest/services/manifest.kh` | The `Manifest` capsule: struct fields, `//memar:impl` methods, a sha3 derivation of the app UUID. Implementation layer. |
| `edges/manifest/services/manifest_test.kh` | A test that asserts `&Manifest{}` satisfies the data model. Tests are re-derived from behavior, not translated. |
| `services/init.kh`, `services/service-init.kh` | Entry points and service registration. Phase 4. |
| `services/service-get-new-phrase.kh`, `services/service-get-phrase-audio.kh`, `services/service-solve-phrase.kh` | sRPC/HTTP handlers, syllab and JSON encoders, and the service metadata records. Implementation layer; Phase 3. |

## Related Artifacts

- [`README.md`](README.md)
- [`software.md`](software.md)
- `org/modules/identity/thing/protocol/dt-uuid.kh`, `model.kh`
- `org/modules/knowledge/language-human/protocol/dt-uuid.kh`
- `memar/modules/math/boolean/protocol/boolean.kh`, `memar/modules/math/integer/unsigned-16.kh`
