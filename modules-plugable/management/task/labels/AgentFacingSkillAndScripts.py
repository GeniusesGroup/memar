#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from modules.knowledge.label.primitive.declared_label import DeclaredLabel
from modules.knowledge.content.labels.Topic import Label_Topic

class Label_AgentFacingSkillAndScripts(DeclaredLabel):
    title = 'agent-facing-skill-and-scripts'
    id = '01a154e2-a32b-7c06-b910-db3f22dd8695'
    labels = (Label_Topic,)

    @classmethod
    def Overview(cls) -> str:
        return 'The Memar skill and the scripts an agent reads and runs.'
