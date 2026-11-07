#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from importlib import import_module
_m_store_errors = import_module('modules.computer.memory.store.errors.errors')
_StoreRaised = _m_store_errors.Raised
_StoreRefusal = _m_store_errors.Refusal
_StoreUnavailability = _m_store_errors.Unavailability

class Error(Exception):
    def __init__(self, detail: str = '') -> None:
        super().__init__(detail)
        self.detail = detail

class Refusal(Error):
    pass

class NotNamed(Refusal):
    pass

class GitNotInstalled(Refusal):
    pass

class NotARepository(Refusal):
    pass

class PathAbsent(Refusal):
    pass

class NothingToCommit(Refusal):
    pass

class FoldMisused(Refusal):
    pass

class MergeInFold(Refusal):
    pass

class PublishedHistory(Refusal):
    pass

class EmptyMessage(Refusal):
    pass

class ReplacementMalformed(Refusal):
    pass

class MoveWouldNotBeRename(Refusal):
    pass

class TaskNotCited(Refusal):
    pass

class TaskUnknown(Refusal):
    pass

class TaskByHand(Refusal):
    pass

class NotConfirmed(Refusal):
    pass

class NotHead(Refusal):
    pass

class NotOneParent(Refusal):
    pass

class ReindexHeadMoved(Refusal):
    pass

class IndexChanged(Refusal):
    pass

class StagedByOthers(Refusal):
    pass

class NotAFolder(Refusal):
    pass

class PatternMalformed(Refusal):
    pass

class NoMatch(Refusal):
    pass

class GitFailed(Error):
    pass

class ServerUnreachable(Error):
    pass

class Locked(Error):
    pass

class MoveFailed(Error):
    pass

class BadReference(_StoreRaised):

    def __init__(self, detail: str='') -> None:
        super().__init__(_StoreRefusal.MALFORMED, detail)

    def summary(self) -> str:
        return 'A reference the adapter may not keep a store in'

class ReferenceCollision(_StoreRaised):

    def __init__(self, detail: str='') -> None:
        super().__init__(_StoreRefusal.MALFORMED, detail)

    def summary(self) -> str:
        return 'The reference of a class is a folder of the reference of another'

class NotInRepository(Exception):

    def __init__(self, detail: str='') -> None:
        super().__init__(detail)
        self.detail = detail

    def summary(self) -> str:
        return 'The project is not in a git repository'

class BadParameter(Exception):

    def __init__(self, detail: str='') -> None:
        super().__init__(detail)
        self.detail = detail

    def summary(self) -> str:
        return 'A key of the adapter is not class equals value pairs separated by commas, each class once, or holds a value it does not know'

class Lost(_StoreRaised):

    def __init__(self, detail: str='') -> None:
        super().__init__(_StoreUnavailability.FAILED, detail)

    def summary(self) -> str:
        return 'A long lived git process ended or answered what cannot be used'

class NotFastForward(Exception):

    def __init__(self, detail: str='') -> None:
        super().__init__(detail)
        self.detail = detail

    def summary(self) -> str:
        return 'The shared store refused a push because another writer published to the same reference first'
