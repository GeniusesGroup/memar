# Khayyam JavaScript Target Changelog
This file records what changed in [target.md](./target.md) and what each change reached. See [Documentation — Changelog](../../../../docs/documentation-changelog.md) for what this file's structure means.

## Changelog

### A call hands over the slot rather than what is in it, and a field is a variable the capsule own methods reach
- Time: 2026-09-29T18:00:00Z
- Type: Added
- Cited:
  - [Khayyam](../../../../docs/khayyam/khayyam.md) - Depends_on: a call passes every variable of a call strictly by reference, and the three groups being one list of variable references in the underlying layer - the claim this target was not honouring, and the one the owner ruling about a capsule own method rests on
  - [Encapsulation](../../../../docs/khayyam/encapsulation.md) - Depends_on: the privacy the language states, which is about a passed capsule fields and leaves a method reaching its own capsule state to the capsule own methods
- Changed:
  - [target.md](./target.md) - Rewrote the section on a field: what a body may reach it as, and that a call given a field to write is refused on purpose rather than held open, with the endorsed shape and the two boundaries that keep it honest.
  - [target.handoff.md](./target.handoff.md) - Recorded the call carrying the slot in the decision on every variable being a cell, and closed the field-access question in the owner own two rulings rather than one.
  - [targets/js/src/emit.ts](./src/emit.ts) - A call now passes the slot of a variable and not its value, a supplied implementation is handed the same slots, and a field is resolved as the slot it is; the class of a capsule declares one cell per field.
  - [targets/js/src/run.ts](./src/run.ts) - The host entry hands over slots for the influencing group as it already did for the influenced one, so both boundaries of a call say the same thing.
  - [demo/greeting.kh](./demo/greeting.kh), [demo/node-host.js](./demo/node-host.js), [demo/browser.html](./demo/browser.html) - A capsule that holds a field, a host that hands the value over, and a supplied method that reads the slot.
- Added:
  - [bootstrap/write-field.kh](./bootstrap/write-field.kh) - the record of the ruling: the same call written on a name the body binds and on a field, and the second is refused on purpose.
  - [run.test.ts](./test/run.test.ts) - the measurement the endorsed shape needed: a host supplies the method that writes, and the test reads the field back.
- Published:
  - Nothing outside this folder was published for this change.


### A field is a variable: a body reaches its own capsule's state, and the one position left open is named
- Time: 2026-09-29T12:00:00Z
- Type: Added
- Cited:
  - [Encapsulation](../../../../docs/khayyam/encapsulation.md) - Depends_on: the privacy the language states, which is about a passed capsule's fields and leaves a method reaching its own capsule's state to the capsule's own methods
  - [Method in Khayyam](../../../../docs/khayyam/method.md) - Depends_on: a call passes every variable of a call strictly by reference, which is why a field is the same slot a `vr` is
  - [Khayyam](../../../../docs/khayyam/khayyam.md) - Depends_on: the separation of syntax and governance, which is why a host still creates every value and hands the values over rather than the slots
- Changed:
  - [target.md](./target.md) - Added the section on a field being a variable: what a body may reach it as, what the emitted class holds, and the one position that is still refused with the label that says so.
  - [target.handoff.md](./target.handoff.md) - Recorded the field half of the decision on every variable being a cell, narrowed the field-access question to the single line a call would write, and replaced the state probe's finding with its result.
- Added:
  - [bootstrap/write-field.kh](./bootstrap/write-field.kh) - the probe that holds the open question open: two calls in one body, one written into a name the body binds and one into a field, and the second is refused.
- Published:
  - Nothing outside this folder was published for this change.


### The control-flow concept is modelled before any library is written, and the reading of a body moves to the frontend
- Time: 2026-09-29T00:00:00Z
- Type: Added
- Cited:
  - [Khayyam module README](../../README.md) - Depends_on: the rule that target-independent code never lives inside a target folder, and that language-wide library source lives in the other module folders
  - [Modeling Practice](../../../../docs/modeling.practice.md) - Depends_on: the method this work followed before writing anything, and the rule that a model settles before code is written
  - [Control Flow](../../../../docs/protocols/process/control-flow.md) - Depends_on: the document the model was checked against, and the examples in it that this language cannot write as they stand
  - [Method in Khayyam](../../../../docs/khayyam/method.md) - Depends_on: the two call groups of a call and all three of a signature, which is what the questions the model carries turn on
- Changed:
  - [target.md](./target.md) - Rewrote the paragraph on what a host supplies: the link form the language names for a body-less method on a concrete capsule is the whole of what a host supplies, and what a program composes out of belongs to a library under `modules/`, modelled before it is written. The demo paragraph now says what the demo is - a capsule, an owner, and a value handed to a method - and the prohibition paragraph names the model instead of a folder.
  - [target.handoff.md](./target.handoff.md) - Recorded the decision as revised, the narrowed body question, the two answers the compose probe gave by the way, the state the field question is now in, and the next steps: the influenced group first, the control-flow model second, and the module that names the interfaces a program may call third.
- Added:
  - [modules/process/control-flow/model.md](../../../process/control-flow/model.md) and [model.handoff.md](../../../process/control-flow/model.handoff.md) - the model of the control-flow library: its concepts, what the protocol asks that this language cannot write, and the questions its writing waits on.
  - [bootstrap/compose.kh](./bootstrap/compose.kh) - rewritten as the sixth probe: a scope, a driver, a call that carries a value in and receives what the call wrote into a slot, and an early return.
  - [core/src/body.ts](../../core/src/body.ts) and [core/test/body.test.ts](../../core/test/body.test.ts) - the reading of a body, moved out of this target on the owner ruling.
- Removed:
  - `targets/js/lib/` - the Khayyam libraries this folder held, and the demo that branched through them. Reason: a library belongs with the rest of the library under `modules/`, and a model settles before code is written.


### The JavaScript target: a `.kh` program runs, branching through a Khayyam library
- Time: 2026-09-28T07:00:00Z
- Type: Added
- Cited:
  - [Khayyam - Programming Language](../../../../docs/khayyam/khayyam.md) - Depends_on: the command set a method body may hold, the one invocation form, both call groups of a call and all three of a signature, the body-less method as contract and as link, the lowering of a scope to a function, and the absence of literals, operators, and construction forms
  - [Method in Khayyam](../../../../docs/khayyam/method.md) - Depends_on: the three call groups, pass-by-reference, and the single invocation form
  - [Control Flow](../../../../docs/protocols/process/control-flow.md) - Evidence: the branch-grouping primitive, the generic conditional receiving an explicit branch scope, the jump the library is built on, and the mechanism summary `lib/control-flow.kh` is checked against
  - [Compiler](../../../../docs/protocols/computer/compiler.md) - Depends_on: entry and lifecycle as configuration rather than grammar, and the rule that no library name is an intrinsic of a compiler
  - [Khayyam Rule — Qualified Names](../../rules/qualified-names/qualified-names.md) and [Khayyam Rule — Receiver Method Names](../../rules/receiver-method-names/receiver-method-names.md) - Depends_on: the names of a contract method and of the method a receiver's own type satisfies
- Propagates to:
  - [execution.md](../../execution.md): Pending - goal 3 is answered by the artifact running under Node and in a browser, goal 4's second half by a compiled program that branches through the library, goal 5's part that needs no compiler in a browser by the page that loads the artifact, and goal 6 by the cache; the plan's wording is not this session's to change
  - [execution.handoff.md](../../execution.handoff.md): Pending - the goals this target answers, and the questions its work raised, are the parent handoff's to record
  - [core/src/sr.ts](../../core/src/sr.ts): Pending - a method body is carried as text, and the commands read out of that text belong to the shared representation rather than to a target; the owner of `core/` decides
  - [core/src/frontend.ts](../../core/src/frontend.ts): Pending - the frontend resolves every `in` before the map is asked, so a link cannot stand in for a `.kh` file that is not there
  - [docs/khayyam/](../../../../docs/khayyam/): Pending - two questions the library this work wrote ran into, each of which decides what a program may mean
  - [package.json](../../package.json): Done - the test script runs the target's tests and, in a second invocation, the browser load check
- Contributors:
  - [Space Bunny Alpha](../../../../CONTRIBUTORS.md#space-bunny-alpha) (space-bunny via [OpenCode](../../../../CONTRIBUTORS.md#opencode)) - wrote, tested

#### What changed
- `lib/control-flow.kh` — the branch-grouping primitive, the generic `IF`/`ELSE` conditional as two abstractions, and the two methods that implement it over a jump, written in Khayyam and compiled by this backend. Its header records what was checked against which section of the Control Flow protocol.
- `lib/text.kh` — a capsule of text and the two things a host may be asked of it, both body-less on a concrete capsule.
- `demo/greeting.kh` — the program: a capsule, two named scopes, a condition the host's `IsBlank` produced, and two calls on the library's `Flow`.
- `demo/node-host.js` and `demo/browser.html` — the two hosts, which supply the jump, a condition the other way, and what a text can be asked, and nothing that decides what a branch means.
- `src/body.ts` — reads the commands of a method body or a scope's block, refusing anything outside the four forms the language documents admit, with the frontend's own labels and at the line a person reads.
- `src/program.ts` — reads a unit and everything it reaches, asks the link map before a unit's own source, tells the three kinds of body-less method apart, holds what the backend translates, and offers the caller a unit it already holds before reading any source.
- `src/emit.ts` — writes one unit as one ES module, resolving every name before it emits anything, so a name it cannot resolve is a refusal rather than an artifact that is nearly right; a contract is carried by no artifact and cannot be called.
- `src/cache.ts` — the build: a unit's key is the hash of its source, this target's three versions, the host profile, the map's own text, and the keys of the units it names; a unit that is the same stands in for itself, is written only when its text moved, and a build reports what it compiled, stood in for, and wrote.
- `src/link.ts` and `link_map.json` — the map the link-first rule is read under, and the checks every entry answers before anything is compiled. It holds no entry.
- `bootstrap/` and `test/bootstrap.test.ts` — one probe per thing a compiler written in Khayyam needs, each compiled by this target, so that what the language does not yet admit is a measurement.
- `demo/browser.html` — loads the artifact with no bundler and no build step on the page, which is the part of the reader-goal that does not need a compiler in the browser.
- `test/body.test.ts`, `test/emit.test.ts`, `test/link.test.ts`, `test/run.test.ts`, `test/cache.test.ts`, `test/bootstrap.test.ts`, `test/browser.check.ts` — the shapes above, each written before the code that produces them.

#### Considered and not done
- A JavaScript implementation of the branch library was not kept. Writing the conditional in another language answers a question the language owns, and the same question is answered by `lib/control-flow.kh` at the height the compiler needs it: the answer is a Khayyam library, and only the jump under it comes from the host.
- A link-map entry was not written, and with the archived sources absent an entry would have meant a JavaScript implementation written for the map's sake rather than a conformant one that already existed.
- A cache over the artifacts was written, and it is the whole of goal 6: a second build over unchanged sources compiles nothing, a change to one file compiles that file and the units that name it, and a change to a version, to the host profile, or to the map reaches every unit. Its key covers the sources, this target's three versions, the environment, and the keys of the units each unit names; the versions are named constants rather than values computed at run time, because a key that depended on running the toolchain could not be compared with a stored one without running it.
- A browser page that compiles the program it runs was not written, because entry and lifecycle belong to the host and the page that takes a file and compiles it needs the toolchain in a browser, which is the step after it. The page here loads what the build wrote.
- Compiling the corpus under `modules/` was not attempted, because the parent handoff's open questions — the meaning of a qualified type reference among them — stand in the way, and a target that compiles what it cannot yet read would answer a question nobody asked.
