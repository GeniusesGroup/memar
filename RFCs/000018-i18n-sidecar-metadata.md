---
RFC Number: 000018
Title: "Native Localization (I18n) via Sidecar Metadata (-detail.kh)"
Status: Proposed
Start Date: 2026-06-30
Applied to: []
Supersedes: null
Superseded by: null
Related:
  Depends_on: ["000001"]
  Extends: []
  Conflicts with: []
Author(s): []
---

## Summary
Human-centric metadata — internationalization strings, localization labels, UI presentation text — is attached directly to types (`tp`) and capsules (`cp`) via sidecar files (`-detail.{lang}.kh`), rather than being scattered across disconnected translation files (`en.json`, `fa.json`) decoupled from the type system.

## Motivation
In traditional architectures, a simple type like `username` suffers extreme fragmentation: its behavior is defined in the backend, its validation duplicated in the frontend, and its human-readable labels scattered across unrelated translation files. This violates the Single Source of Truth principle, generates heavy boilerplate, and creates a high risk of desynchronization between system types and the user interface.

## Guide-level explanation
A type like `username` carries its own visual identity stack-wide. Multi-lingual documentation, user-friendly labels, and localized error definitions are embedded directly into the sidecar `-detail.kh` file associated with that type, keeping the main `.kh` file purely functional and free of heavy language strings. GUI frameworks and API gateways can then dynamically query this metadata directly from the Khayyam source/binary's Abstract Syntax Tree, rather than maintaining a separate, parallel mapping.

## Reference-level explanation
- **Native Human Multi-Language Support:** sidecar files hold localized labels/documentation/error text per type, separate from functional logic.
- **Single Source of Truth for GUIs:** because this metadata lives in the AST itself, visual layout engines and API gateways can query the compiled source directly for localized presentation data.
- **Zero-Redundancy Presentation Alignment:** there is no need to redefine or remap names inside a separate GUI framework layer; the end-user consistently observes localized text driven directly by the type system.

## Drawbacks
Coupling presentation/localization metadata this tightly to the type system means any change to that metadata (e.g. a wording tweak by a non-technical translator) touches files that live directly alongside source code, which may require additional tooling/workflow design so that non-developer translators can safely edit sidecar files without needing full development environment access.

## Rationale and alternatives
The conventional approach (separate `en.json`/`fa.json`-style translation files entirely decoupled from the type system) was rejected as the direct cause of the fragmentation and desynchronization problem this RFC addresses.

## Prior art
This pattern echoes annotation-based localization in some frameworks (e.g. Java's resource bundles tied to class-level annotations) but goes further by making the sidecar file a first-class, AST-visible part of the type definition itself rather than an external resource keyed by string lookup.

## Unresolved questions
None at this time.

## Future possibilities
None recorded yet.
