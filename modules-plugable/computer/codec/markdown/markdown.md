---
Title: "Markdown"
Status: Draft
Start Date: 2026-10-24
ID: 498006
---

# Markdown
## Abstract
**Markdown** is a text format Memar does not own: its syntax is the outside world's (CommonMark and GitHub Flavored Markdown), and a document written in it is one representation of content, never the content ([Content](../../../../modules/knowledge/content/content.md)). This module is Memar's side of that surface and nothing else: the services that read a Markdown document as the format defines it — what is a link and what is only text about one, the anchor a heading makes, a section from its heading to the next of its level, the front matter and the Abstract, and which documents link to a file. It is a [guest](../../../../modules/knowledge/modularity/labels/guest.md) module, filed under the codecs, the modules it attaches to (a format is read and written by a codec, not a concept of knowledge; owner, 2026-10-24) ([Pluggable](../../../../modules/knowledge/modularity/labels/pluggable.md)), and is removable whole: [Text](../../../../modules/knowledge/text/text.md) and [Documentation](../../../knowledge/documentation/documentation.md) stay whole without it.

## What it holds
- `markdown.py` and `links.py`: the links of a document and the anchors of its headings, judged as the format makes them.
- `content_get_section.py` and `content_section.py`: one section of a document (`memar content get-section`, `memar content section`).
- `content_get_meta.py` and `content_meta.py`: front matter and Abstract (`memar content get-meta`, `memar content meta`).
- `content_backlinks.py`: the documents that link to a file (`memar content backlinks`).

## What it does not hold
- Memar's own conventions for a written document (no blank line under a heading, the citation layers, the lists of normative references): those are [Documentation](../../../knowledge/documentation/documentation.md)'s, and they apply because Memar wrote them, not because Markdown asks for them.
- Reading and writing files: a service here takes text and returns text. The storage layer is not a service's concern ([memory port programme](../../../../.agents/tasks/20261022-T185903Z-15504/docs/change-plan.md)).

## Open
How [Text](../../../../modules/knowledge/text/text.md) learns that a document has parts is not yet a relationship text exposes: `index.py` there loads `content_get_section` at run time. The relationship is to be designed with the Text domain's own development (owner, 2026-10-24: text itself may have no view of the structure it holds, so the first design may be wrong and is corrected in the modules' own course).
