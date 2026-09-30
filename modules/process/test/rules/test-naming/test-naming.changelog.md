# Test Rule — Test Naming Changelog

## Changelog

### Rule added
- Time: 2026-09-30T00:00:00Z
- Type: Added
- Cited:
  - [test.md](../../../../../docs/protocols/process/test.md) - Depends_on: the subject whose structural condition this Rule states.
  - [test-placement.md](../test-placement/test-placement.md) - Depends_on: the folder this Rule's naming follows from, and the reason a marker in the name is unnecessary.
  - [documentation.md -> File Naming](../../../../../docs/documentation.md#file-naming) - Extends: the repository's rule for a name carrying another angle on the same subject, which this Rule deliberately does not use for a Test.
  - [Linter -> How a governance rule is authored](../../../../../docs/protocols/computer/linter.md#how-a-governance-rule-is-authored) - Extends: the members a governance Rule carries, supplied here as Subject, Tier, Default, and Override.
- Contributors:
  - [Omid Hekayati](../../../../../CONTRIBUTORS.md#omid-hekayati) - ruled that a Test is a separate identity rather than another angle on the file it checks, and settled the name form that follows
  - Auto (model not recorded) - drafted the Rule
- Propagates to:
  - [test-naming.handoff.md](./test-naming.handoff.md): Added - open state, including whether a Test's subject should be machine-readable in its name.
  - [../README.md](../README.md): Done - indexed.
  - [modules/process/test/README.md](../../README.md): Done - the module states its own open state.

#### What changed
- Added a governance Rule removing the marker from a Test's name, on the ground that the `tests/` folder already states the location and a marker would state it twice.
- Required the Process's name inside the Test as well as in its file name, keeping the protocol's subject obligation independent of the naming convention.
- Distinguished Test-support artifacts from Tests, so a reader scanning a folder for subjects does not find one twice.
- Stated that the Rule is a pair with Test Placement, adopted or relaxed together, since a marker is a substitute for a folder rather than an addition to one.

#### Considered and not done
- **A marker retained as a cross-tool convention.** Keeping `*_test.kh` would let a tool written against this repository's earlier language find Test files unchanged. Rejected because no such tool exists for the language the modules are now written in, so the convention would serve a migration rather than the repository; the archived artifacts are recorded in the module README as what they are.
