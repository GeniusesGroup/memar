# App relation - app (SubCompile)

## Model

- Candidate (unconfirmed): `(app)-[:sub_compile]->(app)` — label `SubCompile` for "a compact version such as GUI, Edge, ..." of another app; direction unconfirmed.

## Policies (rules)

- SubCompile marks an app as the compact/derived build of another app (GUI, Edge variants named in source).

## Placement

- **Core `software` keeps a structural app-to-app edge for now — verdict deferred.** Edge vs module: no independent processing is recorded yet, so this is not a module; if SubCompile turns out to carry build or deployment processing, the complete capability (edge + processing together) becomes a pluggable attaching to software. Entry point is the app either way.

## Open questions

- Is SubCompile a build-artifact relation or a deployment relation?
- Which end is the compact version (direction and naming unconfirmed — nothing ratified)?

