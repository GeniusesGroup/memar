---
Title: "Type Rule — No String Outside the Text Domain"
Labels: Draft
Start Date: 2026-11-02
---
# Type Rule — No String Outside the Text Domain
A rule of this repository, held for [Type](../../type.md), whose identity is what a type says of itself ([No Comments in Code](../no-comments-in-code/no-comments-in-code.md)). It applies to code in every language this repository's code is written in. It is held by Type because what a member, a parameter and a result are typed by is a type's, and the characters are the [text domain's](../../../../knowledge/text/text.md).

## The rule
- **Stored text belongs to the text domain and the string codec it stands on.** For stored or supplied text, another module takes a `Text`, or the type of its own concept that the text domain's `Text` makes (a title is `Title`, [the title module's](../../../../../modules-plugable/uri/title/title.md)). Immutable text supplied by code follows the boundary below.
- **A stored name is a domain concept.** Naming anything is the [`uri`](../../../../identity/uri/uri.md) concept's, and naming in a human language is the title module's. A module that holds a stored name, such as a word, a label name or a file name, uses `Field_Title` or the owner's field. A fixed name returned by a type's own code is covered by the binary-text boundary below.
- **Text fixed in the binary and independent of stored data remains in code.** A type's immutable human-facing descriptions are returned by its own methods in language-specific companion files, such as `.eng.kh`; their `String` results do not make the type an owner of stored text. The five [`detail.kh`](../../protocol/detail.kh) methods are one such contract. This exception is about the origin and purpose of the text, not the filename alone: a companion file is not a store for editable or persisted text.
- **Text recorded in a store is owned by the text domain.** Other domains refer to the text or to the owner's domain type rather than introducing their own stored string, validation, or storage model.
- **A new or changed file follows the rule;** older files are repaired when a task changes them, not in a sweep that touches files for no other reason.

## Why it exists
The owner's ruling of 2026-11-02: the label module declared `Field_LabelWord` over a `String` after the owner had said that only the text domain holds one, and a name that is a string is a name every module checks, stores and shows by its own code ([A concept has one owner module](../../../../knowledge/modularity/rules/one-owner/one-owner.md)).

## Keep it or drop it
An organization may type its members by strings and remain conformant to Memar's concepts; it then keeps a check of its own for every string that is really a name, a text or an address.

## What this rule does not claim
- It does not claim what a `Text` accepts; that is the text domain's.
- It does not claim a realization's local variables: only what a contract declares.
- [`check_no_string_outside_text.py`](./check_no_string_outside_text.py) lists `String` declarations outside the two domains and `.eng.kh` files. It does not distinguish fixed binary text from stored or supplied data, so its output requires review against this rule; it does not enforce the boundary. No commit gate runs it yet.
