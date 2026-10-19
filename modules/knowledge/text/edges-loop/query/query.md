# Query

## Model

- `(text)-[:query]->(---)`

## Policies (rules)

- allowed vertices: text

## Open questions

- query-as-edge vs query-as-service-request; filter semantics.
- A query's `DataModel` says nothing about `Precision`. The precision of a
  search — the trade between matching exactly and matching loosely — is
  declared in [`protocol/dt-precision.kh`](protocol/dt-precision.kh) as a value
  with no vocabulary yet, and nothing carries it. Two references for it are
  worth reading before it is given one:
  [precision tuning values](https://www.elastic.co/guide/en/app-search/current/precision-tuning.html#precision-tuning-values)
  and
  [terms and phrases matching](https://www.elastic.co/guide/en/app-search/current/precision-tuning.html#precision-tuning-terms-phrases-matching).
- The same file leaves two things as questions rather than as model: whether a
  query is a text edge or a comment edge, and whether a module and a pagination
  are filters. A query is a request someone made, not a relation between texts,
  which argues that this folder is a service request rather than an edge at all
  — the question the model line `(text)-[:query]->(---)` has been carrying
  since it was written.
- The reason a query reads as a record at all: keyword order does influence the
  result, but it is one factor among many. The user's location, the user's
  search history, and the quality and relevance of the pages all weigh too.
- The protocol half of this folder cannot be converted: [`protocol/model.kh`](protocol/model.kh)
  composes the label domain's model, and no file declares it. See the handoff.

## Source

> Source: `modules/knowledge/text/edges-loop/query/protocol/data_model.kh` and `modules/knowledge/text/edges-loop/query/protocol/dt-precision.kh` (in code).
