#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations


class Text_Error_Edit_Error(Exception):
    pass


class Text_Error_Edit_Refusal(Text_Error_Edit_Error):
    pass


class Text_Error_Edit_OldEmpty(Text_Error_Edit_Refusal):
    pass


class Text_Error_Edit_MatchAbsent(Text_Error_Edit_Refusal):
    pass


class Text_Error_Edit_MatchAmbiguous(Text_Error_Edit_Refusal):
    pass


class Text_Error_Edit_EmptyText(Text_Error_Edit_Refusal):
    pass


class Text_Error_Edit_CreateNotAsked(Text_Error_Edit_Refusal):
    pass


class Text_Error_Edit_TextAbsent(Text_Error_Edit_Refusal):
    pass


class Text_Error_Edit_NotUtf8(Text_Error_Edit_Refusal):
    pass


class Text_Error_Edit_ReadFailed(Text_Error_Edit_Error):
    pass


class Text_Error_Edit_WriteFailed(Text_Error_Edit_Error):
    pass


class Text_Error_Edit_Locked(Text_Error_Edit_Error):
    pass


class Text_Error_Edit_LockUnwritable(Text_Error_Edit_Error):
    pass


class Text_Error_Edit_ChangedWhileWaiting(Text_Error_Edit_Error):
    pass


class Text_Error_Edit_NamedTextNotUtf8(Text_Error_Edit_Error):
    pass
