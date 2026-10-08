# Vote accept
One seated person's recorded acceptance of this case as filed. The vote stays. It is not rewritten when later votes go the other way. It is never a vote on another case.

## Model

- `(case)-[:vote_accept]->(user)`

## Policies (rules)

- The user has a [judge](../judge/judge.md) edge on this case. An expert or another opinion-giver who votes is seated on that same edge. There is no second adjudicator type.
- The vote is that person's own. A signature on another person's draft is not this edge.
- The person does not see another seated person's vote or reason on this case before casting.
- A judge has at most one of `vote_accept` and [vote_reject](../vote-reject/vote-reject.md) on this case. There is no abstention. The person must choose and must explain.
- This edge accepts the claim as filed, including its filed service. It has no attachment. A changed request is not this edge. A judge who wants a change uses [vote reject](../vote-reject/vote-reject.md), which may point at one request. That pointer is a proposal. It is not an enrichment of this edge, and it is not a third ballot edge.
- This edge is not a vote on any other case.
- The edge is not deleted, not retargeted, and not flipped. A later majority that disagrees leaves this edge in place. It is then a minority vote. It is not a second ruling. Continuation and the final margin are on [ruling](../../edges-shortcut/ruling/ruling.md).
- The edge is written only when the case is not in draft.
- The edge carries no prose and no weight. Human-language reasons are timeline texts on the case. The plaintiff's [grounds](../grounds/grounds.md) stay the plaintiff's text. A party's score does not weight this vote.
- Until every required judge has voted, no party sees this vote or its explanatory text. That hide is a note for the content and timeline domains. Those domains are not modeled here.
- What would falsify the accept-as-filed rule: any judge attaches an alternate request to `vote_accept` and the margin still treats that edge as accept of the filed service. Critique v4. The alternate request is a proposal this repository has not ratified: it is named on [vote reject](../vote-reject/vote-reject.md) as a pointer, and that pointer is not a drawn edge.
- What would falsify the same rule, in the storage shape: `vote_accept` carries a service UUID and parameter bundle that differ from the claim's filed `claim_service`. Critique v3. The conditional accept that would produce it is a proposal the pilot has not adopted.
- What would falsify the independent-vote rule: a valid vote that is a signature on another person's draft; or a party who sees a judge's or an expert's vote or explanatory text before every required judge has voted. Model v4 point 1.
- What would falsify the no-abstention rule: a valid disposition that is neither accept nor reject; or a vote with no explanation. Model v4 point 4.
- What would falsify the rule that a vote stays on its own case: one judicial act that is, by the claim's own rule, a single vote on two cases, so that writing two edges would record two acts. Model v3. Hearing two claims together does not make one stored vote the vote on both.

## Placement

- **The edge type is the position.** A property "accept or reject" on one vote edge would be a classification stored as data. The type is the classification, the same way a status type is the status.
- **Not** [law vote-agree](../../../law/edges/vote-agree/vote-agree.md). That edge is a signature over a law's frozen digest. This edge is a position on one claim. A law signature that must be dropped when the digest changes is a different relation. Case votes are kept when the pool grows, which is the opposite of dropping a signature.
- **Nearest alternative rejected:** one vote edge plus a numeric weight, including a weight taken from a party's score. No scale is recorded. An average of accept and reject is undefined.
- **Nearest alternative rejected:** an accept stored at an amount, or at a service, other than the claim as filed.
- **Rejected:** a conditional accept written onto this edge, an attachment on this edge, and a third ballot edge beside this one. Accept means the request as filed.

## Open questions

- None on this edge. A changed request is the proposal on [vote reject](../vote-reject/vote-reject.md): the reject may point at one request. This edge stays accept of the request as filed, with no attachment.
