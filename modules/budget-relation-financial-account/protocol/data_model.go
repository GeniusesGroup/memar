/* For license and copyright information please see the LEGAL file in the code repository */

package bsrp

import (
	"libgo/protocol"
	bp "org/modules/budget/protocol"
	fap "org/modules/financial-account/protocol"
	qsp "org/modules/quiddity-status/protocol"
	urp "org/modules/user-request/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	BudgetID() bp.BudgetUUID             //
	AccountID() fap.FinancialAccountUUID //
	Type() Type                          //
	Status() Status                      //
	SaveTime() protocol.Time             //
	RequestID() urp.UserRequestUUID      //
}

type Type uint8

const (
	Type_Unset Type = iota
	Type_withdrawal
	Type_Deposit
	Type_Suggester
)

type Status qsp.Quiddity_Status
