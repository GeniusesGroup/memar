# Expired

The invoice has expired: the customer cannot pay against it anymore, and it can neither be cancelled nor deleted - view only.

**Review question**: what sets expiry - a rule (validity duration) or an explicit action? Where does the expiry time live?

**Open question (2026-10-10)**: is a price-validity window one cause of expiry? An issued-but-unpaid invoice or pro-forma keeps its issue-date price while prices move, as price inputs have a maximum age ([replacement cost staleness](../../../../../modules-plugable/economics/replacement-cost/replacement-cost.md#policies-rules)); who sets that window, and does it run per invoice or per [item](../../edges/item/item.md#open-questions)?
