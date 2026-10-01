// Where the host's own bundle may be, on a platform this run is not.
//
// The check looks for the editor's bundle under environment variables that name a Windows
// install - `LOCALAPPDATA`, `ProgramFiles`, `ProgramFiles(x86)`. A candidate is spelled as
// the parts it is made of and joined, and a part that is not there is not a shorter path:
// `join` throws on one. So on a POSIX machine, where none of the three is set, the check
// threw while building its own candidate list and said nothing at all - which is the worse
// of the two failures available to it, because the one thing it exists to report is that
// the product is not installed there.
//
// The candidates are built when the module is loaded, so the platform is a property of the
// process and this run cannot become a POSIX one: Windows fills `ProgramFiles` back into
// every child it starts, whatever the environment block said. So the candidates are built
// from an environment the caller passes (`hostRootsOf`), and this asks about a POSIX one
// and a Windows one side by side. The Windows half is the half that would go missing: a
// builder that dropped everything would answer the POSIX half and find no product here.
import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import { join } from "node:path";
import test from "node:test";
import { pathToFileURL } from "node:url";
import { EXTENSION } from "./shipped.ts";

const MODULE = join(EXTENSION, "scripts", "host-classification.mjs");

/** The candidates for the environments given, read out of the extension's own module in a
 *  child process. The child is a boundary, not a convenience: the module reads the
 *  environment when it loads, so the only way to ask it about an environment this machine
 *  does not have is to hand that environment to the function it builds them from. */
function candidatesFor(...environments: Record<string, string | undefined>[]): string[][] {
  const script = `
    const { hostRootsOf } = await import(${JSON.stringify(pathToFileURL(MODULE).href)});
    console.log(JSON.stringify(${JSON.stringify(environments)}.map((env) => hostRootsOf(env))));
  `;
  const result = spawnSync(process.execPath, ["--input-type=module", "-e", script], { encoding: "utf8" });
  assert.equal(result.status, 0, `the candidates could not be built:\n${result.stderr ?? ""}`);
  return JSON.parse(result.stdout.trim()) as string[][];
}

test("an environment with no Windows install root yields no candidate, and no throw", () => {
  // A POSIX machine's environment: none of the three roots is set, and nothing names a
  // bundle either. Every candidate is spelled under one of them, so there is none - and the
  // question that must be answered without throwing is the one this check exists for.
  const [posix] = candidatesFor({});
  assert.deepEqual(posix, [], "a candidate spelled under a root that is not there is not a candidate");
});

test("a root that is set still yields its candidates, so the drop above is not a blind one", () => {
  const root = "C:\\Users\\a\\AppData\\Local";
  const [localOnly, both] = candidatesFor(
    { LOCALAPPDATA: root },
    { LOCALAPPDATA: root, ProgramFiles: "C:\\Program Files" },
  );
  assert.deepEqual(
    localOnly,
    [
      join(root, "Programs", "Microsoft VS Code", "resources", "app", "out", "vs", "workbench", "workbench.desktop.main.js"),
      join(root, "Programs", "Microsoft VS Code Insiders", "resources", "app", "out", "vs", "workbench", "workbench.desktop.main.js"),
      join(root, "Programs", "Microsoft VS Code"),
    ],
    "the three candidates under the one root that is set, joined as the path module joins",
  );
  assert.equal(both.length, 5, "the two roots that are set contribute their candidates between them");
  assert.ok(
    both.includes(join("C:\\Program Files", "Microsoft VS Code")),
    "and the second root's own candidate is among them, joined and not dropped",
  );
});

test("a root that is set to nothing names no path, rather than a path relative to the cwd", () => {
  // An empty root is not an absent one, and `join` does not refuse it: it answers the rest
  // of the parts, resolved against whatever directory the run happens to be in. A candidate
  // that read as a path under the cwd is a candidate this check would report having tried.
  const [empty] = candidatesFor({ LOCALAPPDATA: "", ProgramFiles: "C:\\Program Files" });
  assert.deepEqual(
    empty,
    [join("C:\\Program Files", "Microsoft VS Code", "resources", "app", "out", "vs", "workbench", "workbench.desktop.main.js"), join("C:\\Program Files", "Microsoft VS Code")],
    "only the root that names a directory contributes candidates",
  );
});
