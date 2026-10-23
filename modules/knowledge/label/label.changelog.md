# Label Changelog

## Changelog

### Research on what the label domain is for, its kernel, and the owner's questions
- Time: 2026-10-18T21:00:00Z
- Type: added
- Cited:
  - [Modules → Placement](../../modules.md#placement) - Reference: the kernel and pluggable tests the research applies
  - [Classification Emerges From Rules and Relations](../../../docs/modeling.md#classification-emerges-from-rules-and-relations-not-from-intrinsic-labels) - Reference: label, status and edge read as classification by loop-edge
- Contributors:
  - [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) — requested the work (2026-10-18, away)
  - An AI agent (Claude, model claude-sonnet-5-5 as reported by the runtime; no CONTRIBUTORS.md entry) — researched and drafted

#### What changed
- [label.research.001.md](label.research.001.md) is added (label, status and edge as one cluster): ten scenarios, a three-element kernel, six rival-model choices, a mapping of every folder, thirty-two test scenarios, a reconciliation with the sibling researches, eighteen contradictions reported not resolved, and twenty-six owner questions with defaults; [label.handoff.md](label.handoff.md) gains the questions and Next Steps. This is the domain's first changelog entry. Nothing in [label.md](label.md), in any edge document, or in any `.kh` file was changed; nothing was moved or deleted.

---

### Carry organization's label.md text into the merged label.md after the repository merge
- Time: 2026-10-19T10:50:00Z
- Type: changed
- Cited:
  - [Documentation → Recording Is Not Gated; Removal Is](../documentation/documentation.md#recording-is-not-gated-removal-is) - Reference: what is dropped is named here with its reason
  - [Modules → Placement](../../modules.md#placement) - Reference: the kernel and pluggable tests behind the contradiction left open below
- Contributors:
  - [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) — requested the work (2026-10-19)
  - An AI agent (Claude, model claude-sonnet-5-5 as reported by the runtime; no CONTRIBUTORS.md entry) — carried the text by hand (task 20261019-T103358Z-22340)

#### What changed
- The merge of the organization repository (2026-10-19, merge ceba0177) kept memar's [label.md](label.md) and left organization's version at commit 19834121 only. Organization's sections are now carried into the one text, not pasted beside it: **Dictionary** (the noun and verb senses this module uses), **Taxonomy** (the definition and the three registries, with the pointer to [Label → Labels](./label.md#a-modules-labels) added), **Type** (with its tie to a kind being a label that other labels take), and **Text** (unchanged in meaning). The headings `#taxonomy`, `#text` and `#type` that [label.research.001.md](label.research.001.md) links resolve again. memar's sections (Abstract, A name is one label, What belongs in a label, Where the rules for names live, Related artifacts) are kept as they were; two rows were added to Related artifacts, for Text and for the three registries.
- [README.md](README.md) holds the one word `label.md` in both versions; it is unchanged.

#### Considered and not done
- Dropped from organization's Dictionary: the senses of a recording company's trade name, a radioactive isotope, to pronounce judgment on, and to distinguish a molecule or element by a labeled atom. They are not senses this module uses; the Dictionary now says so in one sentence.
- Nothing of organization's Taxonomy, Type or Text was dropped; the two Taxonomy paragraphs on the word's history were folded into one with the same claims.
- Organization's heading "Taxonomy" is not renamed to memar's older "Taxonomies" (the handoff's wording) because the links the research makes use the singular.

#### Left open
- The Taxonomy section names three pluggable registries from a kernel module, which [Kernel](../modularity/labels/kernel.md) says a kernel module does not do; [label.research.001.md](label.research.001.md) reports this as contradiction 1 and leaves it to the owner. It is carried as organization wrote it, not resolved here.
- `text-type`, named in Type, is defined nowhere in this tree (research contradiction 14).
- [label.handoff.md](label.handoff.md) line 22 and line 98 still describe `label.md` by organization's former sections ("Taxonomies paragraph and the two sections added by this conversion"); that file is not this chat's and was not changed.

---

### Write the owner's rulings of 2026-10-20 on where labels are declared
- Time: 2026-10-23T10:00:00Z
- Type: changed
- Cited:
  - [Label Research 002 → Owner decisions needed](../../../.agents/tasks/20261019-T191745Z-15972/docs/label.research.002.md#7-owner-decisions-needed) - Evidence: decisions 1 to 5 as the owner ruled them
  - [Modules Research 001 → Owner decisions needed](../../../.agents/tasks/20261019-T191746Z-12632/docs/modules.research.001.md#6-owner-decisions-needed) - Evidence: rulings D4 and D7
- Contributors:
  - [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) — ruled (2026-10-20) and requested the work (2026-10-23)
  - An AI agent (Claude, model claude-opus-5-5 as reported by the runtime; no CONTRIBUTORS.md entry) — wrote the rulings in (task 20261023-T091509Z-17584)

#### What changed
- [label.md](label.md) gains the section Where labels are declared: a domain declares its labels and statuses as code; when a value becomes code and in what order; a free topic is the task domain's; a project that is not a Memar domain declares its labels in its own module folder; one shape for every registry of an organization's words; the central `.agents/memar/labels.md` stays frozen; the task domain's statuses are the first vocabulary declared this way. Each carries its reason. The rulings had stood only in the inquiry note, which was a research file beside this module until this task moved it to the docs of the task that answered it.
- A name is one label no longer says a free kind is defined in the project's own registry; it points at the new section.

---

### Retire the central labels file: each topic is declared as code by the domain whose it is
- Time: 2026-10-23T12:00:00Z
- Type: changed
- Cited:
  - [Label Research 002 → Owner decisions needed](../../../.agents/tasks/20261019-T191745Z-15972/docs/label.research.002.md#7-owner-decisions-needed) - Evidence: decisions 1 to 5, the shape and home of a declaration
  - [Kernel Neutrality → The rule](../modularity/rules/kernel-neutrality/kernel-neutrality.md#the-rule) - Evidence: a list of label words is a choice, kept out of a kernel module
- Contributors:
  - [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) — requested the file be retired (2026-10-23)
  - An AI agent (Claude, model claude-opus-5-5 as reported by the runtime; no CONTRIBUTORS.md entry) — implemented it (task 20261023-T091510Z-17584)

#### What changed
- `.agents/memar/labels.md` is removed. Its 22 topics, with their identifiers, are declared as code: the streams of work in `modules-plugable/management/task/labels/topics.py`, and the three topics that name a module (`task`, `label`, `khayyam`) in that module's `labels/topics.py`. Two topics that plans carried but the file had lost (`memar-skill`, `memar-cli`) are declared with them.
- A declaration is `LabelDefinition` with its meaning and its end of life (`ended`, `replaced_by`), made by `topic()` in `modules/knowledge/documentation/plan/labels/topic.py`; a declaring file holds a `LABELS` tuple and forces no store.
- [services/declarations.py](services/declarations.py) finds the declarations by walking the project's tree; `memar label add` and `memar task ensure --label` refuse a topic declared nowhere, printing the declaration to write and the declared topics near it, and refuse an ended one naming what replaced it; `memar label list` lists the declared topics too, and a carried label nobody declares as undeclared.
- [label.md](label.md): Where labels are declared says the file is retired and where a label is declared instead; A name is one label no longer says a free kind takes a word when it is first used.

#### Left open
- The cycle `content` → `task` → `label` → `task` in `bundles/memar/tests/module_graph.py` was there before this change (`label` imports `TaskId`, `task` imports `plan_labels`); it is not resolved here.
- Where labels are declared still names the task domain's statuses as the first vocabulary declared this way; the topics now are.

---

### The topics are the first vocabulary declared as code
- Time: 2026-10-23T10:20:00Z
- Type: Changed
- Cited:
  - [Label → Where labels are declared](./label.md#where-labels-are-declared) - Depends_on: the owner's rulings of 2026-10-20 and 2026-10-23 that labels are declared in the `labels/` folder of the module whose they are.
- Tasks:
  - 20261023-T100229Z-17920: Closed - the task that corrected it.
- Contributors:
  - [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) - ruled
  - [Claude](../../../CONTRIBUTORS.md#claude) (Opus 5.5 via Claude Code) - applied

#### What changed
- [Where labels are declared](./label.md#where-labels-are-declared) names the topics as the first vocabulary declared this way, and the task domain's statuses as the next.
