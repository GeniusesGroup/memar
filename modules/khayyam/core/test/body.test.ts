import assert from "node:assert/strict";
import test from "node:test";

import { readCommands } from "../src/body.ts";
import type { Command, Fault, RefusalReason } from "../src/body.ts";

/** The text a body is carried as is read from the line the block opens on, so a
 *  fault's line is counted from the declaration's own line. */
const AT_LINE = 7;

function reads(text: string, atLine = AT_LINE): Command[] {
  const result = readCommands(text, atLine);
  assert.equal(
    result.ok,
    true,
    result.ok ? "" : `refused: ${result.fault.reason} at line ${result.fault.line}`,
  );
  if (!result.ok) return [];
  return result.commands;
}

function refuses(text: string, reason: RefusalReason, atLine = AT_LINE): Fault {
  const result = readCommands(text, atLine);
  assert.equal(result.ok, false, result.ok ? "accepted" : "");
  if (result.ok) throw new Error("refused was expected");
  assert.equal(result.fault.reason, reason, result.fault.reason);
  return result.fault;
}

test("a variable declaration is a declare command (khayyam.md → Variable)", () => {
  assert.deepEqual(reads("vr index W32\n"), [
    { form: "declare", name: "index", type: "W32" },
  ]);
});

test("a variable declaration keeps a qualified type as written", () => {
  assert.deepEqual(reads("vr index pkg.W32\n"), [
    { form: "declare", name: "index", type: "pkg.W32" },
  ]);
});

test("a variable declaration does not take a qualified name", () => {
  assert.equal(refuses("vr pkg.index W32\n", "declaration-form").reason, "declaration-form");
});

test("a method invocation carries both call groups (khayyam.md → Method Invocation Rules)", () => {
  assert.deepEqual(reads("greeting.Say(line)(out)\n"), [
    {
      form: "invoke",
      receiver: "greeting",
      method: "Say",
      influencing: ["line"],
      influenced: ["out"],
    },
  ]);
});

test("an empty group is written, and a call on the parent type names the type before the dot", () => {
  assert.deepEqual(reads("Logger.Dispatch()()\n"), [
    { form: "invoke", receiver: "Logger", method: "Dispatch", influencing: [], influenced: [] },
  ]);
});

test("a group written with its arguments and the other left empty is read whole", () => {
  assert.deepEqual(reads("IF.OnTrue(blank, OnBlank)()\n"), [
    {
      form: "invoke",
      receiver: "IF",
      method: "OnTrue",
      influencing: ["blank", "OnBlank"],
      influenced: [],
    },
  ]);
});

test("a call with the second group missing is refused, because both groups are written", () => {
  refuses("a.Say(b)\n", "declaration-form");
  refuses("Say(a)(b)\n", "declaration-form");
});

test("a call whose first group is empty and whose second is written is read whole", () => {
  assert.deepEqual(reads("a.Say()(b)\n"), [
    { form: "invoke", receiver: "a", method: "Say", influencing: [], influenced: ["b"] },
  ]);
});

test("a scope is a command holding the commands in it (khayyam.md → Scope)", () => {
  assert.deepEqual(reads("tp OnBlank sc {\n    self.Print(fallback)()\n}\n"), [
    {
      form: "scope",
      name: "OnBlank",
      body: [
        {
          form: "invoke",
          receiver: "self",
          method: "Print",
          influencing: ["fallback"],
          influenced: [],
        },
      ],
    },
  ]);
});

test("return is a command with nothing on its line (khayyam.md → Scope)", () => {
  assert.deepEqual(reads("return\n"), [{ form: "return" }]);
});

test("commands are read in the order the lines carry them", () => {
  assert.deepEqual(reads("vr blank Condition\nIF.OnTrue(blank, OnBlank)()\nreturn\n"), [
    { form: "declare", name: "blank", type: "Condition" },
    {
      form: "invoke",
      receiver: "IF",
      method: "OnTrue",
      influencing: ["blank", "OnBlank"],
      influenced: [],
    },
    { form: "return" },
  ]);
});

test("an empty body is no commands", () => {
  assert.deepEqual(reads(""), []);
});

test("a blank line between commands is no command", () => {
  assert.deepEqual(reads("vr blank Condition\n\n\nreturn\n"), [
    { form: "declare", name: "blank", type: "Condition" },
    { form: "return" },
  ]);
});

test("a scope holding a variable declaration and a call is read whole", () => {
  assert.deepEqual(reads("tp Body sc {\n    vr inner W32\n    outer.Take(inner)()\n}\n"), [
    {
      form: "scope",
      name: "Body",
      body: [
        { form: "declare", name: "inner", type: "W32" },
        {
          form: "invoke",
          receiver: "outer",
          method: "Take",
          influencing: ["inner"],
          influenced: [],
        },
      ],
    },
  ]);
});

test("a nested scope is a scope inside a scope", () => {
  assert.deepEqual(reads("tp Outer sc {\n    tp Inner sc {\n        return\n    }\n}\n"), [
    {
      form: "scope",
      name: "Outer",
      body: [{ form: "scope", name: "Inner", body: [{ form: "return" }] }],
    },
  ]);
});

test("a name in any script is a name (khayyam.md → Identifiers)", () => {
  assert.deepEqual(reads("vr داده W32\n"), [
    { form: "declare", name: "داده", type: "W32" },
  ]);
});

test("a body carried as the text of its block is read from the opening brace", () => {
  // What the frontend carries: the tokens of the block, from its opening brace,
  // with the closing brace left out because the depth it tracks is what ends the
  // body. The tokens of a line are separated by a space, so a line's break shows
  // as a newline between them.
  assert.deepEqual(reads("{ \n vr blank Condition \n greeting . IsBlank ( ) ( blank ) \n"), [
    { form: "declare", name: "blank", type: "Condition" },
    {
      form: "invoke",
      receiver: "greeting",
      method: "IsBlank",
      influencing: [],
      influenced: ["blank"],
    },
  ]);
});

test("a body carried as text is read without its original spacing mattering", () => {
  assert.deepEqual(reads("vr    blank    Condition"), [
    { form: "declare", name: "blank", type: "Condition" },
  ]);
});

test("a refusal is one of the frontend's labels, on the line it stands on", () => {
  assert.equal(refuses("vr W32\n", "declaration-form").line, AT_LINE);
  assert.equal(refuses("a.Say(b)\n", "declaration-form").line, AT_LINE);
  assert.equal(refuses("Say(a)(b)\n", "declaration-form").line, AT_LINE);
  assert.equal(refuses("vr in W32\n", "keyword-as-identifier").line, AT_LINE);
  assert.equal(refuses("vr x tp\n", "keyword-as-identifier").line, AT_LINE);
  assert.equal(refuses("tp Named\n", "missing-subtype").line, AT_LINE);
  assert.equal(refuses("a > b\n", "unexpected-character").line, AT_LINE);
  assert.equal(refuses("vr x W32 Y32\n", "declaration-form").line, AT_LINE);
  assert.equal(refuses("tp Open sc {\n", "unbalanced-block").line, AT_LINE + 1);
});

test("a fault's line is the line it stands on in the file, counted from the declaration's line", () => {
  assert.equal(refuses("vr blank Condition\na > b\n", "unexpected-character").line, AT_LINE + 1);
  assert.equal(refuses("vr blank Condition\nvr W32\n", "declaration-form").line, AT_LINE + 1);
  assert.equal(
    refuses("tp Open sc {\n    return\n", "unbalanced-block").line,
    AT_LINE + 2,
  );
});

test("a fault carries what stood there and how much of the line it took", () => {
  const fault = refuses("a > b\n", "unexpected-character");
  assert.equal(fault.text, ">");
  assert.equal(fault.column, 3);
  assert.equal(fault.length, 1);
  assert.equal(fault.extent, "line");
});

test("a fault is the one met first, as a gate's is (gate.ts → parseUnit)", () => {
  const fault = refuses("a > b\nvr W32\n", "unexpected-character");
  assert.equal(fault.line, AT_LINE);
});
