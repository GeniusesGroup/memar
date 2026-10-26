/* For license and copyright information please see the LEGAL file in the code repository */

// The check service: runs the core front end (`core/src/frontend.ts` analyze) over named
// Khayyam files and says, per file, accept or refuse with the reason and line. It decides
// nothing about the language; every verdict is the front end's own.
//
// Nothing is implicit. The corpus is the folder `root` names, a file is a path inside it,
// and a file that is not yet in the corpus is handed as a draft that stands at the
// repository path it proposes, for the file itself and for any `in` that names it.

import { existsSync, readFileSync } from "node:fs";
import { join } from "node:path";

import { analyze, type FileSystem } from "../../core/src/frontend.ts";

export interface CheckRequest {
  /** The folder repository paths resolve against. */
  readonly root: string;
  /** Repository paths, in the order they are reported. */
  readonly files: readonly string[];
  /** Repository path -> the local file that stands at it. */
  readonly drafts: ReadonlyMap<string, string>;
}

export interface CheckResult {
  readonly lines: string[];
  readonly refused: number;
}

export type Parsed<T> = { ok: true; value: T } | { ok: false; message: string };

export function parseCheckArguments(argv: readonly string[]): Parsed<CheckRequest> {
  let root: string | undefined;
  const files: string[] = [];
  const drafts = new Map<string, string>();
  for (let i = 0; i < argv.length; i++) {
    const argument = argv[i]!;
    if (argument === "--root") {
      root = argv[++i];
      if (root === undefined) return { ok: false, message: "--root needs the folder repository paths resolve against" };
    } else if (argument === "--draft") {
      const pair = argv[++i] ?? "";
      const cut = pair.indexOf("=");
      if (cut < 1 || cut === pair.length - 1) return { ok: false, message: "--draft needs REPO_PATH=LOCAL_FILE" };
      drafts.set(pair.slice(0, cut), pair.slice(cut + 1));
    } else if (argument.startsWith("--")) {
      return { ok: false, message: `unknown option ${argument}` };
    } else files.push(argument);
  }
  if (root === undefined) return { ok: false, message: "--root is required: the folder repository paths resolve against" };
  if (files.length === 0) return { ok: false, message: "name at least one .kh file (a path inside --root)" };
  return { ok: true, value: { root, files, drafts } };
}

export function checkFiles(request: CheckRequest): CheckResult {
  const locate = (path: string): string => request.drafts.get(path) ?? join(request.root, path);
  const fileSystem: FileSystem = {
    read(path) {
      const local = locate(path);
      return existsSync(local) ? readFileSync(local, "utf8") : undefined;
    },
  };
  const lines: string[] = [];
  let refused = 0;
  for (const path of request.files) {
    const source = fileSystem.read(path);
    if (source === undefined) {
      refused++;
      lines.push(`refuse  ${path}  file not found`);
      continue;
    }
    const result = analyze(path, source, fileSystem);
    if (result.outcome === "accept") lines.push(`accept  ${path}`);
    else {
      refused++;
      lines.push(`refuse  ${path}  ${result.reason}${result.line ? ` line ${result.line}` : ""}`);
    }
  }
  return { lines, refused };
}
