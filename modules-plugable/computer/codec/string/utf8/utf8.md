---
Title: "UTF-8"
Labels: Draft
Start Date: 2026-11-05
---
# UTF-8
## Abstract
**UTF-8** is the character encoding of the Unicode Standard that writes each code point as one to four bytes; this module is Memar's side of it, a [guest](../../../../../modules/knowledge/modularity/labels/guest.md) module of the string codecs. The encoding abstraction is [`protocol/utf8.kh`](protocol/utf8.kh). The byte-order mark is a concept of UTF-8: [`protocol/utf8-byte-order-mark.kh`](protocol/utf8-byte-order-mark.kh) detects, strips and reports it, and [`protocol/utf8-codec.kh`](protocol/utf8-codec.kh) realizes the codec port the [text](../../../../../modules/knowledge/text/text.md) domain owns, decoding bytes and refusing those that are not UTF-8, with the errors in [`errors/errors.kh`](errors/errors.kh) realizing the text domain's.
