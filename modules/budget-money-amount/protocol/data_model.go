/* For license and copyright information please see the LEGAL file in the code repository */

package bmap

import (
	"libgo/protocol"

	bp "org/modules/budget/protocol"
	fcp "org/modules/financial-currency/protocol"
	urp "org/modules/user-request/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	BudgetID() bp.BudgetUUID             //
	Currency() fcp.FinancialCurrencyUUID //
	Amount() protocol.MoneyAmount        //
	Type() Type                          //
	SaveTime() protocol.Time             //
	RequestID() urp.UserRequestUUID      //
}

type Type uint8

const (
	Type_Unset Type = iota
	Type_Suggested
	Type_Approved
	Type_Executed
	Type_Inspected
)

// Usage:
// - Shareholders can see org profit and decide to sell or buy more stocks.
// - Country Governments: need to steal organizations profits by the name of law as Tax, ...! so force them to implement these services.
// - Stock Markets: need to show related data to traders to know the quality of organizations in making profit.
