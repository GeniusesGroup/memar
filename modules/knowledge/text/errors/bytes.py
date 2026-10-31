#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

class Text_Error_Bytes_Bom(Exception):
    pass


class Text_Error_Bytes_NotUtf8(Exception):
    pass


class Text_Error_Bytes_Replacement(Exception):
    pass


class Text_Error_Bytes_Mojibake(Exception):
    pass


class Text_Error_Bytes_MixedEndings(Exception):
    pass


class Text_Error_Bytes_NoFinalNewline(Exception):
    pass
