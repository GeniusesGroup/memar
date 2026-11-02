# Form status

## Model

- Candidate (unconfirmed): a form Status-kind [label](../../../../../modules/knowledge/label/label.md) — `Terminated` (one word in the source; whether it takes `Status` unconfirmed).

## Policies (rules)

- Only the status word recorded — what Terminated blocks (answering? editing? viewing?) is absent from the source (no bare edges).

## Placement

- **Correct here — a domain Status-kind word belongs with the domain that owns the claim** ([Documentation → Status](../../../../../modules-plugable/knowledge/documentation/documentation.md#status): general words under `thing/labels/`, domain-specific ones under that domain's `labels/` as `Label_<Word>` taking `Label_Status`; the form domain states its candidate here, never repeating the list in [form.md](../../form.md)).
- **Not a general Status-kind word on thing:** `Terminated` is form-specific vocabulary — placed with the form capability that gives it meaning (placement by entry point; pluggable owns complete capability: the label + the answering-session rules that read it).
- **Not a new module:** one status word is not processing semantics (parameters vs semantics; prefer existing homes over inventing new modules).
- Confirm before ratifying that Terminated is Status-kind (takes `Label_Status`) rather than another label kind ([Documentation → Status](../../../../../modules-plugable/knowledge/documentation/documentation.md#status); no bare edges).

## Open questions

- Own form Status-kind set under form `labels/`, or a shared word under `thing/labels/`? (Receiving [form.md](../../form.md) backlog question.)
- What does Terminated block, and who attaches or withdraws it (no bare edges)?
- Interaction with `Type_Duration`/`Type_StartPoint` type flags ([types](../types/types.md)) — does termination follow the duration, or is it an explicit move?

