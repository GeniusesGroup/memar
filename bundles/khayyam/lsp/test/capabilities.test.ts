import assert from "node:assert/strict";
import test from "node:test";

import { ROLES } from "../src/contract.ts";
import { declaredCapabilities, contradictsDeclaredChange } from "../src/capabilities.ts";

// What this server says it can do at initialize, and what a payload that contradicts
// that statement is. Both are answers about the wire, so both are checked as the wire
// carries them — the wire tests check what a client observes after the server is running,
// and this fixes the statement the client reads before it asks for anything.

test("the declared capabilities are the contract's legend and this server's own document reading", () => {
  const { capabilities, serverInfo } = declaredCapabilities();
  assert.deepEqual(capabilities.textDocumentSync, { openClose: true, change: 1 });
  assert.equal(capabilities.definitionProvider, true);
  assert.deepEqual(capabilities.semanticTokensProvider, {
    legend: { tokenTypes: [...ROLES], tokenModifiers: [] },
    full: true,
  });
  assert.deepEqual(serverInfo, { name: "khayyam-language-server", version: "0.1.0" });
});

test("the legend advertised is the contract's own roles in the contract's own order", () => {
  // The legend entry is the token type the editor matches a styling rule against, whole,
  // so a legend that reordered or respelled the contract's roles would match no rule.
  const legend = declaredCapabilities().capabilities.semanticTokensProvider.legend.tokenTypes;
  assert.deepEqual(legend, [...ROLES]);
  assert.equal(new Set(legend).size, legend.length, "no role is advertised twice");
  assert.equal(legend.indexOf("method-local"), ROLES.indexOf("method-local"), "the order is the contract's");
});

test("one content change carrying the whole document contradicts nothing", () => {
  // What a client sends under a Full declaration: the whole text, once, with no range.
  assert.equal(contradictsDeclaredChange([{ text: "tp Reader ab\n" }]), null);
});

test("a change carrying a range is refused by the field that carries it", () => {
  const why = contradictsDeclaredChange([
    {
      text: "Bigger",
      range: { start: { line: 4, character: 11 }, end: { line: 4, character: 20 } },
    },
  ]);
  assert.ok(why, "a range is not a change this server declared it would read");
  assert.match(why!, /textDocumentSync\.change is 1 \(Full\)/);
  assert.match(why!, /contentChanges\[0\] carries the range/);
  assert.match(why!, /no ranges/);
});

test("a change of more than one entry is refused, and the count is named", () => {
  const why = contradictsDeclaredChange([{ text: "a" }, { text: "b" }]);
  assert.ok(why);
  assert.match(why!, /one content change carrying the whole document/);
  assert.match(why!, /carries 2\./);
});

test("a change carrying nothing at all is refused as the count it is", () => {
  // The payload a client sends when it has no text to send is still a payload, and the
  // count it contradicts is named rather than assumed.
  const why = contradictsDeclaredChange([]);
  assert.ok(why);
  assert.match(why!, /carries 0\./);
});
