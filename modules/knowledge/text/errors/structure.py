#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

class Text_Error_Structure_Malformed(Exception):
    pass


class Text_Error_Structure_NotEncodable(Exception):
    pass


class Text_Error_Structure_Foreign(Exception):
    pass


class Text_Error_Structure_Position(Exception):
    pass


class Text_Error_Structure_Empty(Exception):
    pass


class Text_Error_Place_Changed(Exception):
    pass


class Text_Error_Place_Unavailable(Exception):
    pass


class Text_Error_Place_Refused(Exception):
    pass
