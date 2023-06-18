/* For license and copyright information please see the LEGAL file in the code repository */

package ftp

import (
	"libgo/protocol"

	fap "org/modules/financial-account/protocol"
	urp "org/modules/user-request/protocol"
)

// DataModel indicate the domain record data fields.
// each FinancialTransaction is an immutable record and so use version mechanism to chain FinancialTransactions in AccountID way.
type DataModel interface {
	AccountID() fap.FinancialAccountUUID     //
	AccountSideID() fap.FinancialAccountUUID // or AccountPartyID
	Reference() [16]byte                     // Any ID that user can assign to track for any purpose. It can't be nil.
	ReferenceType() FinancialTransaction_RT  //
	Amount() protocol.MoneyAmount            // This transaction
	Balance() protocol.MoneyAmount           // Account balance with this transaction
	SaveTime() protocol.Time                 //
	RequestID() urp.UserRequestUUID          //
}

// libgo: ganjine --ShardConsistency=strict

// FinancialTransaction_RT indicate FinancialTransaction record reference type
type FinancialTransaction_RT uint8

// FinancialTransaction types
const (
	FinancialTransaction_RT_Unset   FinancialTransaction_RT = iota
	FinancialTransaction_RT_Failed                          // Refund for any reason e.g. not same currency account, not reachable bank, ...
	FinancialTransaction_RT_Blocked                         // by justice
	FinancialTransaction_RT_TransactionFee
	FinancialTransaction_RT_Exchange
	FinancialTransaction_RT_Prize
	FinancialTransaction_RT_Donate
	FinancialTransaction_RT_Charity
	FinancialTransaction_RT_Tip
	FinancialTransaction_RT_Cash          // InvoiceID, PosID >> Due to digital era banking, prefer to not support cash transactions
	FinancialTransaction_RT_RevolvingFund // >> Due to digital era banking, prefer to not support this type
	// FinancialTransaction_RT_SameBankTransfer     >> Not the goal and just the way of transaction that can check by RequestID
	// FinancialTransaction_RT_ForeignBankTransfer  >> Not the goal and just the way of transaction that can check by RequestID
	// FinancialTransaction_RT_POSTransfer          >> Not the goal and just the way of transaction that can check by RequestID
	// FinancialTransaction_RT_WebTransfer          >> Not the goal and just the way of transaction that can check by RequestID
	FinancialTransaction_RT_Asset
	FinancialTransaction_RT_Stock
	FinancialTransaction_RT_RentalFee
	FinancialTransaction_RT_Bill
	FinancialTransaction_RT_Invoice // both buy or refund for any reason(ReturnInvoice)
	FinancialTransaction_RT_Tax
	FinancialTransaction_RT_Commission
	FinancialTransaction_RT_Salary // Reward
	FinancialTransaction_RT_Profit
	FinancialTransaction_RT_Credit
	FinancialTransaction_RT_Loan
	FinancialTransaction_RT_BadDebt // Debt default
	FinancialTransaction_RT_Installment
	FinancialTransaction_RT_Compensation
	FinancialTransaction_RT_Order
)
