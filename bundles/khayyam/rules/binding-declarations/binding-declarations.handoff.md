# Khayyam Rule — Binding Declarations Live in a Side File Handoff
Open state for [binding-declarations.md](./binding-declarations.md). See the repository's [documentation-handoff.md](../../../../modules-plugable/knowledge/documentation/handoff/handoff.md) for what a handoff is.

## Status
Active — drafted 2026-10-02, following the owner's ruling that the file's name is the discriminator and that `bindings` is the facet key.

## Open Questions
- **How a binding's correspondence is recorded, and who owns the claim that it must be.** Nothing states it. The language is silent about how a foreign function is reached ([Language Gaps → I-B](../../targets/js/language-gaps.md#i-b--whose-name-a-body-less-method-carries--withdrawn-by-the-owners-ruling)), and the intervention that would have required a checkable record was withdrawn with it. What this rule's name buys is that a unit is findable as a place where bindings are declared; the record itself is unowned. A ruling could restore it as a governance claim of this repository, which is a different claim from the language sentence that was withdrawn.
- **Whether the refusal half belongs in this rule or in the file-layout rule.** The alternative placement is [`file-layout.md`](../file-layout/file-layout.md), whose first bullet at `:12` is the "one coherent responsibility" claim this rule leans on and whose *What this rule does not claim* at `:22`–`:26` would then govern a name the run's own address depends on. Decided for now: here, because the subject is a binding rather than a file, and recorded here so a reader can see the alternative.
- **Whether the facet key is `bindings` or something else.** The owner's ruling gives `bindings`. What is not settled is whether the rule's *folder* name should match the key — the catalog's rules name their subject (`file-layout`, `scope-placement`, `method-separation`), so `binding-declarations` names the subject rather than the key, and the two do not have to agree. An owner ruling either way is a rename here and in the catalog index.
- **What this rule does for a party that is not a repository-readable module.** [`link.ts:191`](../../targets/js/src/link.ts) refuses a link entry whose module cannot be read, so a binding whose crossing is reached by a party outside this repository is never a key of the map. The rule is written on the name rather than on the map's key precisely so it holds in both cases, but nothing checks either case yet.
- **Whether the rule applies to the second and third crossings.** The rule is written in the widened sense — a route, a shape, or a place — because the model is, and no source file yet carries a binding of the second or third kind. If the language rules that a place is inexpressible, the third kind has no file to govern and the rule's second bullet may need narrowing.

## Related Artifacts
| Artifact | Relation | Action |
| --- | --- | --- |
| [binding-declarations.md](./binding-declarations.md) | Base — the rule | Keep in sync with the model's Binding Unit concept |
| [modules/computer/binding/binding.md](../../../../modules/computer/binding/binding.md) | Depends_on — the concept of a binding, the three crossings, and the model of the side file | Keep in sync; the model's open questions 9 and 10 touch this rule |
| [Language Gaps → I-P](../../targets/js/language-gaps.md#i-p--what-tells-a-binding-from-an-ordinary-conversion) | Depends_on — the drafted text this rule was written from, and the owner's placement question | Read; not edited here |
| [Language Gaps → I-B](../../targets/js/language-gaps.md#i-b--whose-name-a-body-less-method-carries--withdrawn-by-the-owners-ruling) | Depends_on — the withdrawal this rule must not contradict | None (read) |
| [bundles/khayyam/targets/js/target.md → The three kinds of body-less method](../../targets/js/target.md#the-three-kinds-of-body-less-method) | Depends_on — the same convention stated in this toolchain's own document, at `:68` | Keep in sync; that document's owner may narrow it to the first crossing |
| [file-layout.md](../file-layout/file-layout.md) | Depends_on — the "one coherent responsibility" claim this rule cites | None (read) |
| [Documentation → File Naming](../../../../modules-plugable/knowledge/documentation/documentation.md#file-naming) | Depends_on — the dot as the separator between a facet key and a base name | None (read) |
| [Khayyam → Minimal Legislation](../../../../docs/khayyam/khayyam.md#minimal-legislation-a-principle) | Depends_on — why this is a rule and not grammar | None (read) |
| [bundles/khayyam/rules/README.md](../README.md) | Catalog index | **Needs a row** for this rule; not edited here, and the catalog's README symlink for this folder also needs recording as mode `120000`, which no git operation in this session may perform |

## Notes
- Measurements behind this rule, all from a full walk rather than a sample: 30 `.locale.<lang>.kh` files (23 eng, 5 per, 1 en, 1 fa), 100 `.observers.kh`, 9 `.mutators.kh`, over 1,281 `.kh` files. The 59 body-less methods on a concrete capsule declared in the same file — 43 in `modules/math/`, 8 in `modules/time/duration/`, 8 under `bundles/khayyam/targets/js/` — are carried from [language-gaps.md:19](../../targets/js/language-gaps.md) and `:33` rather than re-measured.
- This rule and its handoff are the only files this session wrote under `bundles/khayyam/rules/`. The catalog index was not edited and no git command was run.
