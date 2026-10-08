# Vote reject
One seated person's recorded rejection of this case. It stays in the pool when later votes go the other way. It is never a vote on another case.

## Model

- `(case)-[:vote_reject]->(user)`

## Policies (rules)

- Same voter rule, same immutability, and same one-vote limit as [vote accept](../vote-accept/vote-accept.md). The vote is that person's own. A signature on another person's draft is not this edge.
- Rejecting five cases is five edges, one on each case. One reject edge on one case does not reject the others.
- There is no abstention. The person must choose and must explain.
- The person does not see another seated person's vote or reason before casting. Until every required judge has voted, no party sees this vote or its explanatory text.
- This edge is a reject of the claim as filed. A plain reject remains allowed. A plain reject points at no request.
- The request type this proposal points at already exists: [`computer/request`](../../../../computer/request/request.md) is a node type in this repository, and it carries `(request)-[:called]->(service)`, `(request)-[:sub_request_of]->(request)`, `(request)-[:authorized_by]->(rule)`, `(request)-[:data]->(---)`, `(request)-[:signature]->(---)`, `(request)-[:called_by]->(connection)`, and `(request)-[:request_time]->(time)`. What does not exist is an edge from a vote to that type.
- Proposal, model v6: a judge who wants a change rejects, and this reject may point at one request. The request is a `computer/request`, born by editing the draft request attached to the case. Editing produces a new request and leaves the case's filed service in place. The vote's text explains. The registered request wins. A typo in the explanation, writing 100 where the request says 1000, does not change the request. The pointer is not drawn as an edge. Who may create it, what validates it, and what triggers it are not stated.
- On a consensus case the reject points at no new request. That case files one request an earlier reject already points at, and fresh votes on it are accept or reject of that filing.
- This edge does not store several positive votes at several amounts or at several services. The reject tally does not split by which request is pointed at.
- Opened sources treat a partial grant as relief on the same claim. Critique v2 records Forlati (*infra petita*), Germany § 301 ZPO, and FRCP Rules 54 and 56. This file does not switch to that shape. The disagreement stays a recorded departure.
- A case with no vote edges is unanswered. It is not rejected.
- A party's score does not weight this vote.
- Human-language explanations stay timeline texts on the case. That text is not an invocable service parameter. The plaintiff's [grounds](../grounds/grounds.md) stay the plaintiff's text.
- What would falsify the reject-only rule: a judge who changes the claim's amount; or a stored positive vote at an amount other than the amount claimed. Model v4 point 5.
- What would falsify the attached-request pointer: All seated judges `vote_reject` with distinct attached requests and `ruling_accept` fires on the original filing. Critique v4. The attached requests are a proposal this repository has not ratified; the pointer is not a drawn edge.
- What would falsify the rule that the vote is that person's own: Two judges' conditional accepts are merged into one text without each judge's own accept/reject edge on that text. Critique v3. The merged conditional accepts are a proposal the pilot has not adopted.

## Placement

- **Its own edge type,** paired with vote-accept, so the two positions are not a field.
- **Nearest alternative rejected:** one blanket rejection edge on the petition path, copied by interpretation onto every case. The path is not a voter, and a case with no vote must remain visible as unanswered.
- **Nearest alternative rejected:** an accept on this same case at a lower amount, or at a different service, with the remainder deemed rejected. That is the source shape this revision departs from.
- **Proposal, not a drawn edge:** this reject may point at one `computer/request`. Accept does not. A consensus case does not grow a new request on this edge.
- A vote on one case is never a vote on another case. Hearing two claims together does not change that.

## Open questions

- **The draft request has no home edge.** `computer/request` exists and carries the edges listed above. The request the proposal calls "the draft request attached to the case" has no edge attaching it: not `computer/request` via `sub_request_of`, and not `claim_service`, whose endpoint is a service rather than a request. Who may edit it, and after votes exist, is not recorded either.
- **The owning module of the vote-to-request edge is not stated.** [case.handoff.md](../../case.handoff.md) asks which edge attaches the draft request. Which module owns the pointer is a separate question and is not recorded.
- The pointer to one request is a proposal. It is not an edge with create, validation, and trigger rules. Timeline text stays the explanation. A field on [vote accept](../vote-accept/vote-accept.md) is not the home.
