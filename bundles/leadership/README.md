<!--
  NOTE: consolidated from a ChatGPT conversation (Omid, 2026-07-21):
  https://chatgpt.com/g/g-p-6a4e21c9b9548191a86d6761bf57ea34/c/6a5f2c5c-d754-83ed-9c60-517d90a28340
  Everything of lasting value from that chat is captured here, so the chat
  can be safely deleted. This is a seed document, not a finished RFC.
-->

# Leadership

**Status: composition bundle — deliberately NOT a module.** This bundle owns no schema of its own (no node, no edge, no rule). It is a named composition of capabilities that live in other modules, provided for organizations that want "leadership" features without the umbrella word ever entering the data model.

## Why a bundle and not a module

"Leadership" is an **umbrella concept**, not an operational management concept. Per [core-vs-pluggable criteria](../../modules/economics/core-vs-pluggable.md), a module must own a complete capability (edges with identifiable semantics + processing, installable/removable as a unit; bare edges forbidden). No such capability exists here to own:

- Delegation of authority → `modules/rights/delegate`
- Mentorship / sponsorship relationships → `modules/identity/person/edges/social_connections` (mentor, mentee)
- Oversight membership, small single-purpose membership edges → `modules/management/group/README.md`
- Concrete positions (C-level manager, judge, shift lead) → `modules/management/role`
- Incentive design → rules domain (`modules/computer/rule`)

Each of those is already a first-class capability elsewhere. A `leadership` module would have nothing of its own to own — it would be a reification of a colloquial word, precisely the failure this document argues against. A bundle that composes them is the honest answer to "where do we put this concept": the word lives here, the semantics live in the real modules.

## Summary of the position

"Leadership" must not be placed at the same tier as operational management concepts (Planning, Budgeting, Coordination, Incentive, Governance, Delegation, Feedback, Process, ...). It is a colloquial label covering a set of behaviors, relationships, and organizational mechanisms. It is not useless — the problem starts when the umbrella is mistaken for a real entity, i.e. when the word itself replaces the concrete components underneath it. Those concrete mechanisms are what this bundle composes.

## The three usages that keep getting conflated

1. **Leadership as a common word** — everyday language, no fixed meaning.
2. **Leadership as a philosophical-normative concept** — e.g. Simon Sinek's "Leadership is a lifestyle, not a position". Inspiring, but this has moved into ethics/philosophy of life; ask ten people what "leadership behavior" is, get ten different answers, and nothing measurable comes out.
3. **Leadership as a research subject in organizational science** — decades of attempts at operationalization (Trait Theory, Behavioral Theory, Situational Leadership, Transformational, Transactional, Servant Leadership).

Compare: "inventory level" or "delivery time" are understood nearly identically by everyone in management; after roughly a century of research, "Leadership" still has fundamental disagreement about what it even refers to. That is a signal about the weak boundaries of the concept itself.

## The post-hoc label critique

Much of what is called "great leadership" is an interpretive label applied after the fact: a team succeeds → "they had a good leader"; the same team fails → "they had a weak leader". This is a post hoc explanation. What actually produced the outcome may be:

- a suitable organizational structure,
- correct economic incentives,
- selecting the right people,
- a healthy organizational culture,
- luck.

All of it gets collapsed into one magic word. This resembles explaining natural phenomena with the 19th-century "vital force" (élan vital): a word that names the mystery instead of explaining it.

## What entity is it? (the modeling danger)

If we tried to model "leadership" as an entity, the first question is: what does the term refer to?

- A Role?
- A Capability?
- A Behavior?
- A Relationship?
- An Outcome?

The leadership literature gives no stable answer — sometimes the person is called the leadership, sometimes the behavior, sometimes the outcome, sometimes the culture. Using one term for several different entities is a warning sign in modeling, and it is precisely why it must not be made a sibling of operational concepts like Planning (an observable activity), Budget (a concrete artifact), Process (a modelable structure), or Incentive (a specific mechanism).

## The maturity trajectory (why staying at the word level is suspicious)

Mature sciences show a characteristic path: vague concept → theories → operationalization → measurable variables → the original umbrella word fades while the concrete mechanisms take over. "Intelligence" is the canonical example: working psychologists rarely argue about Intelligence as such; they work with Working Memory, Processing Speed, Verbal Reasoning, Spatial Ability.

"Leadership" broke this pattern: after ~100 years of research, most of the literature is still at the word level. Bestsellers still say "Be a better leader" — not "improve trust formation mechanisms", "improve organizational alignment", or "improve coordination structures". A word that resists decomposition for a century is, at minimum, a word to classify very carefully.

## Misattributed findings

Much of the value currently credited to "leadership research" was actually produced by other disciplines and later relabeled: personality psychology, social psychology, cognitive science, sociology, network science. Trait Theory, for instance, belongs to psychology/cognitive science in origin and is not specific to leadership at all. If extraversion correlates with social influence, that discovery belongs to personality psychology; "leadership" is merely one of its application sites. Findings should be evaluated independently of the word — the word did not create them.

## What this bundle composes (concrete capabilities)

| Umbrella gesture | Concrete capability | Lives in |
|---|---|---|
| "Empower people to act for you" | Delegation | `modules/rights/delegate` |
| "Develop people" | Mentor/mentee, sponsorship edges | `modules/identity/person/edges/social_connections` |
| "Guide the group" | Concrete roles + oversight membership | `modules/management/role`, `modules/management/group` |
| "Align and coordinate" | Coordination structures, task decomposition | `modules/management/task`, `modules/management/department` |
| "Motivate" | Incentive rules | `modules/computer/rule` |
| "Communicate direction" | Timeline/event broadcast | `modules/management/timeline` |

Rules for this bundle:

- It must never define a schema entity named "leader/leadership" (no attribute, no node type, no abstract capability edge).
- A GUI service request phrased as "add leadership to X" must be decomposed into the table above before design work starts.
- If a genuinely operationalized leadership-like construct ever reaches consensus in the literature (see unresolved #1), *then* this bundle may be promoted to a real module owning that construct.

## Related

- [`modules/management/README.md`](../../modules/management/README.md) — Fayol's functions, incl. Commanding (leading)
- [`modules/management/group/README.md`](../../modules/management/group/README.md) — membership decomposition, oversight membership
- [`modules/management/role/README.md`](../../modules/management/role/README.md) — roles as sets of behaviors/norms
- [`modules/rights/README.md`](../../modules/rights/README.md) — delegation
- [`modules/economics/core-vs-pluggable.md`](../../modules/economics/core-vs-pluggable.md) — module ownership criteria this bundle relies on

## Discussion

### Drawbacks

- The umbrella word is convenient shorthand; refusing it makes communication wordier ("trust formation mechanisms" vs "leadership"), and the team must stay disciplined about decomposing instead of just banning the word.
- A composition bundle adds one more indirection layer: readers looking for "leadership functionality" must hop through this README to the owning modules.
- The position rests partly on an unsettled empirical bet: the word may yet be successfully decomposed (see unresolved #1), in which case a precise, legitimate construct could re-emerge and this bundle would need revision or promotion to a module.

### Rationale and alternatives

- Alternative considered: model "leadership" as a first-class entity (a capability/attribute on persons or roles). Rejected: the literature cannot say consistently what entity it is (Role/Capability/Behavior/Relationship/Outcome), so any schema choice would silently pick one meaning among several.
- Alternative considered: a real pluggable module at `modules-plugable/management/leadership`. Rejected for now: a module must own a complete capability with identifiable edge semantics; everything "leadership" gestures at already has an owner, so the module would own nothing and violate the no-bare-edges / complete-capability criteria.
- Alternative considered: keep the word out of the repo entirely (documentation only). Rejected: the question "where does this concept go?" deserves a visible, findable answer at exactly the path a future contributor would search — this bundle README is that answer.
- The intelligence analogy drove the choice: mature fields decompose their umbrella words into measurable constructs; a word that has resisted decomposition for a century while remaining bestseller material is treated as colloquial until proven otherwise.

### Prior art

- Simon Sinek, "Leadership is a lifestyle, not a position" — the normative/lifestyle usage that motivated the discussion (inspirational, not operational).
- The operationalization attempts inside leadership studies: Trait, Behavioral, Situational, Transformational, Transactional, Servant Leadership — a century without firm consensus.
- "Vital force" (élan vital) in 19th-century biology — the archetype of a label that names a mystery instead of explaining it.
- Operationalization of "Intelligence" into Working Memory / Processing Speed / Verbal Reasoning / Spatial Ability — the positive example of a discipline dissolving its umbrella word.
- Ambiguity of Value / Utility / Welfare in early economics, later given rigorous mathematical frameworks — the counterexample showing an ambiguous word can mature, and why hypothesis #2 below cannot be dismissed.
- Related umbrella abstractions with the same failure mode when reified: Quality, Culture, Trust.

### Unresolved questions

1. **Word problem or discipline problem?** Is the fault in the word "Leadership" itself, or in the insufficient maturity of management science as a discipline? Two hypotheses remain open and logically exclusive:
   - (a) Leadership is inherently an umbrella concept, irreducible to operational components;
   - (b) Leadership is simply not yet decomposed and modeled well enough.
   Notably, after ~100 years of research there is still no consensus choosing between them — which is itself the strongest evidence in favor of treating the word cautiously.
2. Should `role` ever define a generic "lead" role edge for groups, or only concrete roles (C-level manager, judge, shift lead) with delegation? (Connects to the mechanism-choice question in `group/README.md` unresolved #1.)
3. Is the mentor/mentee edge set sufficient as the concrete decomposition of one leadership-adjacent mechanism, or do we need more (e.g. sponsorship, supervision, coaching as distinct edges)?
4. How should a GUI service expose "assign a lead" without introducing the umbrella word into the data model — what is the canonical phrasing/edge set?

### Future possibilities

- Use this document as a boundary test during `role`/`group` service design: every proposed entity named after an abstraction (leader, culture, trust) must pass the "what node/edge/rule is it?" question before entering a schema.
- Watch the literature for a genuinely operationalized leadership-like construct; if one reaches consensus, revisit hypothesis (b) and promote this bundle to a real module owning that construct.
- A checklist entry for the low-code GUI: when a builder-facing service template uses the word "leadership", force decomposition into selectable concrete mechanisms (delegation, mentorship, coordination structure, incentive rule) instead of exposing a "leadership" toggle.

## Test cases any resolved criterion must pass

- A military commander with formal authority — decidable purely via role + delegation edges?
- An informal friend group where one person habitually organizes everything but holds no role — is any entity needed, or is the observed behavior just emergent?
- A DAO "core team" with pseudonymous members and no registered hierarchy — where does coordination structure live?
- A mentor/mentee pair — should map to the existing social-connection edges, not to any "leadership" attribute.
- A CEO praised post hoc for "great leadership" after success — the model must be able to attribute the outcome to structure, incentives, people, culture, or luck, without needing the umbrella word.
