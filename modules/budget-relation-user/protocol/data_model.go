/* For license and copyright information please see the LEGAL file in the code repository */

package brup

import (
	"libgo/protocol"
	bp "org/modules/budget/protocol"
	urp "org/modules/user-request/protocol"
	up "org/modules/user/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	BudgetID() bp.BudgetUUID //
	UserID() up.UserUUID
	Type() Type
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}

type Type uint8

const (
	Type_Unset Type = iota
	Type_Suggester
	Type_Rectifier
	Type_Executor
	Type_Quality_Controller
)
