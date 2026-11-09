# Supersedes
This record takes the place of that record. The earlier record stays in the graph.

## Model
- `(thing)-[:supersedes]->(thing)`
- reverse (Tentative): `(thing)-[:superseded_by]->(thing)`, written in the same batch, so what took a record's place is one read. The reverse is owed by Thing: no realization writes it yet.

## Policies (rules)
- The relation is defined once, on thing. [A relation several domains need is defined once](../../../../../modules/knowledge/modeling/modeling.md#a-relation-several-domains-need-is-defined-once). A law, a [contract](../../../../rights/contract/contract.md), a product that replaces another product, and an [estate](../../../estate/estate.md) that is the one now realized can all take it. Copying it into each of those domains would be several edges for one concern.
- The edge does not delete the earlier record.
- A size or color child of a product is another product, not a supersession. A fork that leaves the original in place is not a supersession.
- A content takes it when a proposal is accepted: the proposal supersedes the content it replies to, and at most one `supersedes` enters a content ([Content → Proposals and replacement](../../../../knowledge/content/content.md#proposals-and-replacement)). A duplicate is likewise superseded by the thing it duplicates.
- Thing owns the relation. The domain, or the organization, owns the rule for when a record may take it. A vote on a law does not by itself create this edge.
