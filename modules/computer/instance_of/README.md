# Node
Node is running version of applications. Any application CAN have many running instance.

## Model

- `(software)-[:instance_of]->(software)`

## Policies (rules)

- A Software Instance (SI) node represents an instance of an off-the-shelf software product or equivalent proprietary item of software.

## Idea backlog from edge code comments

Raw proposals from comment notes inside edge .go files (comments remain in code as source). Review discipline per modules/management/vocabulary-discipline.handoff.md. Nothing below is ratified.

### Node lifecycle - edges/node-status.go
- **Idea**: lifecycle states (Starting - plan to start, e.g. wait for hardware; Running; Stopping; Stopped); power-source labels (Power_Failure, Power_Green - recyclable sources, Power_UPS, Power_Diesel); stability (Stable, NotResponse); cluster operations (Splitting, ReAllocate, AcceptWrite).
- **Review questions**: are lifecycle and cluster-operation states one state machine or two?

### Node types - edges/node.go
- **Idea**: node types LocalNode, Cloud, Edge, GUI.
- **Review questions**: closed set or organizational-open?

### Node relations and resources - edges/node-relation-hardware.go, node-relation-node.go, node-resource.go
- **Idea**: node-hardware states Running/Ran; node-node Replication; resource as Desired vs Actual duality.
- **Review questions**: is Desired/Actual a general pattern (also usable for estate/production)?

### Net address - edges/net-address.go
- **Idea**: address types DomainName, HostName, IPv4, IPv6, GP - with an open comment: WHY? NS system?
- **Review questions**: is this the placement for name/address resolution (URI domain overlap)?

### Active users - edges/user-active/users.go
- **Idea**: OperatingSystem_User interface exposing ActiveUser and the Users list (ID + SocietyID).
- **Review questions**: is OS-user a distinct identity from app-user (identity/user)?

### Health and audit-log (data models with idea semantics)
- **Idea**: ping via stream timeout with TTL/RTT (health); audit-log config where disabled modes still must Dispatch() to subscribed clients even when not saved locally.
- **Review questions**: audit-log dispatch semantics vs storage policy - rule or code?