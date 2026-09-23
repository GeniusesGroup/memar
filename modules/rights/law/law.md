# Law
A law is one signed instrument. The legal order is the set of such instruments that are in force together.

## Abstract
A law node carries a human-language sentence and a machine-checkable form of the same norm, signed together with a goal, an explanation of its words, and an executive guarantee. Names people use for that sentence are labels on comments. A change after the signature is a new node. Specific statutes are instances of this node.

## Introduction

### Motivation
A statute book that treats a title as identity and then writes numbered articles and rider-notes mixes purpose, interpretation, exception, and procedure into one linear text. Coverage hides in notes; how the text will take effect can be omitted; later precision rewrites the norm. Judges and officers then fill the gaps with preference.

This type keeps a law clear because a change after a binding signature is a different law, and that change has a large cognitive cost for the people who live under it. A rate moving from 20 percent to 30 percent is a new node because its effects are large.

## Explanation

### Definition
A law node is one instrument. It does not store the legal order on itself. The order is which instruments are in force together.

Names people attach while commenting are labels beside the comment, in the [label](../../knowledge/label/label.md) domain. What those words mean for this domain is written in [law labels](../../../modules-plugable/rights/law-labels/law-labels.md). A label does not make a second kind of law. The same signature, the same companions, and the same rule that a change is a new node apply to every instrument. A label does not block that change, and it does not hold a wish that the human code and the computer code do not state.

The human-language sentence is [human code](edges/human_code/human_code.md). The machine-checkable form is [computer code](edges/computer_code/computer_code.md). They state the same norm before a binding signature opens. The word code alone is not the name of either edge. Together they state the position the instrument creates: a duty, a permission, a power, or an immunity. The type does not add a companion whose only job is to name that position.

A record opens for a binding signature together with these companions:

1. **Human code** — the sentence a person reads.
2. **Computer code** — the machine-checkable form of that sentence, realized by edges to [Rule](../../computer/rule/rule.md) nodes. A form that no input can satisfy is not opened for a signature.
3. **Goal** — why the instrument was written, carried in the payload so the reason is not lost. It does not outrank human code or computer code. If following the goal would produce a result those two refuse, the record is not ready for a signature. A goal that only states the reason more generally than the sentence is still a goal.
4. **Explanation** — a definition of the words used in the human code. A definition that changes who the sentence binds, or what it counts, belongs in the human code.
5. **Executive guarantee** — how the instrument takes effect in the world. Punishment for disobedience is one form of that path. A constitutive or power-conferring text has an operational path as well. The instrument can be in force before that path has been used. Using the path is not what makes the signature valid.

Opening for a binding signature requires every companion to be present. The signature is over a digest of the whole payload. After that opening, the payload stays as signed. A later change is a **new law node**.

An instrument is in force when it has a binding signature and no other instrument [supersedes](../../identity/thing/edges/supersedes/supersedes.md) it. Among instruments in force, the computer-code forms do not contradict, and the two do not both execute. A proposal is not in force. It may name an instrument that is. If the organization's update claim succeeds, the new instrument supersedes the earlier one. Until that success, the earlier instrument remains the one in force.

The human code is the sentence in the payload a person reads before signing. The type does not add a separate publication record. Who is bound without having signed is not this type.

The instrument is the same wherever people bind themselves by it. A society's statute and an organization's articles of association are both laws of this type. The type is not the government of a society. That narrowing is the same mistake as treating [politics](../../../modules-plugable/management/politics/politics.md) as the theater of rulers.

Human-readable bodies live in the [text](../../knowledge/text/README.md) domain; this type holds relations to them. That is the [attribute-or-edge test](https://github.com/GeniusesGroup/memar/blob/main/docs/modeling.md#the-attribute-or-edge-test): this node does not own storage, translation, or search of prose. The relations themselves live under `edges/`; the code-level interface is `edges/aggregation.go`. Identity of a node is `protocol/dt-uuid.go`.

This type is **Code** in Memar's [structure/policy split](https://github.com/GeniusesGroup/memar/blob/main/docs/modeling.md#separating-structure-code-from-policy-rule): it says what a law node is. A statute — a density cap, a tax rate, a deconstruction fund — is an **instance** of the node, written onto that structure.

Signatures, delegation, and the public critique of a proposition are the [election](widgets/election/election.md) widget.

### Boundaries
- **Law is an independent source.** `Right -> law = ...` collapses that source into an attribute. A [contract](../contract/contract.md) is the source for an arrangement its parties sign.
- **A signature is a consent record.** The vote edges in this folder record that consent. They are the signature, and the law text is the thing signed.
- **A law is realized as Rules.** A [Rule](../../computer/rule/rule.md) is an executable conditional policy reacting to events. Computer code is the machine-checkable claim, realized by edges to Rule nodes. The law is the instrument people sign. The Rules are how it executes. A Rule added after the signature is a new law, because the Rule set is inside the digest.
- **Instances are laws written on this structure.** Coverage ratios, infrastructure anchors, and similar proposals belong to the bundle that runs them. No-retroactivity, when a contract yields to a law, and whether a law supersedes a contract, are statutes in [laws](../../../modules-plugable/rights/laws/laws.md), not this type.
- **What a vote does to another law is not this type.** That effect is an optional edge of a [case](../case/case.md), included from [claims](../../../modules-plugable/rights/claims/claims.md).
