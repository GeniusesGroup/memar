# Node
Node is running version of applications. Any application CAN have many running instance.

## Model

- `(software)-[:instance_of]->(software)`

## Policies (rules)

- A Software Instance (SI) node represents an instance of an off-the-shelf software product or equivalent proprietary item of software.

## Idea backlog

Review discipline per modules/management/vocabulary-discipline.handoff.md. Nothing below is ratified.

### Health and audit-log (data models with idea semantics)
- **Idea**: ping via stream timeout with TTL/RTT (health); audit-log config where disabled modes still must Dispatch to subscribed clients even when not saved locally.
- **Review questions**: audit-log dispatch semantics vs storage policy - rule or code?
