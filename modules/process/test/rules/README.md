# Test Rules (`modules/process/test/rules/`)
Rules for the process of writing and keeping a Test in this repository, being the conditions a module's Tests are held to. The general Memar concept of Rule is defined in [`docs/rule.md`](../../../../docs/rule.md); the subject these Rules check is the [Test](../../../../docs/protocols/process/test.md) protocol, whose document owns the definition and states no structural condition of its own.

| Rule | Subject | Tier | What it is |
| --- | --- | --- | --- |
| [Test Placement](./test-placement/test-placement.md) | Where a Test lives relative to the module whose Process it names | Governance | A `tests/` folder inside the module that owns the Process, so the tested surface reads without interleaved Test artifacts |
| [Test Naming](./test-naming/test-naming.md) | What a Test's own artifacts are called, and how a runner may recognize them | Governance | The folder is the only marker; a Test file is named for what it tests, with no marker in the name |

Both Rules are governance-tier: turning either off changes how well this repository's Tests are kept, not what may exist. Neither is enforced by a check this repository runs, per [Linter → Configuration and override](../../../../docs/protocols/computer/linter.md#configuration-and-override); an organization adopting this repository's rules may keep, relax, or replace either without forking anything.
