# Subject
Subject (mouzu) is the case. It is not a second node beside the request.

## Model

- No edge type named `subject`.
- The proposition the complaint asserts is the case, read together with [grounds](../grounds/grounds.md) and [evidence](../evidence/evidence.md).
- The request (darkhast) is [claim service](../service/service.md): the one organization service this case invokes.

## Policies (rules)

- A ruling accepts or rejects the case, which accepts or rejects that invocation as it was filed. The ruling does not accept the grounds and refuse the service as two outcomes. It does not substitute a different service.
- The filed service's input is not only a number. A number is one input. A text written on the defendant's timeline, addressed to the claimant, is another. The case does not own that input. Same parties and the same amount are already not the same claim. See [refiling](../refiling/refiling.md). A changed execution is a new request a [vote reject](../vote-reject/vote-reject.md) may point at. The claimant may file that one request as a later case. The ruling on this case does not substitute it.

## Placement

- **Not an edge.** The attribute-or-edge test already sends the prose to [text](../../../../knowledge/text/README.md) and the invoked service off the case. Those two edges are the split between "why" and "what is asked." They are not two concepts with two lifecycles.
- **Nearest alternative rejected:** a subject node and a request node, each with its own ruling. That split would survive only if a ruling must be able to accept one and refuse the other. No such ruling is recorded. One vote pair on the case is the ruling.
- What would make this placement wrong: a complaint whose proposition is accepted and whose service is refused, or the reverse, and that split has to be queried as two results. Then each part needs its own votes.

## Open questions

- The changed input is the proposal that a reject may point at one `computer/request`. The vote-to-request edge is not drawn. Same parties and the same amount do not decide it.
