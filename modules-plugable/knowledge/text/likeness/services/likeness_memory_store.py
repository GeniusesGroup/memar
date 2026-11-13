#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from math import sqrt

def _as_weights(signature) -> dict[str, float]:
    if signature is None:
        return {}
    if isinstance(signature, dict):
        return {str(k): float(v) for k, v in signature.items()}
    weights: dict[str, float] = {}
    for item in signature:
        if isinstance(item, tuple) and len(item) == 2:
            title, weight = item
            weights[str(title)] = float(weight)
        else:
            weights[str(item)] = 1.0
    return weights

class Likeness_Memory_Store:

    def __init__(self) -> None:
        self.entries = {}
        self.renewed_at: dict = {}
        self._renewal_counts: dict = {}

    def begin_renewal(self, scope) -> None:
        snapshot = {}
        for (held_scope, _holder, _id), entry in self.entries.items():
            if held_scope != scope or entry.get('retired'):
                continue
            for title in entry['weights']:
                snapshot[title] = snapshot.get(title, 0) + 1
        self._renewal_counts[scope] = {
            'text_count': self.text_count(scope),
            'frequency': snapshot,
        }

    def mark_renewed(self, scope) -> None:
        self._renewal_counts.pop(scope, None)
        self.renewed_at[scope] = self.text_count(scope)

    def put(self, scope, holder, id, signature, module: str='', role: str='') -> None:
        self.entries[(scope, holder, id)] = {
            'weights': _as_weights(signature),
            'module': module,
            'role': role,
            'retired': False,
        }

    def forget(self, scope, holder, id) -> None:
        entry = self.entries.get((scope, holder, id))
        if entry is not None:
            entry['retired'] = True

    def forget_text(self, scope, id) -> None:
        for key, entry in self.entries.items():
            if key[0] == scope and key[2] == id:
                entry['retired'] = True

    def remove_retired(self, scope) -> None:
        for key in [key for key, entry in self.entries.items() if key[0] == scope and entry.get('retired')]:
            del self.entries[key]

    def text_count(self, scope) -> int:
        snap = self._renewal_counts.get(scope)
        if snap is not None:
            return snap['text_count']
        return len({key[2] for key, entry in self.entries.items() if key[0] == scope and not entry.get('retired')})

    def entry_count(self, scope) -> int:
        return sum(1 for key, entry in self.entries.items() if key[0] == scope)

    def retired_count(self, scope) -> int:
        return sum(1 for key, entry in self.entries.items() if key[0] == scope and entry.get('retired'))

    def retired_share(self, scope) -> float:
        total = self.entry_count(scope)
        if total == 0:
            return 0.0
        return self.retired_count(scope) / float(total)

    def frequency(self, scope, label_title: str) -> int:
        snap = self._renewal_counts.get(scope)
        if snap is not None:
            return int(snap['frequency'].get(label_title, 0))
        return sum(
            1
            for key, entry in self.entries.items()
            if key[0] == scope and not entry.get('retired') and label_title in entry['weights']
        )

    def signatures_of(self, scope, holder) -> list:
        return [
            entry['weights']
            for key, entry in self.entries.items()
            if key[0] == scope and key[1] == holder and not entry.get('retired')
        ]

    def rank(self, scope, query, excluded, limit: int, min_likeness: float=0.0, module: str='', role: str=''):
        query_weights = _as_weights(query)
        query_norm = sqrt(sum(weight * weight for weight in query_weights.values()))
        if not query_weights or query_norm == 0.0 or limit <= 0:
            return []
        best = {}
        for (held_scope, holder, _id), entry in self.entries.items():
            if held_scope != scope or holder in excluded or entry.get('retired'):
                continue
            if module and entry.get('module', '') != module:
                continue
            if role and entry.get('role', '') != role:
                continue
            likeness = 0.0
            for title, qw in query_weights.items():
                ew = entry['weights'].get(title)
                if ew is not None:
                    likeness += qw * ew
            entry_norm = sqrt(sum(weight * weight for weight in entry['weights'].values()))
            if entry_norm == 0.0:
                continue
            likeness /= query_norm * entry_norm
            if likeness <= 0.0 or likeness < min_likeness:
                continue
            prior = best.get(holder)
            if prior is None or likeness > prior:
                best[holder] = likeness
        ordered = sorted(best.items(), key=lambda item: (-item[1], item[0]))
        return ordered[:limit]
