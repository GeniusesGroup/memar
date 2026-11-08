# Agency Rule — The Stable segment is reproducible
Status: Draft

## The rule
- **The Stable segment of a serialization holds only the entries whose layer is Stable, in the order the resolve returned them.** No clock, random identifier or per-chat nonce appears in its bytes.
- **The Session segment follows the Stable segment and is never a breakpoint of it.** The Event segment follows both and is never part of the Stable segment.
- **For one version and one serializer, two takeups yield identical Stable bytes;** [Prefix Stability](/modules/management/agency/protocol/prefix-stability.kh) decides it by comparing the two.
- **Two takeups bound to one version resolve to the same ordered materials, and only the event may differ;** [Context Continuity](/modules/management/agency/protocol/context-continuity.kh) decides it.

## Why it exists
A prompt cache reuses only an unchanged prefix. A Stable segment that varies with the chat pays the whole context again on every new chat.

## How a check would run
The realization's tests in `modules-plugable/management/agency/tests/durable_context.py` serialize one version twice and compare the Stable bytes.
