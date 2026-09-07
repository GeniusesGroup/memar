---
name: document-explanation-creator
description: Use when creating a new formal explanation document, or when revising an existing one to bring it in line with the current specification.
---

# How to make a new explanation document
This is the procedure for producing an Explanation-facet document that follows `documentation-explanation.md`. It assumes you already know, or will look up as needed, what each field and section in that specification means. This file only covers the steps, not the deep definitions.

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
4. Write the body.
   - `Abstract`, `Introduction` (`Motivation`, `Methodology`) stay unified, document-wide prose.
   - Under `Explanation`, split the content into topics; nest `#### {Sub section title}` under a topic where finer structure helps. See `documentation-explanation.md`'s `Optional Sections` for the optional building blocks (`Motivation`, `Methodology`, `Risks`, `Implications`, and others) and place them wherever the content calls for them. Cite premise evidence for a claim inline, at the claim it supports.
   - Exercise the thinking modes while writing — critical examination of your own claims is one component of writing, applied while drafting, not a separate later phase. When critique of a draft is the dominant activity rather than a component of writing it, [thinking.practice.md](./thinking.practice.md) covers that exercise.
   - Document-wide optional sections sit directly under the body's top level, not inside any topic.
   - Do not put considered-and-rejected alternatives, open questions, or anticipated work in the body: alternatives go to the changelog entry's `Considered and not done` section, open questions to the handoff's `Open Questions`, anticipated work to the handoff's `Anticipated Work` (steps 6-7).
   - Leave `Results` empty unless there is real, observed outcome to report — it is retrospective, not a prediction made while writing the document.
5. If this is a revision of a document written under an earlier version, bring it in line with the current structure at this edit — see `documentation-explanation.md`'s "Progressive migration" topic.
6. Create or update the paired Changelog-facet file `<same-slug>.changelog.md` alongside the base document. Its first entry records the document's creation (and, if this is a revision of an older document, migrates any `Citations`, `Contributors`, `Applied to` front-matter fields and `## Change Rationale` body content from the old version into Changelog entries — see `documentation-changelog.md` for the entry structure). The base document keeps none of that provenance in its own front matter or body.

## The Template
This is illustrative, not normative — it shows the shape every document starts from, not a rigid enforcement of exactly what must be present. Copy everything below into a new file and replace every placeholder.

```
---
Title: ""
Status: Draft
Start Date: ""
ID: ""
---

# Document Title

## Abstract

## Introduction

### Motivation

### Methodology

### {Sub section} (Can be one of Optional Sections)

## Explanation

### {Section}

#### {Sub section} (Can be one of Optional Sections)

## Results
```

## Reference files
Use below paths or fetch the relevant document via [`memar` SKILL](../.agents/skills/memar/SKILL.md) rather than inventing an answer.
- [documentation.md](./documentation.md) — meta-layer: defines Facets, names current facets, and defines cross-cutting conventions (Citations, URI) that apply to every facet.
- [documentation-explanation.md](./documentation-explanation.md) — the Explanation facet specification this procedure follows.
- [documentation-changelog.md](./documentation-changelog.md) — the Changelog facet specification; the paired `<base>.changelog.md` file created in step 6 follows this structure.
