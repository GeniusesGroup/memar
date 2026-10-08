# Go Port Rules (`targets/go/rules/`)

## What this folder is
The conditions on what the Go → Khayyam port left in this repository's `.kh` sources. The general Memar concept of Rule — ownership, `rules/` beside `protocol/`, linters, and rule engines — is defined in [`docs/rule.md`](../../../../../docs/rule.md); [Rule → Which Module a Rule Belongs To](../../../../../docs/rule.md#which-module-a-rule-belongs-to) fixes a Rule's home by its subject, and the subject of every Rule here is the port's residue rather than the language, the sources' conventions, or the tool that checks them. The target these Rules are applied by, and what that target owes, are stated in [`targets/go/target.md`](../target.md); the port's own record is the paired [research](../target.research.001.md).

## What the three have in common
Each of these Rules rewrites Go residue inside a Khayyam source: text the port wrote into a `.kh` file, or text it left in one. None is about a Khayyam program — a `.kh` file with no clue block at all satisfies every Rule of the [language catalog](../../../rules/README.md) and violates each of these, which is what places them here rather than in that catalog ([Khayyam rules → Which rules here are the language's own](../../../rules/README.md#which-rules-here-are-the-languages-own)). Every one is droppable: an organization that reads a residue block whole, or writes a generated parameter by hand, loses the measure and not the language.

They are applied by one command, `abstraction_bridge.py tidy --rule …` in [`targets/go/`](../abstraction_bridge.py), and by no other. The invocation stayed with the tool; the Rule documents moved with the subject.

## The rules
Each rule has its own folder, holding a main document named after the rule, a handoff beside it carrying that rule's open questions, and a pointer README. The documents are not restated here.

| Rule | Subject | Tier | What it is |
| --- | --- | --- | --- |
| [Go Clue Residue](./go-clue-residue/go-clue-residue.md) | The Go clue block a ported file ends with | Source rewrite | The block loses every declaration the Khayyam side already carries, and goes when nothing else is left |
| [Commented Generic Bindings](./commented-generic-bindings/commented-generic-bindings.md) | A generic Go interface whose methods stayed in the clue block | Source rewrite | A type parameter whose constraint names one abstraction becomes that abstraction in a real method |
| [Result Parameter Names](./result-parameter-names/result-parameter-names.md) | A parameter name the port wrote where the Go signature named nothing | Source rewrite | `resultN` and `argN` take the first letter of their type |

These three came from the Khayyam catalog on 2026-10-04 rather than being retired, because the material each governs is still being produced: the port writes a new clue block and a new `resultN` for every Go file it transfers, and 852 of the repository's 1279 `.kh` files still carry one. `go-clue-residue` states of itself that it retires with the last block, which is when this catalog ends.

## Membership criterion
A Rule belongs here when its subject is the Go → Khayyam port: text the port wrote into a `.kh` file, or text it left in one. It is enforced by a mechanism in [`targets/go/`](../abstraction_bridge.py), which is where the check lives and is not where the Rule lives; a Rule about a Go source file, about the Go language, or about anything outside the port's residue does not belong here either, and neither does a Rule about what a Khayyam program means — that is the [language catalog's](../../../rules/README.md), whatever tool applies it.
