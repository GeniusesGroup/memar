import assert from "node:assert/strict";
import test from "node:test";

import { encodeTokens } from "../src/token-stream.ts";
import type { SemanticToken } from "../src/role-emitter.ts";
import { semanticRoles } from "../src/semantic.ts";

// The stream the editor reads: LSP's delta encoding of the roles, in the contract's own
// role order. What the wire tests decode is the stream this builds, so what they cannot
// reach is anything about it no real document produces — a role the contract does not
// define being among them, which is answered by not sending it at all.

const SOURCE = ["tp Reader ab", "tp Run mt (self Reader) (err Error) () {", "\terr.Copy()", "}", ""].join("\n");

/** A role as the reading answers it, for a stream the corpus cannot produce. */
const roleAt = (line: number, startChar: number, length: number, role: string, text: string): SemanticToken => ({
  line,
  startChar,
  length,
  role,
  text,
  resolvedTo: "said so",
});

/** Every token of a stream placed back on the lines it stands on, as the editor reads it. */
function placed(data: number[], source: string): string[] {
  const lines = source.split("\n");
  const out: string[] = [];
  let line = 0;
  let character = 0;
  for (let at = 0; at < data.length; at += 5) {
    line += data[at]!;
    character = data[at] === 0 ? character + data[at + 1]! : data[at + 1]!;
    out.push(`${lines[line]!.slice(character, character + data[at + 2]!)}@${line}:${character}:${data[at + 2]}`);
  }
  return out;
}

test("a stream is five integers per token, in LSP's own order", () => {
  const data = encodeTokens(semanticRoles(SOURCE));
  assert.equal(data.length % 5, 0);
  assert.ok(data.length > 0);
  assert.equal(semanticRoles(SOURCE).length, data.length / 5, "one token per role the reading answered with");
});

test("the first token stands at the origin, and each token after it is a delta", () => {
  // [deltaLine, deltaStart, length, tokenType, tokenModifiers] — the first token has
  // nothing to be a delta of, so its own line and character are sent as the deltas.
  const first = encodeTokens(semanticRoles(SOURCE)).slice(0, 3);
  assert.deepEqual(first, [0, 0, 2], "`tp` at 0:0, covering two characters");
  assert.deepEqual(placed(encodeTokens(semanticRoles(SOURCE)), SOURCE).slice(0, 3), [
    "tp@0:0:2",
    "Reader@0:3:6",
    "ab@0:10:2",
  ]);
});

test("a token's type is the role's index in the contract's legend, and its modifiers are none", () => {
  const data = encodeTokens(semanticRoles("tp Reader ab\n"));
  assert.deepEqual(data, [0, 0, 2, 0, 0, 0, 3, 6, 6, 0, 0, 7, 2, 1, 0]);
  // The contract's roles in its own order: `keyword` is the first and `subtype` the
  // second, and a type sent by a role's own name would be a number no legend names.
  assert.deepEqual(data.filter((_, at) => at % 5 === 4), [0, 0, 0], "no token carries a modifier");
});

test("a role the contract does not define is not sent as a token", () => {
  // The editor matches styling rules against the token type whole, so a type the legend
  // names no entry for is a token the editor would drop while merging it into the
  // grammar's. It is better not to send it — and the token after it is measured from the
  // token before that, since the dropped one was never placed.
  assert.deepEqual(
    encodeTokens([
      roleAt(0, 0, 2, "keyword", "tp"),
      roleAt(0, 3, 6, "invented-role", "Reader"),
      roleAt(0, 10, 2, "subtype", "ab"),
    ]),
    [0, 0, 2, 0, 0, 0, 10, 2, 1, 0],
  );
});

test("a document the reading has nothing to answer sends an empty stream", () => {
  // The empty stream is a real answer for a real document — and for a document the
  // frontend could not read at all, which is why the handler refuses a document it was
  // never told about rather than answering with one.
  assert.deepEqual(encodeTokens(semanticRoles("tp Reader ab\n")).length, 15);
  assert.equal(encodeTokens([]).length, 0);
});
