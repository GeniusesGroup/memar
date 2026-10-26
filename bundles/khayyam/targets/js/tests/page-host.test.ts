/* For license and copyright information please see the LEGAL file in the code repository */

// The page's host glue (target.md → Compiling in a browser): it compiles the units
// it is handed, and loads each emitted unit after the units it imports, from a URL
// the host makes for the text. A browser makes a Blob URL; this test makes a
// `data:` URL, which a relative specifier cannot be resolved against either, so
// what passes here is the replacement of every specifier the program records.

import assert from "node:assert/strict";
import test from "node:test";

import { compileProgram, emitUnit } from "../src/program.ts";
import { readLinkMap, type LinkMap } from "../src/link.ts";
import { run } from "../src/run.ts";
import { compileUnits, loaderOf } from "../demo/page-host.ts";

const compiler = { compileProgram, emitUnit, readLinkMap };
const urlOf = (text: string): string => `data:text/javascript,${encodeURIComponent(text)}`;

const LIBRARY = "x/lib/text.kh";
const ROOT = "x/demo/greet.kh";

const units = [
  {
    uri: ROOT,
    source: [
      `tp Text in "${LIBRARY}"`,
      "",
      "tp Greeter cp {",
      "}",
      "",
      "tp Greet mt (self Greeter) (greeting Text) () {",
      "    greeting.Print()()",
      "}",
      "",
    ].join("\n"),
  },
  {
    uri: LIBRARY,
    source: ["tp Text cp {", "    text Text", "}", "", "tp Print mt (self Text) () ()", ""].join("\n"),
  },
];

test("a unit that imports another loads after it, from the URL its host made, and runs", async () => {
  const compiled = compileUnits({ compiler, units, linkMap: "{}", buildRoot: "build" });
  assert.equal(compiled.ok, true, compiled.ok ? "" : compiled.problem);
  if (!compiled.ok) return;
  assert.ok(
    compiled.program.units.find((unit) => unit.uri === ROOT)!.imports.some((entry) => entry.from === LIBRARY),
    "the root's artifact imports nothing from the library, so this test checks nothing",
  );
  const load = loaderOf({ program: compiled.program, texts: compiled.texts, urlOf });
  const { Text } = (await load(LIBRARY)) as { Text: new (values: Record<string, unknown>) => unknown };
  const said: string[] = [];
  await run(
    {
      uri: ROOT,
      units: [LIBRARY, ROOT],
      method: "Greet",
      owner: { type: "Greeter" },
      influencing: [new Text({ text: "from the library" })],
      supplied: {
        [LIBRARY]: { "Text$Print": (self: unknown) => void said.push((self as { text: { value: string } }).text.value) },
      },
    },
    load,
  );
  assert.deepEqual(said, ["from the library"]);
});

test("a unit the page was not handed is the compiler's refusal, not a fetch", () => {
  const compiled = compileUnits({ compiler, units: [units[0]!], linkMap: "{}", buildRoot: "build" });
  assert.equal(compiled.ok, false);
  if (compiled.ok) return;
  assert.equal(compiled.problem, `${ROOT} is refused: unresolved-import at line 1`);
});

test("a link map that is not a map is refused before anything compiles", () => {
  const compiled = compileUnits({ compiler, units, linkMap: "not json", buildRoot: "build" });
  assert.equal(compiled.ok, false);
});

test("a unit the link map names is compiled from its own source, since the page reads no module it was not handed", () => {
  const map: LinkMap = {
    [LIBRARY]: {
      module: "x/lib/text.js",
      protocol: "docs/khayyam/khayyam.md",
      checked: [{ requirement: "a stand-in", at: "Method" }],
      declares: { Text: { kind: "capsule" } },
      provides: { Text: "Text" },
    },
  };
  const compiled = compileUnits({
    // The map is handed over already read: what this test is about is what the
    // page reads, not how a map's text is checked.
    compiler: { ...compiler, readLinkMap: () => ({ ok: true as const, map }) },
    units,
    linkMap: JSON.stringify(map),
    buildRoot: "build",
  });
  assert.equal(compiled.ok, true, compiled.ok ? "" : compiled.problem);
  if (!compiled.ok) return;
  assert.equal(compiled.program.units.find((unit) => unit.uri === LIBRARY)!.origin, "compiled");
  assert.equal(typeof compiled.texts[LIBRARY], "string");
});
