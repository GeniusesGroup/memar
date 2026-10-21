#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""mcp/services/_tools.py — Memar's verbs as MCP tools: each tool made from what its verb declares, and a call turned back into the verb's arguments.

The command line the services declare is the one authority for what a verb accepts and what its
help says (the router's docstring), so a tool is generated from it and nothing about a verb is
written here. A tool is one leaf verb: its name the verb's words joined by `_`; its description the
summary the verb declared and its overview; its input one property per argument, named by the
argument's own word (`--no-links` is `no_links`), typed by what the argument takes, and described by
the argument's own help. One property more, `stdin`, is what the verb reads on standard input,
because a verb such as `content write` takes its text there.

A call is turned into the arguments the CLI would be typed with, and run by the same parser: a value
the verb would refuse is refused by the verb, in its own words, as the CLI refuses it.
"""
from __future__ import annotations
import argparse
from typing import NamedTuple
STDIN = 'stdin'
NAME_SEPARATOR = '_'
JSON_TYPES = {int: 'integer', float: 'number'}

class Argument(NamedTuple):
    """One argument of a verb: the argparse action that declares it, its property's name, and the flag it is typed with."""
    action: argparse.Action
    name: str
    flag: str | None

    @property
    def counted(self) -> bool:
        return isinstance(self.action, argparse._CountAction)

    @property
    def switch(self) -> bool:
        return self.action.nargs == 0 and (not self.counted)

    @property
    def many(self) -> bool:
        return isinstance(self.action, argparse._AppendAction) or self.action.nargs in ('*', '+', argparse.REMAINDER) or (isinstance(self.action.nargs, int) and self.action.nargs > 1)

class Tool(NamedTuple):
    words: tuple[str, ...]
    parser: argparse.ArgumentParser
    summary: str
    arguments: tuple[Argument, ...]

    @property
    def name(self) -> str:
        return NAME_SEPARATOR.join(self.words)

class Refused(ValueError):
    """A call whose arguments do not fit the tool's input; its message says which and why."""

def _sub_verbs(parser: argparse.ArgumentParser) -> argparse._SubParsersAction | None:
    return next((action for action in parser._actions if isinstance(action, argparse._SubParsersAction)), None)

def _arguments(parser: argparse.ArgumentParser) -> tuple[Argument, ...]:
    found = []
    for action in parser._actions:
        if isinstance(action, (argparse._HelpAction, argparse._VersionAction, argparse._SubParsersAction)):
            continue
        if action.help == argparse.SUPPRESS:
            continue
        if action.option_strings:
            flag = max(action.option_strings, key=len)
            name = flag.lstrip('-').replace('-', '_')
        else:
            flag, name = (None, action.dest)
        found.append(Argument(action, name, flag))
    return tuple(found)

def tools(parser: argparse.ArgumentParser, left_out: tuple[str, ...]=()) -> list[Tool]:
    """Every leaf verb of PARSER as a tool, in the order the command line lists them, but the verbs LEFT_OUT and theirs."""

    def walk(parser, words, summary):
        verbs = _sub_verbs(parser)
        if verbs is None:
            yield Tool(words, parser, summary, _arguments(parser))
            return
        summaries = {each.dest: each.help or '' for each in verbs._choices_actions}
        for word, child in verbs.choices.items():
            if not words and word in left_out:
                continue
            yield from walk(child, (*words, word), summaries.get(word, ''))
    return list(walk(parser, (), ''))

def _schema_of(argument: Argument, parser: argparse.ArgumentParser) -> dict:
    action = argument.action
    if argument.switch:
        schema = {'type': 'boolean'}
    elif argument.counted:
        schema = {'type': 'integer', 'minimum': 0}
    else:
        item = {'type': JSON_TYPES.get(action.type, 'string')}
        if action.choices is not None:
            item['enum'] = list(action.choices)
        schema = {'type': 'array', 'items': item} if argument.many else item
    text = parser._get_formatter()._expand_help(action) if action.help else ''
    if argument.flag:
        text = f'{argument.flag}: {text}' if text else argument.flag
    if text:
        schema['description'] = text
    return schema

def _required(argument: Argument) -> bool:
    action = argument.action
    if argument.flag:
        return bool(action.required)
    return action.nargs not in ('?', '*')

def definition(tool: Tool) -> dict:
    """TOOL as `tools/list` gives it."""
    properties = {argument.name: _schema_of(argument, tool.parser) for argument in tool.arguments}
    properties[STDIN] = {'type': 'string', 'description': 'text the verb reads on standard input; empty when not given'}
    description = tool.summary
    if tool.parser.description and tool.parser.description.strip() != tool.summary.strip():
        description = f'{tool.summary}\n\n{tool.parser.description}' if tool.summary else tool.parser.description
    return {'name': tool.name, 'title': 'memar ' + ' '.join(tool.words), 'description': description, 'inputSchema': {'type': 'object', 'properties': properties, 'required': [argument.name for argument in tool.arguments if _required(argument)], 'additionalProperties': False}}

def _text(value, argument: Argument) -> str:
    if isinstance(value, (dict, list)) or isinstance(value, bool):
        raise Refused(f'{argument.name} takes one value, not {json_name(value)}')
    return str(value)

def json_name(value) -> str:
    return {bool: 'a boolean', list: 'a list', dict: 'an object', str: 'a string', type(None): 'null'}.get(type(value), 'a number')

def argv(tool: Tool, given: dict) -> tuple[list[str], str]:
    """The arguments the CLI would be typed with for a call of TOOL with GIVEN, and the text for its stdin."""
    if not isinstance(given, dict):
        raise Refused('the arguments of a tool are an object')
    known = {argument.name for argument in tool.arguments} | {STDIN}
    unknown = sorted(set(given) - known)
    if unknown:
        raise Refused(f"{tool.name} takes no argument named {', '.join(unknown)}")
    stdin = given.get(STDIN) or ''
    if not isinstance(stdin, str):
        raise Refused(f'{STDIN} is a string')
    options: list[str] = []
    positionals: list[str] = []
    separate = False
    for argument in tool.arguments:
        if argument.name not in given or given[argument.name] is None:
            continue
        value = given[argument.name]
        if argument.switch:
            if not isinstance(value, bool):
                raise Refused(f'{argument.name} is true or false')
            if value:
                options.append(argument.flag)
            continue
        if argument.counted:
            if isinstance(value, bool) or not isinstance(value, int) or value < 0:
                raise Refused(f'{argument.name} is a whole number, how many times {argument.flag} is given')
            options.extend([argument.flag] * value)
            continue
        values = value if isinstance(value, list) else [value]
        if not argument.many and isinstance(value, list):
            raise Refused(f'{argument.name} takes one value, not a list')
        texts = [_text(each, argument) for each in values]
        if argument.flag is None:
            positionals.extend(texts)
        elif isinstance(argument.action, argparse._AppendAction):
            options.extend((f'{argument.flag}={text}' for text in texts))
        elif argument.many:
            options.extend([argument.flag, *texts])
            separate = True
        else:
            options.append(f'{argument.flag}={texts[0]}' if argument.flag.startswith('--') else argument.flag)
            if not argument.flag.startswith('--'):
                options.append(texts[0])
    if positionals and (separate or any((text.startswith('-') for text in positionals))):
        positionals.insert(0, '--')
    return ([*tool.words, *options, *positionals], stdin)
