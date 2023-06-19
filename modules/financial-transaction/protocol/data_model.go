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
	Reference() protocol.UUID                // Any ID that user can assign to track for any purpose. It can't be nil.
	ReferenceType() ReferenceType            //
	Amount() protocol.MoneyAmount            // This transaction
	Balance() protocol.MoneyAmount           // Account balance with this transaction
	SaveTime() protocol.Time                 //
	RequestID() urp.UserRequestUUID          //
}

// libgo: ganjine --ShardConsistency=strict

// ReferenceType indicate FinancialTransaction record reference type
type ReferenceType uint8

// FinancialTransaction types
const (
	ReferenceType_Unset   ReferenceType = iota
	ReferenceType_Failed                // Refund for any reason e.g. not same currency account, not reachable bank, ...
	ReferenceType_Blocked               // by justice
	ReferenceType_TransactionFee
	ReferenceType_Exchange
	ReferenceType_Prize
	ReferenceType_Donate
	ReferenceType_Charity
	ReferenceType_Tip
	ReferenceType_Cash          // InvoiceID, PosID >> Due to digital era banking, prefer to not support cash transactions
	ReferenceType_RevolvingFund // >> Due to digital era banking, prefer to not support this type
	// ReferenceType_SameBankTransfer     >> Not the goal and just the way of transaction that can check by RequestID
	// ReferenceType_ForeignBankTransfer  >> Not the goal and just the way of transaction that can check by RequestID
	// ReferenceType_POSTransfer          >> Not the goal and just the way of transaction that can check by RequestID
	// ReferenceType_WebTransfer          >> Not the goal and just the way of transaction that can check by RequestID
	ReferenceType_Asset
	ReferenceType_Stock
	ReferenceType_RentalFee
	ReferenceType_Bill
	ReferenceType_Invoice // both buy or refund for any reason(ReturnInvoice)
	ReferenceType_Tax
	ReferenceType_Commission
	ReferenceType_Salary // Reward
	ReferenceType_Profit
	ReferenceType_Credit
	ReferenceType_Loan
	ReferenceType_BadDebt // Debt default
	ReferenceType_Installment
	ReferenceType_Compensation
	ReferenceType_Order
)
