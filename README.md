# Organization
**An identity & structural framework for any collective entity — part of the Memar project**

## What is this?

Most organizational software is built around a single business vertical (CRM, e-commerce, ticketing, forums, etc.). This project starts from a different premise: the large majority of structural requirements are shared across every kind of organization — a government agency, a corporation, a small shop, a non-profit institute — and they mainly differ in scale and in the specific rules applied to that shared structure, not in the structure itself.

`Organization` is the identity/management module implementing that shared structural core, as part of the [Memar](https://github.com/GeniusesGroup) framework. Groups, departments, staff, tasks, ... are modeled as a small set of general-purpose graph domains rather than one-off, vertical-specific concepts.

## Goals

- Let service developers easily add more specific services via GUI.
- Continue developing the software in a low-code manner.
- Compile an application as a **UniKernel** instead of regular OS binaries.
- Develop highly available, distributed software without requiring an admin at any infrastructure layer (DevOps-culture goal).

## Not Goals

Nothing has been identified yet as explicitly out of scope for this project. This section is intentionally left open and will be filled in as such boundaries become clear through continued development — it is not an oversight.

## Project status

This project has been under active, multi-year development. Some directories and files are placeholders for future work and are not yet final. Architectural decisions are documented as RFCs within this repository; the exact folder location is still being finalized (repo-level folder structure is under active reconsideration).

## Relationship to the wider Memar framework

This repository focuses on the Organization identity/management domain. It is part of a larger, multi-generational software architecture project (Memar), which also includes components such as:
- Khayyam — a custom programming language
- PersiaOS — an operating system component
- Chapar / GP / sRPC — networking protocols

The relationship is methodological before it is technical: **Memar defines the way of thinking and modeling; Organization is one of the largest domains to be modeled with that method.** This is why Memar is required reading before contributing design judgments here — a contributor who has not internalized it tends to restart from industry defaults (starting from common management vocabulary instead of extracted concepts), repeating the exact failures Memar's method exists to prevent (see [`modules/management/vocabulary-discipline.handoff.md`](modules/management/vocabulary-discipline.handoff.md)).

See [GeniusesGroup](https://github.com/GeniusesGroup) for the full set of related repositories.

## Enterprise

Contact us by [email](mailto:ict@geniuses.group) or [email](mailto:omidhekayati@gmail.com) if you need enterprise support for developing highly available and distributed software. Enterprise package includes:
- Development of exclusive features in a short time
- Fast bug fixing

## Alternatives

[DRAFT — framed as architectural direction, not a claim of finished feature parity; please confirm which parts, if any, are accurate to say as "delivered" today vs. "the direction we're building toward"]
Unlike the tools below, which are generally built around one specific vertical (CRM, ERP, forums) and then extended outward, this project starts from a single shared structural model of "any organization" and lets specific verticals be added as thin, GUI-configurable extensions on top of it. It also targets deployment as a UniKernel and distributed operation without a dedicated admin/DevOps layer, rather than running as a conventional application on a general-purpose OS.

### Open Source
- [Odoo](https://www.odoo.com/) — [GitHub](https://github.com/odoo/odoo)
- [Discourse](https://www.discourse.org/) — [GitHub](https://github.com/discourse/discourse/)
- [ERPNext](https://erpnext.com) — [GitHub](https://github.com/frappe/erpnext/)

### Commercial
- [Salesforce](https://www.salesforce.com)
- [Softr](https://www.softr.io/)
