#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

from __future__ import annotations
from importlib import import_module
_span = import_module('modules.knowledge.text.primitive.text_span')
_item = import_module('modules.knowledge.text.primitive.text_item')
_errors = import_module('modules.knowledge.text.errors.structure')
Observer_Text_Span = _span.Observer_Text_Span
Observer_Text_Items = _item.Observer_Text_Items
Mutator_Text_Items = _item.Mutator_Text_Items
Text_Error_Structure_Position = _errors.Text_Error_Structure_Position


class Text_Section(Observer_Text_Items, Observer_Text_Span):

    def __init__(self, level: int=0, title: str='', titled: bool=False) -> None:
        Observer_Text_Items.__init__(self)
        Observer_Text_Span.__init__(self)
        self._level = level
        self._title = title
        self._titled = titled
        self._sections: list = []

    def GetSectionLevel(self) -> int:
        return self._level

    def GetTitle(self) -> tuple[str, bool]:
        return self._title, self._titled

    def GetOccupiedLength(self) -> int:
        return len(self._sections)

    def GetElement(self, position: int):
        if not 0 <= position < len(self._sections):
            return None, Text_Error_Structure_Position()
        return self._sections[position], None


class Mutator_Text_Section(Mutator_Text_Items):

    def SetTitle(self, title: str) -> None:
        self._title = title
        self._titled = True

    def AppendSection(self, section) -> None:
        self._sections.append(section)

    def InsertSection(self, position: int, section):
        if not 0 <= position <= len(self._sections):
            return Text_Error_Structure_Position()
        self._sections.insert(position, section)
        return None

    def ReplaceSection(self, position: int, section):
        if not 0 <= position < len(self._sections):
            return Text_Error_Structure_Position()
        self._sections[position] = section
        return None

    def RemoveSection(self, position: int):
        if not 0 <= position < len(self._sections):
            return Text_Error_Structure_Position()
        del self._sections[position]
        return None


class Text_Section_Editable(Text_Section, Mutator_Text_Section):

    def GetEditableItemAt(self, position: int):
        return self._items[position]

    def GetEditableSectionAt(self, position: int) -> Text_Section_Editable:
        return self._sections[position]
