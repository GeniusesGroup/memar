# Organization
An [organization](https://en.wikipedia.org/wiki/Organization) or organisation ([Commonwealth English](https://en.wikipedia.org/wiki/English_in_the_Commonwealth_of_Nations); [see spelling differences](https://en.wikipedia.org/wiki/American_and_British_English_spelling_differences#-ise,_-ize_(-isation,_-ization))), is an entity—such as a company, or corporation or an institution (formal organization), or an association—comprising one or more people and having a particular purpose.

There are a variety of legal types of organizations, including corporations, governments, non-governmental organizations, political organizations, international organizations, religious organizations, armed forces, charities, not-for-profit corporations, partnerships, cooperatives, and educational institutions, etc.

## Legal person

In law, a [legal person](https://en.wikipedia.org/wiki/Legal_person) is any person or legal entity that can do the things a human person is usually able to do in law – such as enter into contracts, sue and be sued, own property, and so on. The reason for the term "legal person" is that some legal persons are not human persons: companies and corporations (i.e., business entities) are persons, legally speaking (they can legally do most of the things an ordinary person can do), but they are not, in a literal sense, human beings.

## Juridical person

A [juridical person](https://en.wikipedia.org/wiki/Juridical_person) is a legal person that is not a natural person but an organization recognized by law as a fictitious person such as a corporation, government agency, non-governmental organisation, or international organization (such as the European Union). Other terms include artificial person, corporate person, judicial person, juridical entity, juridic person, or juristic person. A juridical person maintains certain duties and rights as enumerated under relevant laws. The rights and responsibilities of a juridical person are distinct from those of the natural persons constituting it.

## Naming rationale (resolved)
"Organization" is confirmed as the umbrella term for any collective, non-person identity (government, legal company, civil company, non-commercial institute, etc.).

- **Alternative terms rejected**: `Entity`, `Party`, `Body`, `Institution` were considered and rejected because the software's end users are general customers (including staff at large companies) with no expectation of specialized/legal/academic vocabulary; all alternatives were judged too specialized or uncommon compared to "Organization," which is both accurate and broadly understood.
- **External conventions not binding**: external industry conventions for the word (e.g., SaaS "Organization = tenant") are not treated as binding on this project's internal definition, as long as the internal definition is coherent and consistently applied.
- **Tenant-collision concern resolved**: the deployment model is a unikernel. A possible future multi-tenant hosting layer (for organizations that don't want to self-host and only care about the GUI) is deliberately named **"Government"** — not "Organization" or "Tenant" — because providing governance/hosting-of-others is precisely a government's function in this framework's own vocabulary. This keeps the business-domain `Organization` node and the hosting/tenancy boundary conceptually and structurally separate.

## Organization vs. Group (conceptual level)
`Organization` is a higher-order concept than `Group` — effectively "a group of groups." An organization can contain multiple departments; departments are modeled as groups; groups can themselves contain persons, other groups, or even other organizations as members (e.g., a university committee can have another organization as an external oversight member). Architecturally: `User`/`Organization` sit under the `identity` domain; `Group` sits under the `management` domain. This distinction is considered clear and settled. The remaining structural/implementation questions live in [`modules/management/group`](../../management/group/README.md).
