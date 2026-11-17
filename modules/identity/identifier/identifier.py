# For license and copyright information please see the LEGAL file in the code repository

from .errors.value import Identifier_Error_InvalidBytes


def complete_bytes(value):
    if type(value) is not bytes or len(value) != 16:
        raise Identifier_Error_InvalidBytes()
    return value
