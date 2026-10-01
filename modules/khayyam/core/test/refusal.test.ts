import assert from "node:assert/strict";
import { readFileSync, readdirSync } from "node:fs";
import { join } from "node:path";
import test from "node:test";

import { refuses } from "./harness.ts";

// What a refusal means: the one label a form the language does not have must carry. The
// label is the whole claim of a row here — a form that is refused for a reason other than
// the one its row names is a different fault, and a row that only said "refused" would
// pass on it. The forms these rows are about are in form.test.ts; none of them is asked
// here, because a form the language admits is not a question this file answers.

test("no label names a mechanism the language does not have", () => {
  // A label is the one thing a reader meets before any explanation, and this one was read
  // wrong on 2026-09-30: `name-not-exported` on a real corpus claim was taken to mean the
  // target file was fine and had withheld the name, when the file declared nothing at all.
  // The fault was correct and the label sent the reader looking for a publication step the
  // language has no word for. So every label is checked here against the language's own
  // vocabulary, and this list is where a borrowed word gets caught — a check that would
  // otherwise have run only on a human noticing, which is what happened.
  //
  // `export` is the word this is about, and it is listed rather than left out: the language
  // uses it once, in a sentence about *other* languages' exports, and a word that appears
  // only there must not appear in anything this toolchain names.
  const borrowed = ["export", "published", "visibility", "public", "private", "namespace", "package"];
  const vocabulary = join(import.meta.dirname, "..", "src", "sr.ts");
  const source = readFileSync(vocabulary, "utf8");
  // The labels themselves, read out of the union rather than out of the file around it: the
  // file says `export` in every other sentence, and a check that read the whole file would
  // fail on TypeScript rather than on anything a reader ever sees.
  const labels = [...source.matchAll(/\| "([a-z-]+)"/g)].map((found) => found[1]!);
  assert.ok(labels.length >= 12, `the union of refusal reasons was read, and it has ${labels.length} members`);
  for (const word of borrowed) {
    for (const label of labels) {
      assert.doesNotMatch(label, new RegExp(`\\b${word}\\b`, "i"), `the label "${label}" names "${word}"`);
    }
  }
  // And the three inclusion labels are siblings, which is what makes them readable beside
  // each other in a problems list: all three say what is not there, in the language's words.
  for (const label of ["unresolved-import", "name-not-declared", "kind-mismatch"]) {
    assert.ok(labels.includes(label), `${label} is one of the labels the toolchain draws from`);
  }
});

refuses(
  "a top-level scope — placement rule (khayyam.md → Scope)",
  "scope-placement",
  "tp Run sc {\n    a command\n}\n",
);

refuses("a bare type with no subtype (Q1 ruling)", "missing-subtype", "tp Foo\n");

refuses("a keyword used as a name", "keyword-as-identifier", "tp W16 ab\nvr tp W16\n");

refuses("a subtype used as a name", "keyword-as-identifier", "tp W16 ab\nvr in W16\n");

refuses("a semicolon between declarations", "semicolon", "tp A ab;\ntp B ab\n");

refuses("two declarations on one line", "declaration-form", "tp A ab tp B ab\n");

refuses(
  "an import written without the in keyword (archive: mutable.kh)",
  "declaration-form",
  'tp Error "memar/process/error/protocol"\n',
);

refuses(
  "an unresolvable import path (a URI with no file behind it)",
  "unresolved-import",
  'tp Bool in "modules/math/boolean.kh"\n',
);

refuses(
  "an import of a file that is there and does not parse — the target's own fault",
  "missing-subtype",
  'tp Bool in "lib/broken.kh"\n',
  { "lib/broken.kh": "tp Bool\n" },
);

refuses(
  "a name the import target does not declare (the shape of archive: if.kh's Error import)",
  "name-not-declared",
  'tp Missing in "lib/boolean.kh"\n',
  { "lib/boolean.kh": "tp Bool ab\n" },
);

refuses(
  "a kind mismatch — the tp form importing a variable",
  "kind-mismatch",
  'tp MaxTimeout in "lib/config.kh"\n',
  { "lib/config.kh": "vr MaxTimeout W16\n" },
);

refuses(
  "an unbound type name (the shape of archive: if.kh's signature)",
  "unbound-type-name",
  "tp Use mt (self Owner) () (err Error)\n",
);

refuses("an unterminated capsule block", "unbalanced-block", "tp A cp {\n");

refuses("an unterminated composition block", "unbalanced-block", "tp A ab {\n");

refuses("an unterminated string", "unterminated-string", 'tp A in "lib/x\n');

refuses(
  "a character the language does not admit (archive: mem.kh, a Go source named .kh)",
  "unexpected-character",
  "tp A cp {\n    addr [8]W\n}\n",
);

refuses(
  "the archive's method-without-mt form (concurrency.kh, blocking.kh)",
  "declaration-form",
  "tp IsAsync (self Async) () (async Bool)\n",
);

refuses(
  "the archive's subtype-before-name form (weak.kh)",
  "keyword-as-identifier",
  "tp mt ReferenceAlive (self WeakReference) () (err Error)\n",
);
