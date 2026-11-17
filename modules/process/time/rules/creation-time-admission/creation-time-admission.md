---
Title: "Process Time Rule — Creation Time Admission"
Labels: Draft
---
# Process Time Rule — Creation Time Admission
A rule of [Process Time](../../protocol/creation.kh).
## The rule
- The creating process retains the actual creation instant through [Time_Creation](../../protocol/creation.kh). [Identifier](../../../../identity/identifier/protocol/identifier.kh) exposes its retained effective issuance coordinate through its direct error-aware time observation. When generation occurs with entity creation, the process checks that relation under its trusted clock-accuracy and bounded-rollback allowance; the encoded coordinate does not replace actual creation time.
- Every generator and receiving node interprets the identifier's time using the same declared reference timeline and epoch. Clock synchronization supplies observations of that timeline; a node's private startup time or arbitrary epoch is converted before comparison.
- At first admission of a newly created entity, the receiving node applies its trusted [Time_Creation_Admission](../../protocol/creation-admission.kh) to the declared creation instant and its observed current time. Past and future deviations are explicit finite nonnegative policy parameters. Out-of-window or incomparable time is refused. The policy values come from the receiving node's configuration, not from untrusted request fields.
- An earlier actual creation instant is admitted through an explicitly authorized historical-creation path whose source evidence is verified by the receiving process. The node checks the Identifier's creation relation against that verified instant. A client-supplied historical label or timestamp alone establishes no such evidence.
- Admission preserves the originating creation instant. A receiving node records receipt or persistence time in that event's own role rather than replacing creation time.
- Reading, referencing, retrying or transporting an already admitted identity preserves that identity. Fresh-creation clock bounds are applied to the creation event, not as a recurring expiration rule for its identity.
- A bounded local generator may preserve ordering only while its reported time remains within the permitted deviation. When this is impossible, generation waits or reports failure; it does not advance an artificial timestamp without bound.
## Why it exists
SDK-side generation avoids a server allocation round trip. A common time basis and admission policy retain meaningful creation time while supporting delayed transport and authorized historical imports.
