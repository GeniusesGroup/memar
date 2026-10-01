#!/usr/bin/env python3
"""What a copy of Memar never carries.

Interpreter output, dependency trees and host noise: never part of what a copy
means. A development tree belongs in the checkout that typechecks the extension,
not in a folder the editor loads. Shared by the two things that copy part of a
checkout somewhere else, so that what is left out is one decision.
"""
from __future__ import annotations

import shutil

NEVER_COPIED = shutil.ignore_patterns("__pycache__", "*.pyc", ".DS_Store", "node_modules")
