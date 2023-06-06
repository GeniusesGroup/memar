/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"
	urp "org/modules/user-request/protocol"
)

// BudgetMoneyAmount indicate the domain record data fields.
type BudgetMoneyAmount interface {
	BudgetID() BudgetUUID            //
	Currency() FinancialCurrencyUUID //
	Amount() protocol.MoneyAmount
	Type() BudgetMoneyAmount_Type   //
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type BudgetMoneyAmount_StorageServices interface {
	Save(dm BudgetMoneyAmount) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(budgetID BudgetUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(budgetID BudgetUUID, vo protocol.VersionOffset) (dm BudgetMoneyAmount, nv protocol.NumberOfVersion, err protocol.Error)
}

type BudgetMoneyAmount_Type uint8

const (
	BudgetMoneyAmount_Type_Unset BudgetMoneyAmount_Type = iota
	BudgetMoneyAmount_Type_Suggested
	BudgetMoneyAmount_Type_Approved
	BudgetMoneyAmount_Type_Executed
	BudgetMoneyAmount_Type_Inspected
)

// Usage:
// - Shareholders can see org profit and decide to sell or buy more stocks.
// - Country Governments: need to steal organizations profits by the name of law as Tax, ...! so force them to implement these services.
// - Stock Markets: need to show related data to traders to know the quality of organizations in making profit.
