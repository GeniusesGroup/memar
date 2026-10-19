# App kinds and run targets

## Model

- Candidate (unconfirmed): two label spaces on the app node (package `label` comment vocab — names are labels; UUIDs are identity): kinds `Firmware`, `Hypervisor`, `Application`, `Game` and run targets `Local`, `Storage`, `Server`, `GUI`, `Edge`.

## Policies (rules)

- Kinds and run targets were recorded in one label file; the source does not separate identity vocab from deployment vocab.

## Placement

- **Core `software` keeps the kind vocabulary; the run-target half is undecided (create now, decide later).** App kinds are app identity — identity of a kernel concept is core-by-necessity — and a label list is a parameter (parameters vs semantics ⇒ one module + configuration), so no module is warranted.
- If run targets are a deployment projection rather than app identity (standing review question), that projection is a pluggable capability attaching to software. Nothing here proposes a bare edge.

## Open questions

- Are run targets a deployment projection rather than an app identity?
- Closed set or organizational-open vocabulary for each space?
- Kind name: recorded as `Application` in the domain backlog but `OrganizationApplication` in the recovered source — which is current?

