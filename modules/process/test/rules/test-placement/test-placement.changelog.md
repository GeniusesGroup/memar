# Test Rule — Test Placement Changelog

## Changelog

### Rule added
- Time: 2026-09-30T00:00:00Z
- Type: Added
- Cited:
  - [test.md](../../../../../docs/protocols/process/test.md) - Depends_on: the subject whose structural condition this Rule states.
  - [rule.md](../../../../../docs/rule.md) - Depends_on: the concept placing an owner's executable conditions in a module `rules/` folder beside its `protocol/` folder.
  - [Linter -> How a governance rule is authored](../../../../../docs/protocols/computer/linter.md#how-a-governance-rule-is-authored) - Extends: the members a governance Rule carries, supplied here as Subject, Tier, Default, and Override.
  - [Rule handoff -> Follow-up work: relocate document-level rules](../../../../../docs/rule.handoff.md) - Extends: the inventory this Rule is a first realized entry against.
- Contributors:
  - [Omid Hekayati](../../../../../CONTRIBUTORS.md#omid-hekayati) - ruled that the structural condition about Test placement is a Rule rather than protocol text, and that the folder is plural
  - Auto (model not recorded) - drafted the Rule
- Propagates to:
  - [test-placement.handoff.md](./test-placement.handoff.md): Added - open state, including the unsettled question of the plural as a repository-wide convention.
  - [../test-naming/test-naming.md](../test-naming/test-naming.md): Done - the sibling Rule depends on this one's placement and is adopted or relaxed with it.
  - [../README.md](../README.md): Done - indexed.
  - [modules/process/test/README.md](../../README.md): Done - the module states the module's own open state, including that no check enforces this Rule.

#### What changed
- Added a governance Rule placing every Test in a `tests/` folder inside the module that owns the Process the Test names, and stating the conditions under which that folder must not exist.
- Argued the placement against the sibling-file arrangement on the cost each pays, and the plural over the singular from the count of instances a role folder holds.
- Stated that the Rule is not enforced by any check this repository runs, and that an organization may organize its tests differently while still conforming to the protocol.

#### Considered and not done
- **A Test artifact beside what it tests.** The ecosystem's ordinary choice, and the one this repository's source tree already carries. Rejected for the module surface's readability, at the cost of the tested unit's proximity; recorded here because the rule's own handoff still records the question of a readable, checkable subject.
- **Enforcing the Rule with a check.** No check over a folder tree exists in this repository, and writing one before the module's protocol surface is designed would state a decision the module has not made.
