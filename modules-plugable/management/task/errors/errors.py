#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

class Task_Error_Changed(Exception):
    pass


class Task_Error_NotFound(Exception):
    pass


class Task_Error_NotActive(Exception):
    pass


class Task_Error_PriorityRefused(Exception):
    pass


class Task_Error_WrittenByPredecessor(Exception):

    def __init__(self, writer: str, successor: str, conversion: str) -> None:
        super().__init__(writer, successor, conversion)
        self.writer = writer
        self.successor = successor
        self.conversion = conversion


class Task_Error_NotConvertible(Exception):

    def __init__(self, reason: str) -> None:
        super().__init__(reason)
        self.reason = reason
