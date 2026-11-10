#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations

class ReleaseRefused(Exception):
    pass

class NoBuilder(ReleaseRefused):
    pass

class BuildFailed(ReleaseRefused):
    pass

class DoesNotStart(ReleaseRefused):
    pass

class NoneInstalled(ReleaseRefused):
    pass
