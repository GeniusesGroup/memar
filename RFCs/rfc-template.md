---
Title: "RFC Template" # "{Unique name}"
Status: Proposed # Draft | Proposed | Final | Superseded | Rejected
Start Date: 2026-06-30
RFC Number: 495000 # PLACEHOLDER — generate per rfc-numbering.md at file creation time.
Applied to: ["*"] # File-URI, * means applied to all rfc in `memar` e.g. ["Khayyam.md#control-flow"] — empty until pasted into the target doc
Related RFCs:
    - Title: "RFC Unique name"
      URI: "" # RFC uri
      Reason: "" # Reference | Depends_on | Depends_for | Extends | Extends_by | Conflicts (left non-empty only if a real, still-unresolved tension exists) | Superseded (obsolete other RFC)  | Superseded_by (obsolete by other RFC)
      Explanation: ""
Contributor(s):
  - Name: "Omid Hekayati"
    URI: "mailto:omid@geniuses.group"
    Contribution: ""
    Tasks: 
      - Titles: [] # e.g. `Model financial account`, ...
        URI: "" # Task uri such as `chat share url`, `issue url`, ...
        Explanation: ""
  - name: "Claude"
    URI: "https://claude.ai"
    Model: "claude-sonnet-5"
    Effort: "Medium - extended thinking enabled"
    Contribution: "Drafted initial text, argued for and against alternatives, incorporated revisions"
    Tasks:
      - Titles: [] # e.g. Model `financial account`, ...
        URI: "" # Task uri such as `chat share url`, `issue url`, ...
        Explanation: ""
---

# RFC
A [Request for Comments (RFC)](https://en.wikipedia.org/wiki/Request_for_Comments) is a publication in a series from the principal technical development and standards-setting bodies. Replace any part of this file with your desire RFC text.

## Summary
One paragraph explanation of the decision/feature.

## Motivation
What problem in software development is this solving? Concrete pain points and use cases.

## Guide-level explanation
Explain as if teaching a new developer: introduce the concept, show examples, explain how it changes the way they think and write code.

## Reference-level explanation
The technical detail: exact syntax, interaction with other language features, edge cases.

### Suggested Naming Conventions (optional — delete this subsection if not applicable)
If this RFC introduces a new family of types, methods, or files whose naming is not already fixed by another RFC, state the suggested naming convention here (e.g. a required prefix, a suffix pattern, or a file/slug convention). Note explicitly that it is a non-binding convention: enforcement, if any, is a per-organization Linter configuration choice, not a language-level requirement.

## Drawbacks
Honest accounting of the costs of this decision — what gets harder, not just what gets better.

## Rationale and alternatives
- Why is this the best design among alternatives considered?
- What alternatives were rejected, and why?
- What is the impact of *not* doing this?

## Prior art
What do other languages/ecosystems do here? What worked, what didn't?

## Unresolved questions
What is still open and intentionally deferred to a future RFC or to tooling?

## Future possibilities
Natural extensions or related ideas, out of scope here but worth recording.

## Change Rationale
Explanation of the fundamental reasons this RFC changed in each revision.
<!-- TODO::: Really need this part? Is it duplicate functionality with version control like GIT?? -->
