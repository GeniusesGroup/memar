// The report's own wording.
//
// The check's verdict is its own last line, and the last line is the only place a
// reader learns what the check concluded - so it is fixed here as a test rather than
// read as output. What the report must say is four things: which mechanism answers a
// role and which roles each of the two answers, the kinds and the roots among them, the
// score that decides which value a reader sees, and what selecting a theme costs. A
// reader who sees only a count of roles styled cannot tell a value the contract states
// from one a theme supplied.
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { basename } from "node:path";
import test from "node:test";
import { MANIFEST, baseBackground, baseChain } from "./shipped.ts";
import { run } from "./the-check.ts";

test("the verdict names the mechanism that answers a role, the roles each answers, and the pairs valued", () => {
  const verdict = run();
  assert.equal(verdict.status, 0, `the check refused something:\n${verdict.refusals.join("\n")}`);
  // The last line says which mechanism reaches the editor, because a reader who sees
  // only a count of roles styled cannot tell a value the contract states from one a
  // theme supplied - and it now names the themes, because a theme is what carries a
  // value to a reader who selects one, and the sheet the default keeps for a reader who
  // selects none.
  assert.equal(
    verdict.verdict,
    "OK: 20 roles implemented by a grammar scope and 1 declared server-only (method-local), each with its reason " +
      "stated in the contract; 21 roles over 14 kinds read against the host's own 24 registered token types: 12 " +
      "declare a super type, 4 are this language's own root (scope, identifier-reference, invalid-number, " +
      "invalid-operator), 5 stand as a standard type of their own name and are registered nowhere; 42 role-attribute " +
      "pairs valued in every theme; every one of the 21 legend entries is a name the host can match and is carried by 2 " +
      "contributed themes under that spelling, each with its own sheet's value, so the contract's value is the one that " +
      "reaches a reader; the lowest measured value is 4.54:1 against a floor of 4.5:1 and the warm band is held by the two " +
      "refusals alone; the [khayyam] default carries khayyam-dark.json for a reader who selects no theme, and the " +
      "manifest contributes no semanticTokenScopes for a host's theme to overwrite it with.",
  );
  // The per-theme count is on its own line, in the order the manifest offers the themes,
  // because a theme can be worth a full sheet and be offered by nothing.
  const manifest = JSON.parse(readFileSync(MANIFEST, "utf8"));
  const counts = manifest.contributes.themes.map((theme: any) => `${basename(theme.path)} 42/42 pairs`).join(", ");
  assert.match(verdict.out, new RegExp(`^themes {5}: 2 \\(${counts.replaceAll(".", "\\.")}\\)$`, "m"));
});

test("the report states what selecting a theme costs, and names the base it rests on", () => {
  // A contributed theme REPLACES the active one, and this one is no longer a skin over
  // Khayyam alone: it rests on a base the extension ships, which gives the workbench its
  // colours and every other language its token colours, and the theme overrides none of
  // them. What that costs a reader belongs in the report of the run rather than in a
  // session that happened to select it, so the run says which base and what it gives.
  const verdict = run();
  assert.equal(verdict.status, 0, `the check refused something:\n${verdict.refusals.join("\n")}`);
  const manifest = JSON.parse(readFileSync(MANIFEST, "utf8"));
  for (const theme of manifest.contributes.themes) {
    const file = basename(theme.path);
    assert.ok(
      verdict.out.includes(
        `note       : theme '${file}': rests on ${baseChain(file).join(" -> ")}, which the extension ships and a ` +
          "host reads before this theme's own values: the base gives the workbench its colours and every other " +
          `language its token colours (its editor.background is ${baseBackground(file)}), and this theme overrides ` +
          "none of them",
      ),
      `the base '${file}' rests on was not among the notes:\n${verdict.out}`,
    );
  }
});

test("the check proves by the host's own score that our rule wins a role with a hierarchy of more than one entry", () => {
  // A rule keyed the role's own name sits at depth 0 of the token's hierarchy and scores
  // 100; a reader's rule for the standard type sits one entry deeper and scores 99; and
  // the host writes a style when a rule's score is greater than OR EQUAL to the score
  // already held. So ours wins, and the check says the arithmetic rather than the claim.
  const verdict = run();
  assert.equal(verdict.status, 0, `the check refused something:\n${verdict.refusals.join("\n")}`);
  assert.ok(
    verdict.out.includes(
      "note       : score: 'subtype' keyed by its own name sits at depth 0 of the hierarchy ['subtype, keyword'] " +
        "and scores 100; a reader's rule for 'keyword' sits at depth 1 and scores 99, and a style is written when a " +
        "rule's score is greater than or equal to the one held, so the value this extension contributes is the one a " +
        "reader sees while a theme that never heard of Khayyam still reaches our roles through their declared kind",
    ),
    `the score was not among the notes:\n${verdict.out}`,
  );
});

test("the verdict names the kinds, the roots, and the score that decides which value a reader sees", () => {
  const verdict = run();
  assert.equal(verdict.status, 0, `the check refused something:\n${verdict.refusals.join("\n")}`);
  assert.ok(
    verdict.verdict.startsWith(
      "OK: 20 roles implemented by a grammar scope and 1 declared server-only (method-local), each with its reason " +
        "stated in the contract; 21 roles over 14 kinds read against the host's own 24 registered token types: 12 " +
        "declare a super type, 4 are this language's own root (scope, identifier-reference, invalid-number, " +
        "invalid-operator), 5 stand as a standard type of their own name and are registered nowhere",
    ),
    `the verdict does not name the kinds and the roots:\n${verdict.verdict}`,
  );
  assert.ok(verdict.verdict.includes("the lowest measured value is 4.54:1 against a floor of 4.5:1"), verdict.verdict);
  assert.ok(verdict.verdict.includes("the warm band is held by the two refusals alone"), verdict.verdict);
});
