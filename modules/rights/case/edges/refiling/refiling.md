# Refiling
A later filing may be a different claim. The same parties, even with the same amount, are not the same claim. Whether a repeated claim is allowed is an organization choice, not a kernel ban.

## Model

- No edge type named `refiling`.
- He may claim the same sum from the same person in a different year. That filing is a different claim.
- The kernel does not forbid the later filing, and it does not require a link before the filing exists. An organization may choose to refuse a repeat.
- The defendant and the system may surface an earlier claim as evidence. That is not a kernel ban, and it is not a generic edge meaning that the two claims are related.

## Policies (rules)

- A later filing is not refused by the kernel on the ground that a claim was already ruled.
- Votes stay on the case where they were cast. A vote on one case is never a vote on another case.
- A past majority is not its own edge. The votes on that case are enough.
- Continuation of a case stops on the vote margin, not by growing a fixed pool of 1, then 3, then 5, and not because the parties keep paying.

## Placement

- **Not an edge.** "Refiling" names the later filing. It does not name a relation. A link, when an organization wants one, is a pluggable edge for a stated reason.
- **Nearest alternative rejected:** matching parties and a matching amount as the test that the later filing is the same case.
- **Nearest alternative rejected:** a kernel ban on an unlinked duplicate.
- **Nearest alternative rejected:** a history edge that stores the majority after the shortcut changes. The votes are the record.

## Open questions

- None that block an edge. Whether a given organization allows a repeat is that organization's choice.
