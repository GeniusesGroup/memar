# Test Rule — Test Placement Changelog

## Changelog

### Rule added
- Time: 2026-09-30T00:00:00Z
- Type: Added
- Cited:
  - [test.md](../../../../../docs/modules/process/test.md) - Depends_on: the subject whose structural condition this Rule states.
  - [rule.md](../../../../../docs/rule.md) - Depends_on: the concept placing an owner's executable conditions in a module `rules/` folder beside its `protocol/` folder.
  - [Linter -> How a governance rule is authored](../../../../../docs/modules/computer/linter.md#how-a-governance-rule-is-authored) - Extends: the members a governance Rule carries, supplied here as Subject, Tier, Default, and Override.
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

### `tests/` is the only name
- Time: 2026-10-11T06:30:00Z
- Type: Changed
- Cited:
  - [Modules → The kinds of folder here](../../../../README.md#the-kinds-of-folder-here) - Depends_on: the role-folder definition, which now requires a role's exact name and separates a role folder from a module that shares its name.
- Contributors:
  - [Omid Hekayati](../../../../../CONTRIBUTORS.md#omid-hekayati) - ruled that `tests/` is mandatory so the question does not recur, that role folders carry no prefix or suffix, and that a module named for a role is not that role
  - Auto (model not recorded) - drafted the change and renamed the remaining `test/` folders
- Propagates to:
  - [test-placement.handoff.md](./test-placement.handoff.md): Done - the open question on the plural removed as answered.
  - [docs/modules/process/test.handoff.md](../../../../../docs/modules/process/test.handoff.md): Done - the mirrored question removed.
  - [modules/README.md](../../../../README.md): Done - the role list names `tests/` alone and states the exact-name and module-versus-role conditions.
  - [bundles/README.md](../../../../../bundles/README.md): Done - the role list names `tests/` alone.

#### What changed
- The folder's name is now `tests/` with no variant — not `test/`, not `spec/`, not a padded name — in every module and bundle of the repository; the bullet that limited the settled name to the folders this Rule governs was removed.
- The singular `test/` folders of Khayyam's toolchain are recorded as a drift, and were renamed: `core/`, `display/`, `lsp/`, `services/rename/`, and `targets/js/` now carry `tests/`, and `targets/go/`'s loose `test_*.py` files moved into one.
- `services____/`, a padded name left from keeping a folder out of a Go tool's reach, was corrected to `services/` in the reasoning.

#### Considered and not done
- **Renaming the test files' own markers (`.test.ts`, `test_*.py`).** The runners these files are written for find them by those markers; [Test Naming](../test-naming/test-naming.md) makes no claim about another language's convention.
