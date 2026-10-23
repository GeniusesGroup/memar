# Syllab - Encoder Handoff
Open work for `modules/computer/codec/syllab.md`. Entries are mutable current state — revised as each item moves, removed when it resolves or is dropped. See [documentation-handoff.md](../../../knowledge/documentation/handoff/handoff.md) for what a handoff is.

## Open Questions

### What is the maximum size of a Syllab buffer?
- State: the document gives two limits that cannot both hold. The Dynamically Size Array structure stores an address and a length as two `uint32` values, counted from the start of the buffer, which reaches at most 2^32 bytes. The Size Limits section then says "A Syllab buffer can't be larger than 2^128 and Non dynamically size array fields can be larger than 2^32", and the fixed-size table has an `[nn]byte` row with no bound. A decoder cannot know how wide a pointer it must read, and an encoder cannot know when a buffer is too large to encode.
- Options: (1) the limit is 2^32 bytes because the pointer is `uint32`; Size Limits is rewritten to say so, the 2^128 figure dropped. Cheapest, and agrees with the structures. (2) the limit is larger and the pointer and length widths are declared by the buffer, which changes the structures and the encoding example. (3) the limit is per structure, stated beside each structure.
- Anchor: `modules/computer/codec/syllab.md`, sections Size Limits and Dynamically Size Array; the answer lands there.
- Blocks: any declaration of the protocol in Khayyam, since a field's width is part of its type. Meanwhile 2^32 is assumed as the working reading, Tentative.
- Asked: 2026-10-14, task 20261014T124123Z-27296-0.

### What replaces the Go structure sketches?
- State: the Structures sections show the dynamically sized array, the hash table, the tuple and the `Capsule` with a `typeID` as Go types, and the encoding example takes a Go schema. Owner ruling (2026-10-15, Decided): no trace of Go may remain in any module, so the Go sketches are to be replaced, not kept as illustrations. What is not ruled is what replaces them and which structures are normative; [Documentation → A Fact in Code Is Written Once](../../../knowledge/documentation/documentation.md#a-fact-in-code-is-written-once) keeps a module document independent of one language's syntax.
- Options: (1) declare the normative structures in Khayyam in the module's protocol folder and let the document name the path; the owner has ruled that new protocol declarations may be written in Khayyam. (2) describe each structure in prose and a table of widths and offsets, with no code. Recommended: (1). Decided by the chat that develops Syllab, together with the buffer-size question above.
- Anchor: `modules/computer/codec/syllab.md`, sections Structures, Hash Table - Map, Tuple, Data Fields; the answer lands there and in `modules/computer/codec/`.
- Blocks: deciding which structures a conforming codec must support. Meanwhile the sketches stay in the text only until replaced and are read as illustrations, Tentative.
- Asked: 2026-10-14, task 20261014T124123Z-27296-0.
