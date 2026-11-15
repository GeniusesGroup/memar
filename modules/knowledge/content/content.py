#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""modules/knowledge/content/content.py — the written content of a Memar checkout: read it, relate it, audit it, write it.

Reached as flat calls (`content_search`, `content_find`, …): CLI and MCP share
one name. Each verb is declared by its own service file, kept in the module
whose subject the act is: the text module for search and ranking, the Markdown
module for what is a section or a link, the documentation module for the
changelog, the questions and the check, the filesystem module for putting text
into a file. This folder keeps `resolve-path` and `path`, the two verbs that
turn a reference into a file, and the reference they share (owner, 2026-10-24).
Usage is the interface; each call's own `--help` is the authority for what it
accepts. List every call with `memar memar_commands`. What is left here is what
a help text cannot carry: why this domain exists, what its boundary is, and what
it cannot do.

**The boundary is the whole checkout, not `docs/`.** The written content of a
Memar repository is not only its Markdown: `modules/` holds the model
definitions, the rules, the protocol implementations, and `.kh` sources,
`bundles/` holds what runs or aggregates those modules, and `.agents/` holds
the configuration a task is driven by. A tool named for
content that could not search code would be a tool for documents. So `search`,
`backlinks`, `obligations`, and the Memar half of `check` all read across the
checkout, and the folders a reader does not want are excluded rather than the
ones they happen to live in. The tasks' records are content too, but each is
one task's claim and never a ruling, so `find` and `search` read them only
when asked with `--from tasks` (`primitive/corpus_source.py`), from the
records branch and the live task folders, and every hit names the task. See [Lib → The rule](../modularity/labels/guest.md#the-rule)
for the shape of that reasoning applied elsewhere: the subject decides the
folder, and a name that states a narrower subject than the file serves is a
name that will be believed.

**The Memar root is not decided here.** `machine/env_location.py` is the one place
that reads the location variable, and `bundles/memar/services/location/memar_location.py` resolves the root from
it; each verb asks that module once when it runs, and nothing decides for
itself. Minting a document ID asks the clock rather than the checkout, so it
works on a machine that has not installed Memar at all.

**What a verb needs is imported when it runs.** Every `memar` invocation imports
every module of this domain to assemble its command line, so a module here
holds only light standard-library imports at its top, and the root, the lock,
and the repository test are reached inside the verb that uses them.
"""
from __future__ import annotations
VERB = 'content'
# No `describe`: public calls are flat (`content_search`, …). List them with `memar memar_commands`.
