"""The Khayyam frontend's verdict on a set of files.

`overrides` stand in for files that are not on disk yet, so a caller can ask what
the frontend would say of a result before it is written. Every tool that writes
Khayyam goes through this one call."""

import json
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Sequence

from failures import BridgeFailure


FRONTEND_CHECK = Path(__file__).with_name("frontend_check.ts")


def frontend_outcomes(memar_root: Path, paths: Sequence[str], overrides: dict[str, str]) -> dict[str, dict]:
    """The Khayyam frontend's outcome for each of `paths`; `overrides` stand in for files on disk."""
    if not paths:
        return {}
    node = shutil.which("node")
    if node is None:
        raise BridgeFailure(["node is not on PATH; run with --no-frontend to skip the Khayyam frontend"])
    with tempfile.TemporaryDirectory() as directory:
        request = Path(directory) / "request.json"
        request.write_text(
            json.dumps({"root": str(memar_root), "paths": list(paths), "overrides": overrides}),
            encoding="utf-8",
        )
        completed = subprocess.run(
            [node, str(FRONTEND_CHECK), str(request)],
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
    if completed.returncode != 0:
        raise BridgeFailure([f"frontend check failed: {completed.stderr.strip()[:400]}"])
    return json.loads(completed.stdout)
