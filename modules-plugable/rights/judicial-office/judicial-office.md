# Judicial office
A role that may exist together with the judge edge when assignment uses task management. The edge still points at the user.

## Model

- A role may exist together with [judge](../../../modules/rights/case/edges/judge/judge.md), and that edge still points at the user.
- The role is how assignment works if adjudication uses task management.
- This domain does not hide the person behind an alias, and it does not reveal the person through a competence claim. A person hiding their own identity is a choice in the user domain. That choice is not modeled here.
- Until every required judge has voted, no party sees any judge's or expert's vote or explanatory text. That hide is a note for the content and timeline domains. It is not an alias, and it is not this role.

## Policies (rules)

- The edge points at the user. The role is not a substitute end that replaces the user.
- This is an authorization companion for assignment. It is not the social role whose title text is "judge" ([management role](../../../modules/management/role/data/judge/judge.md)).
- Plaintiff and defendant stay user edges. They are not offices in this module.
- Specialty, rank, and fee are self-declared and must carry evidence. Not an exam and not a badge. Whether any person may be a judge stays open. This file does not close it.
- Confidentiality of an inquiry's records is not this office. An inquiry returns a package. See [registry inquiry](../claims/edges/registry-inquiry/registry-inquiry.md).

## Placement

- **`modules-plugable/rights/judicial-office/`.** Functional roles are authorization, and they are not kernel. The case needs the judge edge whether or not this companion is copied.
- **Nearest alternative rejected:** `(case)-[:judge]->(role)` as the only end. The edge points at the user. The role sits with it for assignment.
- **Nearest alternative rejected:** `modules/management/role` as the seating. That module's judge file is a group title.

## Open questions

- None for an alias. Whether any person may be a judge stays open on [judge assignment](../judge-assignment/judge-assignment.md).
