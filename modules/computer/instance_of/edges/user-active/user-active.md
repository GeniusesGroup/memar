# User active

## Model

- `(software_instance)-[:user_active]->(user)`
- Candidate (unconfirmed): code shape seed — `OperatingSystem_User` interface exposing `ActiveUser()` and `Users()`, each user carrying `ID` + `SocietyID` — see [users.go](users.go).

## Policies (rules)

- Just one user can be active on any instance.
- Active user CAN change only by valid connection and valid token.

## Placement

- **Core `instance_of` keeps the active-user edge.** Entry point is the software instance; one-active-user is a policy on the kernel's running instance, and its connection/token preconditions are referenced by UUID across domains — no embedded types. Not a module: one relation plus policy has no independent processing to install or remove (edge vs module), and it is not derived data (analytics is always pluggable).

## Open questions

- Is OS-user a distinct identity from app-user ([user](../../../../identity/user/user.md))?

## Source

> Source: `modules/computer/instance_of/edges/user-active/users.go` (in code).
