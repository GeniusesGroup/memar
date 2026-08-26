# Type Practice Changelog

## Changelog

### Creation, absorbing the operational content of "Static Concepts Must Be Types"
- Time: 2026-08-25T00:00:00Z
- Type: Added
- Cited:
  - [Type](./type.md) — Depends_on: this practice operationalizes that document's principles (nominal identity, stateless Types, category model) as steps; every rule here derives from it.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — requested: directed that pre-facet micro-documents be dissolved into strong Explanation documents plus sufficient Practice documents, so an agent needing only the how reads one lean file without inheriting false assumptions from argumentative history.
  - [ox-alpha](../CONTRIBUTORS.md#ox-alpha) (opencode) — drafted: composed this procedure from the retired document's operational content and type.md's principles.

#### Summary
Created `type.practice.md` per `documentation-practice.md`'s Practice-facet schema (two-field front matter, imperative body). Absorbed the operational layer of the dissolved *Static Concepts Must Be Types* document (495421): the Type-qualification checklist, the category-choice table, the static-concept mapping rules with their detection test and gray zones, the multi-outcome abstraction-return pattern with its dispatch-vs-identification distinction, and the `Err` naming convention. Deliberately excluded everything argumentative (rejected alternatives, prior art, rationale) — those live in type.md and in that artifact's consolidated heritage record under type.changelog.md — and routed concept-existence questions to modeling practice, since classification was never a type-layer decision. A completion audit added two further clauses from the source: family-member graduation (a member acquiring genuine per-instance data becomes a data carrier while static members stay distinct) and the note that other static-concept families record their own naming conventions. A third pass, cross-checking an external review's gap list, restored the framework's review maxim ("polymorphism is about code reuse, not about teaching the compiler how to do its job") and the interim manual-completeness-discipline note, both of which had survived nowhere verbatim after dissolution. The same pass surfaced the exhaustiveness mechanism candidates (code-generator metadata; whole-program analysis; Kotlin sealed classes and Swift closed hierarchies as prior art over compiler-known closed sets of Types) into step 4 itself, so they no longer live only in type.changelog.md's Pending ledger.

---

### Type Identity stub dissolved
- Time: 2026-08-25T00:00:00Z
- Type: refactor
- Propagates to:
  - type.practice.md: Done — the stub's sole non-redundant asset, the apartment illustration (color differences leave one Type; an ownership relation may itself be a Type because it carries independent meaning), absorbed into the qualification step.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — directed: review and merge the small type-series companions into the strong documents.
  - [ox-alpha](../CONTRIBUTORS.md#ox-alpha) (opencode) — reviewed, applied.

#### Summary
Dissolved `type-identity.md`, a 42-line pre-facet stub, after a lens review found every claim already carried by a deeper home: identity-as-modeling-decision → "Type and Modeling" here plus Modeling's justification criteria; the identity-sources list (domain meaning, lifecycle, behavior ownership, relationships, rules, external recognition) → the qualification checklist ("external recognition" being this document's already-stated "domain participants recognize, name, and reason about"); attributes-describe-vs-identity-defines-existence → "What Is Not a Type" plus Modeling's Attribute-or-Edge Test; language-as-expression-not-source → "Type Beyond Programming Languages" and "Type vs Implementation Type". Its title also collided with this document's own deeper "Type Identity" section, so it could never have remained standalone without confusion. The conventions document's mention of the filename is a naming-pattern example, not a content reference, and needed no change.

---

### Absorption of the individual type-companion documents
- Time: 2026-08-25T00:00:00Z
- Type: Added
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — directed: dissolve the single-topic companions into the strong documents and this practice file, with no summarization loss. Supplied the metadata framings (access expectations span behavior invocation as much as state; multilingual identity is each Type's single-source-of-truth duty).
  - [ox-alpha](../CONTRIBUTORS.md#ox-alpha) (opencode) — reviewed, applied.

#### Summary

**From `type-identity.md`** (42-line stub): the apartment illustration absorbed into the qualification step — color differences leave one Type; an ownership relation may itself be a Type because it carries independent meaning. Everything else already lived in deeper homes (type.md's Type Identity / What Is Not a Type / Beyond Programming Languages; modeling.md's justification criteria), so nothing further was imported.

**From `type-metadata.md`** (ID 000018): new "Carrying Type metadata" section — construct-first answers for access and intent signals (never surface keywords); one companion artifact per required language beside the Type's definition, all sharing a single base name qualified by the target language (e.g. `TypeName-detail.en` / `TypeName-detail.fa`); localized names, labels, documentation, and failure descriptions live there, never inline or in external translation maps; regenerate-not-re-translate when an implementation language is added; translator-edits-without-developer-round-trips edge case; plus a routing rule for any unlisted metadata family (carrier by audience: tools/logic → constructs, humans/volume → companion artifacts — then record the decision).

**From `type-explicit_behavior_ownership.md`** (ID 495466): new "Behavior ownership" operational section — the three always-local questions (where defined / why available / who owns); delegation written as a visible call so what/where/why read in place, navigation reserved for depth; never default-implement — generate explicit methods from the single source instead; generated code must land in readable, auditable source files, never intermediates; multiple delegation targets allowed, each explicit; runtime injection (dynamic proxies, reflection-added methods) prohibited; the macro/generation boundary tested by human cognitive accessibility; and two relocated operational diagrams — the EBO decision flowchart and the Processor→Validator delegation sequence.

`type-rules_and_invariants`, `type-relations`, and `type-concepts_vs_data` were reviewed in the same series but left no practice-layer residue: their why-level content went to type.md and modeling.md respectively (see those changelogs).

---

