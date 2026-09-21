# Credit

Credit — money that exists as debt — is NOT modeled by the kernel. This module currently only records that an account can be in a credit state (allowing negative balance) vs a cash state; that is a label, not a premise: organizations without credit must be able to simply not install this.

## Model

- [credit_account](edges-loop/credit_account/README.md) — draft edge marking an account's credit state.

## Policies (rules)

- Negative balance is neither allowed nor forbidden by the account kernel; installing this module is what makes it possible, per account.
- Overdraft consequences (fee after long overdraft, forced liquidation of holdings) are rules reacting to balance events, not fields here.

## Discussion

### Drawbacks

- A single flag understates the domain; leaving more here risks half-modeling debt-based money.

### Rationale and alternatives

- Credit limits as account fields were rejected (policy, not identity).
- Modeling money-creation as a kernel capability was rejected: it decomposes into two transactions between two accounts with two different units (see settlement discussion).

### Prior art

- Credit card debt / revolving credit — the closest existing model; deliberately not copied.

### Unresolved questions

- The full debt-based-money model was explicitly deferred to a dedicated session; nothing here should be treated as its design.
- Interaction of credit state with restriction and settlement rules on the same account.

### Future possibilities

- Lending as transactions between accounts with different units (principal vs interest obligations) — must be tested against invariants #4/#5.
