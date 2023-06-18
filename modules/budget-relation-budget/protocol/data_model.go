/* For license and copyright information please see the LEGAL file in the code repository */

package brbp

import (
	"libgo/protocol"
	bp "org/modules/budget/protocol"
	qsp "org/modules/quiddity-status/protocol"
	urp "org/modules/user-request/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	BudgetID() bp.BudgetUUID      //
	OtherBudgetID() bp.BudgetUUID //
	Type() Type
	Status() BudgetBudget_Status
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}

type BudgetBudget_Status qsp.Quiddity_Status

type Type uint8

const (
	Type_Unset Type = iota
	Type_Blocking
	Type_Complement
	Type_Continuous
)
