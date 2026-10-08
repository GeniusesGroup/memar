# Grounds
The text of why this complaint should be accepted.

## Model

- `(case)-[:grounds]->(text)`

## Policies (rules)

- The case does not store the prose. Text storage, translation, and search stay with [text](../../../../knowledge/text/README.md).
- The text is the plaintiff's reason. A vote has no reason field. Human-language explanations of the judges are timeline texts on the case, not this edge. That timeline text is not an invocable service parameter. Where an alternate service's parameters live is blocked.
- One case may reference one grounds text. Several cases may reference the same text node. Sharing the text does not share the ruling.

## Placement

- **An edge to text,** by the attribute-or-edge test. The case does not own prose.
- **Nearest alternative rejected:** a string field on the case. That field would make every domain that stores a reason reimplement text.
- **Nearest alternative rejected:** a subject node whose body is this text. The text is a companion of the case. See [subject](../subject/subject.md).
- A registry inquiry does not hold this edge back. See [acceptance required](../acceptance-required/acceptance-required.md).

## Open questions

- None for a reason field on a vote. Judge reasons are timeline texts. Whether the case UUID is the group that can carry that timeline is the premise in [case.research.001.md](../../case.research.001.md).
