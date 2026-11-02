---
Title: "Label Rule — One Declaration per Label"
Start Date: 2026-11-01
---
# Label Rule — One Declaration per Label
A rule of this repository, held for [Label](../../label.md), so that every word that is a label has one address a reader or a search can open. It applies with [One Type per File](../../../../computer/type/rules/one-type-per-file/one-type-per-file.md): a label is a Type, and its declaration is that Type's file.

## The rule
- **One label, one file — or one folder named for the word that holds that file.** Under a module's `labels/`, a Python file declares exactly one label: its module-level `LABELS` is a one-element tuple of a `LabelDefinition` (or of what `topic()` returns). A folder named for the word may hold that file beside the word's Model document; it does not hold a second word's declaration.
- **No bag file.** A file that defines many labels in one `LABELS` tuple, or an `enum.Enum` whose members are the vocabulary, is refused. A closed set is a folder of types, read by walking that folder ([Catalog](../../../content/primitive/catalog.py)), not one type with many members.
- **A list file only imports.** Where a reader needs every word of a kind in order, a thin module imports the types or builds a Catalog from the folder and holds no definition of its own ([One Type per File](../../../../computer/type/rules/one-type-per-file/one-type-per-file.md)).
- **Status-kind words obey the same rule.** Shared values live each as `Label_<Word>` under [`identity/thing/labels/`](../../../../identity/thing/labels/); a domain's Status-kind words live each under that domain's `labels/`. The Status *kind* label itself is [`Label_Status`](../../labels/Label_Status.py); it is not a container for the values.
- **Khayyam has no enum.** A vocabulary is not written as `enum.Enum` in Python either: each word is a Type whose identity and contract sit in its file, explained by Type's detail methods when the language is Khayyam ([`type.kh`](../../../../computer/type/protocol/type.kh); owner ruling 2026-11-01).

## Why it exists
Owner (2026-11-01): aggregating Status, TaskKind and topics into Enums or one Python bag made a second mechanism beside Label and hid each word from content search. One declaration per label is the address; Catalog and `memar label` walk the tree.

## Keep it or drop it
An organization that keeps a bag file remains able to attach labels, and loses the one-address check and the Type discipline Memar's tools assume.
