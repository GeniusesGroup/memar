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

## Ambiguities Resolved

- **The captcha domain has no home — its own domain, or wherever authentication lives?** — answered (2026-10-08): it stays under `computer/software`. By `modules.md` → Placement a capability is filed under the domain through which it is instantiated, and captcha's entry point is software's own `services/` (get-new-phrase, get-phrase-audio, solve-phrase); the domain's other authentication material (`edges-loop/authentication-deny_password/`, `edges-loop/authentication-force_use_2factor/`) is already here, and captcha has no edge of its own to another domain — no explicit relationship, so the pluggable test never fires. There is also no `rights/access` anywhere in this tree to receive it. Its `internal/` placement is the right one: implementation of software's authentication, complete and removable with it.

- **Three edge folders have no domain document at all** — answered (2026-10-08): the documents exist now — [`accepted_protocols/accepted_protocols.md`](edges/accepted_protocols/accepted_protocols.md), [`language-human/language-human.md`](edges/language-human/language-human.md) and [`manifest/manifest.md`](edges/manifest/manifest.md), each with a one-line README, written from the protocol sources in the Edge folder shape (Model, Policies, Placement, Open questions). What the sources could not state went into those Open questions: accepted_protocols composes no identity and its Go called it the *user domain's* while the folder says software; manifest's far end and edge label are stated nowhere and its domain-name hash disagrees with `instance_of/edges/node-metric`'s; language-human sits next to `edges/language-human-ability/` and the two are not yet told apart.

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
- **The Phase 0 "wrong kind-folder" pass has not been applied.** `edges/language-human-ability/` next to `edges/language-human/` still suggests the two are one relation seen twice; the question is recorded in [`edges/language-human/language-human.md`](edges/language-human/language-human.md)'s Open questions, and the new documents do not settle it.
- **Should `SoftwareModel` carry `Field_SoftwareID`?** `RuleModel` and `ModuleModel` do;
  `UserModel`, `EstateModel` and now `SoftwareModel` do not.
- **The captcha Go has three unimplemented things marked `TODO:::`** that a re-modelling would have
  to answer: `randomMath()` returns an empty string, `createAudio()` returns an empty byte slice
  (so `GetPhraseCaptchaAudio` always returns silence), and `lenAsString()` returns an empty string
  (so the dev-mode expiry log always prints nothing). `Difficulty` is read by nothing — there is a
  `// TODO::: Difficulty??!!` at the image renderer.
- **The manifest's society and permission fields exist only in the capsule.** `Manifest` in
  `edges/manifest/services/manifest.kh` also carries `Society`, `SocietyUUID`, `SocietyID`,
  `appUUID`, `AppDetail`, and `RequestedPermission`, none of which the protocol data model
  declared. `identity/society` is another unconverted neighbour, so this could not be settled here.

### From Request Research 001 (2026-10-19): the software end of the request chain
Pointer only; the reasoning is in [Request Research 001](../request/request.research.001.md#1-what-the-domain-is-for) and nothing in this domain changed.
- A request reaches the software through the connection, not through an edge of its own: "is it the official GUI app, an SDK or an API call" is answered from the app kind and run target of the client instance's software ([`edges/app`](edges/app/app.md), where kinds and run targets are still a candidate), so the request carries no software field. Whether the run-target half of `app` is a deployment projection (its open question) is what that answer depends on.
- The two `authentication-*` loops are software-level rules about how a requester may be authenticated; the proposal is that they fire at the request's before-point through the generic `condition_is`, which fits their present Policies without change.
- A software agent is a requester like a user (the node-details service authorizes `user_p.Type_App`); the node manifest's `AppID` (a hash of the domain name, in [instance_of node-metric](../instance_of/edges/node-metric/node-metric.md)) is what ties an instance's calls to its software; this domain's [`manifest`](edges/manifest/manifest.md) carries only the local OS application id. Asked in the request handoff as question 5 (the requester) and, for acting-for, X3 of the synthesis.

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
- `modules/identity/thing/protocol/dt-uuid.kh`, `model.kh`
- `modules/knowledge/language-human/protocol/dt-uuid.kh`
- `memar/modules/math/boolean/protocol/boolean.kh`, `memar/modules/math/integer/unsigned-16.kh`
