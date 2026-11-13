#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""modules/knowledge/text/services/rank_likeness.py — Likeness_Rank. Typed field filters are the text-index's work."""
from __future__ import annotations


class Likeness_Rank:

    def rank(self, scope, query, store, excluded, limit: int, min_likeness: float=0.0, module: str='', role: str=''):
        hits = store.rank(
            scope=scope,
            query=query,
            excluded=frozenset(excluded or ()),
            limit=max(int(limit), 0),
            min_likeness=float(min_likeness or 0.0),
            module=module,
            role=role,
        )
        return hits
