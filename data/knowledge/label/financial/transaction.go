/* For license and copyright information please see the LEGAL file in the code repository */

package label

const (
// transaction fee, split, refund, ...
)

// Financial transaction reference types
const (
	ReferenceType_Failed  = iota // Refund for any reason e.g. not same currency account, not reachable bank, ...
	ReferenceType_Blocked        // by justice
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

// BlockByJustice

// Below labels use to send the transaction to desire matching engine
// use to register an order to e.g. exchange(an instruction to buy or sell) currencies
// A matching engine uses the orders book to determine which orders can be fully or partially executed.
//
// An DataModel submitted without a specified price, and sequentially matched at the best available price in the market or in other words
// if user want to limit price, must fill order-price record otherwise market price will choose for the deals.
//
// use to register an order to e.g. exchange(an instruction to buy or sell) currencies
// A matching engine uses the orders book to determine which orders can be fully or partially executed.
// Order
// Deal

// Budget labels:::
// Materials
// Labor
// Investments // Equipment
// Markup          // the % added to the cost to determine the wholesale price
// WholesaleProfit // The amount of wholesale markup
// Margin          // the % of product price to determine the retail price
// RetailProfit    // The amount of retail margin
// Cost
