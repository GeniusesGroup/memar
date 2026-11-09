# Data in
A thing carries a mark for each domain that has written data on it, so asking which domains wrote on one identifier does not require checking every edge of every domain.

## Model
- `(thing)-[:data_in]->(domain)` — the thing has data in that domain. The domain is named by its identity.
- The edge is optional for every domain: a domain may write it when it writes on a thing, and none is required to. A thing with no mark is not a thing without data; the mark only shortens the question.
- No domain's edge, rule or service depends on the mark, and no edge is mandatory.

## Policies (rules)
- Written by the domain whose data it marks, in the same batch as the first edge of that domain on the thing.
- Thing owns the mark and declares it once. [A relation several domains need is defined once](../../../../../modules/knowledge/modeling/modeling.md#a-relation-several-domains-need-is-defined-once), in the domain that covers every record those domains are; a domain that wants the mark uses this edge and declares none of its own.
- What the data is, and what its edges mean, stay with the marked domain.
