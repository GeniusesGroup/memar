#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from importlib import import_module
_m_edit = import_module('modules.knowledge.text.errors.edit')


class Text_Edit:

    def replace(self, store, old, new, every, choice, rule, codec, lock, limits, writer):
        if old == '':
            raise _m_edit.Text_Error_Edit_OldEmpty()
        if not store.exists():
            raise _m_edit.Text_Error_Edit_TextAbsent()
        held = lock.take(store, writer, f'replace {len(old)} chars with {len(new)}', limits)
        try:
            text, had_mark = codec.decode(store.get_bytes())
            found = text.count(old)
            if found == 0:
                raise _m_edit.Text_Error_Edit_MatchAbsent()
            if found > 1 and (not every):
                raise _m_edit.Text_Error_Edit_MatchAmbiguous(found)
            replaced = text.replace(old, new)
            line_ending = rule.choose(choice, text)
            store.replace_bytes(codec.encode(rule.normalize(replaced, line_ending)))
        finally:
            held.release()
        return (found, had_mark)

    def write(self, store, text, choice, create, rule, codec, lock, limits, writer):
        if not store.exists() and (not create):
            raise _m_edit.Text_Error_Edit_CreateNotAsked()
        if not text.strip():
            raise _m_edit.Text_Error_Edit_EmptyText()
        held = lock.take(store, writer, f'write {len(text)} chars', limits)
        try:
            had_mark = False
            held_text = ''
            if store.exists():
                held_text, had_mark = codec.decode(store.get_bytes())
            line_ending = rule.choose(choice, held_text)
            data = codec.encode(rule.normalize(text, line_ending))
            store.replace_bytes(data)
        finally:
            held.release()
        return (len(data), had_mark)

    def write_from(self, store, source, choice, create, rule, codec, lock, limits, writer):
        if not store.exists() and (not create):
            raise _m_edit.Text_Error_Edit_CreateNotAsked()
        text = codec.decode_bare(source.get_bytes())
        return self.write(store, text, choice, create, rule, codec, lock, limits, writer)
