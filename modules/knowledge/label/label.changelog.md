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
  - An AI agent (Claude, model claude-sonnet-5-5 as reported by the runtime; no CONTRIBUTORS.md entry) — carried the text by hand (session 20261019-T103358Z-22340)

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
- [label.handoff.md](label.handoff.md) line 22 and line 98 still describe `label.md` by organization's former sections ("Taxonomies paragraph and the two sections added by this conversion"); that file is not this session's and was not changed.
