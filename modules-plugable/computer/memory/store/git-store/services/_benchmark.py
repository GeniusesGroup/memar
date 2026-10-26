#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""The benchmark of `git-store`: what writing nodes through it costs on one machine, and what a push and a fetch send.

Its procedure and the numbers it measured are [Memory Git Store Benchmark](../git-store.benchmark.md); the baseline it is
compared with is task `20261020-T131910Z-22300`'s `bench_baseline.py`. Windows only: each measured run is a worker
process inside a Job Object, so its numbers count the worker and every git process it starts (wall time, CPU time,
processes started, write operations), the way the baseline counts a command. Defender's CPU (MsMpEng) is read before and
after each case, which only an elevated run can; unelevated it is `null`. It changes no setting; its only writes are
scratch repositories under `--where` and the JSON lines it appends to `--out`.

    python _benchmark.py like-for-like --where DIR --label L [--repeat 5] [--files 200] --out FILE
    python _benchmark.py nodes --where DIR --label L [--nodes 100000] [--batch 200] [--points 1000,100000] --out FILE
    python _benchmark.py single --where DIR --label L [--batches 10000] [--sample 100] --out FILE

`like-for-like` is the baseline's shape: 200 small nodes created in one batch, then the same 200 edited in one batch,
each in a fresh repository, the median of `--repeat`. `nodes` writes `--nodes` nodes in batches of `--batch`, stopping at
each of `--points` to measure the bytes a push and a fetch send, for the store as it is (a commit per batch) and for a
reference pointing at the bare tree of the same state; then it writes one batch of one node and measures again. `single`
writes `--batches` batches of one write each and samples the number of packs, so the bound `repack` keeps is seen.
Put `--where` on the path whose scanner condition is measured: inside a folder Defender excludes, and outside it.
"""
from __future__ import annotations
import argparse
import datetime
import json
import os
import statistics
import subprocess
import sys
import time
from pathlib import Path
HERE = Path(__file__).resolve()
TOP = next((p for p in HERE.parents if (p / 'modules-plugable').is_dir() and (p / 'bundles').is_dir()))
REFERENCE = 'refs/memory/notes'
BARE_REFERENCE = 'refs/memory-bare/notes'
SPACING_MS = 300000
BASE_MS = 1735689600000

def now() -> str:
    return datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='milliseconds')

def node_key(i: int) -> bytes:
    """The key of the `body` part of the I-th node: a UUID version 7 whose instant is five minutes after the last one's."""
    ms = BASE_MS + i * SPACING_MS
    tail = (2 << 62) | i
    at = ms.to_bytes(6, 'big') + (0x7000).to_bytes(2, 'big') + tail.to_bytes(8, 'big')
    return at + b'body'

def node_value(i: int, edited: bool) -> bytes:
    """The baseline's small file, as the bytes of a node's part."""
    return f'# file {i}\n\nsmall record {i}\n{"edit" + chr(10) if edited else ""}'.encode('utf-8')

def _job_api():
    import ctypes
    from ctypes import wintypes
    k32 = ctypes.WinDLL('kernel32', use_last_error=True)
    k32.CreateJobObjectW.restype = wintypes.HANDLE
    k32.AssignProcessToJobObject.argtypes = [wintypes.HANDLE, wintypes.HANDLE]
    k32.QueryInformationJobObject.argtypes = [wintypes.HANDLE, ctypes.c_int, ctypes.c_void_p, wintypes.DWORD, ctypes.c_void_p]
    k32.CloseHandle.argtypes = [wintypes.HANDLE]

    class BasicAndIo(ctypes.Structure):
        _fields_ = [('TotalUserTime', ctypes.c_int64), ('TotalKernelTime', ctypes.c_int64), ('ThisPeriodTotalUserTime', ctypes.c_int64), ('ThisPeriodTotalKernelTime', ctypes.c_int64), ('TotalPageFaultCount', wintypes.DWORD), ('TotalProcesses', wintypes.DWORD), ('ActiveProcesses', wintypes.DWORD), ('TotalTerminatedProcesses', wintypes.DWORD), ('ReadOperationCount', ctypes.c_uint64), ('WriteOperationCount', ctypes.c_uint64), ('OtherOperationCount', ctypes.c_uint64), ('ReadTransferCount', ctypes.c_uint64), ('WriteTransferCount', ctypes.c_uint64), ('OtherTransferCount', ctypes.c_uint64)]
    return (ctypes, k32, BasicAndIo)

def run_job(args: list[str]) -> dict:
    """Run ARGS to its end inside a job: wall and CPU seconds, processes, write operations and bytes, and what it printed last."""
    ctypes, k32, BasicAndIo = _job_api()
    job = k32.CreateJobObjectW(None, None)
    start = time.perf_counter()
    process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.DEVNULL)
    k32.AssignProcessToJobObject(job, int(process._handle))
    out, err = process.communicate()
    wall = time.perf_counter() - start
    info = BasicAndIo()
    k32.QueryInformationJobObject(job, 8, ctypes.byref(info), ctypes.sizeof(info), None)
    k32.CloseHandle(job)
    lines = out.decode('utf-8', 'replace').strip().splitlines()
    try:
        reported = json.loads(lines[-1]) if lines else {}
    except ValueError:
        reported = {}
    return {'wall_s': round(wall, 3), 'cpu_s': round((info.TotalUserTime + info.TotalKernelTime) / 10000000.0, 3), 'processes': info.TotalProcesses, 'write_ops': info.WriteOperationCount, 'write_bytes': info.WriteTransferCount, 'exit': process.returncode, 'worker': reported, 'stderr': err.decode('utf-8', 'replace')[-2000:]}

def defender_cpu() -> float | None:
    """MsMpEng's CPU seconds so far, readable only elevated; else None."""
    done = subprocess.run(['powershell', '-NoProfile', '-Command', '(Get-Process MsMpEng -ErrorAction Stop).TotalProcessorTime.TotalSeconds'], capture_output=True, text=True)
    try:
        return float(done.stdout.strip())
    except ValueError:
        return None

def git(*args: str, cwd: Path | None=None) -> str:
    return subprocess.run(['git', *args], cwd=cwd, check=True, capture_output=True, text=True, stdin=subprocess.DEVNULL).stdout

def fresh_repository(where: Path, name: str) -> tuple[Path, Path]:
    """A new repository with one commit in its working tree, and an empty data area beside it."""
    repository, data = (where / name, where / f'{name}-data')
    repository.mkdir(parents=True)
    data.mkdir()
    git('init', '-q', str(repository))
    (repository / 'tracked.txt').write_bytes(b'tracked\n')
    git('-C', str(repository), 'add', 'tracked.txt')
    git('-C', str(repository), '-c', 'user.name=bench', '-c', 'user.email=bench@example.invalid', 'commit', '-q', '-m', 'scratch')
    return (repository, data)

def files_under(*folders: Path) -> dict[str, int]:
    found: dict[str, int] = {}
    for folder in folders:
        for root, _, names in os.walk(folder):
            for name in names:
                path = os.path.join(root, name)
                try:
                    found[path] = os.path.getsize(path)
                except OSError:
                    pass
    return found

def packs(repository: Path) -> int:
    return sum((1 for each in (repository / '.git' / 'objects' / 'pack').glob('*.pack')))

def worker_args(repository: Path, data: Path, start: int, count: int, batch: int, edited: bool, sample: int=0, progress: Path | None=None) -> list[str]:
    args = [sys.executable, str(HERE), 'worker', '--repository', str(repository), '--data', str(data), '--start', str(start), '--count', str(count), '--batch', str(batch)]
    if edited:
        args.append('--edited')
    if sample and progress is not None:
        args += ['--sample', str(sample), '--progress', str(progress)]
    return args

def measured_write(repository: Path, data: Path, start: int, count: int, batch: int, edited: bool, sample: int=0, progress: Path | None=None) -> dict:
    """A worker's write measured in a job, with the files it left created and removed in the repository and data area."""
    before = files_under(repository / '.git', data)
    result = run_job(worker_args(repository, data, start, count, batch, edited, sample, progress))
    after = files_under(repository / '.git', data)
    result['files_created'] = len(set(after) - set(before))
    result['files_removed'] = len(set(before) - set(after))
    result['packs'] = packs(repository)
    return result

def worker(o: argparse.Namespace) -> int:
    """Write nodes START..START+COUNT-1 in batches of BATCH through `record` over `git-store`; print one JSON line."""
    for each in (TOP / 'bundles' / 'memar' / 'services', TOP):
        if str(each) not in sys.path:
            sys.path.insert(0, str(each))
    from importlib import import_module
    git_store = import_module('modules-plugable.computer.memory.store.git-store.git-store')
    record = import_module('modules-plugable.computer.memory.store.record.record')
    committed = import_module('modules.computer.memory.store.protocol.store').Committed()
    started = time.perf_counter()
    adapter = git_store.GitStoreAdapter(o.repository, REFERENCE, data_area=o.data)
    store = record.RecordAdapter(adapter).open()
    most_packs, done = (0, 0)
    progress = open(o.progress, 'a', encoding='utf-8') if o.progress else None
    try:
        for first in range(o.start, o.start + o.count, o.batch):
            last = min(first + o.batch, o.start + o.count)
            answer = store.batch([], [(node_key(i), node_value(i, o.edited)) for i in range(first, last)])
            if answer != committed:
                print(json.dumps({'error': repr(answer), 'at': first}))
                return 1
            done += 1
            if o.sample and done % o.sample == 0:
                count = packs(Path(o.repository))
                most_packs = max(most_packs, count)
                progress.write(json.dumps({'batches': done, 'elapsed_s': round(time.perf_counter() - started, 3), 'packs': count}) + '\n')
                progress.flush()
        stats = store.stats()
    finally:
        adapter.close()
        if progress:
            progress.close()
    print(json.dumps({'batches': done, 'elapsed_s': round(time.perf_counter() - started, 3), 'processes_started': stats.processes_started, 'files_opened': stats.files_opened, 'most_packs_sampled': most_packs}))
    return 0

def _wire(command: str, record_to: Path) -> str:
    """A `--receive-pack` or `--upload-pack` value that runs COMMAND and keeps a copy of what the client sends it
    (receive-pack) or what it sends the client (upload-pack) in RECORD_TO, so the file's size is the bytes on the wire."""
    target = record_to.as_posix()
    if command == 'git-receive-pack':
        return f'f() {{ tee "{target}" | git-receive-pack "$@"; }}; f'
    return f'f() {{ git-upload-pack "$@" | tee "{target}"; }}; f'

def push_bytes(repository: Path, shared: Path, source: str, target: str, record_to: Path) -> tuple[int, str]:
    """The bytes a push sends, and why an unforced push was refused, when it was: then the push is forced and measured."""
    try:
        git('-C', str(repository), 'push', '-q', f'--receive-pack={_wire("git-receive-pack", record_to)}', str(shared), f'{source}:{target}')
        return (record_to.stat().st_size, '')
    except subprocess.CalledProcessError as refused:
        why = ' '.join((line.strip() for line in (refused.stderr or '').splitlines() if 'rejected' in line or 'non-commit' in line))
    git('-C', str(repository), 'push', '-q', f'--receive-pack={_wire("git-receive-pack", record_to)}', str(shared), f'+{source}:{target}')
    return (record_to.stat().st_size, why)

def fetch_bytes(fetcher: Path, shared: Path, reference: str, record_to: Path) -> int:
    git('-C', str(fetcher), 'fetch', '-q', f'--upload-pack={_wire("git-upload-pack", record_to)}', str(shared), f'+{reference}:{reference}')
    return record_to.stat().st_size

def transfers(repository: Path, where: Path, point: int, stage: str, ends: dict) -> dict:
    """The bytes a push sends to a shared store and a fetch receives from it, for the commit chain and for the bare tree.

    Stage `full`: fresh shared stores and fetchers, the whole store sent. Stage `one-more`: the same stores, after one
    more batch, so only what the new batch adds should travel."""
    git_dir = repository / '.git'
    tip = git('--git-dir', str(git_dir), 'rev-parse', REFERENCE).strip()
    tree = git('--git-dir', str(git_dir), 'rev-parse', f'{tip}^{{tree}}').strip()
    git('--git-dir', str(git_dir), 'update-ref', BARE_REFERENCE, tree)
    found = {}
    for variant, reference in (('commit', REFERENCE), ('bare-tree', BARE_REFERENCE)):
        # Short names: a shared store's incoming objects lie deep inside it, and Windows refuses a path past 260 characters.
        shared, fetcher = (where / f's-{variant[0]}-{point}.git', where / f'f-{variant[0]}-{point}.git')
        if stage == 'full':
            for each in (shared, fetcher):
                git('init', '-q', '--bare', str(each))
        wire = where / f'w-{variant[0]}-{point}-{stage}'
        sent, refused = push_bytes(repository, shared, reference, reference, wire.with_suffix('.push'))
        found[variant] = {'push_bytes': sent, 'fetch_bytes': fetch_bytes(fetcher, shared, reference, wire.with_suffix('.fetch')), 'unforced_push_refused': refused}
    return found

def write_line(out: Path, line: dict) -> None:
    with open(out, 'a', encoding='utf-8', newline='\n') as handle:
        handle.write(json.dumps(line) + '\n')

def like_for_like(o: argparse.Namespace) -> None:
    runs: dict[str, list[dict]] = {'create': [], 'edit': []}
    av: dict[str, list[float | None]] = {'create': [], 'edit': []}
    for n in range(o.repeat):
        repository, data = fresh_repository(Path(o.where), f'like-{os.getpid()}-{n}')
        for case, edited in (('create', False), ('edit', True)):
            before = defender_cpu()
            runs[case].append(measured_write(repository, data, 0, o.files, o.files, edited))
            after = defender_cpu()
            av[case].append(None if before is None or after is None else round(after - before, 3))
    for case, measured in runs.items():
        median = {key: statistics.median((each[key] for each in measured)) for key in ('wall_s', 'cpu_s', 'processes', 'write_ops', 'files_created')}
        median['in_process_s'] = statistics.median((each['worker'].get('elapsed_s', 0) for each in measured))
        defender = None if None in av[case] else statistics.median(av[case])
        write_line(Path(o.out), {'label': o.label, 'case': f'git-store {case} {o.files} nodes, one batch', 'where': o.where, 'median': median, 'defender_cpu_s_per_run': defender, 'runs': measured, 'at': now()})
        print(f"{o.label:24} {case:7} wall {median['wall_s']:.3f} cpu {median['cpu_s']:.3f} in-process {median['in_process_s']:.3f} procs {median['processes']:.0f} writes {median['write_ops']:.0f} files {median['files_created']:.0f} defender {defender}")

def nodes(o: argparse.Namespace) -> None:
    repository, data = fresh_repository(Path(o.where), f'nodes-{os.getpid()}')
    progress = Path(o.out).with_name(f'{Path(o.out).stem}-{o.label}-progress.jsonl')
    written, extra = (0, 0)
    for point in sorted((int(each) for each in o.points.split(','))):
        before = defender_cpu()
        segment = measured_write(repository, data, written + extra, point - written - extra, o.batch, False, sample=10, progress=progress)
        after = defender_cpu()
        written = point
        segment['defender_cpu_s'] = None if before is None or after is None else round(after - before, 3)
        full = transfers(repository, Path(o.where), point, 'full', {})
        more = measured_write(repository, data, written + extra, 1, 1, False)
        extra += 1
        one_more = transfers(repository, Path(o.where), point, 'one-more', {})
        counted = git('--git-dir', str(repository / '.git'), 'count-objects', '-v')
        write_line(Path(o.out), {'label': o.label, 'case': f'git-store {point} nodes in batches of {o.batch}', 'where': o.where, 'segment': segment, 'transfers_full': full, 'one_more_batch': more, 'transfers_one_more': one_more, 'count_objects': counted, 'at': now()})
        print(f"{o.label} {point}: segment wall {segment['wall_s']} cpu {segment['cpu_s']} procs {segment['processes']} writes {segment['write_ops']} files+ {segment['files_created']} packs {segment['packs']}; full {full}; one more {one_more}", flush=True)

def single(o: argparse.Namespace) -> None:
    repository, data = fresh_repository(Path(o.where), f'single-{os.getpid()}')
    progress = Path(o.out).with_name(f'{Path(o.out).stem}-{o.label}-progress.jsonl')
    result = measured_write(repository, data, 0, o.batches, 1, False, sample=o.sample, progress=progress)
    counted = git('--git-dir', str(repository / '.git'), 'count-objects', '-v')
    write_line(Path(o.out), {'label': o.label, 'case': f'git-store {o.batches} single-write batches', 'where': o.where, 'result': result, 'count_objects': counted, 'at': now()})
    print(f"{o.label}: wall {result['wall_s']} cpu {result['cpu_s']} procs {result['processes']} writes {result['write_ops']} packs at end {result['packs']} most sampled {result['worker'].get('most_packs_sampled')}", flush=True)

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    verbs = parser.add_subparsers(dest='verb', required=True)
    for name in ('like-for-like', 'nodes', 'single'):
        each = verbs.add_parser(name)
        each.add_argument('--where', required=True, help='folder the scratch repositories are made in')
        each.add_argument('--label', required=True)
        each.add_argument('--out', required=True, help='JSON lines file the results are appended to')
    verbs.choices['like-for-like'].add_argument('--repeat', type=int, default=5)
    verbs.choices['like-for-like'].add_argument('--files', type=int, default=200)
    verbs.choices['nodes'].add_argument('--nodes', type=int, default=100000)
    verbs.choices['nodes'].add_argument('--batch', type=int, default=200)
    verbs.choices['nodes'].add_argument('--points', default='1000,100000')
    verbs.choices['single'].add_argument('--batches', type=int, default=10000)
    verbs.choices['single'].add_argument('--sample', type=int, default=100)
    work = verbs.add_parser('worker')
    for name in ('--repository', '--data'):
        work.add_argument(name, required=True)
    for name in ('--start', '--count', '--batch'):
        work.add_argument(name, type=int, required=True)
    work.add_argument('--edited', action='store_true')
    work.add_argument('--sample', type=int, default=0)
    work.add_argument('--progress', default=None)
    o = parser.parse_args()
    if o.verb == 'worker':
        return worker(o)
    Path(o.where).mkdir(parents=True, exist_ok=True)
    {'like-for-like': like_for_like, 'nodes': nodes, 'single': single}[o.verb](o)
    return 0
if __name__ == '__main__':
    raise SystemExit(main())
