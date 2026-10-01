---
Title: "Khayyam Rule — Receiver Method Names"
Status: Draft
Start Date: 2026-09-26
ID: "497338"
---

# Khayyam Rule — Receiver Method Names
Khayyam's rules live one rule per folder under [`modules/khayyam/rules/`](../README.md), and this is the rule for the name a method carries when the method is reached only through the receiver it is attached to. It is a companion to the [qualified names rule](../qualified-names/qualified-names.md), which governs the names of *declarations* that another file may meet; the two answer different questions, and a repository may keep either without the other.

## The rule
A method that no other file brings in by name keeps the bare name. The receiver supplies the context the name would otherwise have to carry, so `Timer.Start` — the declaration `tp Start mt (self Timer) (d Duration) (err Error)` — is written `Start`, not `Timer_Start`. Where a timer arrives inside another capsule, it is called through that receiver, and the call names the method alone.

The bare name holds when another declaration has the same plain name. A method named after the type it returns — `Domain` on `BS_Init_Request`, returning a domain; `Type` and `Status` on `GUI_Element` — keeps the bare name, and the other declaration carries its module's path under the [qualified names rule](../qualified-names/qualified-names.md): the abstractions are `App_Domain`, `GUI_Element_Type`, and `GUI_Element_Status`, and the methods are `Domain`, `Type`, and `Status`. A method name that a tool prefixes with its owner, or numbers, to get out of such a collision — `BS_Init_Request_Domain`, `GUI_Element_Type_2` — is a report of the collision, not a name this rule accepts.

An observer abstraction's method is named for the value it returns — neither its owner's name nor the observer's name doubled. On `Observer_X` / `Mutator_X` families the accessor is `Get` followed by the full concept in natural English order ([observer and mutator rule](../../../computer/adt/rules/observer-mutator/observer-mutator.md)). The owner's ruling on `modules/net/uri/protocol/scheme.kh` (2026-09-29) is the shape example: the accessor of `Observer_Scheme` is `GetScheme`, not `URI_Field_Scheme_Scheme`, because an observer abstraction's methods are implemented by the capsules that hold the state, and the name is what each of them writes. The short name stands when it is unambiguous for those implementers, checked over the corpus; when another owner's method of the same name returns something else, the accessor takes the observer's own qualifier — `FileMetadata` and `DirectoryMetadata`, not two `Metadata` — and the scheme accessor would be `GetURIScheme` if a second scheme observer existed. A module path segment the observer's name does not carry is not borrowed for the accessor, and a counter a tool falls back to is a report here too, not a name. An owner prefix is kept only when the bare name is ambiguous in the corpus.

An owner prefix is kept only when the bare name is ambiguous in the corpus. Methods are implemented by other capsules, so a method name never carries its owner's name unless the bare name is taken. The owner's ruling on `modules/computer/datatype/protocol/detail.kh` (2026-09-29) is the example: `Computer_Detail_Domain` is `Domain`, because the receiver already says which detail is asked and nothing else in the corpus claims `Domain` as a method of another signature. A bare name that equals another declaration, a `_2` counter, or the Record/Storage UUID pair is left as written and reported.

## Why it exists
Because a method is reached by its receiver rather than by its own name at the use site, prefixing the method with the owner's name repeats what the call already says. [Khayyam → Method in Khayyam](../../../../docs/khayyam/method.md#method-structure) writes the call as the receiver, the method name, and the two variable groups — ``W32.Sum(a, b)(total, err)`` for a type, ``k.Set(value)(err)`` for a variable, and ``helper.When(d)(t1)`` for a method attached to a variable's type — and the same document uses one bare name for methods of different owners: `W32.Sum`, `I64.Sum`, and `Decimal_64_64.Sum` are all `Sum`, and each is complete because the receiver says which one. A timer arriving inside another capsule is the same case: the receiver is the value the capsule holds, and `Start` on it needs nothing more.

The prefix also costs something the language charges for: a method "is itself a type, structurally analogous to a capsule" ([Method Structure](../../../../docs/khayyam/method.md#method-structure)), so every extra syllable in a method name is a syllable a reader carries through every call site, for no gain in meaning.

When a method name and a declaration's name meet, the method is the side that must not move. A capsule satisfies an abstraction by implementing every method the abstraction declares, matched by name, with itself as the receiver ([Abstraction → Abstraction Realization](../../../../docs/khayyam/abstraction.md#abstraction-realization-implicit-satisfaction)): `Read` on `FileReader` satisfies `Read` on `Reader`. A method's name is therefore part of the contract every realization repeats. Prefixing it to escape a collision — `BS_Init_Request_Domain` — makes every capsule that realizes `BS_Init_Request` declare a method named after an abstraction the capsule never names, and two abstractions that require one operation under two different prefixes can no longer be satisfied by one method. The declaration's name carries no such cost: it is already where qualification puts the context.

## How the call is written
The call form is the language's, and the language document is where it is stated; this rule does not invent a spelling. A method names its parent type in the owner group and the call writes the receiver, the name, and both groups:

```khayyam
tp Start mt (self Timer) (d Duration) (err Error)
timer.Start(d)(err)
```

The name before the dot is the parent type named in `self` ([Method Invocation Rules](../../../../docs/khayyam/method.md#method-invocation-rules)); a single `.` is the only call operator the grammar has, and `a.Foo().Bar()` is not legal syntax — every intermediate result is an explicitly declared, named variable ([Composition Depth as a Decomposition Signal](../../../../docs/khayyam/method.md#composition-depth-as-a-decomposition-signal-no-expression-chaining)). For a receiver whose type is an abstraction, the document's own example of the same operation dispatching to different code is `h.Hash(data)` ([Khayyam → Polymorphism](../../../../docs/khayyam/polymorphism.md)), against the language's statement that an abstraction is "a declaration that a capsule will respond to certain method calls" ([Khayyam → Abstraction](../../../../docs/khayyam/abstraction.md)).

The shape `socket.Timer().Start()` is therefore **not** Khayyam syntax and is not offered as such: it names the idea — a receiver, a method, a call — and the language's own spelling of that idea is the form above. The two questions the shape leaves open, whether the two variable groups are written when the receiver is an abstraction, and whether one unit may hold the same bare method name under two owners, are recorded in this rule's [handoff](./receiver-method-names.handoff.md) rather than answered here.

## Keep it or drop it
An organization may qualify every method name, drop the qualifier only where two owners would otherwise collide, or drop this rule and keep the [qualified names rule](../qualified-names/qualified-names.md)'s habit of qualifying everything. Acceptance answers whether the convention fits the organization holding it, not whether it is valid; a repository whose methods are imported by name — which the language permits, since a method is a type and `in` resolves any declared name ([name not exported rule](../name-not-declared/name-not-declared.md)) — cannot apply the rule at all, and that is a legitimate answer, not a rejection.

## What this rule does not claim
- It does not claim a method name must be bare. It claims the prefix is redundant when the method is reached only through its receiver, and leaves the choice to the organization.
- It does not claim methods and declarations are the same question. A declaration that another file meets by name — an abstraction, a field accessor, a composition entry — is governed by the [qualified names rule](../qualified-names/qualified-names.md). Where a name would be both a declaration and a bare method name, this rule keeps the method bare and the declaration is qualified under that rule.
- It does not claim one unit may declare the same bare method name under two owners. That is open in the [handoff](./receiver-method-names.handoff.md), and a prefixed or numbered name a tool emits for the second owner meanwhile is a report, not a resolution.
- It does not claim the receiver is always a variable. The type form ``W32.Sum(a, b)(total, err)`` is legal, and a rule that assumed a variable receiver would be wrong about it.
- It does not claim the language checks anything here. Nothing in the grammar requires a method name to be bare or to repeat its owner; both spellings analyze.

## Open questions
This rule's own open state lives in its [handoff](./receiver-method-names.handoff.md).
