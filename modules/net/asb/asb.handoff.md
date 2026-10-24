# Asb - Physical Protocol Handoff
Open work for `modules/net/networking-osi_1-Asb.md`. Entries are mutable current state — revised as each item moves, removed when it resolves or is dropped. See [documentation-handoff.md](../../../modules-plugable/knowledge/documentation/handoff/handoff.md) for what a handoff is.

## Open Questions

### What distinguishes Asb from Parvaz, and is each a protocol or a hardware description?
- State: the body of this document is word for word the body of [Parvaz](../parvaz/parvaz.md) except the title line. Neither states what the protocol is: both open with "This Frame structure will transport by physical layer", yet no frame structure follows; the sections describe hardware (switching fabric unit, line processing unit, port types, adaptors) and a wireless access point with its channels. Owner ruling (2026-10-15, Decided): Asb and Parvaz are developed in separate chats, one per protocol; the likely reason for the duplicate is that they are two protocols the author had no time to separate. What each name is, is answered in the chat that develops that protocol.
- Options: (1) the owner states, in that chat, what each name is; the text is split so each document holds only its own part. (2) the two are one module with two realizations and the shared hardware text moves to one document that both name. (3) one is dropped. Recommended: (1).
- Anchor: `modules/net/networking-osi_1-Asb.md` and `modules/net/networking-osi_1-Parvaz.md`, whole body; the answer lands in both. The same question also bears on the file names, which break the one-layout rule (`osi_1-Asb` for a folder `asb`).
- Blocks: the naming session for the net category, and any declaration of a physical-layer protocol. Meanwhile each document is Draft and unchanged, Tentative.
- Asked: 2026-10-14, session 20261014T124123Z-27296-0.

### Which author notes inside the text are still wanted?
- State: the Wireless Access Point section carries an unanswered question in the text itself ("--- why not page device by DTCH?????"), a sentence that stops mid-thought ("to broadcast available"), and the same sentence about two hops and 2^16 devices twice. The channel 49 (694-790 MHz) choice is stated with no reason.
- Options: (1) the owner answers the paging question and completes the sentence; the duplicate is removed. (2) the notes move here as questions and the text is left until answered.
- Anchor: `modules/net/networking-osi_1-Asb.md`, section Wireless Access Point.
- Blocks: nothing else. Meanwhile the text is unchanged.
- Owner ruling (2026-10-15, Decided): examined in the chat that develops Asb, not before.
- Asked: 2026-10-14, session 20261014T124123Z-27296-0.
