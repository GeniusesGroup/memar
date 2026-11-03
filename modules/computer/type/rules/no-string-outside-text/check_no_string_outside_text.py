#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
import re
import sys
from pathlib import Path

ALLOWED = ('modules/knowledge/text/', 'modules/computer/codec/')
SKIPPED = {'node_modules', '__pycache__', 'temp'}
USE = re.compile(r'\bString\b')
IMPORT = re.compile(r'^\s*tp\s+String\s+in\s+')

def violations(root: Path, only: list[Path] | None = None) -> list[str]:
    found: list[str] = []
    files = only if only else sorted(root.rglob('*.kh'))
    for path in files:
        relative = path.relative_to(root).as_posix()
        if any(part in SKIPPED or part.startswith('.') for part in path.relative_to(root).parts) or relative.endswith('.eng.kh') or relative.startswith(ALLOWED):
            continue
        inside = False
        for number, line in enumerate(path.read_text(encoding='utf-8').splitlines(), 1):
            if inside:
                inside = '*/' not in line
                continue
            code = line.split('//', 1)[0]
            if '/*' in code:
                inside = '*/' not in code
                code = code.split('/*', 1)[0]
            if USE.search(code) and not IMPORT.match(code):
                found.append(f'{relative}:{number}: {line.strip()}')
    return found

if __name__ == '__main__':
    base = Path(sys.argv[1]).resolve()
    scope = [Path(item).resolve() for item in sys.argv[2:]]
    problems = violations(base, scope)
    print('\n'.join(problems))
    print(f'{len(problems)} declarations of String outside the text domain')
    sys.exit(1 if problems else 0)
