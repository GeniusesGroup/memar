/* For license and copyright information please see the LEGAL file in the code repository */

package gives

// [transaction, `gives`, account] >>

// Policy (rule):::
//     =~ SELL
// but `sell` is not good name as other side MUST be `money` not other types.
//
// Indicate what will gives in this transaction
// It is optional! It means a `user` want to `takes` something without `gives` anything!
// https://en.wikipedia.org/wiki/Negative_pricing
//
// Use financial account to support almost all transaction types
// e.g. bond be exchanged for currency and deposits
// e.g. sell product and buy other product by JUST move inventory to middle temp accounts.
