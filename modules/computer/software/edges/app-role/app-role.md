# Rule permission roles (rule-app)

## Model

- Candidate (unconfirmed): role labels over rules scoped to an app — `(rule)-[:app_role]->(app)` / reverse, with labels `(Rule)Developer`, `(Rule)Observer`, `(Rule)Supervisor`, `(Rule)Executive`; direction unconfirmed.

## Policies (rules)

- `(Rule)Executive` is who administers the rule; Developer / Observer / Supervisor are the further admin/visibility roles over rules on an app.

## Placement

- **Rule domain, not software.** Who-may-administer a Rule is organization policy — Core never knows Rule (decided in [rule.handoff.md](../../../rule/rule.handoff.md)), the same verdict shape as the sell-limit audience roles filed in [sell-limit](../../../../economics/product/edges/sell-limit/sell-limit.md).
- No new module: if the existing rights/delegate machinery already models admin roles, these labels should reuse it (edge vs module: no independent processing here). The app side must reference rules generically, never embed role semantics in core `software`.

## Open questions

- Do these reuse the rights/delegate machinery instead of new labels?
- Are the four labels one role edge to app, or separate edges per role?
- Direction/naming unconfirmed — nothing ratified.

