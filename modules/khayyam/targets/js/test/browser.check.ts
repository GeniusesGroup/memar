import assert from "node:assert/strict";
import { closeSync, createReadStream, existsSync, mkdirSync, openSync, readFileSync, statSync, writeFileSync } from "node:fs";
import { createServer } from "node:http";
import { extname, join } from "node:path";
import { spawn } from "node:child_process";
import test from "node:test";
import { fileURLToPath } from "node:url";

import { build } from "../src/cache.ts";
import { compileProgram } from "../src/program.ts";
import { readLinkMap } from "../src/link.ts";
import type { FileSystem } from "../../../core/src/frontend.ts";

/** The repository, served to the browser as it stands: the page is loaded from
 *  the repository root, so every artifact and every linked module is reachable
 *  by the path its URI is written as. */
const ROOT = fileURLToPath(new URL("../../../../../", import.meta.url));
const BUILD_ROOT = "modules/khayyam/targets/js/build";
const DEMO = "modules/khayyam/targets/js/demo/greeting.kh";
const PAGE = "modules/khayyam/targets/js/demo/browser.html";
const PROFILE = `${BUILD_ROOT}/.browser-profile`;

const at = (path: string): string => join(ROOT, ...path.split("/"));

const files: FileSystem = {
  read: (path) => {
    try {
      return readFileSync(at(path), "utf8");
    } catch {
      return undefined;
    }
  },
};

const TYPES: Record<string, string> = {
  ".html": "text/html; charset=utf-8",
  ".js": "text/javascript; charset=utf-8",
  ".json": "application/json; charset=utf-8",
  ".kh": "text/plain; charset=utf-8",
};

/** A browser, if this machine has one. The check the goal asks for is that the
 *  artifact loads, so where no browser is installed the check is skipped and
 *  says so rather than passing on something else. */
function browser(): string | undefined {
  const candidates = [
    "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe",
    "C:\\Program Files\\Microsoft\\Edge\\Application\\msedge.exe",
    "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
    "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe",
  ];
  return candidates.find((path) => existsSync(path));
}

test("the artifact of the program loads in a browser with no bundler, and runs there", async (t) => {
  const executable = browser();
  if (executable === undefined) {
    t.skip("no Edge or Chrome is installed on this machine");
    return;
  }
  const map = readLinkMap(files.read("modules/khayyam/targets/js/link_map.json") ?? "");
  assert.equal(map.ok, true, map.ok ? "" : map.problems.join("; "));
  if (!map.ok) return;
  const compiled = compileProgram({
    root: DEMO,
    files,
    links: map.map,
    buildRoot: BUILD_ROOT,
  });
  assert.equal(compiled.ok, true, compiled.ok ? "" : compiled.problem);
  if (!compiled.ok) return;
  build({ root: DEMO, files, links: map.map, buildRoot: BUILD_ROOT }, {
    cache: { load: () => undefined, save: () => undefined },
    sourceOf: files.read,
    currentText: (path: string) => {
      try {
        return readFileSync(at(path), "utf8");
      } catch {
        return undefined;
      }
    },
    buildRoot: BUILD_ROOT,
    host: "browser",
    linkMap: files.read("modules/khayyam/targets/js/link_map.json") ?? "",
    write: (path: string, text: string) => {
      mkdirSync(at(path).slice(0, at(path).lastIndexOf("\\")), { recursive: true });
      writeFileSync(at(path), text, "utf8");
    },
  });

  const server = createServer((request, response) => {
    const path = (request.url ?? "/").split("?")[0]!.replace(/^\/+/, "");
    const target = at(path === "" ? PAGE : path);
    if (!existsSync(target) || !statSync(target).isFile()) {
      response.writeHead(404).end("not there");
      return;
    }
    response.writeHead(200, { "content-type": TYPES[extname(target)] ?? "text/plain" });
    createReadStream(target).pipe(response);
  });
  const port = 8747;
  await new Promise<void>((resolve) => server.listen(port, "127.0.0.1", resolve));
  const dump = at(`${BUILD_ROOT}/.browser-dom.html`);
  mkdirSync(at(BUILD_ROOT), { recursive: true });
  const dumpFile = openSync(dump, "w");
  const browser_ = spawn(
    executable,
    [
      "--headless=new",
      "--disable-gpu",
      "--no-sandbox",
      `--user-data-dir=${at(PROFILE)}`,
      "--virtual-time-budget=8000",
      "--dump-dom",
      `http://127.0.0.1:${port}/${PAGE}`,
    ],
    // The browser is a windowed program and its output goes to a file, and the
    // browser is waited for without blocking: the server answering it runs in
    // this process, so a blocking wait here would be a deadlock.
    { stdio: ["ignore", dumpFile, "ignore"] },
  );
  try {
    const code = await new Promise<number | null>((resolve, reject) => {
      browser_.on("error", reject);
      browser_.on("close", resolve);
    });
    assert.equal(code, 0);
    const dom = readFileSync(dump, "utf8");
    assert.match(dom, /Hello, Khayyam/);
    assert.doesNotMatch(dom, /running…/);
  } finally {
    try {
      closeSync(dumpFile);
    } catch {
      // already closed
    }
    server.close();
  }
});
