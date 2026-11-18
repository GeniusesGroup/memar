#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations

class Label_Overlap_Score:

    def __init__(self, to_labels) -> None:
        self._to_labels = to_labels

    def do(self, scope, text, preds, store, excluded, limit: int):
        query = {label.id: label for label in self._to_labels.to_labels(text)}
        if not query or limit <= 0:
            return []
        excluded = set(excluded or ())
        entry_scores = {}
        posting_count = getattr(store, 'get_label_posting_count', None) or getattr(store, 'GetLabelPostingCount', None)
        posting_at = getattr(store, 'get_label_posting_at', None) or getattr(store, 'GetLabelPostingAt', None)
        matches_preds = getattr(store, 'entry_matches_preds', None) or getattr(store, 'EntryMatchesPreds', None)
        if posting_count is None or posting_at is None or matches_preds is None:
            raise TypeError('the index realization must expose label postings and entry_matches_preds')
        for label in query.values():
            count = int(posting_count(scope, label))
            for position in range(count):
                text_id, holder = posting_at(scope, label, position)
                if holder in excluded:
                    continue
                key = (holder, text_id)
                entry_scores[key] = entry_scores.get(key, 0) + 1
        best = {}
        for (holder, text_id), shared in entry_scores.items():
            if not matches_preds(scope, holder, text_id, preds):
                continue
            score = shared / float(len(query))
            prior = best.get(holder)
            if prior is None or score > prior[0] or (score == prior[0] and str(text_id) < str(prior[1])):
                best[holder] = (score, text_id)
        ordered = sorted(best.items(), key=lambda item: (-item[1][0], item[0]))
        return [{'holder': holder, 'id': text_id, 'score': score} for holder, (score, text_id) in ordered[:limit]]
