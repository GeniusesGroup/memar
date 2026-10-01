# Khayyam Rule — Name Not Declared Changelog

## Changelog

### The label renamed, because it named a mechanism the language does not have
- Time: 2026-09-30T00:00:00Z
- Type: Changed
- Ruling: owner, 2026-09-30
- Contributors:
  - opencode (space-bunny-free) - applied

#### What changed
- The implementation label `name-not-exported` is now `name-not-declared`, and this rule's folder was renamed with it. **The trigger was a fault that was correct and was still read wrong**: the owner followed a real corpus claim to `name-not-exported` and asked why it had failed, having read it to mean the target file was fine and had withheld the name. The file declared nothing at all. The label named a mechanism the language has no word for — [Khayyam → Import Mechanism (`in`)](../../../../docs/khayyam/khayyam.md#import-mechanism-in) gives a declaration a name and a path, and says nothing about a surface, a publication step, or anything being withheld — and a label that borrows another language's vocabulary sends the reader looking for that language's mechanism. `declaration` is the language's own word for what `tp` and `vr` write, and the three inclusion labels are siblings on purpose: all three say what is *not there*.
- The rule's own text was corrected on the same grounds. It said a file publishes a surface, offered a "barrel file" or a "generated export list" as ways to satisfy an importer, and called the old label's word an implementation detail — three borrowings in twenty-six lines, each pointing the reader at a concept this language does not have.
- A check now holds the labels to the language's vocabulary: [core/test/refusal.test.ts](../../core/test/refusal.test.ts) reads the labels out of the `RefusalReason` union and refuses any that names `export`, `published`, `visibility`, `public`, `private`, `namespace` or `package`. This is the part that matters beyond the rename — the wrong label shipped because nothing looked at the labels, and this test is what looks at them.
- The rename reaches the whole toolchain: `core/src/sr.ts` and `core/src/frontend.ts` (the gate, which has no production caller), `lsp/src/diagnostics.ts`, `lsp/src/inclusions.ts`, and eight documents that name the rule or the label. This changelog and this rule's handoff were renamed with the folder, and are therefore new files rather than edited ones.

#### Considered and not done
- **`name-not-exist`, which the owner proposed first.** Considered and not taken, and the difference is worth recording rather than discarding: "exist" answers "does this name exist?" without saying where, and the fault's whole content is *where* — the file behind the path. `declared` is both the language's own word and the answer to that question, and it makes the three inclusion labels siblings, which is what lets a reader read them down a problems list as one family.
- **Renaming `unbound-type-name` for symmetry.** Considered and not done: it is a different fault about a different thing (a type reference no name answers, which needs a reference walk this toolchain does not have), and no reader has met it. A label is renamed when a reader has been misled by it, not when symmetry suggests it.
