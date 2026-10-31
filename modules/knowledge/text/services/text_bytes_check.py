#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

from __future__ import annotations
from importlib import import_module
_m_errors = import_module('modules.knowledge.text.errors.bytes')
_m_structure = import_module('modules.knowledge.text.errors.structure')
_m_text_check = import_module('modules.knowledge.text.services.text_check')


def decode_text(raw: bytes) -> str:
    try:
        return raw.decode('utf-8')
    except UnicodeDecodeError as problem:
        raise _m_errors.Text_Error_Bytes_NotUtf8(str(problem)) from problem


def check_text(text: str) -> None:
    if text.startswith('﻿'):
        raise _m_errors.Text_Error_Bytes_Bom('the text starts with a byte-order mark')
    if '�' in text:
        raise _m_errors.Text_Error_Bytes_Replacement('the text holds a replacement character')
    if _m_text_check.mojibake_hints(text):
        raise _m_errors.Text_Error_Bytes_Mojibake('the text holds the marks of mojibake')
    crlf = text.count('\r\n')
    if crlf and text.count('\n') - crlf:
        raise _m_errors.Text_Error_Bytes_MixedEndings('the text mixes CRLF and LF line endings')
    if text and not text.endswith('\n'):
        raise _m_errors.Text_Error_Bytes_NoFinalNewline('the text does not end in a newline')


def check_substance(text: str) -> None:
    if not any(line.strip() and not line.lstrip().startswith('#') for line in text.splitlines()):
        raise _m_structure.Text_Error_Structure_Empty('the text holds only headings and blank lines')
