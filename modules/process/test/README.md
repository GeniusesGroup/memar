# Test (`modules/process/test/`)

## What this folder is
The realization of the [Test](../../../docs/protocols/process/test.md) protocol in this repository: the Rules an owner of a module places on where a Test lives and on what its artifacts are called, and the ground on which a runner for this repository's language would be built. The protocol document owns the definition; this folder owns the conditions that can differ between one owner and another, per [Rule → Where Rules Live](../../../docs/rule.md#where-rules-live-rules-beside-protocol).

It sits under `process/` beside [rule](../rule/) and [rules-engine](../rules-engine/), which are the evaluation abstractions for rules in general. What distinguishes this module from those is its subject: those evaluate authored conditions at runtime or against analysis input, while this one carries the conditions about the process of writing and keeping a Test, and the runner that would apply them.

## What this folder does not hold yet
There is no `protocol/` folder here, and its absence is current state rather than an oversight. What a runner exposes — what it is asked to do, what it returns, how it reports an outcome — has not been designed, and writing declarations for a mechanism that has no agreed contract would state a decision this module has not made ([modules → Why a folder may exist before it holds code](../../README.md#why-a-folder-may-exist-before-it-holds-code)). The open state is recorded in the protocol document's [handoff](../../../docs/protocols/process/test.handoff.md).

Concretely, this repository today has **no runner for the language its modules are written in**. The test artifacts present under `modules/` are archived from the previous language under a migration marker, so none of them is executable, and no scheme discovers them. Nothing in the protocol requires a runner, per [Test → Test, Check, and Runner](../../../docs/protocols/process/test.md#test-check-and-runner); the obligation it states is that a Test exists, and a Test exists whether or not anything has run it.

## Membership criterion
A folder belongs under this module when it carries a condition about Tests that this repository holds itself to — where they live, what they are called, what they may assume about their subject — and cites [test.md](../../../docs/protocols/process/test.md) for the claim the condition checks. A condition about something other than Tests does not belong here, and a condition another organization would hold about the same subject is a legitimate Rule elsewhere rather than a defect in this set.

## The rules
The listing of [`rules/`](./rules/) is the index; the documents are not restated here. Each Rule states what it is, why it exists, whether an owner may keep it or drop it, and what it does not claim, and each carries the members a governance Rule is authored with per [Linter → How a governance rule is authored](../../../docs/protocols/computer/linter.md#how-a-governance-rule-is-authored): Subject, Tier, Default, Override.

## What does not belong here
- **The definition of a Test.** That belongs to [test.md](../../../docs/protocols/process/test.md); a Rule here cites it and states a condition about it.
- **The procedure for writing a Test.** That belongs to [Test Practice](../../../docs/protocols/process/test.practice.md); this folder realizes nothing about how a participant works.
- **A copy of a Rule another module already states.** A condition about how Khayyam source is written belongs to [Khayyam rules](../../khayyam/rules/), and is cited from here where it applies.
