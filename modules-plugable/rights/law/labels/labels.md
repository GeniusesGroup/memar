---
Title: "Law labels"
Status: Draft
Start Date: 2026-09-23
ID: 497270
---

# Law labels
Registered meanings of the words people attach when they comment on a law.

## Abstract
A name such as constitution, articles, tax, or extortion is a [label](../../../../modules/knowledge/label/label.md) beside a comment. It is not a field of the [law](../../../../modules/rights/law/law.md) node and not a second kind of law. This module is where those words are written down. The attachment edge stays the label domain's `(thing)-[:label]`. This module does not add another one.

## Introduction

### Motivation
The type already says a name is a label. Without a place to write what the word means, each document repeats the point, and a word such as constitution starts to look like a rank. Writing the meaning here keeps the word, and keeps it from governing the signed payload.

## Explanation

### Definition
An organization includes this module when it wants a registry of law-comment labels. Each document under this module is one registered word: what a reader may mean by it, and what it does not do.

Attaching a label is a commenter's act. Registration does not choose who may attach it, and it does not choose which of two conflicting words wins. It does not change the digest. It does not weight a vote.

### What a registered label does not do
- It does not make a second kind of law. The same signature, companions, and new-node rule apply to every instrument.
- It does not block a change. A later instrument is a new node whether or not someone has called the earlier one a constitution.
- It does not hold a wish. If the human code and the computer code do not state it, the label does not state it either.
- It is not the node's identity. Rival texts are compared as nodes. The labels are how commenters name them.
- It is not a rank. A word whose meaning is "harder to change" or "higher than other laws" is not registered. Accepting one such word accepts the next.

### Edge cases
- **Constitution.** Registered below. A comment label for an instrument the commenter treats as foundational. Same cycle as any other law.
- **Articles.** Registered below. The usual name for a law of an organization that is not a government. The instrument is still a law. The label does not move it into another type.
- **Tax and extortion.** Both registered. They can name one sentence. Neither is the sentence. Readers may filter comments. The filter does not weight the signature.
- **Dignity, justice, and similar words.** A comment may use them. They are not registered here, because a registry entry would be read as adding a norm the payload does not contain.
- **Basic law, organic law, fundamental law.** Not registered. Each is a rank.
- **Relabel after signature.** The new label changes what a later comment calls the instrument. The signed payload stays.
- **Label as a title field.** Refused. A title on the node would be an identity. Identity is the node.

### Registered words
- [Constitution](constitution/constitution.md)
- [Articles](articles/articles.md)
- [Tax](tax/tax.md)
- [Extortion](extortion/extortion.md)
