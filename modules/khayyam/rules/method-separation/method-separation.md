---
Title: "Khayyam Rule — Method Separation"
Status: Draft
Start Date: 2026-09-28
ID: 510443
---

# Khayyam Rule — Method Separation
Khayyam's rules live one rule per folder under [`modules/khayyam/rules/`](../README.md), and this is the rule for the vertical space between two method declarations in a file that carries prose. It rewrites source; it is applied by `abstraction_bridge.py tidy --rule method-separation` in [`targets/go/`](../../targets/go/abstraction_bridge.py).

## The rule
In a file that carries textual comments, two method declarations that follow each other are separated by exactly one blank line. Each declaration is taken together with the comment lines directly above it, so the blank line goes above a method's comment, never between the comment and the method.

- A file carries textual comments when it has a comment other than its opening license block and the `// TODO(go-migrate):` marker of a Go clue block. A file whose only comments are those two is left as it is.
- The Go clue block at the end of a file is not Khayyam source and is never touched.
- Two methods already separated by a blank line are left as they are; the rule never writes a second blank line.
- A declaration that is not a method — an abstraction, a capsule, an import — is not separated by this rule.

In [`modules/time/timer/protocol/timer.kh`](../../../time/timer/protocol/timer.kh):

```khayyam
tp When mt (self Timer) () (t Time)

// Status return active status of the timer.
// It is atomic operation and return a state at a particular time and
// can be changed just after you get the status.
tp Status mt (self Timer) () (s Timer_Status)
```

## Why it exists
A method's comment documents that method alone ([comment policy](../comment-policy/comment-policy.md) keeps documentation in comments until the type's own methods write it). When two commented methods touch, a reader cannot see where one method's account ends and the next one's begins; a blank line marks the boundary without adding a word. A file with no prose has no such boundary to mark, which is why the rule is conditional on comments.

## Keep it or drop it
An organization may separate every declaration, separate nothing, or group methods by owner with a blank line only between groups. The rule is a layout convention and changes nothing a program means; dropping it loses only the visual boundary.

## What this rule does not claim
- It does not claim the language reads blank lines. The grammar ignores them, and both layouts analyze the same.
- It does not claim anything about files without textual comments, or about the order of declarations.
- It does not claim that the clue block's Go text follows any layout.

## Open questions
This rule's own open state lives in its [handoff](./method-separation.handoff.md).
