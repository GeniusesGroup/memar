# Type Rules (`modules/computer/type/rules/`)
Rules for the conditions a type and the code that declares it are held to. The general Memar concept of Rule is defined in [`modules/process/rule/rule.md`](../../../process/rule/rule.md); a Rule is held by the module that owns its subject ([Rule → Which Module a Rule Belongs To](../../../process/rule/rule.md#which-module-a-rule-belongs-to)).

| Rule | Subject | Tier | What it is |
| --- | --- | --- | --- |
| [No Comments in Code](./no-comments-in-code/no-comments-in-code.md) | Where a type says what it is | Governance | A type's text is written by its own methods, never by a comment, in every language |
| [One Type per File](./one-type-per-file/one-type-per-file.md) | What a file declares | Governance | A file declares one type and is named for it; a catalog of members with definitions of their own is a set of types, one file each |
| [No String Outside the Text Domain](./no-string-outside-text/no-string-outside-text.md) | What a member, a parameter and a result are typed by | Governance | Only the text domain declares `String`; a name is a `Title` or the owner's field, a text is `Text`; a script lists the violations |
| [Map Concepts onto Realizations](./map-concepts-onto-realizations/map-concepts-onto-realizations.md) | How identified concepts become named Types | Governance | One concept one named entity; stateless still Types; multi-outcome via Abstraction |
| [Explicit Behavior Ownership](./explicit-behavior-ownership/explicit-behavior-ownership.md) | How methods gain a visible owner | Governance | One visible owner; no default-implement; no runtime injection; generation stays readable |
| [Type Metadata Carrier](./type-metadata-carrier/type-metadata-carrier.md) | How Type metadata is carried | Governance | No access markers; intent as constructs; human-facing in companions; one source |
| [Structure Is Fixed by Definition](./structure-is-fixed-by-definition/structure-is-fixed-by-definition.md) | When structure may come into being | Governance | Running system executes definition; no runtime structure minting |
| [Identity at Definition Time](./identity-at-definition-time/identity-at-definition-time.md) | Where concept identity lives | Governance | Identity from the Type alone at definition time; not as runtime data |
| [Categories Are Roles, Not a Hierarchy](./categories-are-roles-not-a-hierarchy/categories-are-roles-not-a-hierarchy.md) | How Capsule/Method/Abstraction/Scope relate | Governance | Roles not subtypes; no fifth category without irreducibility; Abstractions stay pure |

The Rule is governance-tier and is enforced by no check this repository runs today; an organization adopting this repository's Rules may keep, relax, or replace it without forking anything.
