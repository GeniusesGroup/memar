#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

import os
import re
import subprocess
import sys
import concurrent.futures
import time
from pathlib import Path

TOP = Path(__file__).resolve().parents[4]
ROOTS = ('modules', 'modules-plugable', 'bundles')
LIMIT_SECONDS = 150
WORKERS = 6
FILE_BUDGET_SECONDS = 10
SEARCH = (TOP, TOP / 'bundles' / 'memar', TOP / 'bundles' / 'memar' / 'services')
SYSTEM = re.compile(r"^TIER = 'system'$", re.MULTILINE)
RAN = re.compile(r'Ran (\d+) tests?')


def discover(filters, with_system):
    found = []
    skipped = []
    for root in ROOTS:
        for path in sorted((TOP / root).rglob('tests/*.py')):
            if path.name == '__init__.py' or path.name.startswith('_') or path == Path(__file__).resolve():
                continue
            rel = path.relative_to(TOP).as_posix()
            if [f for f in filters if f != '--serial'] and not any(f in rel for f in filters if f != '--serial'):
                continue
            if SYSTEM.search(path.read_text(encoding='utf-8', errors='replace')) and not (with_system):
                skipped.append(rel)
                continue
            found.append(path)
    return found, skipped


def run_one(path, limit):
    env = dict(os.environ, PYTHONPATH=os.pathsep.join(str(p) for p in SEARCH))
    started = time.perf_counter()
    try:
        proc = subprocess.run([sys.executable, str(path)], cwd=TOP, capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=limit, env=env)
    except subprocess.TimeoutExpired:
        return time.perf_counter() - started, '?', 'TIMEOUT'
    seconds = time.perf_counter() - started
    match = RAN.search(proc.stderr + proc.stdout)
    count = match.group(1) if match else '?'
    return seconds, count, 'ok' if proc.returncode == 0 else 'FAIL'


def main(argv):
    limit = LIMIT_SECONDS
    filters = []
    args = iter(argv)
    for arg in args:
        if arg == '--limit':
            limit = int(next(args))
        elif arg in ('--serial', '--system'):
            filters.append(arg)
        else:
            filters.append(arg)
    workers = WORKERS
    with_system = '--system' in filters
    filters = [f for f in filters if f != '--system']
    paths, skipped = discover(filters, with_system)
    if '--serial' in filters:
        workers = 1
    wall = time.perf_counter()
    rows = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as pool:
        futures = {pool.submit(run_one, path, limit): path for path in paths}
        for done in concurrent.futures.as_completed(futures):
            seconds, count, verdict = done.result()
            rel = futures[done].relative_to(TOP).as_posix()
            rows.append((seconds, count, verdict, rel))
            print(f'{seconds:8.1f}s  {count:>4} tests  {verdict:7}  {rel}', flush=True)
    wall = time.perf_counter() - wall
    rows.sort(reverse=True)
    total = sum(r[0] for r in rows)
    print('--- slowest first ---')
    for seconds, count, verdict, rel in rows:
        over = '  OVER' if seconds > FILE_BUDGET_SECONDS else ''
        print(f'{seconds:8.1f}s  {count:>4}  {verdict:7}  {rel}{over}')
    for rel in skipped:
        print(f'    system tier, not run (use --system): {rel}')
    print(f'files={len(rows)} wall={wall:.1f}s total={total:.1f}s over_budget={sum(1 for r in rows if r[0] > FILE_BUDGET_SECONDS)}')
    return 1 if any(r[2] != 'ok' for r in rows) else 0


if __name__ == '__main__':
    raise SystemExit(main(sys.argv[1:]))
