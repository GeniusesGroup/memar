# Petition
A petition (dadkhast) is the path of [petition-next](../petition-next/petition-next.md) edges. This file records why that path is not promoted.

## Model

- No node. No edge type named `petition`.
- The path is the petition. One case and zero `petition_next` edges is a petition of one case. A complaint is a tag on claim types, not a node in this path.

## Policies (rules)

- Do not attach users, evidence, grounds, a service, or a ruling to a petition. Those attach to each [case](../../case.md).
- Do not hang one rejection on the path and treat it as a ruling on every case in the path. Each case is ruled by its own votes. See [ruling](../../edges-shortcut/ruling/ruling.md).

## Placement

- **Not an edge and not a node.** The name is the path. Promoting the label is allowed only when the label has a responsibility the cases and the path do not already have. None is recorded.
- **Nearest alternative rejected:** an upstream petition node, the shape the phase-0 brief said needs a strong argument. The argument is not available. A registry inquiry is its own claim and is not a container for later cases.
- **Not** [complaint-url](../complaint-url/complaint-url.md). That file is an intake URL. A petition is not a channel.

## Open questions

- Whether `claim_relation` is this path's order is open on [petition-next](../petition-next/petition-next.md). The complaint tag does not make the petition a node.
