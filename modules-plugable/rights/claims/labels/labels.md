---
Title: "Claim labels"
Status: Draft
Start Date: 2026-09-27
ID: 497367
---

# Claim labels
Registered meanings of the words people attach when they name a kind of claim.

## Abstract
A name such as complaint (shekvaieh) is a [label](../../../modules/knowledge/label/label.md) on a claim type. It is not a field of the [case](../../../modules/rights/case/case.md) node and not a second kind of case. This module is where those words are written down. The attachment edge stays the label domain's `(thing)-[:label]`. This module does not add another one.

## Introduction

### Motivation
A complaint was easy to redraw as the case node, or as an edge. The afternoon input keeps the word and gives each claim-type label a folder, on the pattern of law labels. Writing the meaning here keeps the word from becoming the dispute.

## Explanation

### Definition
An organization includes this module when it wants a registry of claim-type labels. Each document under this module is one registered word: what a reader may mean by it, and what it does not do.

Attaching a label is a commenter's act. Registration does not choose who may attach it, and it does not choose which of two conflicting words wins. It does not weight a vote. It does not carry the parties.

### What a registered label does not do
- It does not make a second kind of case. Parties, votes, and the ruling stay on the case.
- It does not split the adjudication model. Civil versus criminal stays a label. Execution of a claim is a compelled service whose input is not only a number, for either word. Those two words are not registered in this revision. Which labels exist is pluggable. A folder is not required to keep one adjudication model.
- It is not an edge between claims. Each reason claims are linked is its own edge, and those links are pluggable.
- It is not a rank, an exam, or a badge.
- It is not the node's identity.

### Edge cases
- **Complaint.** Registered below. A label that groups claim types, plus the text explanation a type already carries.
- **Civil and criminal.** Not registered here. The label decision stands. Execution stays one compelled service. Whether a numeric constraint belongs on the split is open, on [claim-labels.handoff.md](claim-labels.handoff.md).
- **Theft, kidnap, stolen, illegal.** Those stay edges of a kind of claim. A label does not redraw them.
- **Label as a title field.** Refused. A title on the case would be an identity. Identity is the node.

### Registered words
- [Complaint](complaint/complaint.md)
