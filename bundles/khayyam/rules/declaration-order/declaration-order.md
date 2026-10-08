---
Title: "Khayyam Rule — Declaration Order"
Status: Draft
Start Date: "2026-10-04"
ID: "497527"
---

# Khayyam Rule — Declaration Order
Khayyam's rules live one rule per folder under [`bundles/khayyam/rules/`](../README.md), and this is the rule for where a method stands relative to the type it belongs to. It is a governance rule of this repository, not a grammar requirement: [Method Structure](../../../../docs/khayyam/method.md#method-structure) states the shape of a declaration and no order among declarations, and the [file layout rule](../file-layout/file-layout.md) already holds that the grammar requires no declaration order. What this rule adds is the part that rule stops short of. File layout's contracts-first order puts a file's contracts before its bodies; a type declaration and the method that belongs to it are both contracts, and that order says nothing about which of the two comes first.

## The rule
- **A method is declared after the type it belongs to.** `self` names the method's owner ([Method Structure → Key Rules](../../../../docs/khayyam/method.md#key-rules)), so a method standing above its owner's declaration meets a reader with a name the file has not introduced:

  ```khayyam
  tp Event cp {
      dt DataType
      time Time
  }

  tp GetDataType mt (self Event) () (d DataType)
  ```

- **The order binds each method to its own owner, and nothing else.** A file may declare several owners, and a method's place is fixed by where the one type its `self` names stands, not by where the file's other declarations stand. A method is also free of any order against a type it does not name.
- **An owner the file brings in with `in` is outside this rule.** `tp DataType in "modules/computer/datatype/protocol/data-type.kh"` puts the owner in another file, so no ordering of this one can place a method before it; the inclusion is where the reader meets the declaration.
- **An accessor on a capsule follows the observer abstraction's accessor of the same operation.** On the `Observer_X` / `Mutator_X` families ([observer and mutator rule](../../../../modules/computer/adt/rules/observer-mutator/observer-mutator.md)), `tp Observer_X ab` is followed by its accessors, and each capsule that holds the state declares its own accessor after its own declaration. This is the first clause applied to the families rather than a rule of its own, and the sources already keep it.

## Why this exists
The reader of a `.kh` file meets declarations in the order the file writes them, and the name in `self` is the one name in a method declaration that the file itself is responsible for introducing. A method above its owner inverts that: the reader arrives at `(self Event)` holding a type they have not been shown, and has to look downward to learn what the method is attached to. The [import address rule](../import-address/import-address.md) makes this repository's files addressable units, and a file that cannot be read from its top without jumping is a file whose address does not tell the reader what it costs to read.

The sources are close to unanimous and not unanimous, which is why the rule is stated as a rule and not as a description. Of the 752 `mt` declarations under `modules/`, 745 name an owner their own file declares, and 734 of those put the owner first. The eleven that do not are named in this rule's [handoff](./declaration-order.handoff.md), because a governance rule that cannot say where its own sources stand is asserting rather than holding.

The observer and mutator families are the clearest case: across the 125 `mt` declarations in the `*.observers.kh` and `*.mutators.kh` companion files, none stands above its owner.

## Keep it or drop it
An organization may write every method before every type, or may let a tool's ordering decide, and remain conformant to the language — nothing in the grammar reads this rule's condition. What an organization may not do is read the language as requiring it, and this rule is what keeps that from happening here; see [What this rule does not claim](#what-this-rule-does-not-claim).

## What this rule does not claim
- It does not claim the grammar requires this order. Both orders analyze; nothing in [Method Structure](../../../../docs/khayyam/method.md#method-structure) bears on it, and the [file layout rule](../file-layout/file-layout.md) says in terms that the grammar requires no declaration order at all.
- It does not claim anything checks it. Satisfaction in this language is structural and by method name ([Abstraction → Abstraction Realization](../../../../docs/khayyam/abstraction.md#abstraction-realization-implicit-satisfaction)), so a method reaches its owner through the name in `self` and not through where the owner was written; the same source answers "Where it is judged" as wherever an abstraction type is required. This rule is about how a reader meets the source, and no tool reports a violation of it.
- It does not claim a method may not be declared before a type it does not name, nor that a file's declarations fall into two blocks. Each method is ordered against its own owner.
- It does not claim anything about the order of a type's **composition block** against its own methods, which the sources do not agree on, nor about a method attached to a method. Both are open questions in this rule's [handoff](./declaration-order.handoff.md), and stating either as a rule here would state a condition the sources do not hold themselves to.
- It does not replace the [file layout rule](../file-layout/file-layout.md), whose contracts-first order this one refines rather than restates: that rule is about contracts against bodies and about file size, and it stops at the declaration.

## Open questions
This rule's own open state lives in its [handoff](./declaration-order.handoff.md).
