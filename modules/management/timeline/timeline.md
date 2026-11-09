---
Title: "Timeline"
Labels: Draft
---
# Timeline

## Abstract
A timeline is the order in which things are placed on a node. Its identity is the address of the node it belongs to, and it knows nothing of what that node is; the address of a node is also the address of its group and of its timeline. A participant, human or agent, places many contents on it; each placement has a number that gives its place in the timeline's order. What a content says, what it replies to, what kind it is and who placed it are not the timeline's: the text is content's and text's, the reply is content's edge, the kind is a label, the placer is Ownership's `creator`. A thing placed may itself be a node whose timeline then becomes an event of this one, a link whose meaning is only the reader's along its path. So the timeline offers reads over its own edge alone, in order and in reverse, and no service has a notion of "the latest" of a kind: the current content of a kind is the contents of that kind nothing supersedes, read by the Conversation widget.

## Usage
- What is said on a node, in the order it was placed.
- Recently viewed items.

## Model

### Edges
Timeline owns one edge, `event_is` with its reverse `event_of`, declared in [event](edges/event/event.md#model): the thing is placed on the timeline, one edge per placement. A placement is not a node; what is said of the placing is the typed values of that edge, declared as [`Timeline_Placement`](edges/event/protocol/timeline-placement.kh), each keyed by the TypeUUID of its type ([Graph → Typed edge fields](../../../modules-plugable/computer/memory/store/graph/graph.md#typed-edge-fields-typeuuid--value-not-opaque-buffers)). No node and no edge is added by this design.

What else is read beside a timeline is other domains' edges, used and not restated: the reply is Content's [`reply_to`](../../knowledge/content/edges/reply/reply.md), the kind is Label's [`label`](../../knowledge/label/edges/label/label.md), the placer is Ownership's [`creator`](../../rights/ownership/edges/creator/creator.md), and replacement is Thing's [`supersedes`](../../identity/thing/edges/supersedes/supersedes.md).

### One content, many timelines
A content may be placed on more than one timeline, by one `event_is` edge from each, and has a number of its own in each. A reply is placed like any content, on the timeline its placer chose; the `reply_to` edge is the content's and holds on every timeline the two contents are placed on. A reply has no kind of its own beyond the kind label of the content that replies, and no reply sets anything aside. A reply placed on a parent's or a child's timeline counts as a reply on this one, and a reply to a content that is superseded is not refused.

### How domains connect through a timeline
Owner ruling 2026-11-06: domains connect in two ways, a graph edge between two things, and a thing placed on a timeline. A conversation is a UI widget and not a concept of this model.

**The group and the timeline of one node.** A thing has one address, and every domain that is a lens on it attaches its edges to that address ([Identifiers Are Memory Addresses](../../computer/memory/address/rules/identifiers-are-memory-addresses/identifiers-are-memory-addresses.md#the-rule)); the timeline of a node and the group of the same node are two such lenses. No edge joins them, and none is wanted: an edge would name a second thing where there is one ([Modeling Workflow](../../../modules/knowledge/modeling/rules/modeling-workflow/modeling-workflow.md), step 3). Timeline reads nothing of the group of its node, and no service of Timeline checks a membership: who may place on a timeline or read it is Rights' over Group's `joined`, joined to a placing by the widget that places ([Widget Aggregates](../../computer/ui/rules/widget-aggregates/widget-aggregates.md#the-rule)). A thing another domain records on the node, a join, a leave or a request, reaches the timeline only by being placed there, by that widget; Timeline does not learn what it was. What Group reads of the timeline is Group's to say ([Group](../group/group.md)).

**A timeline as an event of another.** The thing an `event_is` edge reaches may be any node, so placing a node B on the timeline of A makes B's timeline, at the same address, an event of A's. Timeline gives that link no meaning: it is a placement like any other, with its number and instant, and nothing placed on B is thereby placed on A, nor the reverse. What the link means — that B was opened from A, that B belongs to the work A stands for, that B is a feed A follows — is known only to a reader that reached A along a path whose concept it knows: the widget that walks the path carries that concept, and Timeline keeps no kind of timeline from which to read it ([Kernel Neutrality](../../knowledge/modularity/rules/kernel-neutrality/kernel-neutrality.md#the-rule): which kinds of link exist is an organization's choice). A cycle (A on B and B on A, or A on itself) is not refused, since no placement inherits anything along the link; a widget that walks the links guards against walking round it.

That link needs two reads and both are over Timeline's own edge: what is placed on A, in order ([`ReadAfter`](services/timeline-read/timeline-read.kh)), and the timelines B is placed on, by the reverse `event_of` ([`ReadPlacedOnAfter`](services/timeline-read/timeline-read.kh)). The second was missing: without it "where is this thing placed" is a scan of every timeline ([Graph → What it is to the memory contract](../../../modules-plugable/computer/memory/store/graph/graph.md#what-it-is-to-the-memory-contract)). No edge is added; the reverse is declared in [event](edges/event/event.md#model).

What the link means is settled by the need of the rule that reads it:
- A mere reference is placing a node on a timeline, and nothing more is declared.
- A link a rule acts on in code is its own edge, or the event edge carries a field (a label) saying why the record was placed. Neither exists, and nothing is built for it.
- A feed is a timeline of valuable data kept like any other timeline. It is a label introduced by a pluggable module, not a widget, and a user's own posts and the feed differ in what the display filters, not in concept.

A graph edge and a placement say different things. An edge between two things is a relation with its own meaning and rules, declared by the domain whose subject it is (Group's `parent`, Content's `reply_to`); a placement says only that a thing appears, at a place in an order, on a node's timeline. Where a relation has rules of its own, it is an edge; a placement does not stand in for it.

### Order
The order of a timeline is its numbers. The number is assigned when the edge is written, so two placers cannot take the same one; the store's compare-and-swap is what keeps it unique. Nothing is ended or erased on a timeline ([A placement is added, never written over](rules/a-placement-is-added-never-written-over/a-placement-is-added-never-written-over.md)).

## Reads
Timeline offers two reads over its own edge, the things placed on a timeline in order and the timelines a thing is placed on: [`Timeline_Read`](services/timeline-read/timeline-read.kh). Every read that joins it with another domain's edge (the contents of a kind, the replies placed on this timeline or on a parent's or a child's, the contents not yet replied to) is the [Conversation](../../../modules-plugable/management/timeline/widgets/conversation/conversation.kh) widget's, over Graph's pattern match ([Widget Aggregates](../../computer/ui/rules/widget-aggregates/widget-aggregates.md#the-rule)); the replies to one content are Content's read and who placed a content is Ownership's.

A read of one placement by its number is `ReadAfter` from the number before it. A read across the timeline is a page of `ReadAfter` calls; how many sides one call fetches is the store's.

### The current content of a kind
Several contents of one kind may answer one node, each with replies saying what to change; a later content of a kind does not make an earlier one void. So "the latest of a kind" is not a read. What a reader wants is the contents of that kind on the timeline that nothing supersedes ([Content → Proposals and replacement](../../knowledge/content/content.md#proposals-and-replacement)), read by the Conversation widget.

## What Stays Out of Timeline
- **The text and its revisions** are content's and text's. The timeline places a content and reads nothing it says.
- **The kind** of a content is a label on it, Label's, and reading the placements of a kind is the Conversation widget's. Today a content's kind is held by the content store (`ReadContent` answers it) and the realization of the timeline reads it through that store to filter by kind; with the kind as a label, the timeline reads neither Label's edge nor a content store.
- **The placer** is Ownership's `creator` of the content.
- **The reply** is content's edge. A reply naming other contents to read names them by the timeline's number.
- **Membership** — who may place on a timeline or read it — is group's, and the rule over it is Rights'.
- **The meaning of a link between timelines**, and any kind of timeline (a chat, a feed, a notification list), is the reading widget's along its path, and a kind of timeline is a label a pluggable module introduces.
- **A conversation or a chat** is a UI widget's.
- **Anything derived**: no list of the timelines a thing is on, no count and no latest number is kept beside the edges; each is read from them (owner, 2026-11-05: nothing is cached).
- **How a placement is kept** is the Graph store's and its medium adapter's.
