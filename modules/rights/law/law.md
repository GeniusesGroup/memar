# Law
Law is the independent normative source that determines which rights, obligations, and behaviors are possible, valid, forbidden, or enforceable.

## Abstract
A law is a text that travels with a goal, an explanation of its words, an executive guarantee, and computer code. A name people use for that text is a label on a comment. Rival versions are new nodes. A binding signature is a digest of the whole payload. Specific statutes are instances of this node.

## Introduction

### Motivation
A statute book that treats a title as identity and then writes numbered articles and rider-notes mixes purpose, interpretation, exception, and procedure into one linear text. Coverage hides in notes; how the text will take effect can be omitted; later precision rewrites the norm. Judges and officers then fill the gaps with preference.

This type keeps a law clear because a change after a binding signature is a different law, and that change has a large cognitive cost for the people who live under it. A rate moving from 20 percent to 30 percent is a new node because its effects are large.

## Explanation

### Definition
A law is a **text**. Names people attach while commenting ("tax", "stable public revenue", "extortion") are labels beside the comment, in the [label](../../knowledge/label/label.md) domain.

The human-language text remains so a person can read the law. The computer-language form is the score an independent evaluation runs. Both belong to the same payload. Opening the record for a binding signature requires the text and the computer form to state the same norm.

A record opens for a binding signature together with four companions:

1. **Goal** — why the rule exists, at the root, so execution stays with the reason it was written.
2. **Explanation** — a definition of the words used in the text, written into the payload people will sign.
3. **Executive guarantee** — how the law takes effect in the world. Punishment for disobedience is one form of that path. A constitutive or power-conferring text has an operational path as well.
4. **Computer code** — a machine-checkable realization of the text, realized by edges to [Rule](../../computer/rule/rule.md) nodes.

Opening for a binding signature requires every companion to be present. The signature is over a digest of the whole payload (text, goal, explanation, executive guarantee, computer code). After that opening, the payload stays as signed. A later change is a **new law node**. A graph of relations among rival texts lets people compare. What statute books mix into articles and notes is already split across the companions, so coverage is stated in the text itself.

"Constitution" is a categorising classification. A new law's machine-checkable form agrees with the laws already in force.

Human-readable bodies live in the [text](../../knowledge/text/README.md) domain; this type holds relations to them. That is the [attribute-or-edge test](https://github.com/GeniusesGroup/memar/blob/main/docs/modeling.md#the-attribute-or-edge-test): this node does not own storage, translation, or search of prose. The relations themselves live under `edges/`; the code-level interface is `edges/aggregation.go`. Identity of a node is `protocol/dt-uuid.go`.

This type is **Code** in Memar's [structure/policy split](https://github.com/GeniusesGroup/memar/blob/main/docs/modeling.md#separating-structure-code-from-policy-rule): it says what a law node is. A statute — a density cap, a tax rate, a deconstruction fund — is an **instance** of the node, written onto that structure.

Signatures, delegation, and the public critique of a proposition are the [election](widgets/election/election.md) widget.

### Boundaries
- **Law is an independent source.** `Right -> law = ...` collapses that source into an attribute. A [contract](../contract/contract.md) is the source for an arrangement its parties sign.
- **A signature is a consent record.** The vote edges in this folder record that consent. They are the signature, and the law text is the thing signed.
- **A law is realized as Rules.** A [Rule](../../computer/rule/rule.md) is an executable conditional policy reacting to events. `computer_code` is the machine-checkable claim, realized by edges to Rule nodes. The law is the instrument people sign. The Rules are how it executes. A Rule added after the signature is a new law, because the Rule set is inside the digest.
- **Instances are laws written on this structure.** Coverage ratios, infrastructure anchors, and similar proposals belong to the bundle that runs them.

Owner review of an earlier critique of this type lives in [law.research.001.md](law.research.001.md).
