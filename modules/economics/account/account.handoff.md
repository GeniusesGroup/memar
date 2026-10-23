# Account Handoff

## Topic & Purpose
Load-bearing decisions for the Account domain: quantity-general bookkeeping holder (not money), unit ownership, balance vs availability, and naming. Consolidated from Account & Transaction modeling chats (2026-08) and the Organization ideas backlog (2026-09-16 migration).

## Status
Active — kernel practiced in README; naming and AvailableBalance trust still open.

## Decisions

### From accounting invariants (formerly `modules/economics/accounting-invariants.md`)

#### 4. Unit belongs to the account, not the transaction
The count unit is declared once per account via the general `(thing)-[:count_unit_is]->(count_unit)` edge. Both accounts of one transaction MUST share the same count unit; the transaction stores only a quantity.

#### 8 (account-side). Availability is not account state
`AvailableBalance`-style values are derived from mutable global constraints (legal blocks, pending reservations) and MUST NOT be stored as account fields; they are evaluated from rules (see `modules-plugable/economics/restriction`). Balance snapshot as a bookkeeping-record fact lives on the [bookkeeping](edges/bookkeeping/README.md) edge.

### From Organization ideas backlog

- **Account ≠ money.** An Account maintains the state of *a quantity*; a Transaction records changes to quantities. The quantity may be currency, kilograms of iron, shares — the bookkeeping structure is the same. The name "Accounting" was deliberately avoided because it carries a money reading; the generalized concept is closer to "bookkeeping of quantities and their changes". *(naming — open)*
- **Unit homogeneity.** A single accounting Transaction is same-unit (bookkeeping needs summable/balanceable changes); unit belongs to the Account — defined once — not repeated per Transaction. Cross-unit operations (1000 EUR ↔ 1000 kg iron) belong to a higher **Trade/Exchange** concept linking two homogeneous Transactions. *(decided)* — exchange ownership: [`matching_system`](../../../modules-plugable/economics/matching_system/README.md).
- **Identity for non-UUID records** (e.g. a check number) draws from the `uri` domain (as with usernames), not a bespoke field on Transaction/Account. *(decided)*
- **Core vs. optional is relative to purpose.** Discount without which the organization still buys and sells; Product/Invoice/Account without which an ERP is unrepresentable — but the attribute is not intrinsic to the module (a charity or a government has "sales" too). *(decided)* — Account is core here by necessity (removing it forces fabrication of another foundational quantity-holder); a future repo-wide placement audit may still re-check edges nested under this module.

## Ambiguities Resolved
- Per-change `(quantity, unit)` on the transaction — resolved: rejected; the unit is a stable account property; repeating it per transaction adds no information and permits unbalanced mixed-unit transactions.
- Per-account `AvailableBalance` as legacy model (~10 years old) — resolved: rejected because a global constraint (one judicial block of 1000) copied per account multiplies it (100 accounts × 1000). See restriction module and wage garnishment / bank levy regulation precedent (e.g. US 31 CFR 212.7).

## Open Questions
1. Final name for the quantity-bookkeeping concept (avoid money-only "Accounting") — *(naming — open)*.
2. **"AvailableBalance" trust question** and precise effect of pending Transactions on the Account before AvailableBalance is treated as fundamental truth — *(open; also on bookkeeping)*.
3. Should the account expose a cached "last index" pointer for O(1) balance reads, or is that purely an engine detail?
4. `Field_AccountID` and the account UUID type carry legacy "financial" framing; rename pending.
5. **`Field_Balance`'s stated meaning contradicts the domain.** The Go comment in `edges/bookkeeping/protocol/dt-balance.kh` says Balance "is the total of all the transactions on the account including any pending transactions", while [bookkeeping.md](edges/bookkeeping/bookkeeping.md) §8 and the Policies above make Balance an immutable snapshot of *this record's* realized effect, on a record that only exists once the effect has actually been booked. The two readings differ on exactly the question open #2 is about: under the comment's reading a pending transaction would change a stored balance, which is what "snapshot, never recomputed" forbids. This is a finding about the domain's meaning, not about the conversion. *(open)*

### From Account Research 001 (2026-10-18, agent proposals, nothing ratified)
Each entry: the question, the recommended default, what it blocks. Ordered by what they change: those that change what the domain is first. Reasoning, ten scenarios and six rival models are in [Account Research 001](account.research.001.md#open-questions).
1. **Is the account a domain whose responsibility is the ordered, append-only ledger of one quantity of one unit, or a classification on `thing` with the `bookkeeping` edge as its own module?** Default: a domain. Blocks: the rewrite of the opening paragraph of [account.md](account.md), model B versus C, `AccountModel` beyond `ThingModel` (Khayyam rule 6).
2. **What is the other side of creation, destruction, correction and transformation: may a transaction have no source, or is there a counterpart account per unit?** Default: counterpart accounts. Blocks: transaction's optional source and invariant 3, issuance, opening balances, stocktake, spoilage, `pack` and production legs.
3. **How does an account relate to its holder?** Default: no holder edge in the account domain; title on `rights/ownership` (with fractions if it becomes a node), instruction by delegation, reading by authorization; one edge name (`owner_of` or `own_by`). Blocks: the `own_by` contradiction, `salary`, joint accounts, heirs, the `Personal` label.
4. **Are opening and closing acquired facts with declarer and time; may a closed account be written to; may an account close with a non-zero balance; what does an account with no record read?** Default: status events; no record on a closed account; close only at zero; an empty account reads zero. Blocks: the lifecycle, the status vocabulary, dormant and unclaimed accounts.
5. **Is the count unit fixed once the first record exists?** Default: fixed; change is a new account and a conversion pair. Blocks: the lifecycle, redenomination, product question 8.
6. **Which time orders the ledger?** Default: the index orders recording; the effective time is a field of the transaction; "as of a date" is discovered. Blocks: statements, back-dated entries, the bookkeeping data model.
7. **Does the Balance ever include pending transactions?** Default: no (catalogue E6); a pending effect on availability is a restriction reservation. Blocks: open 2 and 5 above, the comment in `dt-balance.kh`.
8. **Is `TransactionIndex` a domain contract, with the last-index pointer and `Lock`/`Unlock` as engine details?** Default: contract for the ordinal only. Blocks: open 3 above, `storage.kh` keys.
9. **May an account hold identified units (serials, vehicles, credits)?** Default: fungible only; identified units are things in an account of one piece or a registry. Blocks: carbon and asset registries, product question 11.
10. **Is a lot (tranche, serial, batch) an account of its own with the pool a grouping?** Default: yes; expiry is a rule creating transactions. Blocks: club-coin, loyalty, lot valuation, `batch/accounting`.
11. **Is the credit module's per-account flag enough, or is credit a limit with a value that rules change?** Default: a limit. Blocks: [credit](../../../modules-plugable/economics/credit/credit.md), mutual credit, overdraft rules.
12. **Do the words that say what an account is for (cash, credit, deposit, refund, tax deposit, Real, Personal, Asset/Liability/Equity/Revenue/Expense) live in one registered vocabulary?** Default: yes, a loop-edge only where processing needs one. Blocks: the account-labels open question, POS and VAT `financial-account`, `cash_account`, `credit_account`.
13. **Across organizations, is each organization's ledger authoritative for its own accounts, a cross-organization payment being a transaction in each linked by settlement?** Default: yes. Blocks: invoice exchange, the settlement edge shape, product question 4, task question 16.
14. **May a holder's identity be detached from an account's history, leaving the effects?** Default: yes, by an authority-gated event; the ledger is never erased. Blocks: retention policy, content question 7 and text question 15.
15. **Who refuses a movement between accounts of different units: the account at booking, or the transaction at registration?** Default: the account at booking. Blocks: the duplicate rule in [transaction.md](../transaction/transaction.md#policies-rules).
16. **Does the concept keep the name "account", with "bookkeeping" for its edge?** Default: keep both. Blocks: open 1 above, the `Field_AccountID` naming sweep.
17. **Is a budget line an account or a constraint that observes accounts?** Default: a constraint of the budget module. Blocks: the budget module's six edges, the one copy of the budget relation with task.
18. **Where does a cross-account invariant live (a trust account equals the sum of customers' electronic value)?** Default: a reconciliation capability in settlement; a mismatch is reported, never silently corrected. Blocks: settlement's internal structure, e-money and custody products.

### Contradictions between this domain's documents and its neighbours (reported by Account Research 001, not resolved)
See [Contradictions found](account.research.001.md#contradictions-found): the meaning of `Balance` (the Go comment against the snapshot rule); conservation against creation (no document says where the first unit of a thing comes from); four statements of how an account relates to its holder (`owner_of`, `owner_is`, `own_by`, the `Personal` label); two vocabularies for an account's role; a transaction quantity with no unit when both accounts are optional; the budget relation in two homes; the same shape of limit in two buckets; the kernel documents naming pluggables; the same-unit rule stated in two domains; the Status wording "kernel practiced in README".

## Assumptions
- Holding/possession (bookkeeping balance) ≠ legal title (`rights/ownership`).
- Negative balance is neither allowed nor forbidden by the kernel; pluggable rules govern credit/overdraft.

## Key Definitions Established
- Account: bookkeeping holder of one countable quantity with one count unit — not financial by nature.

## Proposed Next Steps
1. Close naming (open #1) with dictionary + rename guard.
2. Define pending-transaction effect on availability jointly with restriction and bookkeeping (open #2).
3. After the owner answers Account Research 001 questions 1 to 3 (what the domain is responsible for, the other side of creation and destruction, the holder relation): rewrite the opening paragraph of [account.md](account.md) and its Unresolved questions, and decide between the ledger-kernel model and the classification-only model ([rival models](account.research.001.md#3-rival-models)).
4. Apply the folder mapping ([finding 5](account.research.001.md#5-how-the-existing-edge-folders-map)) one area at a time, adding to each account-touching pluggable the creator, remover and trigger it lacks; settle the budget relation with the task domain's `settlement-reference` in the same pass.
5. Design the missing pieces the research sketches ([finding 6](account.research.001.md#6-missing-edges-and-modules)): the status loop-edge, `counterpart` (check against settlement and securities), `lot` and `expiry` (check against batch and club-coin), instruction authority (check against `rights/delegate`), and `reconciliation` in settlement.
6. Start a transaction research and an invoice research from the contradictions reported here (optional source, unit-less quantity, the duplicate same-unit rule, invoice exchange); the pair is best read together with this research.
7. Turn the test scenarios ([finding 7](account.research.001.md#7-test-scenarios)) into tests once questions 1 to 8 are answered; scenarios marked "kept" can be written now.
8. Reconcile the contradictions the research reports (Contradictions section above) by the owner's answers, recording each through the changelog.

## Related Artifacts
- [`account.research.001.md`](account.research.001.md) — what the domain is for, kernel and pluggable, rival models, folder mapping, missing modules, 26 test scenarios, 18 owner questions (Review; unratified)
- [`account.changelog.md`](account.changelog.md) — entry for the research (Update, done)
- [`README.md`](README.md)
- [`edges/bookkeeping/README.md`](edges/bookkeeping/README.md)
- [`../transaction/transaction.handoff.md`](../transaction/transaction.handoff.md)
- [`../../../modules-plugable/economics/restriction/README.md`](../../../modules-plugable/economics/restriction/README.md)

## Notes
- Provenance: former `accounting-invariants.md` §§4, 8 (account-side) + Organization ideas backlog Account bullets.

## Khayyam conversion (2026-10-03)

Converted: `protocol/dt-uuid.kh`, `edges/bookkeeping/protocol/dt-balance.kh`, `dt-transaction-index.kh`, `data_model.kh`, `ss-event_target.kh`, `storage.kh`. All six return `accept` from the Khayyam frontend.

Decisions:

- **`Field_AccountID`** with accessor `AccountID`, valued as `ThingUUID` imported from `identity/thing` — the Go's `type UUID thing_p.UUID` is not re-declared as a local abstraction (rule 6; same shape as the rule/module/taxon/estate conversions). This answers the naming half of open #4 for the field: the `AccountID` spelling is now the one in the tree, though no general `Field_XUUID` → `Field_XID` sweep has been run.
- **`Field_Balance`** with accessor `Balance` returning `Decimal_Quantity`, imported from `memar/modules/math/decimal/protocol/dt-quantity.kh` (the Go said `Balance decimal_p.Quantity`). The accessor keeps Go's noun name: it is a `Field_*` accessor, where this repository's ruling (see the receiver-method-names and method-verb-phrases rules, and `Field_LabelType`/`LabelType`) keeps the bare concept.
- **`Field_TransactionIndex`** with accessor `TransactionIndex` returning `Container_ElementIndex` (Go: `container_p.ElementIndex`). `TransactionIndex` is the field abstraction's accessor, so a storage method that takes an index takes `Container_ElementIndex` directly rather than the accessor type.
- **`BookkeepingDataModel`** composes `Field_AccountID`, `Field_Balance`, `Field_TransactionID`, `Field_TransactionIndex`, and memar's `Observer_RequestID` + `Observer_Time_Request` — the Go's `request_p.Field_RequestID` and `audit_time_p.Field_Request`, whose real content is the request identity and its time, and whose declarations are memar's to own.
- **`BookkeepingStorage`** declares `Save`, `Lock`, `Unlock`, `GetByTransactionIndex`, `GetByTransactionID`. `Lock`/`Unlock` are kept because the per-account write-serialization point is a load-bearing decision ([bookkeeping.md](edges/bookkeeping/bookkeeping.md) Drawbacks), not because the Go's implementation was correct.
- **`BookkeepingEventTarget` / `BookkeepingEventTarget_Event`** from `ss-event_target.kh`, dropping the `SS_` storage-service prefix for the domain-qualified name the qualified-names rule asks for.

Left unconverted, with reasons:

- **`protocol/service-storage-save.kh`** — **legacy scaffolding for a record the domain no longer has.** Its `FinancialAccount_StorageService_Save_req` requires a `FinancialAccount`; its whole `FinancialAccount_StorageServices` is already commented out in Go; and its `FinancialAccount_businessServices` is an empty Go interface, which rule 6 forbids converting into an empty `ab`. An account under the current model is a `thing` whose unit comes from `count_unit_is` and whose only kernel edge is bookkeeping — it stores no record of its own, so there is nothing for a storage-service surface to save. Disposition: delete, or re-derive if an account record is ever reintroduced.
- **`edges/bookkeeping/protocol/storage.kh`, the non-storage half** — `Storage_Key_Primary` and `Storage_Key_Cluster` are two declarations that the module path would name identically, each nothing but `Field_AccountID` (the qualified-names rule's "one concept declared twice" case; the corpus-wide `_2` counters beside them are its evidence). They are also probably wrong: a bookkeeping record's primary key is `(accountID, transactionIndex)`, not `accountID` alone, since one account has many records. The `SS_FIND_AccountIDs_BY_UserID` / `SS_LIST_CurrencyIDs_BY_UserID` request-response pairs are dead scaffolding — they resolve accounts by user and list financial currency IDs, both of which [account.md](account.md) puts in pluggable modules and out of this kernel.
- `_import/**` — none under this domain.

Open from this pass:

- **The two key declarations above.** If the storage engine's key vocabulary is wanted back, `Storage_Key_Primary` needs to be re-derived as the `(accountID, transactionIndex)` pair first; the `Field_AccountID`-only form should not be carried forward as-is.
- **`dt-balance.kh` carries a misplaced comment.** Its second comment — "TransactionIndex will auto increment number in each AccountID" — describes `TransactionIndex`, not `Balance`, and the same sentence is duplicated in `dt-transaction-index.kh`. Both files converted without it; the text belongs in [bookkeeping.md](edges/bookkeeping/bookkeeping.md) Fields, which already carries it.
- **`ss-event_target.kh` is an instantiation of a generic** (`event_p.Target[SS_EventTarget_Event]`). The conversion declares two domain-named abstractions instead, which is the only shape Khayyam has; whether `BookkeepingEventTarget_Event` should keep existing at all depends on the same open question as the transaction target (see [../transaction/transaction.handoff.md](../transaction/transaction.handoff.md)).
