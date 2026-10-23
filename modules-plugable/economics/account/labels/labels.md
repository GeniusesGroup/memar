---
Title: "Account labels"
Status: Draft
Start Date: 2026-09-24
ID: 497284
---

# Account labels
Registered meanings of words a person may attach to an account.

## Abstract
Real and Personal are [labels](../../../../modules/knowledge/label/label.md) on an account. They are not kinds of account, and they are not fields of the account kernel. The kernel stays the [bookkeeping](../../../../modules/economics/account/edges/bookkeeping/bookkeeping.md) edge. Attaching a word uses that label domain's `(thing)-[:label]`. This module does not add another edge.

## Explanation

### Definition
An organization includes this module when it wants a registry of account-comment labels. Each document under this module is one registered word: what a reader may mean by it, and what it does not do.

Registration does not choose who may attach the word, and it does not change the quantity the account holds.

### What a registered label does not do
- It does not make a second kind of account. Every account is still the holder of one countable quantity.
- It does not keep the balance. Balance is the bookkeeping snapshot.
- It is not the node's identity.

### Registered words
- [Real](real/real.md)
- [Personal](personal/personal.md)

## Open questions
- Asset, Liability, Equity, Revenue, and Expense were written as an open question beside Real and Personal. They read as categories of a quantity's role in a ledger, which may be bookkeeping rather than a label on the account node. They are not registered until that is decided.
