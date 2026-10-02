# Application Access Control
Access control is base on business rules.

## Examples

- User access to answer exam just when they are in the school or send webcam data

## Idea backlog

Nothing below is ratified.

### Business services
- **Idea**: three role-access service sketches — `Get` → `GetRoleAccess`; `GetRecursively` → `GetRoleAccessRecursively` "to get parent role access if the role has no access" (flagged in code as `bad service??`); `Revoke` → a service "to tell all node change role access control immediately".
- **Review questions**: is parent-role fallback a read-time default (presentation) or stored semantics — a service or a rule? What does `Revoke` reach — "all node" as group descendants, live sessions, cached authorizations — and who triggers it (rule/event vs direct call)? Does the recursive read overlap [authorization](../authorization/authorization.md)'s group policy model — which module owns role-access lookup (flagged, not resolved)?

### Zero-trust application inventory
- **Idea**: a ZTNA application catalog sketched as commented-out Go types — an `Application` base (session duration, custom domain, logo, tags, identity providers, WARP, app launcher, embedded block pages: identity-error / non-identity-error / deny URL) with subtypes `SelfHosted`, `SaaS` (SAML: entity ID, assertion-consumer-service URL, NameID format, attribute statements), `PrivateNetwork` (destination IP, SNI), and `Bookmark` (URL), plus per-application `ApplicationDomain` (subdomain, domain, path) — an inventory of protected applications, not an access-check engine.
- **Review questions**: an application catalog (SAML/IdP/WARP integration) is a different capability from evaluating access — does it belong in this module, beside the network-connection concerns already in [app-connection.kh](app-connection.kh), or in a dedicated zero-trust/app-proxy home? Which module owns SAML/IdP semantics (identity, not access checking)? Do the storage caveats in the sketch's comments (tags, identity providers, session options as JSON vs columns) belong to any protocol contract here?

### Zero-trust policy engine
- **Idea**: the companion policy model — `Policy` (action Allow, session duration, rules, many-to-many groups) built from `Rule` selector/value pairs with an optional justification prompt, `Group` with `GroupCriteria` (e.g. emails `@hr.company.com`, country `US`), and a free-standing `Selector` type shared with rules; the commented example wires an "Internal HR System" self-hosted application to a "Default Access" allow policy matching emails `@company.com`, plus a group rule requiring a business justification.
- **Review questions**: selector/value string pairs read as a reinvented rules-engine — should this materialize as rule-domain configuration (core never knows Rule; the rules-engine decides semantics) rather than access-control code? It is the third access model in this module alongside [app-connection.kh](app-connection.kh)'s Allow/Deny (where/when/which) and [access_control.kh](internal/access_control.kh)'s ContextGraph/Matcher/AccessGrant (allow/deny over matchers) — one model, two capabilities, or competing sketches to converge? Who owns justification-required flows — access control, the rule domain, or a separate justification capability?
