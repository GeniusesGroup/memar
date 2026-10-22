# Khayyam Go Target Research 001 — What the two archived repositories disagree about, and what the JavaScript transfer did not carry

## Table of contents
- [Status](#status)
- [Question and Goals](#question-and-goals)
- [Participants](#participants)
- [Methodology](#methodology)
- [Findings](#findings)
  - [Where the Go and JavaScript archives disagree](#where-the-go-and-javascript-archives-disagree)
  - [Disagreements the sources already decided silently](#disagreements-the-sources-already-decided-silently)
  - [A finding measured and dismissed](#a-finding-measured-and-dismissed)
  - [The archived JavaScript, and what it did not carry](#the-archived-javascript-and-what-it-did-not-carry)
  - [Subjects with no home, parked in the nearest folder that exists](#subjects-with-no-home-parked-in-the-nearest-folder-that-exists)
  - [Two further findings no document records](#two-further-findings-no-document-records)
  - [Live problems the two archives jointly expose — defects in the sources, not findings of this inquiry](#live-problems-the-two-archives-jointly-expose--defects-in-the-sources-not-findings-of-this-inquiry)
  - [What the port did](#what-the-port-did)
- [Decisions of record](#decisions-of-record)
- [Conclusion](#conclusion)
- [Related Artifacts](#related-artifacts)
- [Open Questions](#open-questions)
- [Notes](#notes)

## Status
Complete

## Question and Goals
### Questions
1. Where do the two archived repositories — `memar-go` and `memar-js` — disagree about a subject the sources speak to, and which side do the current sources take? — **Answered**
2. What did the archived JavaScript transfer not carry, and under what condition and rule was it retired? — **Answered**
3. Which archived subjects have no home in the architecture, and where are they parked? — **Answered**

### Goals
1. Establish how many residue blocks each archive left in the sources, and where one file carries both. — **Met**
2. Record every disagreement with its citations intact, so a reader can check a row rather than believe it. — **Met**
3. Record what the JavaScript transfer left behind, so the gap is a stated fact rather than an absence. — **Met**

### Scope
The residue blocks of the two archived repositories as they stand in this repository's sources, the archived `memar-js` README recovered on 2026-10-01, and the governing documents those rows cite. The defects the two archives jointly expose are recorded here and are **not** findings of this inquiry — see the section that says so. It asks nothing about the Khayyam toolchain's design, and it decides nothing about the language.

## Participants
- [Omid Hekayati](../../../../CONTRIBUTORS.md#omid-hekayati) — **Questioner**, **Goal-setter**; recovered the retired `memar-js` README from a real address on 2026-10-01 and is the source of the replacement-scanner condition and the retirement rule recorded below; review outcome: **Not yet reviewed**.
- [space-bunny](../../../../CONTRIBUTORS.md#space-bunny-alpha) (via [OpenCode](../../../../CONTRIBUTORS.md#opencode)) — **Researcher**; review outcome: **Not yet reviewed**.

## Methodology
The inquiry was conducted over this repository's committed sources, not over the two archived repositories, which are not in it. Every measurement below is a count over the `.kh` tree as it stood on the date the row names, taken by reading the tree rather than by asking either archive. Each row of the disagreement table was verified against the tree, and each row names the `path:line` that carries it, so a reader can open the citation and see what was seen. Where a row's verdict is a governing document rather than a declaration, that document is cited beside it.

The JavaScript half rests on a source outside this repository: the retired `memar-js` README, never committed there and recovered by the owner on 2026-10-01. Its statements are recorded as that README's, and the finding they carry is about this repository's sources rather than about what the README says.

The known limits are these. Both archived repositories are recoverable — `memar-go` from its remote, `memar-js` at archive commit `27e013d`, last pushed 2026-01-06 — but neither was consulted here; every claim is a claim about what the sources in this repository say. The residue counts are counts of blocks, not of work: a block's size after `tidy --rule go-clue-residue` is the measure of what is left on that file, and nothing here measures that. And a block is not a transfer record, so nothing below establishes that a Go file is fully ported.

## Findings
### Where the Go and JavaScript archives disagree
Measured 2026-10-02. 815 source files carry a Go clue block, 32 carry a JS block from the archived `memar-js`, and **19 carry both** — the places where two retired repositories speak about one subject and may not agree. A difference only matters where a current declaration or a governing document takes a side, or where the sources are silent and the two contradict each other; the rest is two archives disagreeing about a retired idea, which is what an archive is for. Each row was verified against the tree.
| Subject | Go says | JS says | The sources side with |
| --- | --- | --- | --- |
| HTTP/2 and HTTP/3 | four versions under one heading, `modules/lib/net/http/const.kh:38-44` | "HTTP version 2 and above are new protocol not new version of HTTP!! So we don't support HTTP2 and HTTP3 specs in this package!!" `:329-330` — while still declaring `VersionHTTP2/3` at `:369-370` | **Go**, against JS's own contradiction: `docs/modules/lib/net/http.handoff.md:27`, `docs/modules/lib/net/http.md` framing, `protocol/pseudo_header.kh:14,30` |
| The sRPC multiplexer path | absent | `/m?{{.ServiceID}}`, `modules/lib/net/http/protocol/handler.kh:56` | **JS**: `docs/modules/net/sRPC.md:136` |
| The cookie store | protocol-level headers, `modules/lib/net/http/headers/const.kh:117-118` | `document.cookie`, `:168,177,220` | **Go**: `docs/modules/lib/net/http.md:34` names `Cookie` a credential channel of the protocol, not host-private state |
| Identifier constant naming | `snake_cap` (`Method_GET`, `Key_From`) | `PascalFlat` (`MethodGET`, `HeaderKeyFrom`) | **Go**: every live `.kh` in `modules/lib/net/http/` is `snake_cap` |
| The per-unit type name | `Cent`, `Myriad` (`modules/math/per/cent.kh:11`, `myriad.kh:11`) | `PerCent`, `PerMyriad` (`:23` each) | **Go**: the live declarations are `tp Cent ab` and `tp Myriad ab` |
| Waiting on a span | `monotonic.Time`, heap invariants (`modules/time/timer/const.kh:12-20`) | `Sleep`/`SleepBlocking` in milliseconds on the wall clock (`:27-37`) | **Go**: `docs/modules/time/time.md:36` and `time.handoff.md:34` |
| The Unix epoch's weekday | "was a Monday", `modules/time/unix/time.kh:18` | no claim | **Go's own other file**, against itself: `modules/time/unix/const.kh:11` says Thursday, and `modules/time/utc/time.kh:134` indexes from Thursday. Line 18 is the only place in the tree that asserts a weekday for the epoch |
| `MediaType` | a string alias, `type MediaType = string`, `modules/identifier/mediatype/protocol/media-type.kh:12` | an object with identity, lifecycle, and locale detail, `:60` | **neither, and it splits**: the live `tp Identifier_MediaType ab` is an abstraction, JS's five decomposition slots moved to `parsed.kh:11-21`, JS's dates to `data-type.kh:28-32` |
| `MediaType`'s `tree` slot | carried | carried | neither: `docs/modules/identifier/media-type.md:17` says "tree is empty value. we don't need this", yet `parsed.kh:17` declares `tp Tree` |
| `Error`'s identity | the ID alone, `modules/process/error/protocol/error.kh:62` | `this._id == err._id`, `:125` | **both agree**; the sources take Go's spelling through `Observer_ID`, which the document calls `Field_ID` |
| The release life-cycle states | ten (`LifeCycle_Unset` plus nine), `modules/computer/datatype/protocol/life-cycle.kh:13-35` | nine (`Software_*`, no Unset), `:46-81` | **neither, and `docs/modules/process/error.md:51` is a third**: it names four values — `Experimental`, `Stable`, `Deprecated`, `EndOfLife`. Only `EndOfLife` is common to all three |
| Authorization | nothing; `operation_p.Authorize` appears commented out, `modules/process/service/protocol/service.kh:38` | `{CRUD, UserType}` as a data record, `modules/process/error/protocol/error.kh:227-230` | **neither**: `Authorize` is declared at `modules/process/operation/protocol/authorization.kh:6` and composed into nothing; `docs/framework.handoff.md:60-63` already calls this the largest unowned cluster, and the archives confirm the gap rather than fill it |

### Disagreements the sources already decided silently
The disagreements that need no decision because the sources already picked a side silently are still worth the list: the JS block's notification widgets, `Application.RegisterWidget`, the `Giti.Platforms`/`Giti.Society` registries, and the severity constants have no counterpart in either archive or in any current declaration, and nothing in `docs/` names them.

### A finding measured and dismissed
One recorded finding was measured and dismissed: the JS transfer noted that `user_p.Type` is declared nowhere while generators reference it. Every occurrence is inside an archived Go block — `modules/codec/syllab/services/go-methods/service-generate-go-syllab-methods.kh:20` is a line of Go `import` syntax inside the block that opens at `:5`. No live declaration references it, so nothing dangles.

### The archived JavaScript, and what it did not carry
`memar-js` was archived on 2026-10-01 and 102 of its 113 files were transferred into 32 `.kh` files across 19 folders as `//` comment blocks, each naming its source in a `// source: memar-js/<path>` line, so the placement record is in the tree and needs no ledger beside it.
- **Its marker, and two spellings of it.** The block opens `// TODO(js-idea): archived memar-js source, not Khayyam and not a migration`, then `// Unverified idea from the retired memar-js repository (archive commit 27e013d, last pushed 2026-01-06). Kept as a thought only: the architect has moved on since, so this may contradict the current design.` and `// source: <path>`. `modules/identifier/mediatype/protocol/media-type.kh:15` says "archived memar-js JavaScript" where the other 32 say "archived memar-js source"; nothing says which is the form. Where the format is governed at all is the open question above on the clue block's format, which this block shares.
- **Eleven files were deliberately not carried.** Eight are third-party: `widgets/barcode/storage/*` — `axenfox/onscan.js` and the source and bundles of `samsam2310/zbar.wasm` — plus `widgets/barcode/zbar.c` (C) and `widgets/barcode/zbar-v0.wasm` (a compiled binary). Three are the retired repository's own plumbing: `.gitignore`, `LEGAL`, `LICENSE` (Apache-2.0). The barcode reader's *idea* is in the sources at `modules-plugable/computer/ui/gui/protocol/element.kh:428-444` as archived JavaScript; its scanner implementation is nowhere, and no document records that leaving it out was decided.
- **The owner's condition on a replacement scanner**, recovered from the retired repository's README, which was never committed there: a replacement library must be readable, light and dependency-free, and should preferably be implemented in Khayyam so that it serves any language rather than one.
- **The rule that governed the retirement**, from the same README: a full Go, C, or Rust rewrite comes after writing something in Khayyam; whatever Khayyam lacks gets rewritten in Go; once Khayyam has everything, the Go repository is a full rewrite. `memar-go` began with transfer and simplification, dropping `R&D` functions and conditions, and `memar-c` and `memar-rust` shared that aim; the emphasis is now on implementation quality. `memar-js`, which could have served a faster crossing, is retired.
- **What the transfer did not reach.** The same README records that a complete rewrite of `memar-go` in Khayyam had been done, but that those writings were a smaller subgroup which did not survive into the current archive — present in `memar-go`, `memar-js` and `memar`, absent from `memar-khayyam`. The README was recovered by the owner from a real address on 2026-10-01, moments before it was deleted from disk; nothing in either repository holds it.

### Subjects with no home, parked in the nearest folder that exists
Archived subjects filed where the architecture has no place for them, on the reasoning that the nearest existing home is better than none. **None is a decision to keep them there.**
| Archived subject | Parked at | Why it is not the architect's subject |
| --- | --- | --- |
| `price/currency.js`, `price/amount.js` | `modules/computer/datatype/protocol/data-type.kh:57,77` | Value is the consuming domain's to define. `docs/content.md:136` uses `Price` as an example of a field carrying a real type and never defines it |
| `region/region.js`, `regions.js` | `data-type.kh:182,232` | No document in `docs/` mentions a geographic or administrative region. The word already means something else here: `docs/content.md:119,127` and `docs/content.handoff.md:58` use *region* for a rectangular area of an image |
| `language/language.js`, `languages.js` | `modules/computer/datatype/protocol/detail.kh:68,215` | `docs/type.md` rejects external translation keyed by a string and leaves a general `Text` to the modelling layer |
| `language/persian/digit.js`, `letter.js` | `modules/computer/adt/protocol/adt.kh:66,83` | The same objection reached from the ADT side — one subject, two temporary homes |

### Two further findings no document records
Two further findings no document records, neither settled:
- **A guest identity the sources can see and cannot name.** `modules/computer/runtime/protocol/existence.kh:25,227,230,244` carries an archived browser identity built from an `RTCPeerConnection` capability probe, a `localStorage`/cookie-persisted `ThingID`, and a hash — while `docs/modules/net/giti.md:101` puts thing-scope identifiers in the hypervisor's hands. Nothing declares `Thing`, and the two disagree about who issues the identifier.
- **A numeric ID space with two subjects in it.** `detail.kh:218-226` puts `LanguageMachine = 1`, `LanguageMathematics = 2`, `LanguageMusical = 3`, `LanguageSign = 4` in the same numbers as `LanguagePersian = 5`, `LanguageEnglish = 6`, `LanguageRussian = 7` — a claim about what a language is that no document makes.

### Live problems the two archives jointly expose — defects in the sources, not findings of this inquiry
Each of the following is a fact about the current declarations, verified on 2026-10-02, and not about either archive. Each belongs to the module named in it, and **is owed a route to that module's handoff**. None has been routed, and none is a finding of this inquiry: this record states them so they are not lost with the module they were written in, not so they are answered here.
- **`modules/time/unix/` declares nothing at all** — zero `tp`, `cp`, or `vr` lines across `now.kh`, `atomic.kh`, `epoch.kh`, `const.kh` and `time.kh`. `modules/time/protocol/time.kh:9,15,19,22` therefore has no implementer.
- **`Datatype_LifeCycle` has no live state set.** `modules/computer/datatype/protocol/life-cycle.kh:2` is an empty abstraction; the constants live only inside the archived Go comment at `:13-35`, and 33 source files reference `LifeCycle_*`, `Software_PreAlpha`, or `ServiceStatePreAlpha`. `software-life_cycle.kh:4`'s `SoftwareLifeCycle ab` is a second empty abstraction, imported by nothing.
- **`Event_Methods` is declared in one place and referenced in another that has no such declaration.** Declared at `modules-plugable/computer/ui/gui/protocol/event.kh:40`; `modules-plugable/computer/ui/gui/event.kh:18,56` name `memar/process/event/protocol.Event_Methods` as the realization target, and no `process/event` protocol file declares it.
- **`TAGS` is documented and archived but declared nowhere.** `docs/modules/process/error.md:208,210` lists it as a `Detail` member; `modules/computer/datatype/protocol/detail.kh:61` archives it; no `.kh` file declares it. The sources' `Details` at `detail.kh:19-41` carries the other five, so the document's list of six matches neither archive.
- **The HTTP status vocabulary has no live home.** Both archives carry it; `modules/lib/net/http/const.kh` holds zero live declarations, `protocol/version.kh` is one line, and `protocol/status.observers.kh:6,9` demands `GetStatusCode` and `GetReasonPhrase` with nothing to answer them.
- **`Error-ID` is a named contract with no header key.** `docs/modules/net/sRPC.md:139` makes it a consumed HTTP adapter; every `Key_*` in both archives is comment-only.
- **All nine `modules/math/per/` types are bare `tp X ab`.** Both archives hang their behaviour off a `Calculate` receiver and a symbol method (`%`, `‱`) that no live declaration has; the sign survives only in a comment at `cent.kh:3` and `myriad.kh:3`.
- **`maxWhen`, `verifyTimers` and `heapAry` have no live declaration** (`modules/time/timer/const.kh:12-20`) and are referenced only from archived code, so nothing is broken today and nothing carries the heap's even-arity invariant forward.
- **JS blocks are duplicated inside single files.** `modules/process/error/protocol/error.kh:269-381` repeats `:74-186`; `modules/identifier/mediatype/protocol/media-type.kh:117-154` and `:156-217` repeat `:15-52` and `:54-115`.

### What the port did
One short account of the work whose residue the three Rules govern. On 2026-10-04 the port's residue Rules were moved out of the Khayyam language catalog into a module of their own, because none of the three is about a Khayyam program: each was judged on its own subject, and a `.kh` file with no clue block satisfies every Rule of the language catalog and violates all three, so turning them off would have changed no meaning anywhere. Whether they had anything left to govern was measured rather than assumed, and none was obsolete: 852 of the repository's 1279 `.kh` files still end in a clue block; 52 of them still hold a generic Go declaration `type Name[…]`; and the port's writer produces all three subjects afresh for every Go file it transfers — a clue block for every construct with no Khayyam form (`transfer.py:24-28`) and a `resultN`/`argN` parameter for every unnamed Go parameter (`transfer.py:533`, `corpus_port.py:1010`, `abstraction_bridge.py:340`). `result-parameter-names` is the one whose sources are already clean: the pass renamed 336 parameters in 152 files and its subject now survives only in the writer that still emits them. That is a Rule waiting for the rest of the port, not a Rule with nothing left to say, and it was kept on that reading. Enforcement did not move: all three remain source-rewrite Rules applied by `abstraction_bridge.py tidy --rule …`, and the Rule identifiers are unchanged, so the tool's own naming of them still resolves. The three Rules now live at [`rules/`](./rules/README.md) beside the tool that applies them, which reverses the 2026-10-04 refusal to file them in `targets/go/rules/` — that refusal rested on the folder being scheduled for deletion, and the owner's ruling of 2026-10-05 that Go stays a target of the toolchain settles it.

## Decisions of record
- **The port's residue is a subject a module can own** — Decided (2026-10-04, owner instruction to place the Rules and to create a module where none fits). What the port left in a `.kh` file is neither Khayyam nor Go nor a concept, which is the case `docs/rule.md` leaves to the subject's owner; three Rules with no owner and one tool to enforce them is what made a module necessary rather than convenient.
- **None of the three Rules was retired** — Decided (2026-10-04). Each still governs material the port is still producing, and 852 blocks are still to be worked through.
- **The tool's folder is not the Rules' home, though the tool applies them** — superseded as to placement by the owner's ruling of 2026-10-05 that Go stays a target of the Khayyam toolchain. The separation it rested on — the tool owns the check, not the Rule — is unchanged, and `docs/rule.md` already separates the two.

## Conclusion
The two archives disagree on twelve subjects, and on seven of them the sources have taken a side — one of those seven against the Go archive, in favour of the Go archive's own other file. On four neither archive is right, and on one of those the sources split the subject between them; on the twelfth both agree. That answer is Q1's, and the citations survive verbatim so a reader can check any row rather than take the table's word.

The JavaScript half is a record of what is missing rather than of what is present: eleven files deliberately not carried, a scanner implementation that exists nowhere with nothing recording that leaving it out was decided, a complete Khayyam rewrite of `memar-go` that did not survive into the archive, and a README that existed nowhere at all until the owner recovered it an instant before deletion. That answer is Q2's. The parked subjects are Q3's: four archived subjects filed in the nearest folder that exists, on a reasoning the record states and does not endorse.

Nothing in the language changed as a result of this inquiry, and no governing document was edited. The residue counts are a description of this repository's tree on the dates named, not a measure of the language or of the port's remaining work — a block's size after `tidy --rule go-clue-residue` is that measure, and nothing here measures it.

Nine defects the two archives jointly expose are recorded above and **have not been routed** to the handoff of the module that owns each. This target has no paired handoff, so no route existed for them at the time of this record; a reader who owns one of those modules takes the row from that section and routes it.

## Related Artifacts
- [target.md](./target.md) — the Go target this research is a companion of, and where the port's current state is stated.
- [rules/README.md](./rules/README.md) — the three residue Rules this inquiry's subject belongs to.
- [Rule → Which Module a Rule Belongs To](../../../../docs/rule.md#which-module-a-rule-belongs-to) — the criterion the placement of those three Rules applies.
- [Khayyam rules index → Which rules here are the language's own](../../rules/README.md#which-rules-here-are-the-languages-own) — where the verdict that the three are not the language's is recorded.
- [Documentation — Research](../../../../docs/documentation-research.md) — governs this artifact's structure.
- [`modules/`](../../../../modules/) — the sources this inquiry measured.

## Open Questions
These are the module's questions, carried here because the module they were written in no longer exists. Each is owed a route to the document that owns it; none has been routed.
- **Whether the residue Rules' catalog outlives the port.** `go-clue-residue` states that it retires with the last block, and the last block is 852 files away. When it goes, the question is whether this folder stays as the port's record or goes with its Rules.
- **Where the clue block's format is governed.** No governed document states the `// TODO(go-migrate):` marker or its `* /` escape; the rule states only the format it reads. The archived JavaScript blocks share the gap with no rule at all, so whether one decision governs both archive formats or two govern them separately is still open. Carried from [go-clue-residue.handoff.md](./rules/go-clue-residue/go-clue-residue.handoff.md).
- **Where the port's own ledger lives.** A block is not a transfer record, and four units are known not to be fully carried with nothing in the repository saying so. Carried from the same handoff.
- **Whether the three Rules should be merged into the port's writer.** The bridge writes `resultN` where the Go signature named nothing, and this Rule renames afterwards. Writing the derived name at transfer time would remove the Rule from the sources' work — and would remove the record of why a `result0` is not a name a reader can use. Carried from [result-parameter-names.handoff.md](./rules/result-parameter-names/result-parameter-names.handoff.md).
- **Whether a general rule engine applies this catalog too.** No engine exists, so `tidy --rule …` is the only way to apply these three. Carried from [khayyam.handoff.md → Open Questions](../../khayyam.handoff.md#open-questions).
- **The bridge still places `memar-go/modules/` at `modules/modules/`.** On 2026-10-07 that folder was distributed into the modules that own its files — the program entry, `app/` and `locale/` into [`bundles/memar/`](../../../memar/memar.md), `module/` into `computer/module/`, `service/` into `process/service/`, and so on — and its `internal/` folders were dropped, Khayyam having no use for Go's visibility-by-folder. `bundles/khayyam/targets/go/names.py:216` and the tests asserting it (`test_transfer.py:90-91`, `test_names.py:64`) were left as they are. A transfer run before the map is corrected would recreate `modules/modules/`; if one is needed, the map needs per-folder entries matching the distribution.

## Notes
- **The module this research replaces.** The material above was written as the working state of a temporary module at `modules/go-port/`, which the owner ruled must never enter version control and which this record retires. Its catalog now sits at [`rules/`](./rules/README.md) and its main document is [target.md](./target.md).
- **Repairs owed by the 2026-10-04 move, recorded so they are not rediscovered as broken links.** None is repaired by this re-homing, and `docs/` was not in this work's scope: `docs/rule.changelog.md` — the placement entry belongs on the Rule facet's own changelog, beside [The module a Rule belongs to](../../../../docs/rule.changelog.md); `docs/rule.handoff.md:99-101` — three rows of the inventory still point into `bundles/khayyam/rules/`; `bundles/khayyam/targets/js/target.handoff.md:127` and `:198` — two links into `bundles/khayyam/rules/result-parameter-names/`; `bundles/khayyam/README.md` — the local-placement table has no row for this target's rules; `docs/khayyam/khayyam.research.001.md:187` — records `rules/result-parameter-names/result-parameter-names.md:15` as a path it read, and a research record's list of what it examined is history and is left as written, so the path no longer resolves; each rule folder's `README.md` here and in the Khayyam catalog is a text file naming its target document rather than a symbolic link, which [Folder READMEs](../../../../docs/documentation.practice.md#folder-readmes) asks for and this host cannot record.
- **No citation was rewritten to make it resolve.** The carried material cited the old protocol folder nowhere: every protocol citation in it already read `docs/modules/`, which is where those documents are. The count of citations changed for that reason is zero.
