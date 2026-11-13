#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
import re
from modules.process.service.errors.call_name import InvalidCallName


def _component(value):
    if not isinstance(value, str):
        raise InvalidCallName('Domain and Name must each be a nonempty string')
    normalized = re.sub(r'[\s_-]+', '_', value.strip()).lower()
    if not re.fullmatch(r'[a-z0-9]+(?:_[a-z0-9]+)*', normalized):
        raise InvalidCallName(f'invalid service call-name component: {value!r}')
    return normalized


def call_name(details):
    return _component(details.Domain()) + '_' + _component(details.Name())
