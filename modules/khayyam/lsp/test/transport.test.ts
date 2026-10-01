import assert from "node:assert/strict";
import test from "node:test";

import { frame, refuse, respond, notify, takeFrame, type Taken } from "../src/transport.ts";

// The wire this server speaks: a header, a blank line, and a body of exactly the declared
// byte length. Both halves of a claim about the wire were only ever checked by driving a
// server over its own stdio, which sends whole frames one write at a time — so a body
// split across two reads, a header that declares no length, and a body that will not
// parse were all unreachable by any test. What this file pins is the framing itself.

const of = (payload: unknown): string => frame({ jsonrpc: "2.0", id: 1, method: "ping", params: payload });

test("the length in the header is counted in bytes, not in characters", () => {
  const framed = of({ text: "کالا" });
  const [, body] = framed.split("\r\n\r\n");
  const declared = Number(/Content-Length:\s*(\d+)/.exec(framed)![1]);
  assert.equal(declared, Buffer.byteLength(body!, "utf8"), "a client counting characters would cut the frame short");
  assert.notEqual(declared, body!.length, "which is not the same count");
});

test("a notification, a response and a refusal are the three shapes this server sends", () => {
  assert.equal(
    notify("textDocument/publishDiagnostics", { uri: "file:///w/a.kh" }),
    frame({ jsonrpc: "2.0", method: "textDocument/publishDiagnostics", params: { uri: "file:///w/a.kh" } }),
  );
  assert.equal(respond(7, null), frame({ jsonrpc: "2.0", id: 7, result: null }));
  assert.equal(refuse(7, -32602, "no"), frame({ jsonrpc: "2.0", id: 7, error: { code: -32602, message: "no" } }));
});

test("a notification cannot be refused, because there is nothing to answer", () => {
  assert.equal(refuse(undefined, -32602, "no"), null);
});

function taken(buffer: string | Buffer): Taken {
  return takeFrame(Buffer.isBuffer(buffer) ? buffer : Buffer.from(buffer, "utf8"));
}

test("one whole frame is taken off the buffer, and the bytes after it are kept", () => {
  const first = of({ text: "a" });
  const second = of({ text: "b" });
  const read = taken(first + second);
  assert.equal(read.kind, "frame");
  assert.deepEqual(read.message, { jsonrpc: "2.0", id: 1, method: "ping", params: { text: "a" } });
  assert.equal(read.rest.toString("utf8"), second, "the next frame is still in the buffer");
});

test("a body that has not all arrived is not a frame, and nothing is thrown away", () => {
  const framed = of({ text: "کالا" });
  const whole = Buffer.from(framed, "utf8");
  for (let at = 1; at < whole.length; at += 1) {
    assert.equal(taken(whole.subarray(0, at)).kind, "more", `after ${at} of ${whole.length} bytes`);
  }
  assert.equal(taken(whole).kind, "frame");
});

test("a body split across two reads is one frame", () => {
  // LSP frames arrive as a header, a blank line, then a body of exactly the declared byte
  // length - which may be split across reads, so a buffer is drained in a loop.
  const framed = of({ text: "a longer body than one read carries" });
  const whole = Buffer.from(framed, "utf8");
  const header = whole.indexOf("\r\n\r\n") + 4;
  assert.equal(taken(whole.subarray(0, header + 4)).kind, "more", "four bytes of the body is not the whole body");
  assert.equal(taken(whole).kind, "frame", "and what follows it completes the frame");
});

test("a header that declares no length is not a frame this server can read", () => {
  const read = taken("Content-Type: application/vscode-jsonrpc\r\n\r\n" + of({ text: "a" }));
  assert.equal(read.kind, "skipped", "the frame after it is still read");
  assert.equal(taken(read.rest).kind, "frame");
});

test("a body that will not parse is dropped, and the frame after it is still answered", () => {
  // A frame this server cannot parse is not a reason to stop serving.
  const read = taken("Content-Length: 7\r\n\r\nnot json" + of({ text: "a" }));
  assert.equal(read.kind, "skipped");
  assert.equal(taken(read.rest).kind, "frame");
});

test("a buffer holding nothing at all asks for more rather than reading nothing", () => {
  assert.equal(taken("").kind, "more");
  assert.equal(taken("Content-Length: 40\r\n").kind, "more", "a header that has not reached its blank line");
});
