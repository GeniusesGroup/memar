#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
import enum
from dataclasses import dataclass, field

class RefreshRefusal(enum.Enum):
    NO_PROJECT = 'NoProject'
    NO_VIEW = 'NoView'
    NO_PRESENTATION = 'NoPresentation'

    def summary(self) -> str:
        return {RefreshRefusal.NO_PROJECT: 'the project is not named', RefreshRefusal.NO_VIEW: 'the project defines no view', RefreshRefusal.NO_PRESENTATION: 'no presentation is registered for the class the view shows'}[self]

@dataclass(frozen=True)
class RefreshRefused:
    reason: RefreshRefusal
    detail: str = field(default='', compare=False)

    def summary(self) -> str:
        return f'{self.reason.summary()}: {self.detail}' if self.detail else self.reason.summary()
