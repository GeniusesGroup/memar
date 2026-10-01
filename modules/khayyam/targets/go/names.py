"""How a declaration is named, and the tables a name is chosen from.

Two questions live here. Which module a path names, and what that module is called
in a Khayyam declaration: the corpus roots that moved in the archive, the segments
of an acronym, the field and observer prefixes, the primitive type correspondence,
and the files the first port wrote by hand. And whether a candidate name is free:
whether a qualifier would only repeat what the name already says, whether a prefix
really is this module's own, which of a Go name's three Khayyam spellings stands
for it.

Every table names its columns where it is defined; nothing here repeats a table
another module defines."""

import re
from typing import Iterable, Sequence


PRIMITIVE_MAP = {
    "bool": ("Bool", "memar/math/boolean"),
    "string": ("String", "memar/codec/string/protocol"),
    "error": ("Error", "memar/process/error/protocol"),
    "int": ("S64", "memar/math/integer"),
    "int8": ("S8", "memar/math/integer"),
    "int16": ("S16", "memar/math/integer"),
    "int32": ("S32", "memar/math/integer"),
    "int64": ("S64", "memar/math/integer"),
    "uint": ("U64", "memar/math/integer"),
    "uint8": ("U8", "memar/math/integer"),
    "uint16": ("U16", "memar/math/integer"),
    "uint32": ("U32", "memar/math/integer"),
    "uint64": ("U64", "memar/math/integer"),
    "uintptr": ("U64", "memar/math/integer"),
    "byte": ("U8", "memar/math/integer"),
    "rune": ("S32", "memar/math/integer"),
    "float32": ("F32", "memar/math/float"),
    "float64": ("F64", "memar/math/float"),
}
KHAYYAM_TO_GO = {
    "Bool": "bool",
    "String": "string",
    "Error": "error",
    "S8": "int8",
    "S16": "int16",
    "S32": "int32",
    "S64": "int64",
    "U8": "uint8",
    "U16": "uint16",
    "U32": "uint32",
    "U64": "uint64",
    "F32": "float32",
    "F64": "float64",
}
KNOWN_GO_INTERFACES = {
    "error",
    "any",
    "io.Reader",
    "io.Writer",
    "io.ReadWriter",
    "io.Closer",
    "fmt.Stringer",
    "net.Conn",
    "net.Listener",
    "net.Error",
}


# Written by hand before the port; the port never reads them as targets and
# never rewrites them. Their identifiers are reserved so the port cannot
# declare a name the archive already owns.
PRE_EXISTING_KHAYYAM: tuple[str, ...] = (
    "modules/computer/capsule/protocol/life_cycle.kh",
    "modules/computer/runtime/protocol/blocking.kh",
    "modules/computer/runtime/protocol/concurrency.kh",
    "modules/process/control-flow/protocol/break.kh",
    "modules/process/control-flow/protocol/case.kh",
    "modules/process/control-flow/protocol/continue.kh",
    "modules/process/control-flow/protocol/default.kh",
    "modules/process/control-flow/protocol/defer.kh",
    "modules/process/control-flow/protocol/else-if.kh",
    "modules/process/control-flow/protocol/else.kh",
    "modules/process/control-flow/protocol/for.kh",
    "modules/process/control-flow/protocol/goto.kh",
    "modules/process/control-flow/protocol/if.kh",
    "modules/process/control-flow/protocol/jump.kh",
    "modules/process/control-flow/protocol/loop.kh",
    "modules/process/control-flow/protocol/panic-recovery.kh",
    "modules/process/control-flow/protocol/panic.kh",
    "modules/process/control-flow/protocol/switch.kh",
    "modules/process/control-flow/protocol/while.kh",
    "modules/memory/heap.kh",
    "modules/memory/mem.kh",
    "modules/memory/reference/immutable.kh",
    "modules/memory/reference/mutable.kh",
    "modules/memory/reference/weak.kh",
)

# Go primitives that the archive already owns a capsule for. `modules/math`
# has no integer or float capsules, so those stay unresolved on purpose.
PRIMITIVE_KHAYYAM_TYPES = {"bool": "Boolean", "string": "String", "error": "Error"}

# Go primitives whose Khayyam capsule the archive does not have yet. They are
# reported instead of guessed at, so the method that needs them is dropped.
UNMAPPED_PRIMITIVE_CAPSULES = {
    name: "modules/math/integer"
    for name in (
        "int",
        "int8",
        "int16",
        "int32",
        "int64",
        "uint",
        "uint8",
        "uint16",
        "uint32",
        "uint64",
        "uintptr",
        "byte",
        "rune",
    )
}
UNMAPPED_PRIMITIVE_CAPSULES.update(
    {name: "modules/math/float" for name in ("float32", "float64")}
)
UNMAPPED_PRIMITIVE_CAPSULES.update(
    {name: "modules/math/complex" for name in ("complex64", "complex128")}
)

# The three primitive abstractions keep the names the archive already gave
# them; every other declaration is qualified by its module.
FIXED_KHAYYAM_DECLARATIONS = {
    ("math/boolean/protocol", "Boolean"): "Boolean",
    ("codec/string/protocol", "String"): "String",
    ("process/error/protocol", "Error"): "Error",
}


NAME_SKIP_SEGMENTS = {"protocol"}
ACRONYM_SEGMENTS = {
    "adt": "ADT",
    "ascii": "ASCII",
    "cp": "CP",
    "cpu": "CPU",
    "dns": "DNS",
    "gui": "GUI",
    "http": "HTTP",
    "id": "ID",
    "ip": "IP",
    "json": "JSON",
    "mtu": "MTU",
    "nat": "NAT",
    "os": "OS",
    "ram": "RAM",
    "sha": "SHA",
    "srpc": "SRPC",
    "ssl": "SSL",
    "ttl": "TTL",
    "uri": "URI",
    "url": "URL",
    "urn": "URN",
    "utf8": "UTF8",
    "utf16": "UTF16",
    "uuid": "UUID",
    "xml": "XML",
}


def normalize_name(text: str) -> str:
    return re.sub(r"[^0-9a-z]", "", text.lower())


def pascal_segment(segment: str) -> str:
    """The module identity a path segment contributes to a declaration name."""
    cleaned = segment.strip().strip("_")
    if not cleaned:
        return ""
    if cleaned in ACRONYM_SEGMENTS:
        return ACRONYM_SEGMENTS[cleaned]
    parts = [part for part in re.split(r"[^0-9A-Za-z]+", cleaned) if part]
    rendered: list[str] = []
    for part in parts:
        if part.isupper() or part.isdigit():
            rendered.append(part)
        else:
            rendered.append(part[:1].upper() + part[1:])
    return "".join(rendered)


def module_identity(module: str) -> list[str]:
    """Module segments, least significant first, `protocol` dropped. The
    corpus's `modules/` folder is a place, not an identity: names qualified
    under it are the ones its packages had before it was kept as a folder."""
    parts = [part for part in module.split("/") if part]
    if parts and parts[0] == "modules":
        parts = parts[1:]
    while parts and parts[-1] in NAME_SKIP_SEGMENTS:
        parts.pop()
    return list(reversed(parts))


def strip_protocol(module: str) -> str:
    parts = [part for part in module.split("/") if part and part not in NAME_SKIP_SEGMENTS]
    return "/".join(parts)


def kebab_name(text: str) -> str:
    """`OnFailure` -> `on-failure`, `Field_RecordUUID` -> `field-record-uuid`."""
    spaced = re.sub(r"(?<=[a-z0-9])(?=[A-Z])", "-", text)
    spaced = re.sub(r"(?<=[A-Z])(?=[A-Z][a-z])", "-", spaced)
    return spaced.replace("_", "-").lower()


# Go corpus roots and the archive root each one lives under, most specific
# first. The corpus's `libgo/` tree is the archive's `lib/`, except the timer,
# which the Time module owns (`modules/lib/lib.md`, `modules/lib/lib.handoff.md`).
# The corpus's own `modules/` folder stays a folder named `modules` inside the
# archive's `modules/` tree (memar-go/modules/app -> memar/modules/modules/app);
# stripping it would put its children beside the corpus's root packages.
# memar-go/storage/ maps to the archive's `memory/` tree per the memory/storage
# dichotomy rejection; inner `storage/memory/` paths map to `memory/reference/`,
# `memory/address/`, and siblings.
CORPUS_MODULE_ROOTS: tuple[tuple[str, str], ...] = (
    ("modules", "modules"),
    ("storage/memory/reference", "memory/reference"),
    ("storage/memory/protocol", "memory/address/protocol"),
    ("storage/memory", "memory/address"),
    ("storage", "memory"),
    ("libgo/time", "time"),
    ("libgo", "lib"),
)


def normalize_module(module: str) -> str:
    """A Go corpus module path as the archive module path under the archive's
    `modules/` tree; the relocated roots are in `CORPUS_MODULE_ROOTS`."""
    for corpus, archive in CORPUS_MODULE_ROOTS:
        if module == corpus or module.startswith(corpus + "/"):
            rest = module[len(corpus) :].lstrip("/")
            return "/".join(part for part in (archive, rest) if part)
    return module


def archive_module(module: str) -> str:
    """A module path of a file under the archive root itself: the archive's own
    `modules/` prefix is its root, not part of the module."""
    if module == "modules":
        return ""
    if module.startswith("modules/"):
        return module[len("modules/") :]
    return module


def name_tokens(text: str) -> list[str]:
    """`Field_MediaType` -> `field`, `mediatype`; `ADT` -> `adt`."""
    return [part for part in re.split(r"[^0-9A-Za-z]+", text) if part]


def carries_identity(identity: str, name: str) -> bool:
    """True when `identity` would only repeat what `name` already says."""
    left = normalize_name(identity)
    right = normalize_name(name)
    if not left or not right:
        return True
    if left == right or right.startswith(left):
        return True
    return left in {normalize_name(token) for token in name_tokens(name)}


FIELD_PREFIX = "Observer_"
LEGACY_FIELD_PREFIX = "Field_"


def split_field_name(name: str) -> tuple[str, str] | None:
    """`URI_Observer_Scheme` -> (`URI`, `Scheme`), `Observer_URI_Scheme` -> (``,
    `URI_Scheme`); legacy `Field_*` accepted; None when not an observer abstraction."""
    for prefix in (FIELD_PREFIX, LEGACY_FIELD_PREFIX):
        if name.startswith(prefix):
            concept = name[len(prefix) :]
            return ("", concept) if concept else None
        marker = "_" + prefix
        index = name.find(marker)
        if index > 0:
            concept = name[index + len(marker) :]
            return (name[:index], concept) if concept else None
    return None


def field_name(concept: str, identity: str = "") -> str:
    """An observer abstraction starts with `Observer_`; a qualifier it needs goes
    after it: `Observer_Scheme`, `Observer_URI_Scheme` -- the ADT observer and
    mutator rule, `modules/computer/adt/rules/observer-mutator/`."""
    return f"{FIELD_PREFIX}{identity}_{concept}" if identity else f"{FIELD_PREFIX}{concept}"


def identity_carried(identity: str, bare: str) -> bool:
    """`carries_identity` over what a name says: a field's concept, not `Field`."""
    parts = split_field_name(bare)
    return carries_identity(identity, parts[1] if parts is not None and not parts[0] else bare)


def qualify_name(identity: str, bare: str) -> str:
    """`bare` qualified by `identity`: `Stringer` -> `UTF8_Stringer`, and a
    field `Field_Scheme` -> `Field_URI_Scheme`, never `URI_Field_Scheme`."""
    parts = split_field_name(bare)
    if parts is not None and not parts[0]:
        return field_name(parts[1], identity)
    return f"{identity}_{bare}"


def name_words(text: str) -> list[str]:
    """`OSI_DataLinkLayer` -> `osi`, `data`, `link`, `layer`."""
    words: list[str] = []
    for token in name_tokens(text):
        words += re.findall(r"[A-Z]+(?![a-z])|[A-Z]?[a-z]+|[0-9]+", token)
    return [word.lower() for word in words]


def repeats(qualifier: str, name: str) -> bool:
    """True when `name` already says `qualifier`, word for word."""
    wanted = name_words(qualifier)
    have = name_words(name)
    return bool(wanted) and any(have[index : index + len(wanted)] == wanted for index in range(len(have)))


def concept_forms(concept: str) -> set[str]:
    """`Lengths` -> `Lengths`, `Length`; `Indexes` -> `Indexes`, `Indexe`, `Index`."""
    forms = {concept}
    if concept.endswith("s"):
        forms.add(concept[:-1])
    if concept.endswith("es"):
        forms.add(concept[:-2])
    return forms


def field_holds_its_concept(concept: str, value_types: Sequence[str]) -> bool:
    """True when every value the field's accessors return is its concept --
    `X`, `X` behind a qualifier, or X's singular -- so a qualifier in front of
    `Field_` says nothing the concept does not. `Time_Field_Access` returns a
    `Time`, not an `Access`: its qualifier is what the value is."""
    forms = concept_forms(concept)
    return all(any(value == form or value.endswith("_" + form) for form in forms) for value in value_types)


def field_accessor_options(owner: str, original: str, value_types: Sequence[str] = ()) -> list[str]:
    """The names a method of `owner` may take, best first.

    A field abstraction's method is implemented by other capsules, so it is
    named for the value it returns and never carries its owner's name: the
    original name; the field's concept when that ends with the original
    (`Status` on `Field_SocketStatus` -> `SocketStatus`); the original behind
    the field's own qualifier (`Scheme` on `URI_Field_Scheme` -> `URIScheme`);
    the one value type it returns, when that is the original qualified
    (`URI_Scheme` -> `URIScheme`). No qualifier is taken from further up the
    module path. Any other owner's method has only its name.
    """
    parts = split_field_name(owner)
    if parts is None:
        return [original]
    qualifier, concept = parts
    options = [original]
    joined = concept.replace("_", "")
    if joined != original and joined.endswith(original):
        options.append(joined)
    if qualifier and not repeats(qualifier, original):
        options.append(qualifier.replace("_", "") + original)
    if len(value_types) == 1 and value_types[0].endswith("_" + original):
        options.append(value_types[0].replace("_", ""))
    return list(dict.fromkeys(options))


def module_prefixes(module: str) -> set[str]:
    identities = [pascal_segment(part) for part in module.split("/") if part]
    return {
        "".join(identities[start:end])
        for start in range(len(identities))
        for end in range(start + 1, len(identities) + 1)
    } - {""}


def counterpart_tiers(go_name: str, names: Iterable[str], module: str) -> list[list[str]]:
    """Khayyam names that stand for the Go name `go_name` of `module`, best
    first: the name that carries its module stepped up (`TimerStatus` ->
    `Timer_Status`), the name itself, and the name qualified by its module
    (`Scroll` -> `GUI_Scroll`) -- the qualified names rule's three spellings."""
    prefixes = module_prefixes(module)
    step_up: list[str] = []
    exact: list[str] = []
    qualified: list[str] = []
    for name in names:
        if name == go_name:
            exact.append(name)
        elif any(
            go_name.startswith(prefix)
            and len(go_name) > len(prefix)
            and name == f"{prefix}_{go_name[len(prefix):]}"
            for prefix in prefixes
        ):
            step_up.append(name)
        elif qualified_by_module(go_name, name, module):
            qualified.append(name)
    return [step_up, exact, qualified]


def pick_counterpart(go_name: str, names: Iterable[str], module: str) -> tuple[str | None, str]:
    for tier in counterpart_tiers(go_name, list(names), module):
        unique = sorted(set(tier))
        if len(unique) == 1:
            return unique[0], ""
        if unique:
            return None, "more than one Khayyam name stands for it: " + ", ".join(unique)
    return None, "no Khayyam declaration stands for it"


def field_identity(module: str) -> str:
    identities = module_identity(module)
    return normalize_name(identities[0]) if identities else ""


def qualified_by_module(name: str, candidate: str, module: str) -> bool:
    """True when `candidate` is `name` behind a prefix made of `module`'s
    segments; for a field `Field_<X>` the prefix may also follow `Field_`."""
    if candidate == name:
        return True
    identities = [pascal_segment(part) for part in module.split("/") if part]
    allowed = {
        "".join(identities[start:end])
        for start in range(len(identities))
        for end in range(start + 1, len(identities) + 1)
    }
    parts = split_field_name(name)
    if parts is not None and not parts[0]:
        concept = parts[1]
        if candidate.startswith(FIELD_PREFIX) and candidate.endswith("_" + concept):
            if candidate[len(FIELD_PREFIX) : -len(concept) - 1] in allowed:
                return True
    if not candidate.endswith("_" + name):
        return False
    return candidate[: -len(name) - 1] in allowed
