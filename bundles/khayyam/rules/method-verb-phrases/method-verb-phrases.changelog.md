# Khayyam Rule — Method Verb Phrases Changelog

## Changelog

### Method verb phrases rule added
- Time: 2026-09-29T12:00:00Z
- Type: Added
- Cited:
  - [On the Generation, Structure, and Semantics of Grammar Patterns in Source Code Identifiers](https://doi.org/10.1016/j.jss.2020.110740) (Newman et al., J. Systems & Software 2020) - Premise: callable identifiers predominantly use verb-phrase patterns.
  - [On the Naming of Methods: A Survey of Professional Developers](https://doi.org/10.1109/ICSE43902.2021.00061) (Alsuhaibani et al., ICSE 2021) - Premise: methods should contain a verb or verb phrase.
  - [A New Family of Software Anti-Patterns: Linguistic Anti-Patterns](https://doi.org/10.1109/csmr.2013.28) (Arnaoudova et al., CSMR 2013) - Premise: noun-only method names risk name–behaviour mismatch.
  - [Debugging Method Names](https://doi.org/10.1007/978-3-642-02032-6_14) (Høst & Østvold, ECOOP 2009) - Premise: method phrases are natural-language behaviour descriptions.
  - Meyer, B. *Object-Oriented Software Construction* (2nd ed., Prentice Hall 1997) - Premise: command–query separation.
  - [Concise and Consistent Naming](https://doi.org/10.1109/WPC.2005.14) (Deißenböck & Pizka, IWPC 2005) - Premise: consistent naming; `Read` homonym concern.
- Contributors:
  - Auto (model not recorded) via [Cursor](../../../../CONTRIBUTORS.md#cursor) - applied

#### What changed
- Added [method-verb-phrases.md](./method-verb-phrases.md), [method-verb-phrases.handoff.md](./method-verb-phrases.handoff.md), and this changelog from [Method Verb Phrases Research 001](./method-verb-phrases.research.001.md).
- Index entry added in [rules README](../README.md).

### Domain verbs are one option, not the preferred form
- Time: 2026-09-29T12:30:00Z
- Type: Changed
- Cited:
  - Owner, 2026-09-29 - Premise: domain verbs such as `Elapsed` can be effective in many places; the rule must not be limited to `Get`/`Set`, and the accessor question stays open.
  - [RFC 3986 §5 Reference Resolution](https://www.rfc-editor.org/rfc/rfc3986#section-5) - Premise: `Resolve` on a URI already means reference resolution.
- Contributors:
  - Auto (model not recorded) via [Cursor](../../../../CONTRIBUTORS.md#cursor) - applied

#### What changed
- The rule, handoff and [Research 001](./method-verb-phrases.research.001.md) no longer call domain verbs the preferred direction; they are effective in many places, provided the verb carries no other meaning in the same domain and does not collide with a sibling field's verb in one composing owner.
- `Resolve` removed as a good example; `Is`/`Has` for booleans marked under examination, matching the open question.
