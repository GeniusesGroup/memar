# Priority

## Concept

Priority orders peers that compete for limited attention. Thing owns the scheme. Other domains may call its services; they do not redeclare it.

The durable shape is one Priority label on the thing, with a `Priority_Rank` field (whole number, bounds in the primitive) written on that label edge. Absence of the field means the lowest rank. Completing work does not detach the label. Queue and cache ordering are not this module's subject.

Until Graph typed edge fields are the live medium, Python holds the rank beside the label through a `RankStore` (facts key `priority_rank` for Task).

## Why

The same role appears wherever peers compete for limited attention. A numeric field on the Priority label edge is one value, not ten word labels.

## Related

- [`rules/a-priority-change-states-its-reason/`](rules/a-priority-change-states-its-reason/a-priority-change-states-its-reason.md)
- [`protocol/priority-rank.kh`](protocol/priority-rank.kh)
- [`protocol/rank-store.kh`](protocol/rank-store.kh)
- [`protocol/relation-rank-field.kh`](protocol/relation-rank-field.kh)
- [`labels/Priority.py`](labels/Priority.py)
- [`services/set-priority/protocol/set-priority.kh`](services/set-priority/protocol/set-priority.kh)
- [`services/read-priority/protocol/read-priority.kh`](services/read-priority/protocol/read-priority.kh)
