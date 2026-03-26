/* For license and copyright information please see the LEGAL file in the code repository */

package main_account_give

// [account, `main_account-give_for`, user] >>
//
// [user, `main_account-give_is`, account] >>

// Policy (rule):::
// Each two type of records just can on active `primary` relation.
// e.g. a `user` just can have one `primary` `account` or just have one `primary` `picture`
// rule::: each user in a FinancialCurrency MUST have just one account get this label.
// TODO::: When get this label `Owner` label can get back or not??
// MainAccount
// PrimaryAccount
