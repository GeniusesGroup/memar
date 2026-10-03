# Datatype Handoff

Open state for [datatype.md](./datatype.md). See the repository's
documentation-handoff practice for what a handoff is.

## Topic & Purpose

Converting this domain's one protocol file from the Go it carries to Khayyam, and
recording the duplicate that had to be checked before anything was declared — this
repository's `computer/datatype` sits at the same module path as memar's.

## Status

Active — the single `.kh` file accepts under the Khayyam frontend. No blocking
finding; two things are recorded as open.

## Converted

- `protocol/dt-uuid.kh` — `Field_DataTypeID` + `DataTypeID () (t ThingUUID)`

## The duplicate, checked

The brief for this wave named the check to make before declaring anything, and it
is worth writing down what the check found, because memar's side is larger than
this repository's:

| memar `modules/computer/datatype` | this repository's `modules/computer/datatype` |
| --- | --- |
| `protocol/uuid.kh` → `Datatype_UUID ab` | `protocol/dt-uuid.kh` → `Field_DataTypeID` (Go: `Field_DataTypeID`) |
| `protocol/id.kh` → `Datatype_ID ab` | — |
| `protocol/data-type.kh` → `DataType ab` | — |
| `protocol/detail.kh`, `identifiers.kh`, `life-cycle.kh`, `quiddity.kh`, `software-life_cycle.kh`, and their observers | — |
| — | a graph node: `(software)-[:---]->(software_datatype)` |

Three consequences, and they are the reason this file declares exactly one
abstraction:

1. **No `Datatype_UUID` here.** memar declares it; declaring it again would be the
   duplicate the qualified-names rule calls an architecture error. The Go's
   `type UUID thing_p.UUID` did not need one — it reached `thing_p` — so the
   conversion reaches `ThingUUID` from
   [identity/thing/protocol/dt-uuid.kh](../../identity/thing/protocol/dt-uuid.kh)
   and nothing more.
2. **No local `DataType` abstraction.** `DataType` is memar's, and it is the
   behaviour a capsule satisfies, not a node in this repository's graph. The bare
   name would collide at any import site that also reaches memar — which
   [computer/module](../module/protocol/bs.kh) does.
3. **No `DataTypeModel`.** The Go had no `model.kh`; `datatype.md` states the edge
   and nothing else. Rule 6 says an empty abstraction is a design smell and the
   answer is to design it, not to translate the absence of one — and there is
   nothing here yet to require.

## Decisions

1. **`DataTypeID` returns `ThingUUID`.** The Go's `Field_DataTypeID` returned this
   domain's `UUID`, which was `type UUID thing_p.UUID` — the repository-wide
   identifier alias. The comment above it, "Use to identify any computer data
   type.", is extracted to [datatype.md](./datatype.md).
2. **`Field_DataTypeID` is a field abstraction and `DataTypeID` a body-less method
   on it.** This is rule 2 of the migration map: a getter surface is declared, and
   the body comes from the generator driven by the `abstraction.Implements` intent.
   No body was hand-written.
3. **The `## Identifier` section added to [datatype.md](./datatype.md) is mine, not
   the Go's.** The Go said only what a datatype identifies. The section says the
   identifier is the graph node's identity and points at this handoff for the
   relation to memar's `DataType` — the sentence a reader arriving from the memar
   side needs and the Go did not contain.

## Open Questions

1. **What is a datatype node *for*?** [datatype.md](./datatype.md) says only
   "identify any computer data type", and the edge is `(software)-[:---]->(software_datatype)`
   with no second end named. The field accessor is the only behaviour this domain
   has, and it is the behaviour of every node in the graph. Either the datatype
   node carries something this repository has not written yet — a name, a
   media type, the set of values it admits — or it is a label on software and
   belongs as one. This is the rule-6 question for this domain: what behaviour does
   a datatype node owe its callers?
2. **Should this domain compose memar's `DataType`?** If a datatype node is a
   record *about* a data type rather than the data type itself, the record might
   be required to answer with the `DataType` it describes, and the domain would
   need `tp Datatype_Record ab { Field_DataTypeID }` composed with memar's
   `DataType`. Nothing says either way, and declaring it would commit the domain
   to the "record about" reading.
3. **The same module path, two repositories.** Both `computer/datatype`
   directories exist, and the qualified-names rule cannot separate two declarations
   a shared path names alike. Nothing is declared twice today — this file declares
   one field abstraction, memar declares `Datatype_UUID`, `Datatype_ID`, `DataType`
   — but the path collision is real and will surface the moment either side wants
   a name the other has. The module path itself is a repository-level decision, not
   this domain's.