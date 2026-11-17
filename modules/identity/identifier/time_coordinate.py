# For license and copyright information please see the LEGAL file in the code repository

from .generator import MAXIMUM
from .errors.generation import Identifier_Error_InvalidGeneratorInput


def coordinate_from_time(source, reference_epoch):
    observe = getattr(source, "parts_in_epoch", None)
    if not callable(observe):
        raise Identifier_Error_InvalidGeneratorInput()
    parts = observe(reference_epoch)
    try:
        seconds, remainder, error = parts
    except (TypeError, ValueError) as error:
        raise Identifier_Error_InvalidGeneratorInput() from error
    if error is not None:
        if isinstance(error, Exception):
            raise error
        raise Identifier_Error_InvalidGeneratorInput()
    if type(seconds) is not int or type(remainder) is not int or not 0 <= remainder < 1000000000:
        raise Identifier_Error_InvalidGeneratorInput()
    value = seconds * 1000000000 + remainder
    if not 0 <= value <= MAXIMUM:
        raise Identifier_Error_InvalidGeneratorInput()
    return value


def generate_from_time(generator, source, reference_epoch):
    return generator.generate(coordinate_from_time(source, reference_epoch))
