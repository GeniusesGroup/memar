# Gender

## Sex-determination system

A [sex-determination system](https://en.wikipedia.org/wiki/Sex-determination_system) is a biological system that determines the development of the organism's sex. Most organisms that create their offspring using sexual reproduction have two common sexes, males and females, and in other species there are hermaphrodites, organisms that can function reproductively as either female or male, or both.

## Model

- `(___)-[:gender]->(___)`
- `(taxon)-[:gender_is]->(gender)`
- Candidate (unconfirmed) values: `Male`, `Female` (`Gender:::` in the source).

## Policies (rules)

- Source recorded only the value pair; no who-may-set/what-it-triggers semantics.

## TODO

## Fields

## Placement

- **Correct here** — gender is a classification the organism/taxon domain already owns: the edge sits beside its complete sibling [sexuality](../sexuality/sexuality.md) in this folder (prefer the existing home; the capability, if confirmed, is instantiated with taxon classification, not elsewhere).
- The `Male`/`Female` pair is a value list, not processing semantics (parameters-vs-semantics): configuration/vocabulary for this edge — never grounds a new module on its own.
- Not a lookup recipe to strip: unlike a derived query, `(taxon)-[:gender_is]->(gender)` proposes stored classification state with a vocabulary endpoint.
- Not analytics — nothing here is a discovered/derived query (analytics is always pluggable; does not apply).

## Open questions

- Does gender attach to `(taxon)` (the classification) or to the organism/person instance (`(___)-[:gender]->(___)`) — multi-typing, or two different edges?
- gender vs sex terminology, and relation to the sibling sexuality edge — distinct classifications or one vocabulary?
- Are `Male`/`Female` one vocabulary (a knowledge/label-style value set) or a per-organization policy list?
- Who may set the edge, and what does setting it trigger (no bare edges)?

