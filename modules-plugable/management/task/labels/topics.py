#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""modules-plugable/management/task/labels/topics.py — the streams of work this project's tasks are labelled by, declared once.

A topic that names no module labels a stream of work, and a stream of work is
the task domain's ([Label → Where labels are declared](../../../../modules/knowledge/label/label.md#where-labels-are-declared)).
Which streams an organization runs is its own choice, so they are declared
here, in the task domain's pluggable part, and not in the kernel task module
([Kernel Neutrality → The rule](../../../../modules/knowledge/modularity/rules/kernel-neutrality/kernel-neutrality.md#the-rule)).
A topic that names a module is declared by that module.

Each identifier was minted once and is never changed: task records cite it, and
a search for it finds every record that took the topic. A new stream is a new
line here, with a new identifier and the sentence that says what work it
names; `memar label add` prints both for a word declared nowhere. A word may be
refined and keep its identifier (`memar-tasks` was `memar-sessions`); a stream
whose concept changed ends, with the date and the topics that replace it.
"""
from __future__ import annotations
from modules.knowledge.documentation.plan.labels.topic import topic
LABELS = (
    topic('memar-scripts', '01a14a13-1972-7b1b-8056-e00b30bb0067', "Memar's own scripts and the `memar` command: what each verb does, and the module that holds it."),
    topic('memar-khayyam-types', '01a14a13-1980-7a5f-8be8-e766626965a0', "Memar's own types written as Khayyam types."),
    topic('memar-documentation', '01a14a13-19a1-73a4-9827-b2de020e5476', "Memar's documentation and the content services that read, check and write its documents."),
    topic('memar-boundary', '01a14a13-19b8-7327-94b4-e9a6c6f53ce4', "What belongs in Memar and what belongs outside it, in organization, a library or another project, and the moves that follow."),
    topic('memar-tasks', '01a14a13-19cc-7794-96e1-38952aab81f5', "Memar's task records and the tooling that opens, queues, claims, archives and sweeps them."),
    topic('memar-modules', '01a14a13-19fb-729d-838f-ca7b1fd0e043', "Surveying Memar's modules and upgrading them one module at a time."),
    topic('localization', '01a14a13-1a0e-7dc1-aa1d-a880b7fd45b2', "How a type's words are given in each human language: its details and their files."),
    topic('memar-docs-hygiene', '01a14a13-1a27-798f-bbc4-16921e7f67a0', "Keeping each of Memar's documents in its facet and home: handoffs swept, questions moved to the document they concern."),
    topic('memar-languages', '01a14a13-1a3a-7365-bc2b-112e0ebb062e', "The types of the human languages Memar supports, and the abstraction of how each is written."),
    topic('memar-khayyam-conversion', '01a14a13-1aab-74ec-84e2-c78cd526f2b2', "Converting the Go left in Khayyam files to Khayyam, module by module."),
    topic('knowledge', '01a14f34-bd79-73d9-b20c-3ccb0034fe0a', "Work across the modules of the knowledge category; a category holds modules and no declarations, so the stream is declared here."),
    topic('adapter', '01a14aae-4f4c-7618-a0e2-ab43ef3da0ab', "The adapter executable a project such as organization gives Memar's `.agents/`."),
    topic('concept', '01a15043-2a68-792b-af93-53b6b152c023', "Modeling a concept before it is placed in a module; no record the search reaches carries it, so this sentence is read from its word."),
    topic('import-relocation', '01a1508b-7a5d-7448-870a-396c655df680', "Moving imports to the modules that now hold what they import; no record the search reaches carries it, so this sentence is read from its word."),
    topic('owner-sitting', '01a150bd-710b-7bab-8bcb-0eafafa6f3b3', "Work done in a sitting with the owner present; no record the search reaches carries it, so this sentence is read from its word."),
    topic('legacy-archive', '01a154a5-4510-7194-965d-0273c985375f', "Reviewing the old archive of services and GUI against Memar's modules, and deciding what of it is kept."),
    topic('agent-facing-skill-and-scripts', '01a154e2-a32b-7c06-b910-db3f22dd8695', "The Memar skill and the scripts an agent reads and runs."),
    topic('agent-autonomy', '01a16468-aa1d-765e-84f5-4bfabf5d1ec8', "Why agents hand questions to the owner instead of finding the answers in Memar, and the fixes."),
    topic('memory-port', '01a167b9-f20e-7305-95a0-e055447a1869', "The memory port and its adapters, and the task verbs and records moved onto it."),
    topic('memar-skill', '01a155a9-fc6c-7489-8fbd-92cbdce9b6fc', "The Memar skill file and what every task pays to read before its first step."),
    topic('memar-cli', '01a15a79-c9c2-735a-bbd8-da6731e1bc68', "The names of the `memar` command's verbs and of the services behind them."),
)
