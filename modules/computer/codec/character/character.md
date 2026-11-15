---
Title: Character
Start Date: 2026-10-24
---
# Character
## Abstract
A **Character** is one unit of text, identified by a code point of a character set. It is independent of any encoding: how a Character is stored as octets is the business of a character encoding, not of Character. The abstraction is declared in [`protocol/character.kh`](./protocol/character.kh). It asks only for equivalence, clone and copy.

## Character and encoding are two concepts
- Character is what a text is made of; an encoding is a rule that turns Characters into octets and back. The owner ruled them two concepts (record 20261023-T164151Z-21796).
- Each encoding (UTF-8, ASCII, Harf) offers its own capsule that satisfies Character, such as `UTF8_Char`. No encoding introduces an abstraction of its own, and none is the base of Character.
- The character set (the repertoire of code points, Unicode for the characters of Khayyam source) is not an abstraction of this module: a code point is the number by which a Character is identified.
- The encoding abstraction, `String_CharacterEncoding`, stays in [`modules/computer/codec/string/protocol/`](../string/protocol/character-encoding.kh) with String.

## Home
The module is `modules/computer/codec/character/`, under codec, by the owner's ruling. Whether the folder tree of `modules` and `modules-plugable` is regrouped is the work of record 20261024-T052937Z-22844.

## Character run
A **CharacterRun** is a read-only, finite, ordered run of Characters, declared in [`protocol/character-run.kh`](./protocol/character-run.kh). It is what a compiler hands to a method for a quoted form ([Compiler → What a quoted form hands over](../../compiler/compiler.md#what-a-quoted-form-hands-over)), and any other producer of text, such as the occurrences of a Lexer, may hand one over. It says nothing of where its Characters are kept, how they were read, or in which encoding they are stored. It is neither a String, which composes a dynamic array and offers operations that make or change one, nor the Text of the text domain (Text Handoff). A producer such as a Lexer that would rather lend a view of a source that can change, without a copy, is not served by this guarantee; the Lexer's handoff carries that conflict.

What the signatures cannot say, and every producer keeps true:
- **The Characters do not change, by any route but the `unsafe` patching of a running artifact ([Compiler](../../compiler/compiler.md#runtime-mutation-of-the-artifact-is-unsafe)), while the run exists.** Another holder of the same memory must not be able to change them either, so satisfying the abstraction by structure is not satisfying this guarantee. A producer whose content another process can change hands over a copy.
- **The run lives at least as long as any holder of it.**
- **Reading from the first position until the end yields exactly as many Characters as the count says,** one per read, each position issued by the run and read only by it. A position is a value: reading again with the same one gives the same result, and `FirstPosition` gives the same position each time. A position another run issued is outside the contract and no result is promised for it.
- **The end is a signal, not an error** ([Lexer → Grounding in observable extents](../../lexer/lexer.md#boundary-principles)). When it is true no Character was read, and the Character and position written are of no meaning. An empty run is at its end at the first position, and a run is at its end after its last Character is read, not with it.
- **There is no indexed access:** over a variable-width encoding it costs the length of the run each time.

`CharacterRun_From`, declared beside String in [`protocol/character-run-from.kh`](../string/protocol/character-run-from.kh) so that this module does not import String, is satisfied by a capsule that can write a String from a run. Its error output is in the contract for every implementation: one that cannot fail writes nil, and one that can writes why, by an error its module declares in its `errors` folder.

### Checked character extents
The optional [checked source capability](./protocol/character-run-extent-source.kh) and [extent](./protocol/character-run-extent.kh) serve arbitrary contiguous source intervals. Their refusals are declared in [invalid position](./errors/character-run-error-invalid-position.kh) and [reversed extent](./errors/character-run-error-reversed-extent.kh).

A capability source retains one immutable CharacterRun subject. Its valid boundary positions are exactly FirstPosition and each after position produced by a successful NextCharacter from that source, including the position reached after the final character. For an empty source FirstPosition is the valid end boundary. The unspecified after output from a read that already signals end is never a boundary obtained by that read. Repeated boundary values identify the same boundary.

ComparePositions terminates, validates both inputs before use and returns before=true,same=false for the left boundary preceding the right; false,true for the same boundary; false,false for left following right. true,true is forbidden. Invalid/unrecognized positions and positions of a different run/revision return CharacterRun_Error_InvalidPosition; all Boolean outputs are meaningless on error. This is an additional obligation of this capability, not a call to base NextCharacter on an unchecked foreign position. Implementations may keep provenance privately and compare by a linear walk or their own representation; no indexed-access cost guarantee is added.

MakeExtent terminates, validates both boundaries and refuses invalid/foreign positions with CharacterRun_Error_InvalidPosition before checking their order. A start after end returns CharacterRun_Error_ReversedExtent. On any Error no extent may be consumed. Successful extent includes start and excludes end. Equal boundaries succeed with an empty surface, including at end-of-run. Its source accessor is the exact source subject that received MakeExtent; its boundary accessors preserve the validated boundaries. GetSurface yields exactly the characters read from start until end, and no characters beyond it. The surface has its own run-local positions; they must not be passed as source positions. A surface copy with identical characters is not a source origin.

Source, extent, boundary associations and surface do not change while any holder retains the extent or a returned association; the extent retains its source, and the CharacterRun lifetime guarantee retains every returned surface. Distinct equal substrings remain distinguishable by their boundaries in the retained source. Order/provenance checks must decide membership even for a stale or forged position instead of invoking the base contract outside its domain. A producer unable to make those checks does not satisfy this capability.

Open, by the owner's instruction: whether a form quoted with `'` holds exactly one Character, and what a quoted form that spans lines or carries escapes means.
