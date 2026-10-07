#!/usr/bin/env python3
"""memar_copy_excluded.py — what a copy of Memar never carries.

Interpreter output, dependency trees and host noise: never part of what a copy
means. A development tree belongs in the checkout that typechecks the extension,
not in a folder the editor loads. Shared by the two things that copy part of a
checkout somewhere else, and by the content tool's walk of the checkout, so that
what is left out is one decision rather than three.
"""
from __future__ import annotations

import shutil

# The patterns are named as well as compiled, because a second thing in this
# folder has to answer the same question and a second copy of the answer is
# how the two would come to disagree.
NEVER_COPIED_PATTERNS = ("__pycache__", "*.pyc", ".DS_Store", "node_modules")
NEVER_COPIED = shutil.ignore_patterns(*NEVER_COPIED_PATTERNS)
