import assert from "node:assert/strict";
import test from "node:test";

import { analyze } from "../src/frontend.ts";
import { inspect } from "../src/inspect.ts";
import { accepts, memory } from "./harness.ts";

// What a form means: the shape the language admits, stated as the one outcome a file of
// that shape must have. A row here says nothing about any other row's fault — the label a
// refused form carries is the refusal's business, and a label asserted beside an accept row
// would be a claim about a file that was accepted.

accepts("a body-less abstraction (khayyam.md → Abstraction)", "tp Reader ab\n");

accepts(
  "an abstraction composition block (khayyam.md → Abstraction)",
  "tp DataType ab\ntp Field_MediaType ab\ntp ADT ab {\n    DataType\n    Field_MediaType\n}\n",
);

accepts(
  "a capsule with fields (encapsulation.md → Capsule Structure and Privacy)",
  "tp String ab\ntp W16 ab\ntp TLSConfig ab\ntp ServerConfig cp {\n    Host String\n    Port W16\n    TLSConfig TLSConfig\n}\n",
);

accepts(
  "an empty capsule — no minimum is documented",
  "tp RuntimePanicRecovery cp {\n}\n",
);

accepts(
  "a method with owner, influencing, and influenced groups (method.md → Method Structure)",
  "tp Key ab\ntp String ab\ntp Error ab\ntp Set mt (self Key) (key String) (err Error) {}\n",
);

accepts(
  "a body-less method — the contract form",
  "tp Reader ab\ntp Element ab\ntp Error ab\ntp Read mt (self Reader) (data Element) (err Error)\n",
);

accepts(
  "a variable declaration (khayyam.md → Variable)",
  "tp W16 ab\nvr maxW16 W16\n",
);

accepts(
  "identifiers written in Persian and Chinese scripts",
  "tp داده ab\nvr نام داده\ntp 测试 ab\nvr 名字 测试\n",
);

accepts("two declarations on separate lines", "tp A ab\ntp B ab\n");

accepts(
  "type inclusion from a resolvable path",
  'tp Bool in "lib/boolean.kh"\n',
  { "lib/boolean.kh": "tp Bool ab\n" },
);

accepts(
  "variable inclusion from a resolvable path",
  'vr MaxTimeout in "lib/config.kh"\n',
  { "lib/config.kh": "vr MaxTimeout W16\n" },
);

accepts(
  "a scope declared inside a method body (khayyam.md → Scope)",
  "tp Host ab\ntp Run mt (self Host) () () {\n    tp Step sc {\n        a command\n    }\n}\n",
);

accepts(
  "an inclusion URI carrying no extension — dependency management resolves the URI, the grammar does not grade it",
  'tp Bool in "modules/math/boolean"\n',
  { "modules/math/boolean": "tp Bool ab\n" },
);

accepts(
  "an inclusion URI carrying a foreign extension — a URI is a URI, whatever scheme a resolver makes of it",
  'tp Bool in "lib/boolean.go"\n',
  { "lib/boolean.go": "tp Bool ab\n" },
);

test("the semantic representation is inspectable", () => {
  const result = analyze(
    "main.kh",
    "tp Reader ab\ntp Read mt (self Reader) (data Reader) (err Reader)\n",
    memory(),
  );
  assert.equal(result.outcome, "accept");
  if (result.outcome !== "accept") return;
  const unit = JSON.parse(inspect(result.unit)) as {
    declarations: ReadonlyArray<{ form: string; name: string }>;
  };
  assert.deepEqual(
    unit.declarations.map((declaration) => `${declaration.form}:${declaration.name}`),
    ["tp-ab:Reader", "tp-mt:Read"],
  );
});
