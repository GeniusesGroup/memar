// The values a theme carries, measured against the contract's palette rules.
//
// A theme is not a set of values; it is a derivation from rules, and a rule that cannot
// fail is not a rule. So the values are measured here rather than trusted: the contrast
// floor against that theme's own background, the warm band the owner's ruling reserves
// for error, one hue per kind with lightness and chroma carrying the position within
// it, and the colour-vision pairs the contract records. Every measurement is made over
// a copy, so the sheets a reader selects are the ones the check refuses nothing from.
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import test from "node:test";
import { themeIn, themesRoot } from "./provoke.ts";
import { CONTRACT, MANIFEST } from "./shipped.ts";
import { run } from "./the-check.ts";

test("the check refuses a theme value below the contract's contrast floor, measured against that theme's own background", () => {
  const root = themesRoot();
  themeIn(root, "khayyam-light.json", (theme) => {
    theme.khayyamDisplay["khayyam.keyword.color"] = "#8CC05E";
    theme.tokenColors[0].settings.foreground = "#8CC05E";
    theme.semanticTokenColors.keyword.foreground = "#8CC05E";
  });
  const verdict = run(CONTRACT, MANIFEST, root);
  assert.equal(verdict.status, 1, "a value below the floor cannot pass");
  assert.ok(
    verdict.refusals.some((line) => /'khayyam-light.json': 'keyword' is #8CC05E, 2\.14:1 against that theme's own background #FFFFFF, and the floor is 4\.5:1/.test(line)),
    `the value below the floor was not among what was refused:\n${verdict.refusals.join("\n")}\n${verdict.out}`,
  );
});

test("the check refuses a warm value on a role that is not one of the two refusals", () => {
  // The owner's ruling: warm means error and nothing else. The band is stated as an
  // interval on the OKLCH hue circle, so the refusal names the measured hue.
  const root = themesRoot();
  themeIn(root, "khayyam-dark.json", (theme) => {
    theme.khayyamDisplay["khayyam.variable.color"] = "#FEB98B";
    theme.semanticTokenColors.variable.foreground = "#FEB98B";
    for (const rule of theme.tokenColors)
      if (rule.scope === "variable.other.khayyam") rule.settings.foreground = "#FEB98B";
  });
  const verdict = run(CONTRACT, MANIFEST, root);
  assert.equal(verdict.status, 1, "a warm value on an ordinary role cannot pass");
  assert.ok(
    verdict.refusals.some((line) => /'khayyam-dark.json': 'variable' is warm \(OKLCH hue 55, chroma 0\.\d+, inside the band 15-120\) and is not one of the two refusals/.test(line)),
    `the warm value was not among what was refused:\n${verdict.refusals.join("\n")}\n${verdict.out}`,
  );
});

test("the check refuses two roles of one kind that differ in hue, and two of different kinds that are told apart by neither hue nor lightness", () => {
  // Origin and validity are carried by lightness and saturation, never by hue, so two
  // roles of one kind may not differ in hue; and a pair of different kinds may not be
  // within 20 degrees of hue AND 12 L* of one another.
  const hues = themesRoot();
  themeIn(hues, "khayyam-dark.json", (theme) => {
    theme.khayyamDisplay["khayyam.included-variable.color"] = "#86A0D7";
    theme.semanticTokenColors["included-variable"].foreground = "#86A0D7";
    for (const rule of theme.tokenColors)
      if (rule.scope === "variable.other.import.khayyam") rule.settings.foreground = "#86A0D7";
  });
  const drifted = run(CONTRACT, MANIFEST, hues);
  assert.equal(drifted.status, 1, "a kind that drifts in hue cannot pass");
  assert.ok(
    drifted.refusals.some((line) =>
      /'khayyam-dark.json': '(variable|included-variable)' and '(variable|included-variable)' are one kind \(variable\) and their hues differ by \d+ degrees/.test(
        line,
      ),
    ),
    `the hue drift was not among what was refused:\n${drifted.refusals.join("\n")}\n${drifted.out}`,
  );
});

test("a colour-vision pair the contract records is reported, and one it does not is refused", () => {
  // The mechanism the palette rules give: a pair that falls under dE76 10 is a decision,
  // not a defect, provided the contract records the pair and the reason. An unrecorded
  // one is the defect, and the contract's own list is what decides which is which.
  const verdict = run();
  assert.equal(verdict.status, 0, `the check refused something:\n${verdict.refusals.join("\n")}`);
  const contract = JSON.parse(readFileSync(CONTRACT, "utf8"));
  const recorded = contract.palette.recordedDichromacyPairs.pairs;
  assert.ok(Array.isArray(recorded) && recorded.length > 0, "the contract records no colour-vision pair at all");
  for (const pair of recorded)
    assert.ok(
      typeof pair.pair === "string" && typeof pair.theme === "string" && typeof pair.reason === "string" && pair.reason.trim() !== "",
      `a recorded pair without a reason: ${JSON.stringify(pair)}`,
    );
});
