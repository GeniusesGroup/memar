# Memar Changelog

## Changelog
### A session reaches the Memar skill from AGENTS.md alone; Memar's preferences move to the project's manifest
- Time: 2026-10-19T20:00:00Z
- Type: Changed, removed
- Cited:
  - Owner (2026-10-19, in chat) - Relation: Evidence: AGENTS.md is sent with the prompt, yet it only pointed at `.agents/memar/README.md`, which cost every session a tool call and said nothing more; AGENTS.md says itself what a session loads, and what else is needed is added there, not to a file in between. The preferences file is read by the `memar` command, not by models, so it is not among the files agents are pointed at, and Markdown is the wrong form for it. The projects that use Memar are changed the same way.
  - Task 20261014-T113227Z-24288 - Relation: Evidence: the owner's request of 2026-10-14 that a project's preferences live once in its `manifest.yaml`, Memar's own keys under a key of Memar's.
  - Owner (2026-10-22, in chat) - Relation: Evidence: the note Not every idea belongs in Memar, which stood in the removed preferences file, has lost its meaning and is not kept anywhere.
- Propagates to:
  - `bundles/memar/services/install/services/project.py`: Done — writes only the `## Memar` section of AGENTS.md; the Memar repository's section links its own skill file; an earlier install's `.agents/memar/README.md` goes to the trash, and a `.agents/memar/preferences.md` is named as no longer read and left
  - `bundles/memar/services/install/services/apps.py`: Done — the skill pointer in each agent app names the checkout's `SKILL.md` by its path on the machine, so the skill is one read away
  - `modules/process/project/services/preferences.py`: Done — reads the `memar:` block of the project's `manifest.yaml`; install writes no preferences file and no manifest
  - The `memar` and `organization` repositories: Done — `memar install` rewrote their AGENTS.md and trashed their `.agents/memar/README.md`; Memar's `.agents/memar/preferences.md`, whose keys were all empty, was trashed
  - `modules/knowledge/content/rules/normative_references/normative_references.md`, `modules-plugable/knowledge/documentation/handoff/handoff.handoff.md`, `docs/comparisons/context-mode.001.md`, `docs/framework.handoff.md`: Done — they name the manifest block, or the removed file's last version where an essay cites it
  - Task 20261017-T162520Z-13368: Done — closed without work by the owner's ruling of 2026-10-22
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — claimed, decided
  - [Claude](../../CONTRIBUTORS.md#claude) (Opus 5.5) — carried, recorded

#### What changed
A session in a project that uses Memar read AGENTS.md (sent with the prompt), then `.agents/memar/README.md` (a tool call), then ran `memar content path` (another), then read the skill. AGENTS.md now says what the README said; in the Memar repository it links the skill file. The bootstrap commands are not copied into AGENTS.md: it is paid on every prompt, and only a machine without `memar` needs them.

What a project tells Memar's tools (`sessions`, `records`, `most-characters`, `normative_references`) is a `memar:` block of indented `key: value` lines in the project's `manifest.yaml`, read without a YAML library; the manifest's other keys are not read. Absent, every key is Memar's default.

#### Considered and not done
- A `.agents/memar/preferences.json` or `.toml`: not done, because the owner had already named the project's manifest as the one place for its preferences.
- Writing an empty `memar:` block into a project's manifest on install: not done, because the manifest is the project's and an absent block already means the defaults.

---

### The router is keyed by path, and the checkout is found by a marker, so nested and mirrored modules can move
- Time: 2026-10-26T12:22:00Z
- Type: Changed
- Cited:
  - Task 20261024-T052937Z-22844 - Relation: Evidence: categories nest and a pluggable module stands at the path of the kernel module it realizes, so a leaf name is not unique and a fixed depth is not true.
  - `modules/knowledge/label/labels/category.md` - Relation: Rule: the nesting and the mirror this change makes the tools read correctly.
- Propagates to:
  - `bundles/memar/tests/memar.py`: Done — expects path keys, a nested module and its mirror with one leaf as two domains, and a verb two files declare named and left out
  - `bundles/memar/tests/module_graph.py`: Done — counts `primitive/` code, adds `Nested` and `Mirrored`; six `knowledge/documentation` sub-modules stand at no kernel path and are listed in `UNMIRRORED` until the move tasks place them
  - `modules-plugable/computer/filesystem/services/fs_memar.py`: Done — `checkout_root()` finds the nearest `modules-plugable` folder above the file; about 113 `parents[N]` counts in services and tests are replaced by it or by the same marker in one line where the root must be found before an import
  - `bundles/khayyam/targets/go/corpus_port.py`: Done — a module's rank falls with the leading path segments it shares with the declaration
  - `bundles/memar/services/mcp/services/serve.py`: Done — the folders that hold no worker code are the role folders the module-skeleton profile declares, less `primitive` and `services`, and not a second list
  - Two counts are left: `bundles/memar/services/install/services/apps.py` and its test climb from the skill folder, not from a module
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — claimed
  - [Claude](../../CONTRIBUTORS.md#claude) (Sonnet 5.5) — carried, recorded

#### What changed
`catalog` keys each file that may declare verbs by its folder's path under the checkout (a domain) or that path, `services` and the stem (a capability), and each entry names the domain it goes under: the folder it stands in, or the one domain whose last word, then `_`, begins its stem (`module_ensure_folders` under `module`). Two domains with one last word are two entries; if both declare one verb, the second is named on stderr and left out like a service that fails to import, and a capability that begins with two domains' words is named on stderr and left out. `services_of(word)` gives a domain and its capabilities by the last word, for the tests that ask for one verb.

#### Considered and not done
- Attaching a capability by path alone: not done, because `module_ensure_folders` stands in another module's folder and goes under `module` by its name, which the router's contract says.
- Requiring a leaf to be unique: not done, because a mirror repeats its kernel module's last word by rule.

---

### The entry point declares `open`, the door a service is handed a class of nodes by
- Time: 2026-10-26T16:30:00Z
- Type: Added
- Cited:
  - `modules-plugable/computer/memory/store/record/record.md` - Relation: Reference: "Binding adapters to classes", what `open` does and refuses
- Tasks:
  - main:.agents/tasks/20261026-T150608Z-8256/: Done - step 2 of task `20261023-T074642Z-5420`
- Contributors:
  - An AI agent (Claude, model claude-opus-5-5 as reported by the runtime; no CONTRIBUTORS.md entry) — wrote it; no `approved` is recorded

#### What changed
`memar` binds `open` to `open` of `services/memory/memory.py`, which reads the key `memory`, turns the adapter's name into its module at `modules-plugable/computer/memory/store/<capability>/` and its `bind`, and returns `record` laid over the bound store or a refusal (`NotBound`, `LessThanNeeded`, `SharedStore`, `Malformed`) naming the class and the line to add or mend. Its tests are `services/memory/tests/memory.py`.

#### Considered and not done
- Writing `open` in `memar` itself: the file routes and nothing else, and `RouterNamesNoVerb` refuses verb words (`project`, `add`, `list`) in its strings and names.
