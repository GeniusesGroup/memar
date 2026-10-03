# URI
A [uniform resource identifier](https://en.wikipedia.org/wiki/Uniform_Resource_Identifier) is a locale name in the computer world: it names a resource without saying how the resource is reached. The [uniform resource name](https://en.wikipedia.org/wiki/Uniform_Resource_Name) and the [electronic product code](https://en.wikipedia.org/wiki/Electronic_Product_Code) are the other two forms stored under one record.

## What this domain models
A URI is a [thing](../thing/thing.md) whose text is the URI string, so a URI record is a thing and is a text. Its identity is that thing's identity; this domain mints no identifier of its own. The `uri` label on a text is a loop-edge, and its rules — one URI per text, read-only once created, created by the user — are in [`edges-loop/uri`](edges-loop/uri/uri.md). Showing one as a small rendered widget is the shortcut edge in [`edges-shortcut/preview_link`](edges-shortcut/preview_link/preview_link.md).

## Where a URI value comes from
Not from here. A URI protocol under [`modules-plugable/uri`](../../../modules-plugable/uri/uri.md) — username, iban, isbn, postal code, and the rest — decides what a valid value of its own kind is; this domain stores and hands back the value it was given.

## The quiddity-uri widget
`widgets/quiddity-uri` is the record that attaches a URI to the quiddity it identifies. Its data model carries exactly four fields and nothing else:
- the URI value,
- the UUID of the quiddity the value identifies,
- the request that produced the record,
- the audit time of that request.

Storage over those records saves one, fetches one by its URI value, and lists the URIs of one quiddity inside an offset/limit window, reporting how many versions the query saw.

## Open questions
What this conversion left undecided or blocked on other domains is in [`uri.handoff.md`](uri.handoff.md).
