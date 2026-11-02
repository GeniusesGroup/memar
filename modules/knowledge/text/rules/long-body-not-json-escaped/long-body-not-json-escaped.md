---
Title: "Text Rule — Long Body Not JSON-Escaped"
Labels: Draft
Start Date: 2026-11-01
---
# Text Rule — Long Body Not JSON-Escaped
A rule of this repository, held for the [text](../../text.md) domain. It applies to every Memar project that stores a long prose body (Markdown or other character text) through the memory store’s Files adapter.

## The rule
- **A long Text body is stored as the text’s own character bytes** under the text domain’s part (or under the medium part the Text / content model names). The value a human reads is those characters ([Text → Model](../../text.md#model)), not a JSON string that embeds them.
- **JSON `$files.text` (and any other escaped-JSON embedding of a long body) is not a durable form Memar accepts for long prose.** That shape is a private policy of the JSON Files body codec when that codec is bound; it is not Text’s form and not a requirement of the Files adapter.
- **The Files body codec is selectable** (`files-body-codec`). JSON is one codec, first-ship default only — **not mandatory**. Memar’s intended bind is [Syllab](../../../../computer/codec/syllab/syllab.md) once a Syllab `Files_Body_Codec` exists; until then a project may bind any registered codec that does not force long prose into escaped JSON (the YAML proof codec is one such interim).
- **Domains never name the codec or inspect the body.** Writers and readers use store addresses and part bytes only ([Files → Path encoding](../../../../../modules-plugable/computer/memory/store/files/files.md#path-encoding-stated-once)).

## Why it exists
Owner ruling (2026-11-01): long Markdown inside `{"$files.text": "# …"}` is a bad durable form for Memar users; JSON must not be forced because Memar owns Syllab and will move the Files body onto it. The Files body codec seam already exists; this rule states what Text requires of that seam for long bodies.

## Keep it or drop it
An organization that wants JSON-escaped prose on disk may bind the JSON body codec and remain able to round-trip bytes, at the cost that humans and agents cannot treat the medium as readable Markdown and that Memar’s own samples and conversions will not treat that shape as done.

## What this rule does not claim
- It does not invent a second path scheme or a dedicated text “file” beside the node id ([No File Concept](../../../../../modules-plugable/computer/memory/filesystem/rules/no-file-concept/no-file-concept.md)).
- It does not decide whether Content holds media as an edge or a part — that is Content’s model.
- It does not require human-readable on-disk framing: Syllab’s goals include storage use and do not require human-easy decode; Display owns presentation. The prohibition is escaped-JSON-as-Text, not “must be YAML”.
