# Timeline

## Model

- No edge joins the group and the timeline of one node: they share its address ([Timeline → How domains connect through a timeline](../../timeline.md#how-domains-connect-through-a-timeline)). A domain that wants to mark that a thing has data in it writes the optional edge declared once on Thing ([Data in](../../../../identity/thing/edges/data_in/data_in.md#model)).

## Policies (rules)

- CAN use as ChannelID. Use to store and retrieve comments in time order. It can be UUID, URL hash or any random id.
- Related `Widget` for that domain will show to user in the group of comments.
