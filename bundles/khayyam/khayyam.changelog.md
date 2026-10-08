# Khayyam Changelog
This file records what changed in [khayyam.md](./khayyam.md) and what each change reached. See [Documentation — Changelog](../../docs/documentation-changelog.md) for what this file's structure means.

## Changelog

### The module's main document takes the module's name, the README becomes a link to it, and the operational plan becomes its handoff
- Time: 2026-10-06T00:00:00Z
- Type: refactor
- Cited:
  - [Documentation — File Naming](../../docs/documentation.md#file-naming) - Depends_on: a folder's main document takes the folder's own name beside it, and every companion record takes the same base name
  - [Documentation Practice — Folder READMEs](../../docs/documentation.practice.md#folder-readmes) - Depends_on: a folder that has a main document takes its `README.md` as a symbolic link to it, recorded as git mode `120000`
  - [Documentation — Handoff](../../docs/documentation-handoff.md) - Depends_on: what a `<base>.handoff.md` carries — current state, decisions, open questions — against which a plan still being executed is state rather than definition
  - [Modules — The kinds of folder here](../../modules/README.md) - Depends_on: `khayyam/` is a folder by language carrying the module's own state beside its implementation folders
- Propagates to:
  - [khayyam.handoff.md](./khayyam.handoff.md): Done - the old open state is kept verbatim in substance, and the plan's current state (goals, pipeline, scope decision, readiness gate, milestones table, how work proceeds, compile cache, disciplines, non-goals) moved in beside it under *The plan as it stands*
  - [khayyam.research.001.md](./khayyam.research.001.md): Done - the readiness review record took the new base name, and its links into the plan and the handoff were re-pointed
  - [README.md](./README.md): Done - replaced by a symbolic link to `khayyam.md`, recorded at mode `120000`
  - Code and data references: Done - `display/display.json`, `targets/js/src/layout.ts`, and `services/rename/rename.ts` each name the renamed documents and now name the new paths; the 410-test suite and `tsc --noEmit` are green
  - Live document references: Done - `modules/khayyam/display/`, `modules/khayyam/lsp/`, `modules/khayyam/rules/`, `modules/khayyam/targets/js/`, `modules/go-port/go-port.handoff.md`, `modules/process/control-flow/{control-flow.md,answers.md,answers.handoff.md}`, `docs/rule.handoff.md`, `docs/protocols/modules/sdk.handoff.md`, `docs/protocols/computer/compiler.md`, `docs/protocols/process/control-flow.handoff.md`, and `docs/documentation-research.handoff.md` now point at the renamed documents
  - Historical records: Reference — the references in `docs/khayyam/khayyam.changelog.md`, `docs/khayyam/modularity.changelog.md`, `docs/khayyam/khayyam.research.001.md`, `docs/type.changelog.md`, `docs/rule.changelog.md`, `docs/documentation-changelog.changelog.md`, `docs/protocols/computer/compiler.changelog.md`, `docs/protocols/process/control-flow.changelog.md`, `modules/go-port/go-port.changelog.md`, and `modules/khayyam/targets/js/target.changelog.md` name the paths those entries recorded at the time, and are left as history
- Contributors:
  - [Space Bunny Alpha](../../CONTRIBUTORS.md#space-bunny-alpha) (space-bunny via [OpenCode](../../CONTRIBUTORS.md#opencode)) - restructured

#### What changed
- `modules/khayyam/execution.md` was renamed to `modules/khayyam/khayyam.md` and now carries the module's own claims: the membership criterion and the local-placement table taken from the folder's former `README.md`, with a short statement of scope, milestones, and current state. It is the module's document, not the plan.
- `modules/khayyam/execution.handoff.md` was renamed to `modules/khayyam/khayyam.handoff.md` and is now the module's handoff. It keeps the old open state — the decisions, ambiguities resolved, open questions, assumptions, proposed next steps, anticipated work, related artifacts, and notes — and gains, under *The plan as it stands*, the part of the old plan that is current state rather than definition: the goals and their checks, the pipeline, the language server's own abstractions, the scope decision, the readiness gate, the M0–M5 table, how work in this toolchain proceeds, the compile cache, the binding disciplines, the non-goals, and the implications.
- `modules/khayyam/execution.research.001.md` was renamed to `modules/khayyam/khayyam.research.001.md`, so the readiness review record pairs with the new base name.
- `modules/khayyam/README.md` is replaced by a symbolic link to `khayyam.md`, recorded at git mode `120000` with the target path as its content.
- The references throughout the repository were swept: 49 files named one of the three old paths. Every reference in a live document — the toolchain's own folders, the rules catalog, the language server, the JS target, the go-port handoff, the control-flow module, and the `docs/` documents that point at the toolchain's state — now names the renamed file, and every link into a plan section points at the section's new home in the handoff. The references inside historical changelog entries and inside the completed Khayyam research record were left naming the paths those records wrote down, which is what a historical record is for.

#### Considered and not done
- **Rewriting the historical entries' paths in the ten changelogs and the one completed research record.** A changelog records what was true when written; an entry that says `modules/khayyam/execution.handoff.md` was true of the session that wrote it, and editing it would make the audit trail claim a path that was never there. The rename is recorded here instead, once, where the artifact it names is.
- **Keeping a short pointer document at `execution.md`.** A file whose only content is "this moved" is a second copy of the changelog entry that says it moved, and it would be read as though the module still had a document by that name. The rename is recorded in this changelog and by git itself.
- **Moving the whole plan into the handoff verbatim, including its front matter, Abstract, Introduction, and Methodology.** Those sections describe how the plan was written and why, which is history rather than state; the changelog entry above carries the change, and the sections that state what is still to be executed moved in without them.

Nothing further was changed in this chain: no `.kh` source, no TypeScript, no protocol document, and no test was touched beyond the reference strings the sweep required.

---

### The toolchain moves to `bundles/khayyam/`, and nothing here reads the root scratch file any more
- Time: 2026-10-07T15:46:42Z
- Type: Changed
- Cited:
  - [Bundles](../README.md) — `Depends_on`: a toolchain runs and aggregates modules, so it is a bundle and not a reusable module
- Propagates to:
  - [khayyam.handoff.md](./khayyam.handoff.md), [lsp/lsp.handoff.md](./lsp/lsp.handoff.md), [display/display.handoff.md](./display/display.handoff.md): Done — their links to `main.kh` are dropped, the measurements made on it are kept, and each says once that it was the owner's local scratch file
  - [lsp/test/sync.test.ts](./lsp/test/sync.test.ts): Done — the test that read the scratch file carries its text instead and finds its two lines by content; what it asserts is unchanged
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — decided
  - [Cursor](../../CONTRIBUTORS.md#cursor) — applied

#### What changed
- The folder moved from `modules/khayyam/` to `bundles/khayyam/` under the owner's decision of 2026-10-07 that what runs or aggregates modules lives under `bundles/`. [khayyam.md](./khayyam.md) now names this folder a bundle, and the paths in its placement table, in the rules, the targets, the language server, the tests, and the default excludes of `services/rename/` and `targets/go/tidy.py` name `bundles/khayyam/`.
- The repository-root `main.kh` was the owner's scratch file for trying the extension and is not part of the repository. The links to it are removed, and `lsp/test/sync.test.ts`, which read it from disk, now carries that text in the test, as the suite's harness already requires of every fixture. The eleven links in `lsp.handoff.md` that resolved to a `core/` that was never beside `lsp/` now point at this folder's `core/`.
