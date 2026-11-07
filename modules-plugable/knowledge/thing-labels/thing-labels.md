---
Title: "Thing labels"
Labels: Draft
Start Date: 2026-09-24
---
# Thing labels
Registered meanings of words a person may attach to any node.

## Abstract
Toxic and Sensitivity are [labels](../../../modules/knowledge/label/label.md). They can sit on any node. They are not kinds of node, and they are not a detection rule. Attaching a word uses `(thing)-[:label]`. This module does not add another edge.

A detection rule that looks for toxic material is a different capability: [detection toxicity](../detection-toxicity/edges-loop/detection-toxicity/detection-toxicity.md).

## Explanation
### Definition
An organization includes this module when it wants a registry of words that commenters attach across nodes, not only inside one domain. Each document under this module is one registered word.

Registration does not hide the node, and it does not decide who may attach the word.

### What a registered label does not do
- It does not make a second kind of thing.
- It does not by itself block a reader. A rule may read the label and refuse a view. The rule is not this module.
- It is not the node's identity.

### Registered words
- [Toxic](toxic/toxic.md)
- [Sensitivity](sensitivity/sensitivity.md)
