---
RFC Number: 495002
Title: "RFC Numbering Scheme"
Status: Proposed
Start Date: 2026-07-04
Applied to: []
Supersedes: null
Superseded by: null
Related:
  Depends_on: []
  Extends: []
  Conflicts with: []
Contributor(s):
  - name: "Omid Hekayati"
    uri: "mailto:omid@geniuses.group"
    contribution: ""
    task: []
  - name: "Claude"
    uri: "https://claude.ai"
    model: "claude-sonnet-5"
    effort: "Medium - extended thinking enabled"
    contribution: "Drafted initial text, argued for and against alternatives, incorporated revisions"
    task: []
---

## Summary
RFC Number is a UTC unix-time-derived integer, generated once when the RFC file is first drafted, and never reused or reassigned afterward. It carries no meaning about domain, subsystem, or importance — only relative creation order. Generating the number does not imply the RFC is approved, ready, or stable; that is the job of the `Status` field, entirely independent of the number. Filenames do not contain the number; they contain only a short, human-readable, hyphenated slug derived from the Title. The number lives solely in the `RFC Number` front-matter field and is looked up via full-text search or the README index, not via the filename or directory position.

## Motivation
Three separate problems, discovered across earlier attempts at this project, motivate this RFC:
1. **Domain-encoded ranges create coupling.** An earlier informal scheme reserved number ranges per domain (e.g. 1–999 for Khayyam). This tied a supposedly permanent identifier to a classification that can itself change over time (e.g. deciding the standard library should be its own domain, separate from Khayyam). Any such reclassification would force renumbering, and renumbering breaks every existing cross-reference (`Depends_on`, `Extends`, `Supersedes`) across the whole RFC graph.
2. **A single incrementing counter needs a coordinator.** A project intended to span multiple generations and, potentially, multiple contributors working without constant synchronization cannot safely rely on a single "next number" counter without some registration authority.
3. **Encoding domain or filename content into the number is redundant with, and weaker than, other fields.** `Start Date` already records chronology explicitly; a domain field (if one exists) already records classification explicitly. The number does not need to duplicate either.

## Guide-level explanation
When starting a new RFC:
1. Copy `rfc-template.md` to `<short-descriptive-slug>.md` (no number in the filename — e.g. `sRPC-connection-identity.md`, not `001500-sRPC-connection-identity.md`).
2. Generate `RFC Number` at the time the file is first drafted, using the current UTC time truncated to the hour (see Reference-level explanation for the exact command). Whoever creates the file generates the number; there is no requirement that it be generated specifically at commit time.
3. Once set, this number never changes again for the lifetime of the RFC — even if the RFC is later rejected, superseded, or the title/slug is revised (a title change that alters the concept is treated as a new RFC per existing convention, with its own new number). Assigning a number says nothing about whether the RFC is approved — that is what `Status` is for.
4. To find an RFC by number later, use a text search for `RFC Number: <value>` across the RFCs folder, or consult the README index, which lists Number, Title, and Status together.

## Reference-level explanation
- **Value**: UTC unix time truncated to the hour — i.e. `(unix seconds) / 3600`, taken as an integer — written as a plain decimal integer (e.g. `495317`). UTC is mandatory to avoid ambiguity across contributors in different time zones. This keeps the number roughly six digits for the foreseeable future (it does not reach seven digits until roughly the year 3110), close in length to the numbers already in use in the RFCs folder today.
- **Generation**: any command that yields this value is acceptable; the RFC does not mandate a specific tool, only that the method be simple and available without special setup. Known-working examples per platform:
  - **Linux / macOS (bash or zsh)**: `echo $(( $(date -u +%s) / 3600 ))` — works as-is on both, since macOS's built-in `date` also supports `%s`.
  - **Windows (PowerShell)**: `[math]::Truncate([DateTimeOffset]::UtcNow.ToUnixTimeSeconds() / 3600)`
  - **Any platform with Python installed** (a convenient fallback if the above are inconvenient): `python3 -c "import time; print(int(time.time()//3600))"`
- **Uniqueness and collisions**: because the unit is an hour rather than a second, it is expected and normal — not a rare edge case — for two or more RFCs drafted in the same working session to land in the same hour (this has already happened in practice: the four Chapar RFCs were produced in a single session). When this happens, resolve it manually and simply: keep the first RFC's number as generated, and give the next one the following hour's value (or any other free value), regardless of whether that hour has actually passed yet. No sub-hour precision or automated tie-breaking is defined.
- **Filename**: `<slug>.md`, where slug is a short, hyphenated, lowercase-or-natural-case rendering of the Title, with no number and no domain prefix. The slug is expected to remain stable once the RFC reaches Final status, consistent with the existing rule that a meaningful rename constitutes a new RFC.
- **Retroactive numbering for pre-existing RFCs**: RFCs written before this scheme was adopted may be assigned an hour-value derived from their recorded `Start Date` (e.g. midnight UTC of that date) if and when they are retroactively renumbered. Where multiple pre-existing RFCs share the same `Start Date`, order them by reasonable, manual judgment (e.g. their current legacy number) — no strict formal rule is imposed for this.
- **Storage representation**: out of scope for this RFC. How this number is represented in code (integer width, signedness, etc.) is an implementation detail for whichever system needs to store or process it, not a constraint this RFC imposes.
- **Lookup**: because the number is not in the filename, discovery relies on (a) full-text search for the `RFC Number:` field, and (b) the README index table, which lists Number, Title, and Status.

## Drawbacks
- The number is no longer purely arbitrary — it now encodes creation order, which is a form of meaning. This is a deliberate exception to the earlier "the number should carry no meaning" principle, justified because creation time is an immutable historical fact and cannot later be "reclassified" the way a domain label can.
- Collisions at hour granularity are expected to occur regularly during multi-RFC working sessions, not just in rare theoretical cases, and must be resolved by a human each time rather than automatically, Or can resolved by automated script run in the related PR(Pull Request).
- Retroactive backfilling for pre-existing RFCs sharing the same `Start Date` has no principled ordering signal (only date-level, not hour-level, precision is actually recorded for them), so their relative order among each other will be a manual judgment call rather than a historically exact reconstruction.

## Rationale and alternatives
- **Domain-encoded ranges (rejected)**: couples the identifier to a classification that can change, forcing renumbering and broken cross-references when it does.
- **Single incrementing counter, assigned at creation (rejected)**: requires a central coordinator to avoid collisions in any scenario with more than one simultaneous contributor.
- **Single incrementing counter, assigned only at "Final" / merge time (a leading alternative, not chosen here)**: this is the approach used by the Rust RFC process (see Prior art) — files carry a `0000-` placeholder until a natural, already-unique event (the pull request number) is available, and are renamed only then. This avoids the coordination problem without needing timestamps, and never assigns a number to unstable Draft content. It was not chosen here because a number that exists from the moment an RFC is first drafted was preferred, including so that very old, already-existing ideas could in principle be assigned identifiers retroactively based on when they were actually conceived.
- **Second-level unix timestamp (considered, not chosen)**: minimizes collisions almost entirely but produces a ten-digit number, noticeably longer than the numbers currently in use, for a benefit (near-zero collision risk) that this project's actual RFC-writing pace does not need.
- **Hash of the filename/slug (rejected)**: does not provide content-integrity guarantees (the underlying content can still change after the hash is fixed, since the hash is computed from the name, not the content), produces a long, non-memorable identifier, and does not solve any problem that an hour-based counter does not already solve more simply.

## Prior art
The Rust RFC process assigns no number when an RFC is first drafted; the file is created with a `0000-` placeholder, and the RFC's number is set only once a pull request exists, using that pull request's own number, at which point the file is renamed. Rust's own internal design discussion around this scheme explicitly considered and rejected using something other than a small, continuous-feeling number, on the grounds that continuous small numbers are more attractive to work with than sparse or arbitrary ones, even though using the PR number leaves gaps.

IETF RFCs are also strictly sequential and assigned by a central RFC Editor, with no domain-based range reservation; the number denotes only publication order, not subject matter.

## Unresolved questions
None remaining. The one open questions from the earlier draft — whether to use hour- or minute-level granularity — were resolved during discussion: hour-level granularity is adopted.

## Future possibilities
- A small helper script or shell alias that prints the current hour-value and optionally checks the RFCs folder for an existing collision before a new file is created, once the number of contributors or RFCs justifies the tooling investment.
- If the pace of RFC production, or the number of concurrent contributors, grows enough that hour-level collisions become frequent and burdensome — rather than the occasional same-session overlap seen so far — minute-level granularity should be reconsidered. This is not expected in the near term but is worth revisiting if the project's contributor base grows, since manual, in-person resolution of a collision assumes the colliding authors become aware of each other at the point of merging, which holds less reliably once more than one person is producing RFCs independently and asynchronously. As said earlier it can resolved by automated script run in the related PR(Pull Request).
