---
Title: "Type Rule — No String Outside the Text Domain"
Labels: Draft
Start Date: 2026-11-02
---
# Type Rule — No String Outside the Text Domain
A rule of this repository, held for [Type](../../type.md), whose identity is what a type says of itself ([No Comments in Code](../no-comments-in-code/no-comments-in-code.md)). It applies to code in every language this repository's code is written in. It is held by Type because what a member, a parameter and a result are typed by is a type's, and the characters are the [text domain's](../../../../knowledge/text/text.md).

## The rule
- **No module but the text domain, and the string codec it stands on, declares a member, a parameter or a result of the type `String`.** Characters are the text domain's; any other module takes a `Text`, or the type of its own concept that the text domain's `Text` makes (a title is `Title`, [the title module's](../../../../../modules-plugable/uri/title/title.md)).
- **A name is not a string.** Naming anything is the [`uri`](../../../../identity/uri/uri.md) concept's, and naming in a human language is the title module's. A module declares no name member, such as a word, a label name or a file name, of its own: it embeds `Field_Title` or the owner's field.
- **The one exception is the result of the five [`detail.kh`](../../protocol/detail.kh) methods,** which return `String` by contract and are written in the type's `.eng.kh` file.
- **A new or changed file follows the rule;** older files are repaired when a task changes them, not in a sweep that touches files for no other reason.

## Why it exists
The owner's ruling of 2026-11-02: the label module declared `Field_LabelWord` over a `String` after the owner had said that only the text domain holds one, and a name that is a string is a name every module checks, stores and shows by its own code ([A concept has one owner module](../../../../knowledge/modularity/rules/one-owner/one-owner.md)).

## Keep it or drop it
An organization may type its members by strings and remain conformant to Memar's concepts; it then keeps a check of its own for every string that is really a name, a text or an address.

## What this rule does not claim
- It does not claim what a `Text` accepts; that is the text domain's.
- It does not claim a realization's local variables: only what a contract declares.
- It is checked by [`check_no_string_outside_text.py`](./check_no_string_outside_text.py), which lists the declarations of `String` in `.kh` files other than `.eng.kh` outside the two domains; no commit gate runs it yet.
