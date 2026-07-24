---
name: document-explanation-creator
description: Use when creating a new formal explanation document, or when revising an existing one to bring it in line with the current specification.
---

# How to make a new explanation document
This is the procedure for producing a document that follows `documentation.md`. It assumes you already know, or will look up as needed, what each field and section in that specification means. This file only covers the steps, not the deep definitions.

## Steps
1. Copy the [The Template](#the-template) section into a new file named `<short-descriptive-slug>.md` — no number, no domain prefix, just a short, hyphenated, human-readable slug derived from the Title.
2. Set `ID` to the current UTC hour-count, and never change it again.
   - Linux/macOS: `echo $(( $(date -u +%s) / 3600 ))`
   - Windows PowerShell: `[math]::Truncate([DateTimeOffset]::UtcNow.ToUnixTimeSeconds() / 3600)`
   - Any platform with Python: `python3 -c "import time; print(int(time.time()//3600))"`
3. Fill in the rest of the front matter:
   - `Title`: short, quoted, unique.
   - `Status`: start at `Draft`.
   - `Start Date`: today's date (UTC), matching the moment `ID` was generated.
   - `Applied to`: leave `[]` until the document reaches `Final`.
   - `Citations`: leave `[]` if none apply; otherwise one entry per cited source, with `Relation` one of `Reference`, `Depends_on`, `Depends_for`, `Extends`, `Extends_by`, `Conflicts`, `Superseded`, `Superseded_by`, and `Reason` explaining why.
   - `Contributors`: one entry per contributor, each with at least one `Tasks` item (`Works` — an array of very short, headline-style strings describing what was done — plus optional `URI`). AI contributors also add `Model` and `Effort`.
4. Write the body.
   - `Abstract`, `Introduction` (`Motivation`, `Methodology`) stay unified, document-wide prose.
   - Under `Explanation`, split the content into topic subsections; give each topic its own `#### Discussion` (`Drawbacks` / `Rationale and alternatives` / `Prior art` / `Unresolved questions` / `Future possibilities`) only where the topic genuinely has something to say, never as an empty header. For a topic needing finer sub-sections, nest `#### {Sub section title}` under it. A topic may also propose its own `Conventions` — see `documentation.md`'s "Optional Sections" for this and other optional building blocks; placement is flexible beyond the fixed top-level sections.
   - If a single topic can answer the document's central question on its own, name it for what it does, list it first, and link it from the Abstract labeled "Guide." Anything that applies to the whole document rather than one topic goes in the document-wide `Discussion` section, not into any topic's own bundle.
   - Leave `Results` empty unless there is real, observed outcome to report — it is retrospective, not a prediction made while writing the document.
5. If this is a revision of a document written under an earlier version, bring it in line with the current structure at this edit

## The Template
This is illustrative, not normative — it shows the shape every document starts from, not a rigid enforcement of exactly what must be present. Copy everything below into a new file and replace every placeholder.

```
---
Title: ""
Status: Draft
Start Date: ""
ID: ""
Applied to: []
Citations:
    - Title: ""
      URI: ""
      Relation: ""
      Reason: ""
Contributors:
  - Name: ""
    URI: ""
    Tasks:
      - Works: []
        URI: ""
---

# Document Title

## Abstract

## Introduction

### Motivation

### Methodology

## Explanation

### {A freely-named, illustrative topic answering the document's central question on its own — optional; list it first and link it from Abstract labeled "Guide" if it exists}

### {Section title}
{Description text}

#### {Sub section title}
{Description text}

#### Discussion

##### Drawbacks

##### Rationale and alternatives

##### Prior art

##### Unresolved questions

##### Future possibilities

## Results

## Discussion

### Drawbacks

### Rationale and alternatives

### Prior art

### Unresolved questions

### Future possibilities

## Change Rationale
```

## Reference files
use below paths or fetch the relevant document via `memar-navigator` rather than inventing an answer.
- [documentation.md](../../../documentation.md)
