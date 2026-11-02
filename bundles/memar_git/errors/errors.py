#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations

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

class GitFailed(Error):
    pass

class ServerUnreachable(Error):
    pass

class Locked(Error):
    pass
