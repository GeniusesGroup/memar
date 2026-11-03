#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from modules.knowledge.label.primitive.declared_label import DeclaredLabel
from modules.knowledge.content.labels.Topic import Label_Topic

class Label_MemarCli(DeclaredLabel):
    title = 'memar-cli'
    id = '01a15a79-c9c2-735a-bbd8-da6731e1bc68'
    labels = (Label_Topic,)

    @classmethod
    def Overview(cls) -> str:
        return "The names of the `memar` command's verbs and of the services behind them."
