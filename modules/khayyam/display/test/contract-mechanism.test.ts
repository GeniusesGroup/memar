// The contract's own declaration of which mechanism answers a role.
//
// A role is answered either by a scope a grammar emits or by a resolver that can see
// the whole document, and which of the two is a property of what the role IS. The
// contract says which, per role, and this file fixes the three ways that declaration
// can fail to say so - a role that names neither, a server-only role that does not say
// why, and a role that declares one thing and carries the shape of the other.
import assert from "node:assert/strict";
import test from "node:test";
import { contractWith } from "./provoke.ts";
import { roleNamed } from "./shipped.ts";
import { run } from "./the-check.ts";

test("a role that is neither a grammar scope nor declared server-only is refused", () => {
  const path = contractWith((contract) => delete roleNamed(contract, "keyword").implementedBy);
  const verdict = run(path);
  assert.equal(verdict.status, 1, "a role that says which mechanism answers it cannot pass");
  assert.equal(verdict.refusals.length, 1, `one role is wrong, so one line is refused:\n${verdict.out}`);
  assert.equal(
    verdict.refusals[0],
    "contract: role 'keyword' states implementedBy nothing, which is neither 'grammar-scope' nor 'server-only'; " +
      "a role is answered either by a scope a grammar emits or by a resolver that can see the whole document, and a " +
      "role that says which is neither cannot be checked against anything",
  );
});

test("a role declared server-only that does not say why is refused", () => {
  const path = contractWith((contract) => delete roleNamed(contract, "method-local").serverOnlyBecause);
  const verdict = run(path);
  assert.equal(verdict.status, 1);
  assert.equal(verdict.refusals.length, 1, `one role is wrong, so one line is refused:\n${verdict.out}`);
  assert.equal(
    verdict.refusals[0],
    "contract: role 'method-local' is declared server-only and does not say why: 'serverOnlyBecause' is the one " +
      "place a reader is told a consumer may not be able to answer this role, so the reason is not optional",
  );
});

test("a role declared server-only that names a scope is refused", () => {
  // The two statements contradict each other, and the contradiction is the defect: a
  // scope is what a grammar emits, which is the whole of what `server-only` denies.
  // The mutation is inconsistent in more than one direction - the scope it borrows is
  // also named by another role, and a contributed colour rule styles it - so more than
  // one line is refused, and this asks for the one about the declaration, which comes
  // first.
  const path = contractWith((contract) => {
    roleNamed(contract, "method-local").scopes = ["variable.other.khayyam"];
  });
  const verdict = run(path);
  assert.equal(verdict.status, 1);
  assert.equal(
    verdict.refusals[0],
    "contract: role 'method-local' is declared server-only but names the scope(s) [variable.other.khayyam], which " +
      "is what a grammar emits and is exactly what 'server-only' denies",
  );
});

test("a role declared server-only by a grammar scope is refused, and so is one that names no scope", () => {
  // Both directions of the same contradiction: the declaration and the shape have to
  // agree, whichever of the two a later reader believes.
  const withReason = contractWith((contract) => {
    roleNamed(contract, "capsule").serverOnlyBecause = "because";
  });
  const refused = run(withReason);
  assert.equal(refused.status, 1);
  assert.equal(
    refused.refusals[0],
    "contract: role 'capsule' states implementedBy 'grammar-scope' and carries a 'serverOnlyBecause' reason, which " +
      "only a role declared server-only may have",
  );
  const withoutScope = contractWith((contract) => {
    delete roleNamed(contract, "capsule").scopes;
  });
  const nameless = run(withoutScope);
  assert.equal(nameless.status, 1);
  assert.equal(
    nameless.refusals[0],
    "contract: role 'capsule' states implementedBy 'grammar-scope' and names no scope, so nothing implements it",
  );
});
