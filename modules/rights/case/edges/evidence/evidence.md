# Evidence
A thing attached to this case in support of it.

## Model

- `(case)-[:evidence]->(thing)`

## Policies (rules)

- The case does not own the thing. A picture, a document, or a registry extract is a thing this edge points at. Where the bytes live is not this edge.
- Several evidence edges may leave one case. Several cases may point at one thing.
- Attaching the thing is not a ruling that the thing is authentic. Authenticity, if it is judged, is a case of its own.

## Placement

- **Here.** [Settlement for](../settlement_for/settlement_for.md) already points a case at a thing for a different job (what the dispute settles). Evidence is support, not that job. The two edges can leave the same case toward different things, or toward one thing under two relations if both are true.
- **Nearest alternative rejected:** folding evidence into `settlement_for`. That edge's recorded examples are contract, invoice, and task. It does not say "proof."
- **Nearest alternative rejected:** an evidence node. The thing already exists. A wrapper would hold no rule the edge does not state.
- A registry inquiry does not hold this edge back. [Acceptance required](../acceptance-required/acceptance-required.md) is not that gate.

## Open questions

- The participant label Witness is unratified. Is a witness a user-attachment on the case, or only a person related to the thing this edge points at? Blocks a witness edge.
