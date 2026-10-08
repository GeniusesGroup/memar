// Runs the Khayyam frontend (M1, core/src/frontend.ts) over a list of files for
// abstraction_bridge.py transfer. Usage: node frontend_check.ts REQUEST.json
// REQUEST is {"root": repository root, "paths": [repository-relative .kh],
// "overrides": {path: text}}; an override stands in for the file on disk, so a
// transfer is checked before anything is written. Prints {path: outcome} as JSON.
import { readFileSync } from "node:fs";
import { join } from "node:path";

import { analyze, type FileSystem } from "../../core/src/frontend.ts";

interface Request {
  root: string;
  paths: string[];
  overrides: Record<string, string>;
}

const request = JSON.parse(readFileSync(process.argv[2]!, "utf8")) as Request;

const fileSystem: FileSystem = {
  read: (path) => {
    if (Object.hasOwn(request.overrides, path)) return request.overrides[path];
    try {
      return readFileSync(join(request.root, path), "utf8");
    } catch {
      return undefined;
    }
  },
};

const outcomes: Record<string, { outcome: string; reason?: string; line?: number }> = {};
for (const path of request.paths) {
  const source = fileSystem.read(path);
  if (source === undefined) {
    outcomes[path] = { outcome: "missing" };
    continue;
  }
  const result = analyze(path, source, fileSystem);
  outcomes[path] =
    result.outcome === "accept"
      ? { outcome: "accept" }
      : { outcome: "refuse", reason: result.reason, line: result.line };
}
process.stdout.write(JSON.stringify(outcomes));
