---
Title: "Khayyam Rule — Other-Language Keyword"
Status: Draft
Start Date: 2026-10-03
ID: "497513"
---

# Khayyam Rule — Other-Language Keyword
Khayyam's rules live one rule per folder under [`bundles/khayyam/rules/`](../README.md), and this is the Rule for a word in a `.kh` unit that names a keyword some other language reserves and this one does not. It is a governance report of this repository's toolchain, not a statement of the language: [Khayyam → Language Keyword in a Glance](../../../../docs/khayyam/khayyam.md#language-keyword-in-a-glance) fixes the seven words that name declaration forms — `tp`, `vr`, `in`, `cp`, `mt`, `ab`, `sc` — and [Khayyam → Minimal Legislation](../../../../docs/khayyam/khayyam.md#minimal-legislation-a-principle) at `:177` puts a condition about the words a reader reaches for in the tool that applies it.

## The rule
- **What triggers it.** A name in a call position, a signature, or a declaration, that no declaration in the unit and no `in` declaration supplies, and that a reader is reaching for rather than merely mistyping — because the word is a keyword in some other mainstream language. `if`, `else`, `while`, `goto`, `fn`, `class`, `nil`, and the assignment and equality operators are the ordinary cases; the vocabulary is the tool's and is stated by the organization configuring it, not fixed here.
- **What it requires.** That the report say what the word is, not only that it is unresolved: that this language has no such keyword, that the need behind it is met by a library method, and where the operation that meets it is declared. A reader who came from another language is asking "which keyword does this replace?", and an unresolved-name label alone answers a question they did not ask.
- **What the check is.** The condition the report rests on is the one already carried by the [name not declared rule](../name-not-declared/name-not-declared.md) and the [unbound type name rule](../unbound-type-name/unbound-type-name.md): a name nothing in the unit declares or includes. This Rule adds no second resolution pass and refuses nothing that those Rules do not already refuse; it changes what is said when the refusal happens, and it fires only on the subset of that refusal where the unresolved name is recognizably another language's keyword. The other three import-resolution rules stand unchanged, and a unit that trips this Rule trips one of them too.

## Why it exists
A language document states what the language has. What it does not have is a different kind of statement, and the repository's own principle puts that kind somewhere else on purpose: a language document that enumerates the keywords it refuses carries a list that drifts with every other language, invites a reader to check membership, and answers a question no rule of the program asked. [Khayyam → The Grammar Refuses Protocol Semantics](../../../../docs/khayyam/khayyam.md#the-grammar-refuses-protocol-semantics) states why the grammar declines the constructs themselves — a construct's semantics may not depend on adopting a protocol's definitions — and this Rule is the reader-facing half of the same decision, placed where the owner placed it: **the warning belongs to the rule, not to the language document.**

So the knowledge the reader needs is the knowledge every language-with-less carries informally: that `if` here is a method someone wrote, `goto` is a jump method whose target is named, and `nil` is whatever the owning type's contract says absence is. [Khayyam → Variable](../../../../docs/khayyam/khayyam.md#variable) already routes absence to the type's contract, and [Control Flow → Library-Defined Control Flow](../../../../modules/process/control-flow/control-flow.md#library-defined-control-flow) already routes branching and jumps to named methods; this Rule states that a reader is told so at the moment they reach for the word, rather than leaving them to discover it from an unresolved-name fault.

## Keep it or drop it
An organization may keep the vocabulary and the wording, narrow it, or drop the Rule. Dropping it changes no program's meaning and refuses nothing that the two resolution rules do not already refuse; what a reader loses is the sentence that names what they reached for and where the thing they wanted is declared.

## What this rule does not claim
- **It is not the same Rule as name-not-declared or unbound-type-name.** Those refuse a name nothing supplies, whatever the name is; this Rule speaks about a subset of that refusal and only about what is reported. No program violates this Rule without violating one of those, which is the reason it is not a rule about the language: turning it off changes how well a reader is served, not what a program may mean.
- **It does not claim the words it names are absent.** `if` is not a keyword here; it is also not thereby forbidden as a name, since an identifier may spell anything the grammar's identifier admits ([Khayyam → Language Keyword in a Glance](../../../../docs/khayyam/khayyam.md#language-keyword-in-a-glance)). The Rule fires on a name nothing supplies, not on a spelling.
- **It does not claim a diagnostic contract, a code, or a recovery behavior**, and it does not name the library operation behind any of the words. Which declaration meets a need is that library's business, per [Rule → Which Module a Rule Belongs To](../../../../modules/process/rule/rule.md#which-module-a-rule-belongs-to) on a rule's home being its subject's module.
- **It does not claim anything about what any body of Khayyam source does.** No file or count in this repository is evidence for or against it, and none is cited.

## Open questions
This Rule's own open state — how much of the refusal the report covers, and how an organization states its vocabulary — lives in its [handoff](./other-language-keyword.handoff.md).
