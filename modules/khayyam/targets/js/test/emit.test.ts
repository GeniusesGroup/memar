import assert from "node:assert/strict";
import test from "node:test";

import { compileProgram, emitUnit } from "../src/program.ts";
import type { FileSystem } from "../../../core/src/frontend.ts";
import type { LinkEntry, LinkMap } from "../src/link.ts";

/** The library the demo program reaches: two units the map says nothing about,
 *  so a build exercises the rule the map is read under — with no link, every
 *  unit compiles from its own source. */
const CONTROL_FLOW = [
  "tp Condition cp {",
  "}",
  "",
  "tp Scope cp {",
  "}",
  "",
  "tp Flow cp {",
  "    IF",
  "    ELSE",
  "}",
  "",
  "tp Drive mt (self Flow) (condition Condition, branch Scope) ()",
  "",
  "tp Revise mt (self Flow) (condition Condition) (reversed Condition)",
  "",
  "tp IF ab",
  "",
  "tp IF_OnTrue mt (self IF) (condition Condition, branch Scope) ()",
  "",
  "tp ELSE ab",
  "",
  "tp ELSE_OnFalse mt (self ELSE) (condition Condition, branch Scope) ()",
  "",
  "tp OnTrue mt (self Flow) (condition Condition, branch Scope) () {",
  "    self.Drive(condition, branch)()",
  "}",
  "",
  "tp OnFalse mt (self Flow) (condition Condition, branch Scope) () {",
  "    vr reversed Condition",
  "    self.Revise(condition)(reversed)",
  "    self.Drive(reversed, branch)()",
  "}",
  "",
].join("\n");

const TEXT = [
  'tp Condition in "lib/control-flow.kh"',
  "",
  "tp Text cp {",
  "}",
  "",
  "tp IsBlank mt (self Text) () (blank Condition)",
  "",
  "tp Print mt (self Text) () ()",
  "",
].join("\n");

const GREETING = [
  'tp Condition in "lib/control-flow.kh"',
  'tp Flow in "lib/control-flow.kh"',
  'tp Text in "lib/text.kh"',
  "",
  "tp Greeter cp {",
  "}",
  "",
  "tp Greet mt (self Greeter) (greeting Text, fallback Text, flow Flow) () {",
  "    vr blank Condition",
  "    greeting.IsBlank()(blank)",
  "    flow.OnTrue(blank, OnBlank)()",
  "    tp OnBlank sc {",
  "        fallback.Print()()",
  "    }",
  "    flow.OnFalse(blank, OnPresent)()",
  "    tp OnPresent sc {",
  "        greeting.Print()()",
  "    }",
  "}",
  "",
].join("\n");

const PRINT_ONLY = ["tp Text cp {", "}", "", "tp Print mt (self Text) () ()", ""].join("\n");

/** A unit a link stands in for: a capsule with a method, which is the shape a
 *  conformant implementation of a library unit has. */
const LINKED_UNIT = ["tp Ledger cp {", "}", "", "tp Sum mt (self Ledger) (a Ledger, b Ledger) (total Ledger)", ""].join(
  "\n",
);

const LINKED: LinkEntry = {
  module: "lib/ledger.js",
  protocol: "docs/protocols/computer/compiler.md",
  checked: [
    {
      requirement: "a compiler does not hardcode a syntax-level entry point or lifecycle into the language it consumes",
      at: "Entry and lifecycle are not grammar",
    },
  ],
  declares: {
    Ledger: { kind: "capsule" },
    Sum: {
      kind: "method",
      owner: "Ledger",
      ownerParameter: "self",
      influencing: [
        { name: "a", type: "Ledger" },
        { name: "b", type: "Ledger" },
      ],
      influenced: [{ name: "total", type: "Ledger" }],
    },
  },
  provides: { Ledger: "Ledger", Sum: "Sum" },
};

const files: FileSystem = {
  read: (path) => {
    const table: Record<string, string> = {
      "demo/print.kh": PRINT_ONLY,
      "demo/greeting.kh": GREETING,
        "demo/sum.kh": [
          'tp Ledger in "lib/ledger.kh"',
          "",
          "tp Report mt (self Ledger) (a Ledger, b Ledger) () {",
          "    vr total Ledger",
          "    self.Sum(a, b)(total)",
          "}",
          "",
        ].join("\n"),
      "lib/control-flow.kh": CONTROL_FLOW,
      "lib/text.kh": TEXT,
      "lib/ledger.kh": LINKED_UNIT,
      "lib/ledger.js": "export const Ledger = {};",
    };
    return table[path];
  },
};

const links: LinkMap = { "lib/ledger.kh": LINKED };

const PRINT_ARTIFACT = [
  "// demo/print.kh",
  "// An ES module generated from a Khayyam unit. It is a build product and",
  "// never a source of truth: the semantic representation is.",
  "",
  "const $supplied = Object.create(null);",
  "",
  "// A body-less method's implementation is supplied when the program is linked and",
  "// run: the body-less method is the language's own signal that the implementation",
  "// comes from the link phase (docs/khayyam/khayyam.md → Method).",
  "export function supply(implementations) {",
  "    Object.assign($supplied, implementations);",
  "}",
  "",
  "export class Text { }",
  "",
  "export function Text$Print(self) {",
  '    return $supplied["Text$Print"](self);',
  "}",
  "",
].join("\n");

const GREETING_ARTIFACT = [
  "// demo/greeting.kh",
  "// An ES module generated from a Khayyam unit. It is a build product and",
  "// never a source of truth: the semantic representation is.",
  "",
  'import { Text$IsBlank as $Text$IsBlank, Text$Print as $Text$Print } from "../lib/text.js";',
  'import { Flow$OnFalse as $Flow$OnFalse, Flow$OnTrue as $Flow$OnTrue } from "../lib/control-flow.js";',
  "",
  "export class Greeter { }",
  "",
  "export function Greeter$Greet(self, greeting, fallback, flow) {",
  "    const greeting$ = greeting;",
  "    const fallback$ = fallback;",
  "    const flow$ = flow;",
  "    const blank$ = { value: undefined };",
  "    function $OnBlank$() {",
  "        $Text$Print(fallback$.value);",
  "    }",
  "    function $OnPresent$() {",
  "        $Text$Print(greeting$.value);",
  "    }",
  "    $Text$IsBlank(greeting$.value, blank$);",
  "    $Flow$OnTrue(flow$.value, blank$, $OnBlank$);",
  "    $Flow$OnFalse(flow$.value, blank$, $OnPresent$);",
  "}",
  "",
].join("\n");

const printOnly = compileProgram({ root: "demo/print.kh", files, links, buildRoot: "build" });
const demo = compileProgram({ root: "demo/greeting.kh", files, links, buildRoot: "build" });

test("a unit that reaches nothing compiles on its own", () => {
  assert.equal(printOnly.ok, true, printOnly.ok ? "" : printOnly.problem);
  if (!printOnly.ok) return;
  assert.deepEqual(
    printOnly.program.units.map((unit) => `${unit.origin} ${unit.uri}`),
    ["compiled demo/print.kh"],
  );
  assert.equal(emitUnit(printOnly.program, "demo/print.kh"), PRINT_ARTIFACT);
});

test("every unit compiles from its own source when the map links nothing", () => {
  assert.equal(demo.ok, true, demo.ok ? "" : demo.problem);
  if (!demo.ok) return;
  assert.deepEqual(
    demo.program.units.map((unit) => `${unit.origin} ${unit.uri}`),
    [
      "compiled demo/greeting.kh",
      "compiled lib/control-flow.kh",
      "compiled lib/text.kh",
    ],
  );
});

test("the artifact of a program names the library's own methods, not a name the compiler knows", () => {
  assert.equal(demo.ok, true, demo.ok ? "" : demo.problem);
  if (!demo.ok) return;
  assert.equal(emitUnit(demo.program, "demo/greeting.kh"), GREETING_ARTIFACT);
  const flow = emitUnit(demo.program, "lib/control-flow.kh");
  // The conditional the program branches with is a body of the library's, and
  // the jump under it is what the link phase supplies.
  assert.match(flow, /export function Flow\$OnFalse\(self, condition, branch\)/);
  assert.match(flow, /Flow\$Revise\(self, condition\$, reversed\$\);/);
  assert.match(flow, /return \$supplied\["Flow\$Drive"\]\(self, condition\$, branch\$\);/);
});

test("a contract is a statement about an implementing capsule, so no artifact carries one", () => {
  assert.equal(demo.ok, true);
  if (!demo.ok) return;
  const flow = emitUnit(demo.program, "lib/control-flow.kh");
  assert.doesNotMatch(flow, /IF\$IF_OnTrue/);
  assert.doesNotMatch(flow, /ELSE\$ELSE_OnFalse/);
  // The abstractions the contracts belong to are still declared.
  assert.match(flow, /export const IF = \{ type: "IF" \};/);
});

test("a call on a receiver typed as an abstraction is refused, because this target has no dispatch there", () => {
  const contracted = compileProgram({
    root: "demo/contract.kh",
    files: {
      read: (path) => {
        if (path === "demo/contract.kh") {
          return [
            'tp Condition in "lib/control-flow.kh"',
            'tp Scope in "lib/control-flow.kh"',
            'tp IF in "lib/control-flow.kh"',
            "",
            "tp DriveBranch mt (self IF) (condition Condition, branch Scope) () {",
            "    self.IF_OnTrue(condition, branch)()",
            "}",
            "",
          ].join("\n");
        }
        return files.read(path);
      },
    },
    links: {},
    buildRoot: "build",
  });
  assert.equal(contracted.ok, false);
  if (contracted.ok) return;
  assert.equal(
    contracted.problem,
    "demo/contract.kh: IF$IF_OnTrue: is a contract of an abstraction, and this target resolves a call by the receiver's declared type",
  );
});

test("no specifier an artifact carries is bare, so a browser resolves it without a bundler", () => {
  assert.equal(demo.ok, true);
  if (!demo.ok) return;
  for (const unit of demo.program.units) {
    if (unit.origin !== "compiled") continue;
    for (const dependency of unit.imports) {
      assert.match(
        dependency.specifier,
        /^\.\.?\//,
        `${unit.uri} imports ${dependency.specifier} bare`,
      );
    }
  }
});

test("a unit the map links is not compiled, and the artifact imports its module", () => {
  const linked = compileProgram({ root: "demo/sum.kh", files, links, buildRoot: "build" });
  assert.equal(linked.ok, true, linked.ok ? "" : linked.problem);
  if (!linked.ok) return;
  assert.deepEqual(
    linked.program.units.map((unit) => `${unit.origin} ${unit.uri}`),
    ["compiled demo/sum.kh", "linked lib/ledger.kh"],
  );
  const artifact = emitUnit(linked.program, "demo/sum.kh");
  assert.match(artifact, /import \{ Sum as \$Sum \} from "\.\.\/\.\.\/lib\/ledger\.js";/);
  assert.match(artifact, /\$Sum\(self, a\$, b\$, total\$\);/);
});

test("a link whose module is not there falls back to compiling the unit", () => {
  const fallen = compileProgram({
    root: "demo/sum.kh",
    files: { read: (path) => (path.endsWith(".js") ? undefined : files.read(path)) },
    links,
    buildRoot: "build",
  });
  // With the linked module gone, that unit has no conformant equivalent, so it
  // is compiled like any other, and the program's own body-less method is what
  // the link phase then supplies.
  assert.equal(fallen.ok, true, fallen.ok ? "" : fallen.problem);
  if (!fallen.ok) return;
  assert.deepEqual(
    fallen.program.units.map((unit) => `${unit.origin} ${unit.uri}`),
    ["compiled demo/sum.kh", "compiled lib/ledger.kh"],
  );
  assert.match(emitUnit(fallen.program, "lib/ledger.kh"), /\$supplied\["Ledger\$Sum"\]/);
});

test("the unit the program starts from is refused when it is not there", () => {
  const missing = compileProgram({ root: "demo/absent.kh", files, links, buildRoot: "build" });
  assert.equal(missing.ok, false);
  if (missing.ok) return;
  assert.equal(missing.problem, "demo/absent.kh is not there");
});

test("a unit whose own import is missing is refused by the frontend's own label", () => {
  const missing = compileProgram({
    root: "demo/greeting.kh",
    files: { read: (path) => (path === "demo/greeting.kh" ? GREETING : undefined) },
    links,
    buildRoot: "build",
  });
  assert.equal(missing.ok, false);
  if (missing.ok) return;
  assert.equal(missing.problem, "demo/greeting.kh is refused: unresolved-import");
});
