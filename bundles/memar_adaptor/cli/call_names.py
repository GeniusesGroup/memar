#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
import argparse
import re
from copy import copy
from dataclasses import dataclass
from modules.process.service.primitive.call_name import call_name
from modules.process.service.errors.call_name import CallNameCollision


@dataclass(frozen=True)
class LegacyDetails:
    domain: str
    name: str

    def Domain(self):
        return self.domain

    def Name(self):
        return self.name


def legacy_details(words):
    if not words:
        return LegacyDetails('Memar', 'memar')
    return LegacyDetails(' '.join(words[:-1]) if len(words) > 1 else 'Memar', words[-1])


def call_of_module(module_name: str, service_name: str) -> str:
    """Provisional flat call from a service or widget module path and its declared Name.

    Domain is the folder leaf above `services/` or `widgets/` in MODULE_NAME (the
    same leaf the router uses when a twin file is absent). Do not hard-code the
    resulting string at call sites — ask again through this when the name is needed.
    """
    parts = module_name.split('.')
    domain = 'Memar'
    for role in ('services', 'widgets'):
        try:
            domain = parts[parts.index(role) - 1]
            break
        except (ValueError, IndexError):
            continue
    return call_name(LegacyDetails(domain, service_name))


def _children(parser):
    return next((a for a in parser._actions if isinstance(a, argparse._SubParsersAction)), None)


def _parent_parameters(parser):
    inherited = copy(parser)
    inherited._actions = [a for a in parser._actions if not isinstance(a, (argparse._HelpAction, argparse._SubParsersAction))]
    inherited._action_groups = []
    for group in parser._action_groups:
        kept = copy(group)
        kept._group_actions = [a for a in group._group_actions if a in inherited._actions]
        if kept._group_actions:
            inherited._action_groups.append(kept)
    return inherited


def flat_parser(parser):
    flat = argparse.ArgumentParser(prog=parser.prog, description=parser.description,
                                   epilog=parser.epilog, formatter_class=parser.formatter_class)
    verbs = flat.add_subparsers(title='services', dest='_memar_call', metavar='<verb>', required=True)
    known = {}
    visited = set()
    groups = []

    def add(current, words, parents, summary):
        children = _children(current)
        if children is not None:
            if words:
                groups.append(words)
            summaries = {a.dest: a.help for a in children._choices_actions}
            for word, child in children.choices.items():
                add(child, (*words, word), (*parents, current), summaries.get(word, ''))
            return
        if id(current) in visited:
            return
        visited.add(id(current))
        details = getattr(current, '_memar_details', None) or legacy_details(words)
        name = call_name(details)
        if name in known:
            raise CallNameCollision(f'service call name {name!r} is declared by both {known[name]!r} and {words!r}')
        known[name] = words
        leaf = verbs.add_parser(name, parents=[*(_parent_parameters(p) for p in parents), current],
                                add_help=False, help=summary, description=current.description,
                                epilog=current.epilog, formatter_class=current.formatter_class)
        leaf._memar_details = details
        leaf._memar_call_name = name
        leaf._memar_legacy_words = words
        if summary == argparse.SUPPRESS:
            verbs._choices_actions = [a for a in verbs._choices_actions if a.dest != name]

    add(parser, (), (), '')

    def rendered(text):
        if not isinstance(text, str):
            return text
        for name, words in sorted(known.items(), key=lambda pair: len(pair[1]), reverse=True):
            old = r'[ \t]+'.join(re.escape(word) for word in words)
            text = re.sub(r'\bmemar[ \t]+' + old + r'(?![\w-])', 'memar ' + name, text)
        for words in sorted(groups, key=len, reverse=True):
            old = r'[ \t]+'.join(re.escape(word) for word in words)
            text = re.sub(r'\bmemar[ \t]+' + old + r'[ \t]+--help\b', 'memar --help', text)
        return text

    for shown in (flat, *verbs.choices.values()):
        shown.description = rendered(shown.description)
        shown.epilog = rendered(shown.epilog)
        for action in shown._actions:
            action.help = rendered(action.help)
    for action in verbs._choices_actions:
        action.help = rendered(action.help)
    return flat
